---
layout: default
title: build_back_mos
parent: Mock Tools
grand_parent: sidescan
nav_order: 5
---
# build_back_mos

## Description
`build_back_mos` is a utility designed to generate a backscatter plot (or "table") from a single pair of backscatter strength and grazing angle mosaics. It allows the user to define a specific region of interest (`top_y`, `bot_y`, `left_x`, `right_x`) within the mosaics. Within this region, the tool analyzes the relationship between backscatter intensity and grazing angle, calculating the mean and standard deviation of backscatter for different grazing angle bins. This statistical information is then represented as a new image file, termed a "table", which visually summarizes the angular dependence.

## Usage
```bash
build_back_mos -grazfile <grazing_file> -backfile <backscatter_file> -table <table_prefix> [-top_y <value>] [-bot_y <value>] [-left_x <value>] [-right_x <value>] [-full]
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-grazfile <grazing_file>` | **Required.** The input grazing angle mosaic file (JHC image format). | (None) |
| `-backfile <backscatter_file>` | **Required.** The input backscatter mosaic file (JHC image format). | (None) |
| `-table <table_prefix>` | **Required.** The prefix for the output table file. The output file will have a `.table` extension. | (None) |
| `-top_y <value>` | Specifies the top row index of the region of interest for analysis. | `10` |
| `-bot_y <value>` | Specifies the bottom row index of the region of interest for analysis. | `20` |
| `-left_x <value>` | Specifies the left column index of the region of interest for analysis. | `10` |
| `-right_x <value>` | Specifies the right column index of the region of interest for analysis. | `20` |
| `-full` | This flag is present in the arguments but its functionality is not fully apparent in the provided source code, it might indicate processing the full image rather than a sub-region. | (None) |

## How It Works
1.  **Input Loading:**
    *   The tool opens the specified grazing angle (`grazfile`) and backscatter (`backfile`) mosaics. These files are expected to be in JHC image format, starting with an `acres_c_header`.
    *   It reads the headers to determine image dimensions (`cols`, `rows`).
    *   It seeks to the specified region of interest (`top_y`, `bot_y`, `left_x`, `right_x`) within the input files.
2.  **Data Accumulation:**
    *   A 2D array `table_pointer[241][241+32]` is initialized to accumulate statistics. This array will represent the relationship between backscatter (y-axis) and grazing angle (x-axis), each binned into 240 categories (DN values from 16 to 255).
    *   The tool iterates through each pixel within the defined region of interest across both the backscatter and grazing angle mosaics.
    *   For each valid pixel pair (backscatter and grazing angle both > 15), it increments a counter in `table_pointer[back_stbd_bin][graz_stbd_bin]`, where `back_stbd_bin` and `graz_stbd_bin` are the 8-bit digital numbers minus 15 (to shift the range from 16-255 to 1-240).
3.  **Mean and Standard Deviation Calculation:**
    *   After accumulating counts in `table_pointer`, the tool calculates:
        *   **Mean Backscatter (`aver`):** For each grazing angle bin, it computes the average backscatter value.
        *   **Standard Deviation (`std_dev`):** For each grazing angle bin, it calculates the standard deviation of backscatter values around the mean.
4.  **Output Table Generation:**
    *   The `table_pointer` array is then populated with visual markers to represent the calculated mean and standard deviation:
        *   The mean line is drawn with pixels of value `3` (and `5` for neighbors).
        *   The mean +/- one standard deviation lines are drawn with pixels of value `4` (and `5` for neighbors).
    *   A header (`table_head`) is created for the output table image, defining its dimensions and coordinate ranges.
    *   The `table_head` and the populated `table_pointer` array are written to the output file (`.table`).
