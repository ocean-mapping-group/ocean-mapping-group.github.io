---
layout: default
title: addWG
parent: Grid Tools
nav_order: 7
---
---
layout: default
title: addWG
parent: Grid Tools
nav_order: 7
---
# addWG

## Description
`addWG` is a command-line utility for combining multiple JHC-format 32-bit floating-point grid files (Digital Terrain Models, `.r4` files) into a single, weighted-average output grid. It can either use explicit weight grids (`.r4_weights` and `.r4_weight_depth`) or apply a default weight to each input grid. It also supports applying vertical offsets to individual input grids before combining. This tool is typically used to merge multiple overlapping bathymetric surveys while accounting for their relative quality or reliability.

## Usage
```bash
addWG [OPTIONS] -out <output_file.r4>
```
You must specify input grids using either the `-wg` or `-allr4s` options.

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-wg <prefix> <default_weight>` | Specifies an input grid for weighting. `<prefix>` is the base name for the input grid file (`<prefix>.r4`) and, optionally, its associated weight files (`<prefix>.r4_weights` and `<prefix>.r4_weight_depth`). `<default_weight>` is a float: <br> - `0.0`: Expects explicit weight files (`.r4_weights`, `.r4_weight_depth`). <br> - `>0.0`: Uses this value as a uniform weight for the `<prefix>.r4` depths. <br> - `<0.0`: Uses this absolute value to scale existing explicit weight files. <br> This option can be specified multiple times for multiple input grids. | `-wg survey1 0.0 -wg survey2 1.0` |
| `-allr4s <file1.r4> [file2.r4 ...]` | A convenient option to specify multiple input `.r4` files. It assumes all specified files are depth grids and will be combined using a default weight of `0.0` (expecting explicit weight files for each). This option can take multiple filenames. | `-allr4s area1.r4 area2.r4` |
| `-offset <file_number> <value>` | Applies a vertical offset (`<value>`) to a specific input grid identified by its zero-based index (`<file_number>`) as it was listed with `-wg` or `-allr4s`. This offset is applied to the depth values before weighting. | `-offset 0 0.5` (applies 0.5m offset to the first specified grid) |
| `-out <output_file.r4>` | **Required.** Specifies the path for the output JHC-format 32-bit floating-point weighted-average grid file. | `merged_bath.r4` |
| `-v` | Enable verbose output during processing. | |

## How It Works
1.  **File Opening:** Opens all input `.r4` files and any associated weight files. Opens the output `.r4` file.
2.  **Header Reading:** Reads the `JHC_header` from all input files, ensuring they are geographically co-registered and have compatible dimensions.
3.  **Weight Loading:** For each input grid, it determines its weight:
    *   If `default_weight == 0.0`, it loads pixel-wise weights from `<prefix>.r4_weights` and `<prefix>.r4_weight_depth` files.
    *   If `default_weight > 0.0`, it applies this uniform weight.
    *   If `default_weight < 0.0`, it scales existing pixel-wise weights by the absolute value of `default_weight`.
4.  **Pixel-wise Weighted Averaging:** Iterates through each pixel location in the grid:
    *   For each location, it sums the weighted depth values from all input grids.
    *   It also sums the corresponding weights.
    *   The output pixel value is the sum of weighted depths divided by the sum of weights.
    *   Vertical offsets (from `-offset`) are applied to individual grid depths before weighting.
5.  **Output Header:** Creates a `JHC_header` for the output file and writes it, followed by the processed pixel data.

## Output Files
*   `<output_file.r4>`: A new JHC-format 32-bit floating-point weighted-average grid file.

## Dependencies
*   `array.h`: For `JHC_header` structure and related functions.
*   `support.h`: For general utility functions and error handling.

## Notes
This tool is robust for combining overlapping datasets from different surveys or sensors, allowing for sophisticated control over how each contributes to the final merged grid. Proper weight files are crucial for optimal results.
