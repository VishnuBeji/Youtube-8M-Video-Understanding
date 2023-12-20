import math
import glob
import argparse
from functools import partial
from pathlib import Path

import torch
import pandas as pd
from tqdm import tqdm
import numpy as np
import joblib
import yaml

from train_pure_segment import DATA_DIR_STR, prepare_model as prepare_agnostic_model
from train_segment_w_context import prepare_model as prepare_aware_model
from dataloader import YoutubeTestDataset, DataLoader, collate_test_segments
from telegram_tokens import BOT_TOKEN, CHAT_ID
from telegram_sender import telegram_sender

BATCH_SIZE = 32


def inverse_label_mapping(vocab_path="./data/segment_vocabulary.csv"):
    vocab = pd.read_csv(vocab_path)
    return {
        index: label for label, index in zip(vocab["Index"], vocab.index)
    }


def collect_file_paths():
    return list(glob.glob(str(DATA_DIR_STR + "test/*.tfrecord")))


def prepare_model(model_path):
    with open(model_path / "config.yaml") as fin:
        config = yaml.safe_load(fin)
    state_dict = torch.load(str(model_path / "model.pth"))
    if "context_base" in config:
        # context-aware model
        model = prepare_aware_model(config)
    else:
        # context-agnostic model
        model = prepare_agnostic_model(config)
    model.load_state_dict(state_dict)
    return model


@telegram_sender(token=BOT_TOKEN, chat_id=CHAT_ID, name="Inferencing")
def main():
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg('--model-dir', type=str, default="data/cache/segment/")
    arg('--model-names', nargs="+")
    arg('--offset', type=int, default=3)
    args = parser.parse_args()

    Path("data/cache/predictions/").mkdir(exist_ok=True, parents=True)
    model_dir = Path(args.model_dir)
    model_paths = []
    if args.model_names is None:
        for filepath in glob.glob(str(model_dir / "*" / "model.pth")):
            model_paths.append(Path(filepath).parent)
    else:
        for model_name in args.model_names:
            model_paths.append(model_dir / model_name)
    test_ds = YoutubeTestDataset(
        collect_file_paths(), offset=args.offset, device="cpu")
    loader = DataLoader(
        test_ds, batch_size=BATCH_SIZE, num_workers=1,
        collate_fn=partial(
            collate_test_segments,
            return_vid=False),
        pin_memory=True)
    ref_indices = joblib.load("data/cache/ref_indices.jl")
    with torch.no_grad():
        models = []
        predictions = []
        for model_path in model_paths:
            target_path = f"data/cache/predictions/{model_path.stem}.npy"
            if Path(target_path).exists():
                print("Skipping ", model_path.stem)
                continue
            print(model_path.stem)
            model = prepare_model(model_path)
            models.append(model.eval())
            predictions.append(np.memmap(
                target_path,
                "int16", mode="w+", shape=(1704348, 1000)
            ))
        if not models:
            print("No eligible models found!")
            return
        global_indices = np.zeros(1704348, dtype="int8")
        cnt = 0
        for video_features, video_masks, segment_features, indices in tqdm(
                loader, total=int(math.ceil(1704348 / BATCH_SIZE))):
            # shape(frames / 5, n_classes)
            segment_features = segment_features.cuda()
            video_features = video_features.cuda()
            video_masks = video_masks.cuda()
            n_segments = segment_features.shape[0]
            for i, model in enumerate(models):
                # value range 0 ~ 9999
                probs = np.round(torch.sigmoid(
                    model(
                        video_features, video_masks, segment_features
                    )
                ).cpu().numpy() * 9999, 0).astype("int16")
                predictions[i][cnt:cnt+n_segments] = probs
            global_indices[cnt:cnt+n_segments] = indices
            cnt += n_segments
        assert np.array_equal(ref_indices, global_indices)


if __name__ == "__main__":
    main()
