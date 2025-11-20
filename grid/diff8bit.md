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

## Output Calculation
For each pixel, the output value is calculated as:
`output_pixel = (pixel_from_first_file - pixel_from_second_file) + 128`

The result is clamped to the range [1, 254]. A value of 128 in the output file represents zero difference between the input images.
