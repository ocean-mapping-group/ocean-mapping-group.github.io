---
layout: default
title: glfill
parent: Histogram Tools
grand_parent: sidescan
nav_order: 1
---
# glfill

## Description
`glfill` is a utility designed to fill in invalid data (typically pixels with a value of 255) or anomalously low-level data within JCU GLORIA format files. This is particularly useful for data types like EM-12 multibeam, where data dropouts or weak returns can create gaps or stripes. The tool employs interpolation techniques based on neighboring pixels and optionally utilizes a running average of intensities to identify and correct low-level data.

## Usage
```bash
glfill [-invalid <value>] [-replace] [-lower_level <value>] [-throwout] [-level_below_average <value>] <rawfile> <fillfile>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-invalid <value>` | Specifies the pixel value that represents invalid data. | `255` |
| `-replace` | If specified, when filling a pixel, it will be replaced by the value of the pixel from the previous record (one record back) at the same across-track position. Otherwise, it uses a two-record average. | (None) |
| `-lower_level <value>` | Specifies a pixel intensity threshold. Pixels below this level are also considered invalid and candidates for filling, especially when `-throwout` is used. | `0` |
| `-throwout` | If specified, all pixels below `-lower_level` are immediately set to `invalid` (255) before the main filling process. | (None) |
| `-level_below_average <value>` | If specified, this value is used to dynamically calculate `lower_level` based on a running average of ping intensities. Pixels below `average - level_below_average` are considered invalid. | `0` |
| `<rawfile>` | **Required.** The input JCU GLORIA file containing raw data to be filled. |
| `<fillfile>` | **Required.** The output JCU GLORIA file with invalid data filled. |

## How It Works
1.  **Load Image Data:** The entire input GLORIA file (`rawfile`) is loaded into memory as a 2D array (`image`) of `unsigned char`, representing the pixel intensities for each record.
2.  **Initial Low-Level Data Handling (`-throwout`, `-level_below_average`):**
    *   If `-throwout` is used, any pixel in the loaded `image` that is below the initial `lower_level` (or 0 if not specified) is immediately set to `invalid` (255).
    *   If `-level_below_average` is used, the tool calculates a running average (`average`) of valid pixel intensities for each ping. Then, a 10-point filtered average (`filtav`) is computed. The `lower_level` is then dynamically set to `filtav[i] - level_below_average` for each ping `i`.
3.  **Filling Logic (Main Loop):** The tool then iterates through the `image` array (excluding the first and last two records for boundary conditions):
    *   It looks for "invalid" pixels, defined as either the `-invalid` value or values below the dynamically updated `lower_level` (if `-level_below_average` is active).
    *   A pixel `(i, j)` is considered for filling if `image[i][j]`, `image[i][j+1]`, and `image[i][j+2]` are all "invalid" (this seems like a specific pattern detection for stripes).
    *   **Interpolation Rules:**
        *   **Vertical Interpolation:** If the pixel above (`i-1, j`) and below (`i+1, j`) are both valid, and `-replace` is *not* used, the current pixel `(i, j)` is replaced by the average of `image[i-1][j]` and `image[i+1][j]`.
        *   **Replacement (`-replace`):** If `-replace` is used, the pixel is replaced by the value of `image[i-1][j]`.
        *   **Extended Vertical Interpolation:** If direct neighbors are not both valid, it tries to use pixels two records away (`i-1, j` and `i+2, j`) or (`i+1, j` and `i-2, j`), applying a weighted average.
4.  **Write Output File:** After processing and filling, the modified `image` data is copied back into `gloria_rec` structures and written to the `fillfile`.
