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
1.  **DTM Loading:** Loads the DTM from the `.r4` file into memory.
2.  **Snippet Extraction:** For each valid beam in every ping, the tool extracts the raw backscatter snippet from the associated `.ss_data` file.
3.  **Angle Calculation:** It calculates the angle of each sample within the snippet relative to the beam's central axis (using `build_scallop`). This angle is derived from the beam's geometry and the snippet's time window.
4.  **Statistics Accumulation:** Backscatter intensities are binned into a 2D array (indexed by beam number and relative angle within the snippet). The sum, sum of squares, and count of samples are accumulated for each bin. This captures the intensity distribution at different relative angles for each beam.
5.  **Pattern Derivation:** After processing all input files, the tool calculates the mean and standard deviation of backscatter intensity for each `[beam_num][angle_bin]` combination.
6.  **Weighted Averaging:** A weighted average of these mean intensities is then computed across all beams for each `angle_bin`, yielding the overall receive snippet beam pattern. Bins with more samples contribute more to the average.
7.  **Normalization:** This derived pattern is normalized (by subtracting the maximum value) before output, so the peak of the beam pattern is typically set to 0 dB.

## Output Files
*   **`snippet.bp`**: An ASCII file containing the derived snippet beam pattern. This file lists the relative angle (in degrees, usually from -10 to +10) and the normalized backscatter intensity (in dB).

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `array.h`: For `JHC_header` structure and DTM data handling.
*   `support.h`: For general utility functions and error handling.

## Notes
This tool is a research-oriented utility for advanced analysis of sonar characteristics from raw snippet data. The DTM is used to refine the calculation of grazing angles and beam geometry, leading to a more accurate representation of the receive beam pattern. The output `snippet.bp` can be used for further backscatter correction or analysis of the sonar system's performance. The tool leverages `build_scallop` (likely an internal function) to calculate the across-track geometry of the snippet.