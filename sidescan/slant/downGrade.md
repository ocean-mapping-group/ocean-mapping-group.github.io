---
layout: default
title: downGrade
parent: Slant Tools
grand_parent: sidescan
nav_order: 2
---
# downGrade

## Description
`downGrade` is a utility designed to reduce the resolution of JCU GLORIA format sidescan files. It can decimate the data both along-track (by averaging multiple pings) and across-track (by averaging multiple pixels within a ping). An optional "destriping" mode allows for a different aggregation method across-track, potentially for noise reduction.

## Usage
```bash
downGrade [-v] [-across <pixels>] [-along <pings>] [-destripe] -in <infile> -out <outfile>
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-across <pixels>` | Specifies the number of pixels to average across-track. | `1` |
| `-along <pings>` | Specifies the number of pings to average along-track. | `1` |
| `-destripe` | If specified, when aggregating along-track, instead of averaging, the maximum pixel value will be retained. | (None) |
| `-in <infile>` | **Required.** The input JCU GLORIA format file. |
| `-out <outfile>` | **Required.** The output JCU GLORIA format file with reduced resolution. |

## How It Works
1.  **Input File Reading:** The tool opens the specified input JCU GLORIA file (`inname`) and output file (`outname`).
2.  **Parameter Validation:** It checks if `across` and `along` parameters are within reasonable bounds.
3.  **Along-Track Aggregation:** The tool iterates through the input file, processing pings in blocks of `along` pings:
    *   **Initialize Sums:** For each block, it initializes `sumlat`, `sumlon`, `sumalt`, `sumtime` for header fields, and `tracecount[k]`, `tracesum[k]` for pixel values across the swath.
    *   **Read Pings:** It reads `along` consecutive pings into a temporary array `trace`.
    *   **Across-Track Aggregation (`pack_across`):** For each ping in the block, `pack_across` is called to perform across-track averaging (or aggregation). This function takes a `stbd_data` array and an `aver` parameter (which is `across`), and averages `across` pixels together, reducing the resolution of that ping.
    *   **Accumulate Header and Pixel Data:**
        *   It accumulates `altitude`, `lat`, `lon`, and `time` from the `along` pings.
        *   For each pixel position `k` across the swath:
            *   If `destripe_flag` is set, `tracesum[k]` will store the *maximum* pixel value encountered in that position over the `along` pings.
            *   Otherwise, `tracesum[k]` will store the *sum* of pixel values.
            *   `tracecount[k]` stores the number of valid (non-255) pixels for each position.
4.  **Calculate Averaged Record:** After processing `along` pings:
    *   **Header Averaging:** `altitude`, `lat`, `lon`, and `time` are averaged for the block. `azi` is recalculated using `getazi` from the averaged `dx` and `dy`.
    *   **Pixel Averaging:** For each pixel position `k`:
        *   If `destripe_flag` is not set, `outrecord.stbd_data[k]` is the average of `tracesum[k] / tracecount[k]`.
        *   If `destripe_flag` is set, `outrecord.stbd_data[k]` is the `tracesum[k]` (which holds the maximum value).
    *   `outrecord.header.small_pixel` is adjusted by `across`.
5.  **Write Output:** The averaged `outrecord` is written to the output file.
6.  **Loop:** This process repeats until all pings in the input file have been processed.

**Helper Functions:**
*   `pack_across(data, aver)`: Reduces the across-track resolution of a single data trace by averaging `aver` consecutive pixels.
*   `getdxdy(azi, dx, dy)`: Calculates x and y components from an azimuth.
*   `getazi(dx, dy, azi)`: Recalculates azimuth from x and y components.
