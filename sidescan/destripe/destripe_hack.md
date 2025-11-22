---
layout: default
title: destripe_hack
parent: Destripe Tools
grand_parent: sidescan
nav_order: 2
---
# destripe_hack

## Description
`destripe_hack` is a specialized utility for destriping JCU GLORIA format merged sidescan files. Similar to `destripe.c`, it utilizes a high/low pass filter technique, based on Chavez (1986), to remove striping artifacts. This version includes an `edge` parameter, suggesting custom handling for image edges, and some array sizes appear hardcoded (e.g., `GLORIA_SIDESIZE * 2`).

## Usage
```bash
destripe_hack [-filtlen <length>] [-filtwidth <width>] [-low | -high] [-skip <count>] [-edge <value>] <infile_prefix>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-filtlen <length>` | Specifies the length of the filter (along-track). Must be an odd number. | `71` |
| `-filtwidth <width>` | Specifies the width of the filter (across-track). Must be an odd number. | `7` |
| `-low` | Operate in low-pass filter mode (output is the low-frequency component). | (None, mutually exclusive with `-high`) |
| `-high` | Operate in high-pass filter mode (output is the high-frequency component). | (None, mutually exclusive with `-low`) |
| `-skip <count>` | If in high-pass mode, this option can be used to blank out (`128`) a certain number of records from the start and end of the output file. Must be an odd number. | `0` |
| `-edge <value>` | Specifies an offset for copying filtered data to the output record, possibly related to handling image edges. | `0` |
| `<infile_prefix>` | **Required.** The prefix for the input GLORIA file. The tool assumes the input file has a `.mer` extension. The output file will have a `.low` or `.high` extension based on the filter mode. |

## How It Works
1.  **Initialization:** The tool initializes an array (`filter_array`) to hold `filtwidth` number of GLORIA records, which act as a sliding window for the filter. It also initializes a sum array (`stbd`) and temporary arrays (`centre_stbd`, `high_stbd`) for processing, with a size of `GLORIA_SIDESIZE * 2`.
2.  **Read Input File:** It reads records from the input GLORIA `.mer` file.
3.  **Sliding Window and Summation:**
    *   The tool maintains a window of `filtwidth` records. As new records are read, the oldest record in the window is removed from the sums, and the new record is added.
    *   For each record in the window, it calculates the sum of pixel intensities (`stbd[k]`) for each across-track position `k`.
4.  **Filtering (Main Loop):** For each record `j` in the input file:
    *   **Calculate Filtered Output:**
        *   The filtering operation is applied within a window of `filtlen` pixels along-track and `filtwidth` records across-track.
        *   If `high_flag` is set: The output pixel value is the difference between the central pixel's value and the average value within the filter window. This effectively extracts the high-frequency components (stripes).
        *   If `low_flag` is set: The output pixel value is the average value within the filter window, representing the low-frequency component.
    *   **Populate Output Record:** The filtered data is copied into a new GLORIA record (`out_rec`), specifically to `out_rec.stbd_data`, taking into account the `edge` parameter.
    *   **Write Output:** The `out_rec` is written to the output file (e.g., `.low` or `.high`).
5.  **Edge Handling:** Similar to `destripe.c`, special handling exists for the file's beginning and end. The `edge` parameter allows for an offset during the data copy, possibly to adjust for image boundary effects.
6.  **Skip Option (High-Pass Mode):** If `-high` and `-skip` are used, the tool blanks out (`128`) the specified number of records from the beginning and end of the output file by seeking and overwriting sections.
