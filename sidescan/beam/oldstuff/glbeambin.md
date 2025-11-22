---
layout: default
title: glbeambin
parent: Beam Tools
grand_parent: sidescan
nav_order: 4
---
# glbeambin

## Description
`glbeambin` is a utility that bins up empirical beam pattern data from a JCU GLORIA file across a series of depth windows. It processes the input GLORIA file and calculates the sum of pixel intensities and the count of pixels for port and starboard sides, within specific angle and depth bins. The output is a raw data table showing these accumulated sums and counts.

## Usage
```bash
glbeambin <infile>
```

## Arguments

| Option | Description |
|---|---|
| `<infile>` | **Required.** The input JCU GLORIA file. |

## How It Works
1.  **Process Input File:** The tool reads the input GLORIA file record by record.
2.  **Binning:** For each pixel in the sidescan data (port and starboard):
    *   It determines the `depth_bin` based on the `altitude` in the record header (altitude divided by 500 meters).
    *   It calculates the `theta` (angle) based on the pixel's distance from nadir and the altitude.
    *   It converts `theta` to an integer `itheta` (angle bin).
    *   The pixel's intensity is added to `port_sum[itheta][depth_bin]` or `stbd_sum[itheta][depth_bin]`, and `port_knt[itheta][depth_bin]` or `stbd_knt[itheta][depth_bin]` is incremented.
3.  **Output:** After processing the entire file, the tool prints a formatted table to standard output. This table shows, for each angle bin (0-90 degrees) and each depth bin (0-19), the accumulated `port_sum`, `port_knt`, `stbd_sum`, and `stbd_knt`.
