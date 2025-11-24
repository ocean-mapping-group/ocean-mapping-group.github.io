---
layout: default
title: diff8bit
parent: Grid Tools
nav_order: 20
---
---
layout: default
title: diff8bit
parent: Grid Tools
nav_order: 20
---
# diff8bit

## Description
`diff8bit` is a command-line utility that computes the pixel-wise difference between two 8-bit JHC-format grid files. It subtracts the second image from the first, offsets the result to place zero-difference at a mid-level grey (128), and saves the output as a new 8-bit grid. This is useful for change detection or comparing two images, like sidescan mosaics.

## Usage
```bash
diff8bit -first <file1.8bit> -second <file2.8bit> -out <output.8bit> [OPTIONS]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-first <file1.8bit>` | **Required.** Specifies the path to the first input JHC-format 8-bit grid file (the minuend). | `-first image_A.8bit` |
| `-second <file2.8bit>` | **Required.** Specifies the path to the second input JHC-format 8-bit grid file (the subtrahend). | `-second image_B.8bit` |
| `-out <output.8bit>` | **Required.** Specifies the path for the output JHC-format 8-bit grid file that will store the difference. | `-out difference.8bit` |
| `-ignore <value>` | Specifies a pixel value (0-255) to be treated as an ignore or "no data" value. If a pixel in either input file has this value, the corresponding output pixel will be set to 0. | `0` |
| `-stats` | If specified, the tool will calculate and print the mean and standard deviation of the final difference values (in Digital Numbers, after the 128-offset is applied). | |

## How It Works
1.  **File Opening:** Opens the two input 8-bit grid files and the output 8-bit grid file.
2.  **Header Reading:** Reads the `JHC_header` from both input files, ensuring their dimensions match.
3.  **Pixel-wise Difference:** Iterates through each pixel in the input grids:
    *   Reads the 8-bit pixel values from the first and second input files.
    *   If either pixel value is `ignore_val`, the output pixel is set to `0`.
    *   Otherwise, the difference is calculated as `pixel_first - pixel_second + 128`.
    *   The result is clamped to the range [1, 254] (or 0 if `ignore_val` was present).
4.  **Statistics (`-stats`):** If enabled, calculates the mean and standard deviation of the valid difference values and prints them.
5.  **Output Header:** Creates a `JHC_header` for the output file (copied from the first input file's header, but with updated `min_value` and `max_value`) and writes it to the output file.
6.  **Output Data:** Writes the processed 8-bit pixel data to the output file.

## Output Files
*   `<output.8bit>`: A new JHC-format 8-bit grid file containing the pixel-wise difference.

## Notes
The output `JHC_header`'s `min_value` and `max_value` are set to `1` and `254` respectively, as the pixel values are typically centered around `128` (representing zero difference). This tool is useful for visualizing changes between two successive image acquisitions or for quick quality control.

## Output Calculation
For each pixel, the output value is calculated as:
`output_pixel = (pixel_from_first_file - pixel_from_second_file) + 128`

The result is clamped to the range [1, 254]. A value of 128 in the output file represents zero difference between the input images.
