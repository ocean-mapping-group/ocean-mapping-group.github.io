---
layout: default
title: build_back
parent: Mock Tools
grand_parent: sidescan
nav_order: 6
---
# build_back

## Description
`build_back` is a utility designed to analyze the relationship between backscatter strength and grazing angle by constructing a density plot (or "table") and deriving statistical information. It processes backscatter and grazing angle data from multiple JCU GLORIA files, calculates the mean and standard deviation of backscatter for various grazing angle bins, and outputs this information as both a visual table and an ASCII file. An option for histogram equalization is also available.

## Usage
```bash
build_back [-table <prefix>] [-eq] [-first <record>] [-last <record>]
```
**Interactive prompts:** The tool will interactively ask for input backscatter and impinging (grazing) angle filenames.

## Arguments

| Option | Description |
|---|---|
| `-table <prefix>` | **Required.** Specifies a prefix for output files. The tool will generate: `<prefix>.table` (image), `<prefix>.mean` (ASCII stats), and `<prefix>.resp` (response function). |
| `-eq` | If specified, histogram equalization will be applied to the `table_pointer` data, normalizing the density so it's not a function of the number of values in each grazing angle bin. |
| `-first <record>` | Specifies the first record number to include in the statistical analysis. |
| `-last <record>` | Specifies the last record number to include in the statistical analysis. |

## How It Works
1.  **Initialization:**
    *   A 2D array `table_pointer[241][481]` is initialized. This array will represent the density of backscatter (y-axis, 0-240 DN) versus grazing angle (x-axis, -90 to 90 degrees, mapped to 0-480 bins).
    *   Arrays for `aver`, `std_dev`, `sum`, `sum_weight`, and `max_weight` are initialized for statistical calculations.
    *   Output files (`.table`, `.mean`, `.resp`) are opened.
2.  **Interactive Input:** The tool repeatedly prompts the user to enter paths for backscatter and impinging angle files.
3.  **Data Accumulation:** For each pair of input files provided:
    *   It reads each GLORIA record from both the backscatter and grazing angle files.
    *   For each pixel in the record, it extracts `back_stbd`/`back_port` and `graz_stbd`/`graz_port` values.
    *   If a pixel's backscatter and grazing angle values are valid (typically > 15), it increments a counter in the `table_pointer` array at the corresponding backscatter and grazing angle bin.
4.  **Mean and Standard Deviation Calculation:**
    *   After accumulating all data, for each grazing angle bin (`i` from 0 to 480):
        *   **Mean Backscatter (`aver[i]`):** Calculated by summing `j * (count_at_j)` for all backscatter values `j` in that grazing angle bin, divided by the total `sum_weight`.
        *   **Standard Deviation (`std_dev[i]`):** Calculated from the squared differences between each backscatter value and the mean, weighted by `count_at_j`.
5.  **Histogram Equalization (Optional):** If `-eq` is specified, the counts in `table_pointer` are equalized to normalize the density across different grazing angle bins.
6.  **Output Table Generation:**
    *   The `table_pointer` array is visually enhanced by marking the `aver` line (value 3) and `aver +/- std_dev` lines (value 4, with neighbors at value 5).
    *   A `JHC_header` (`table_head`) is created defining the dimensions and ranges of the output table image.
    *   The `table_head` and the populated `table_pointer` array are written to the `<prefix>.table` file.
7.  **ASCII Output:**
    *   The calculated `aver`, `aver - std_dev`, and `aver + std_dev` values for each grazing angle bin are written to the `<prefix>.mean` ASCII file.
    *   The inverted mean backscatter (240.0 - `aver[i]`) is written to the `<prefix>.resp` ASCII file.
