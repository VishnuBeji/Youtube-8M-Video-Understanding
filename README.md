# YouTube 8M Dataset - Segment-Level Annotations

## Overview

The YouTube 8M dataset, released in June 2019, provides segment-level annotations with human-verified labels on approximately 237,000 segments across 1,000 classes. This dataset was derived from the validation set of the YouTube-8M dataset.

### Dataset Statistics

- **Frame Level Data Size:** 1.71 TB
- **Number of Shards:** 3,844

### Data Schema

The data is organized with the following schema:

- **"video-id":** Unique identifier for each video.
- **"labels":** A list of labels associated with that video.

Each frame in the dataset includes the following features:

- **"rgb":** Float array of length 1,024.
- **"audio":** Float array of length 128.

## Implementation Details

We have provided images to illustrate the architecture and visual aspects of our implementation.

### Architecture Overview

![Architecture Overview](data/architecture.png)

The diagram illustrates the architecture of our implementation, showcasing the flow and components used to process and analyze the YouTube 8M dataset.

### Video Thumbnai
