---
layout: default
title: getSnippetBP
parent: OMG Tools
nav_order: 31
---
# getSnippetBP

## Description
`getSnippetBP` is a specialized command-line utility for analyzing sidescan snippets from Reson multibeam data to derive the sonar's receive beam pattern (BP). This tool infers the receive BP by examining how backscatter intensity within a small section of the sidescan trace (the "snippet" around the bottom detection) changes with the angle relative to the beam's central axis.

## Usage
```bash
getSnippetBP -dtm <dtm.r4> <input_merged_files(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `-dtm <dtm.r4>` | **Required.** The path to a Digital Terrain Model (`.r4` file) used for accurate grazing angle calculations. |
| `<input_merged_files(s)>` | **Required.** One or more OMG-HDCS merged files (specifically for Reson multibeam data). The tool implicitly requires associated `.ss_data` files. |
| `-debug` | Enables additional debug output. |

## How It Works
1.  **Snippet Extraction:** For each valid beam in every ping, the tool extracts the raw backscatter snippet.
2.  **Angle Calculation:** It calculates the angle of each sample within the snippet relative to the beam's central axis (using `build_scallop`).
3.  **Statistics Accumulation:** Backscatter intensities are binned into a 2D array (indexed by beam number and relative angle within the snippet). The sum, sum of squares, and count of samples are accumulated for each bin.
4.  **Pattern Derivation:** After processing all input files, the tool calculates the mean and standard deviation of backscatter intensity for each `[beam_num][angle_bin]` combination.
5.  **Weighted Averaging:** A weighted average of these mean intensities is then computed across all beams for each `angle_bin`, yielding the overall receive snippet beam pattern.
6.  **Normalization:** This derived pattern is normalized (by subtracting the maximum value) before output.

## Output File
*   **`snippet.bp`**: An ASCII file containing the derived snippet beam pattern. This file lists the relative angle (in degrees, usually from -10 to +10) and the normalized backscatter intensity (in dB).

This tool is a research-oriented utility for advanced analysis of sonar characteristics from raw snippet data.
