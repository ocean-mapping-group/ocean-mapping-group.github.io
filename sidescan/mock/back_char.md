---
layout: default
title: back_char
parent: Mock Tools
grand_parent: sidescan
nav_order: 1
---
# back_char

## Description
`back_char` is a utility designed to characterize backscatter strength and grazing angle mosaics. It processes up to 10 pairs of backscatter and impinging angle mosaics (in JHC image format). By running a moving box filter over these images, it calculates and outputs several derived images that describe the angular dependence of backscatter:
*   **Slope:** The slope of the linear fit to the angular dependence of backscatter (between 45 and 78 degrees).
*   **Midi:** The backscatter strength at 67.5 degrees, assuming a linear slope.
*   **Standard Deviation:** The mean standard deviation of backscatter (between 45 and 78 degrees).
*   **Lambertian Fit:** The backscatter strength at vertical incidence, assuming a Lambertian scattering model (over the range of 45 and 78 degrees).
*   **Bounds:** An image indicating the average value within the useful grazing angle range.
*   **Map:** An image representing the total number of useful pixels (if `-map` is used).

All calculations are performed for backscatter measured over the grazing angle range of 45 to 76.8 degrees.

## Usage
```bash
back_char [-box <size>] [-min_useful <count>] [-bounds <upper> <lower>] [-map] [-slope] [-midi] [-stdv] [-lamb]
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-box <size>` | Specifies the size of the square moving box filter (e.g., a value of 5 means a 5x5 box). | `5` |
| `-min_useful <count>` | Sets the minimum number of "useful" pixels required within a box for calculations to be performed. If fewer pixels are available, output values for that box will be marked as invalid (e.g., 8 or 14). | `(box_size*2)^2 * 2` |
| `-bounds <upper> <lower>` | Defines the upper and lower grazing angle bounds (in degrees) for analysis. Values outside this range will be ignored. | `45.0` (upper), `12.0` (lower) |
| `-map` | Instead of calculating derived parameters, generate a map indicating the total number of useful pixels within each box. Forces `box_size` to 1. | (None) |
| `-slope` | Output an image representing the slope of the linear fit to backscatter vs. grazing angle. Output file: `slope.comp`. | (Output by default if no specific flags are given) |
| `-midi` | Output an image representing the backscatter strength at 67.5 degrees. Output file: `midi.comp`. | (Output by default if no specific flags are given) |
| `-stdv` | Output an image representing the mean standard deviation of backscatter. Output file: `stdv.comp`. | (Output by default if no specific flags are given) |
| `-lamb` | Output an image representing the backscatter strength at vertical incidence (Lambertian fit). Output file: `lamb.comp`. | (Output by default if no specific flags are given) |

## How It Works
1.  **Input Loading:**
    *   The tool loads up to 10 pairs of backscatter (`.mos`) and grazing angle (`.imping.mos`) JHC image files into memory. Each file is assumed to have a `JHC_header` at the beginning.
    *   It extracts relevant header information such as image dimensions (`dx`, `dy`).
2.  **Angle Range Conversion:** The user-defined `upper_bound` and `lower_bound` grazing angles are converted into corresponding pixel ranges (`min_range`, `max_range`) for internal processing (mapping from degrees to 8-bit digital numbers).
3.  **Moving Box Filter:** The core of the processing involves iterating a `box_size` x `box_size` window over the entire image (row by row, column by column).
4.  **Data Accumulation within Box:** For each position of the box filter:
    *   It iterates through all 10 input backscatter/grazing angle image pairs.
    *   Within the current box, it examines each pixel. If a pixel's grazing angle is within the `min_range` and `max_range` and its backscatter value is not an invalid value (15 or 255), it's considered "useful".
    *   For useful pixels, it accumulates statistics into a `table_pointer[back_stbd][graz_stbd]` array.
    *   `tot_useful` counts the total number of useful pixels within the box across all 10 input images.
5.  **Derived Parameter Calculation (if `tot_useful > min_useful`):**
    *   **Average Backscatter per Grazing Angle (`aver`):** For each grazing angle bin within the `min_range` to `max_range`, it calculates the average backscatter value from the `table_pointer`.
    *   **Slope:** Performs a least-squares linear fit on the `aver` values against grazing angle to determine the slope of the angular dependence.
    *   **Midi:** Calculates the expected backscatter value at 67.5 degrees grazing angle based on the `aver` values and a predefined `fit_slope`.
    *   **Standard Deviation:** Calculates the standard deviation of backscatter values for each grazing angle bin.
    *   **Lambertian Fit:** Calculates a "Lambertian" constant from the `aver` values, representing backscatter at vertical incidence assuming a Lambertian model.
    *   **Bounds:** Calculates the average of `aver` values within the useful range.
6.  **Output Generation:**
    *   **Map Mode (`-map`):** If this flag is set, the output image pixel for the current box represents `tot_useful`.
    *   **Derived Images:** Otherwise, the calculated `slope`, `midi`, `stdv`, `lamb`, and `bounds` values are scaled and converted to 8-bit unsigned char and written to corresponding output image files (`.comp`).
    *   If `tot_useful` is less than `min_useful`, the output pixel for that box is set to an invalid value (8 or 14).
7.  **Loop and Finalization:** The process continues until all image rows are processed. Initial and final `box_size` rows are filled with default invalid values. Output files are closed.
