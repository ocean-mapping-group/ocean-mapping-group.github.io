---
layout: default
title: glbeam_bydepth
parent: Beam Tools
grand_parent: sidescan
nav_order: 1
---
# glbeam_bydepth

## Description
`glbeam_bydepth` is a utility for beam pattern correction of a JCU GLORIA file. This version applies correction factors based on depth ranges, using 20 correction factor files to adjust the beam pattern according to the nadir depth.

## Usage
```bash
glbeam_bydepth <infile> <outfile>
```

## Arguments

| Option | Description |
|---|---|
| `<infile>` | **Required.** The input JCU GLORIA file. |
| `<outfile>` | **Required.** The output JCU GLORIA file with beam pattern correction applied. |

## How It Works
1.  **Read Beam Pattern Parameters:** The tool reads 20 beam pattern correction files, each corresponding to a specific depth range. These files contain port and starboard beam pattern parameters (`stbd_par`, `port_par`) and average values (`stbd_ave`, `port_ave`).
2.  **Initialize Parameters:** For each beam pattern parameter, the reciprocal is calculated for corrections to be applied by multiplication.
3.  **Process Input File:** The tool reads the input GLORIA file record by record.
4.  **Determine Depth Bin:** For each record, it determines the appropriate depth bin based on the `altitude` in the header. If the altitude is very shallow or very deep, it uses predefined bins. Otherwise, it interpolates between two bins based on the altitude.
5.  **Apply Correction:** For each pixel in the sidescan data (port and starboard):
    *   It calculates the `theta` (angle) based on the pixel's distance from nadir and the altitude.
    *   It interpolates beam pattern correction parameters (`prev_parameter`, `post_parameter`) from the loaded beam pattern files based on `theta` and the determined depth bin.
    *   These parameters are then weighted by `prev_weight` and `post_weight` (which depend on the altitude's position between the two depth bins).
    *   The raw pixel value is multiplied by the calculated parameter to get the `corrected` value.
    *   The `corrected` value is clamped to a maximum of 254.
6.  **Write Output:** The corrected record is written to the output file.
