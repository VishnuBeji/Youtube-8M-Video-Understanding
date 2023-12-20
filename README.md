# Scene Understanding with YouTube 8M Dataset 

## Overview

The YouTube 8M dataset, released in June 2019, provides segment-level annotations with human-verified labels on approximately 237,000 segments across 1,000 classes. This dataset was derived from the validation set of the YouTube-8M dataset.

<img src="data/images/Thumbnails.png" alt="Thumbnails" width="600"/>

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

<img src="data/images/Architecture.png" alt="Architecture" width="500"/>

The diagram illustrates the architecture of our implementation, showcasing the flow and components used to process and analyze the YouTube 8M dataset.

## Context-Gated DBoF Model
<img src="data/images/DBoF.png" alt="Contex Gated DBoF Model" width="500"/>

## Visualising the results
![Prediction Visualisation](data/images/viz.gif)
