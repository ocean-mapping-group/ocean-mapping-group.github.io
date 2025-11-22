---
layout: default
title: LPFbeams
parent: OMG Tools
nav_order: 36
---
# LPFbeams

## Description
`LPFbeams` is a command-line utility that applies a low-pass filter to the `observedDepth` values of selected beams within an OMG-HDCS merged file. Its primary purpose is to remove high-frequency noise or motion artifacts from the depth measurements, resulting in a smoother bathymetry.

The tool operates on a user-defined range of pings and beams, calculating a weighted average of depths within a specified window. The input merged file is modified in place.

## Usage
```bash
LPFbeams <merged_file> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<merged_file>` | **Required.** The path to the OMG-HDCS merged file to be processed. This file is modified in place. |
| `-window <odd_num>` | Specifies the size of the filter window (in number of pings). It must be an odd number. | `11` |
| `-beams <first_beam> <last_beam>` | Specifies the range of beam numbers (inclusive, 0-indexed) to apply the filter to. | |
| `-first <ping_num>` / `-last <ping_num>` | Specifies the range of pings (inclusive) to process. By default, processes all pings. |
| `-cos_square` | Uses a cosine-squared function to calculate the filter weights. By default, a simple cosine function is used. | |
| `-out <filename>` | Creates an ASCII file at the specified path, dumping the original and filtered depths for inspection. | |
| `-v` | Enable verbose output. |

## How It Works
1.  **Data Extraction:** The tool extracts `observedDepth` values for the specified range of beams and pings, storing them in a 2D matrix.
2.  **Weighted Averaging:** For each depth point, it calculates a weighted average of its neighbors along the ping dimension (along-track direction) within the defined `window`. The weights are determined by either a cosine or cosine-squared function, giving more importance to central samples.
3.  **In-Place Update:** The original `observedDepth` values in the merged file are then replaced with these newly calculated, smoothed depths.
