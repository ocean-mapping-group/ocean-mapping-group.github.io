---
layout: default
title: selective_back
parent: Mock Tools
grand_parent: sidescan
nav_order: 11
---
# selective_back

## Description
`selective_back` is a utility designed for advanced analysis of backscatter strength and grazing angle mosaics. Similar to `build_back_mos`, it processes input backscatter and impinging (grazing) angle images to understand their statistical relationship. However, `selective_back` offers more flexibility by allowing analysis either within a user-defined geographic region (`-top_y`, `-bot_y`, `-left_x`, `-right_x`) or specifically for pixels within a certain value range of an external classification image (`-class`, `-range`). It computes mean and standard deviation of backscatter for various grazing angle bins and can visualize these statistics or apply color coding to an image.

## Usage
```bash
selective_back [-image <image_file>] [-color <value>] [-dB <min_dB> <max_dB>] [-table <prefix>] [(-top_y <y0> -bot_y <y1> -left_x <x0> -right_x <x1>) | (-class <class_file> -range <low> <high>)] [-bksct <bksct_file> -imping <imping_file>]
```
**Note:** When using the geographic region (`-top_y`, etc.) or classification (`-class`) options, you generally provide backscatter and impinging angle files directly (`-bksct`, `-imping`) rather than relying on the hardcoded `mos/lineN_` files. The hardcoded files are a fallback.

## Arguments

| Option | Description | Default |
|---|---|---|
| `-image <image_file>` | An optional image file (ACRES format) to be "painted" with a specified color (`-color`) where classification criteria are met. | (None) |
| `-color <value>` | The 8-bit color value to "paint" pixels in the `image_file` if using the `-image` and `-class` options. | `5` |
| `-dB <min_dB> <max_dB>` | Defines the minimum and maximum decibel range for the output table's y-axis, allowing for specific scaling of backscatter values. | `-70 -30` |
| `-table <prefix>` | **Required.** Specifies a prefix for output files. The tool will generate: `<prefix>.table` (image), and `<prefix>.mean` (ASCII stats). |
| `-top_y <y0>` | Top row of the geographic region of interest. | `-1` (use full image) |
| `-bot_y <y1>` | Bottom row of the geographic region of interest. | `-1` (use full image) |
| `-left_x <x0>` | Left column of the geographic region of interest. | `-1` (use full image) |
| `-right_x <x1>` | Right column of the geographic region of interest. | `-1` (use full image) |
| `-class <class_file>` | An external classification image file (ACRES format). Pixels from the backscatter/impinging mosaics will only be processed if their corresponding pixel in this file falls within the `-range`. | (None) |
| `-range <low> <high>` | When used with `-class`, specifies the inclusive range of pixel values in the classification image to consider. | `0 255` |
| `-bksct <bksct_file>` | **Required (if not using hardcoded files).** Path to an individual backscatter mosaic file (ACRES format). | (Hardcoded `mos/lineN_bksct.mos`) |
| `-imping <imping_file>` | **Required (if not using hardcoded files).** Path to an individual impinging (grazing) angle mosaic file (ACRES format). | (Hardcoded `mos/lineN_imping.mos`) |

## How It Works
1.  **Initialization:**
    *   A 2D array `table_pointer[241][241]` is initialized to accumulate backscatter vs. grazing angle density, mapping 8-bit DN values to the 0-240 range for both axes.
    *   Arrays for `aver`, `std_dev`, `sum`, `sum_weight` are initialized for statistical calculations.
    *   Output files (`.table`, `.mean`) are opened.
2.  **Input Loading (Flexible):**
    *   **Hardcoded Files (Default `phase3_flag`):** The tool can automatically load up to 10 pairs of backscatter and impinging angle mosaic files from predefined paths (`mos/lineN_bksct.mos`, `mos/lineN_imping.mos`).
    *   **Explicit Files (`-bksct`, `-imping`):** Alternatively, a single pair of backscatter and impinging angle files can be specified directly.
    *   **Classification Image (`-class`):** If provided, this image is loaded, and only pixels corresponding to valid ranges in this image are processed.
    *   **Output Image (`-image`):** If provided, this image is also loaded for potential "painting" based on classification.
3.  **Data Accumulation:**
    *   The tool iterates through pixels within the specified region of interest (either geographic or defined by classification).
    *   For each pixel:
        *   It extracts backscatter (`back_stbd`, `back_port`) and grazing angle (`graz_stbd`, `graz_port`) values.
        *   **Classification Filtering:** If `-class` is used, it checks if the corresponding pixel in the `class_data` falls within `range_bot` and `range_top`. If not, the backscatter and grazing angle values for that pixel are ignored.
        *   If valid, it increments a counter in the `table_pointer` array at the corresponding backscatter and grazing angle bin.
4.  **Mean and Standard Deviation Calculation:**
    *   After accumulating all data, for each grazing angle bin (`i` from 0 to 240):
        *   **Mean Backscatter (`aver[i]`):** Calculated by summing `j * (count_at_j)` for all backscatter values `j` in that grazing angle bin, divided by the total `sum_weight`.
        *   **Standard Deviation (`std_dev[i]`):** Calculated from the squared differences between each backscatter value and the mean, weighted by `count_at_j`.
5.  **Output Table Generation:**
    *   The `table_pointer` array is visually enhanced by marking the `aver` line (value 3) and `aver +/- std_dev` lines (value 4).
    *   A `JHC_header` (`table_head`) is created defining the dimensions and dB ranges of the output table image.
    *   The `table_head` and the populated `table_pointer` array are written to the `<prefix>.table` file.
6.  **ASCII Output:** The calculated `aver`, `aver - std_dev`, and `aver + std_dev` values for each grazing angle bin are written to the `<prefix>.mean` ASCII file.
7.  **Image "Painting" (Optional):** If `image_flag` and `class_flag` are enabled, pixels meeting the classification criteria within the `image_file` are set to the specified `color`.
