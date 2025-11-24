---
layout: default
title: differ
parent: Grid Tools
nav_order: 21
---
---
layout: default
title: differ
parent: Grid Tools
nav_order: 21
---
# differ

## Description
`differ` is a powerful command-line utility for comparing two JHC-format 32-bit floating-point grid files (`.r4` files). Its primary function is to calculate the pixel-wise difference between two surfaces (e.g., Digital Terrain Models from different epochs). The tool also provides advanced options for statistical analysis, volumetric calculations, handling spatial misalignments, and masking.

## Usage
```bash
differ -first <file1.r4> -second <file2.r4> -out <output.r4> [OPTIONS]
```

## Arguments

### Core Arguments
| Option | Description | Default / Example |
|---|---|---|
| `-first <file1.r4>` | **Required.** The path to the first input float grid file (the minuend). | `-first dtm_2022.r4` |
| `-second <file2.r4>` | **Required.** The path to the second input float grid file (the subtrahend). | `-second dtm_2021.r4` |
| `-out <output.r4>` | **Required.** The path for the output float grid file that will store the difference (`first - second`). | `-out difference_map.r4` |

### Feature Options
| Option | Description | Default / Example |
|---|---|---|
| `-stats <min> <max> <step>` | Enables detailed statistical analysis. It calculates the mean and standard deviation of the differences and generates a histogram of the difference values, which is saved to `<outname>.statistics`. `<min>`, `<max>`, and `<step>` define the histogram's range and bin size. | `-stats -5.0 5.0 0.1` |
| `-volume_calc_net` | Calculates the net volumetric change between the two surfaces by summing the difference at each pixel multiplied by the pixel area. | |
| `-volume_calc_gain` | Calculates the total positive (gain) volumetric change, where the first surface is higher than the second. | |
| `-volume_calc_loss` | Calculates the total negative (loss) volumetric change, where the second surface is higher than the first. | |
| `-perc_wd` | Calculates the difference as a percentage relative to the value in the first file: `((first - second) / first) * 100.0`. | |
| `-xplot` | Creates a simple two-column ASCII file named `<outname>.xplot` containing the paired values from the first and second grids, suitable for generating a scatter plot. | |
| `-min_within_pixels <num>` | Instead of a simple 1-to-1 subtraction, this enables a search mode. For each pixel in the first grid, it searches a square neighborhood of `+/- num` pixels in the second grid and finds the minimum absolute difference. The output value is this minimum signed difference. This is extremely useful for comparing surveys with small, unknown horizontal offsets. | `-min_within_pixels 3` |
| `-mask <mask_file>` | Applies an 8-bit mask file. The differencing operation will only be performed on pixels where the mask value is non-zero. | `-mask valid_area.mask` |
| `-shift <xpix> <ypix>` | Applies a simple integer pixel shift to the *second* grid before differencing. Useful for correcting known, uniform misalignments. | `-shift 2 -1` |
| `-addvalue <value>` | Adds a constant floating-point offset to each value in the first grid before differencing. This is equivalent to applying a vertical shift to the first surface. | `-addvalue -0.35` |
| `-sane_range <min> <max>` | Filters the input data. Any pixel value in either input grid that falls outside this specified min/max range is treated as zero and ignored in the calculation. | `-sane_range -2000 50` |
| `-v` | Enable verbose output during processing. | |

## How It Works
1.  **File Opening:** Opens the two input `.r4` grid files (`-first`, `-second`) and the output `.r4` file (`-out`). Optionally opens a mask file (`-mask`).
2.  **Header Reading:** Reads the `JHC_header` from the input files, ensuring their dimensions and geographic extents are compatible.
3.  **Data Processing:**
    *   **Shift (`-shift`):** If a shift is applied, it adjusts the indexing for the second grid.
    *   **Min Within Pixels (`-min_within_pixels`):** If enabled, for each pixel in the first grid, it performs a local search in the second grid to find the best matching (minimum difference) pixel.
    *   **Pixel-wise Subtraction:** For each pixel location:
        *   Reads `value1` from the first grid and `value2` from the second grid (or the best match from the search).
        *   Applies `addvalue` to `value1`.
        *   If `value1`, `value2` are within `sane_range` and pass the mask filter, calculates `difference = value1 - value2`.
        *   If `-perc_wd` is used, `difference = ((value1 - value2) / value1) * 100.0`.
        *   The calculated `difference` is written to the output `.r4` file.
    *   **Statistical Analysis (`-stats`):** If enabled, accumulates data for mean, standard deviation, and histogram.
    *   **Volumetric Calculations (`-volume_calc_*`):** If enabled, sums the differences (multiplied by pixel area) for net, gain, or loss volumes.
    *   **XPlot (`-xplot`):** If enabled, outputs `value1` and `value2` to an ASCII file.
4.  **Output Header:** Creates a `JHC_header` for the output file and writes it, followed by the processed pixel data.
5.  **Statistics Output:** If `-stats` is used, generates a `.statistics` file.

## Output Files
*   `<output.r4>`: A JHC-format 32-bit floating-point grid file containing the pixel-wise difference.
*   `<outname>.statistics`: An ASCII file with statistical summary and histogram (if `-stats` is used).
*   `<outname>.xplot`: An ASCII file with paired values from the input grids (if `-xplot` is used).

## Dependencies
*   `array.h`: For `JHC_header` structure and grid data handling.
*   `support.h`: For general utility functions and error handling.

## Notes
The `-min_within_pixels` option is particularly powerful for comparing slightly misaligned grids, such as those from different survey epochs or sensor platforms. Volumetric calculations provide quantitative measures of change over time.
