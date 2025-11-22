---
layout: default
title: hack_glbeam
parent: Beam Tools
grand_parent: sidescan
nav_order: 5
---
# hack_glbeam

## Description
`hack_glbeam` is a utility for beam pattern correction of a JCU GLORIA file. This tool applies correction factors based on depth ranges, using 20 correction factor files to adjust the beam pattern according to the nadir depth. Additionally, it incorporates a linear-logarithmic compression function to prevent clipping of data that might otherwise exceed the 255 maximum intensity value after correction.

## Usage
```bash
hack_glbeam <infile> <outfile>
```

## Arguments

| Option | Description |
|---|---|
| `<infile>` | **Required.** The input JCU GLORIA file. |
| `<outfile>` | **Required.** The output JCU GLORIA file with beam pattern correction and compression applied. |

## How It Works
1.  **Linear-Logarithmic Compression (`linear_log_compress`):**
    *   This function takes an intensity value (`before`) as input.
    *   If `before` is greater than `LINEAR_LIMIT` (230.0), it applies a power law compression: `after = (int)(pow(before - LINEAR_LIMIT, (1. / power)) + LINEAR_LIMIT)`. This compresses values above the `LINEAR_LIMIT` into a smaller range, preventing them from exceeding 255.
    *   Otherwise, `after` remains `before`.
    *   A lookup table `linlog_corrected` is pre-computed for efficiency.
2.  **Read Beam Pattern Parameters:** The tool reads 20 beam pattern correction files, each corresponding to a specific depth range (e.g., "ps89_025.beam_pattern", "ps89_075.beam_pattern", etc.). These files contain port and starboard beam pattern parameters (`stbd_par`, `port_par`) and average values (`stbd_ave`, `port_ave`).
3.  **Initialize Parameters:** For each beam pattern parameter, the reciprocal is calculated for corrections to be applied by multiplication.
4.  **Process Input File:** The tool reads the input GLORIA file record by record.
5.  **Determine Depth Bin:** For each record, it determines the appropriate depth bin based on the `altitude` in the header. If the altitude is very shallow or very deep, it uses predefined bins. Otherwise, it interpolates between two bins based on the altitude.
6.  **Apply Correction:** For each pixel in the sidescan data (port and starboard):
    *   It calculates the `theta` (angle) based on the pixel's distance from nadir and the altitude.
    *   It interpolates beam pattern correction parameters (`prev_parameter`, `post_parameter`) from the loaded beam pattern files based on `theta` and the determined depth bin.
    *   These parameters are then weighted by `prev_weight` and `post_weight` (which depend on the altitude's position between the two depth bins).
    *   The raw pixel value is multiplied by the calculated parameter to get the initial `corrected` value.
    *   This `corrected` value is then passed through the `linear_log_compress` function to apply the compression, preventing values from exceeding 255.
    *   The final `corrected` value is clamped to a maximum of 254.
7.  **Write Output:** The corrected record is written to the output file.
