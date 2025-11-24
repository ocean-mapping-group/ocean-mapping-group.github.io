---
layout: default
title: diffOMG
parent: OMG Tools
nav_order: 90
---
# diffOMG

## Description
`diffOMG` is a utility for comparing two OMG-HDCS merged data files. It can generate an `.r4` (float grid) file representing the depth differences between corresponding beams in the two input files. Additionally, it can output statistics (average and absolute difference/standard deviation) of these differences per beam angle, or it can compare profile header information (like orientation data).

This tool is invaluable for quality control, verifying data processing steps, and analyzing subtle differences between datasets.

## Usage
```bash
diffOMG -first <OMG_HDCS_datafile1> -second <OMG_HDCS_datafile2> -out <diff.r4file> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `-first <OMG_HDCS_datafile1>` | **Required.** Path to the first OMG-HDCS merged data file. |
| `-second <OMG_HDCS_datafile2>` | **Required.** Path to the second OMG-HDCS merged data file. |
| `-out <diff.r4file>` | **Required.** Base name for the output difference file. This will be an `.r4` file for depth differences, and also `.stats` and `.abs_stats` for statistical outputs. |
| `-v` | Enable verbose output. |
| `-dumpaverage` | Output an `.avdepth` file containing the average depths. |
| `-shift <val>` | Shift beams in the second file by this amount before comparison (e.g., `-1` to compare beam `j` in first file with beam `j-1` in second). | `0` |
| `-skip <val>` | Skip pings when calculating differences (e.g., `10` to process every 10th ping). | `1` |
| `-average <val>` | Average `val` pings together when writing to the `.r4` output. | `1` |
| `-width <val>` | When outputting to `.r4`, represent the swath as `nopixels` (250) pixels wide, where the entire swath width is `val` meters. Used instead of `-average`. | `0` (disabled) |
| `-profile_header` | Compare profile header information (pitch, roll, heave) instead of beam depths. This mode outputs to `.stats` only. |
| `-stdev` | Calculate standard deviation of differences instead of absolute mean difference. |
| `-bias <biasfile>` | Apply a bias correction from a `biasfile` (format: `beam_idx bias_value`). |

## How It Works
1.  **Input Reading & Initialization:**
    *   Opens the two input merged files and creates output files (`.r4` for differences, `.avdepth` for average depths, `.stats` and `.abs_stats` for statistics).
    *   Reads summary headers from both input files, issuing a warning if their `numProfiles` differ.
    *   If a `-bias` file is provided, it reads the per-beam bias values into `biases[]`.
2.  **Profile Header Comparison (`-profile_header` mode):**
    *   If `-profile_header` is specified, it iterates through pings, reads profile headers from both files, and prints (to `.stats`) the roll, pitch, and heave values from both profiles, along with their differences.
3.  **Beam Depth Difference Calculation (Default Mode):**
    *   If `-profile_header` is *not* specified:
        *   Sets up the header for the output `.r4` file.
        *   Initializes arrays for `av_diff` (average difference), `abs_diff` (absolute difference/standard deviation), `notoav` (count of valid comparisons), `differences` (for single ping differences), and `avdepth`.
        *   Iterates through pings (potentially skipping with `-skip`):
            *   Reads raw beams from both input files for the current ping.
            *   For each beam `j` (potentially shifted by `shift` in the second file):
                *   If both beams have valid `observedDepth`, it calculates `this_difference` as the percentage difference between their depths, and subtracts any `biases[j]`.
                *   Accumulates `this_difference` into `differences[j]` (for `.r4` output), `av_diff[j]`, and `abs_diff[j]`. Increments `notoav[j]`.
                *   If `swathwidth` is specified, it populates `swath[]` with differences based on across-track position.
            *   **Output to `.r4`:** Writes `differences[]` (or `swath[]`) to the `.r4` output file, potentially averaging over `average` pings.
        *   **Statistical Output:** After processing all pings, it calculates final `av_diff[i]` and `abs_diff[i]` (average and absolute difference/standard deviation) per beam index. It writes these statistics (beam angle vs. average/abs difference) to the `.stats` and `.abs_stats` files.
4.  **Cleanup:** Closes all open files.

## Output Files
*   `<diff.r4file>.r4`: A JHC-format `.r4` file containing depth differences (if not in `-profile_header` mode).
*   `<diff.r4file>.avdepth`: An `.avdepth` file containing average depths (if `-dumpaverage` is used).
*   `<diff.r4file>.stats`: An ASCII file with statistics of differences (mean, standard deviation).
*   `<diff.r4file>.abs_stats`: An ASCII file with absolute statistics of differences.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `array.h`: For `JHC_header` structure and `.r4` file handling.
*   `support.h`: For general utility functions and error handling.

## Notes
`diffOMG` provides a powerful means to compare different processing versions of the same data, or to inter-compare independent surveys. The `-min_within_pixels` (not shown in arguments, but relevant for difference tools) or `-shift` options can help mitigate small spatial misalignments. The output statistics per beam angle are crucial for identifying angle-dependent biases.