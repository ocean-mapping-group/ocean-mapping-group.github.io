---
layout: default
title: CnCcolorMap
parent: Colormap Tools
nav_order: 1
---

# CnCcolorMap

## Description
`CnCcolorMap` is a command-line utility that generates a 256-entry color map. It works by interpolating between a specified beginning and ending color in the HSV (Hue, Saturation, Value) color space. The tool calculates the intermediate colors and converts them to the RGB (Red, Green, Blue) color space, outputting a list of 256 RGB triplets.

This tool is useful for creating custom color palettes for use in visualization software.

## Usage
```bash
CnCcolorMap -b <h:s:v> -e <h:s:v> -i <intervals> [ -o <outfile> ]
```

## Arguments

| Option | Description | Example |
|---|---|---|
| `-b <h:s:v>` | **Required.** Specifies the beginning color in HSV format, with values separated by colons. <br> - `h` (Hue): 0-360 <br> - `s` (Saturation): 0.0-1.0 <br> - `v` (Value): 0.0-1.0 | `-b 0:1.0:1.0` (for red) |
| `-e <h:s:v>` | **Required.** Specifies the ending color in HSV format. | `-e 240:1.0:1.0` (for blue) |
| `-i <intervals>` | **Required.** The number of discrete intervals to use for the interpolation between the start and end colors. | `-i 10` |
| `-o <outfile>` | Specifies an optional output file to write the color map to. If not provided, the output is written to standard output. | `-o my_colormap.txt` |

## How It Works

1.  **Parse Arguments:** The tool reads the beginning and ending HSV colors and the number of interpolation intervals from the command line.
2.  **Calculate Steps:** It calculates the step size for each of the H, S, and V components required to transition from the start color to the end color over the specified number of intervals.
3.  **Interpolate and Convert:** It loops 256 times to generate the full color map. In each iteration, it:
    a. Calculates the current interpolated HSV color.
    b. Converts the HSV color to its RGB equivalent using a standard conversion algorithm.
    c. Prints the resulting integer R, G, and B values (ranging from 0 to 255) to the output.
4.  **Output:** The final output is a list of 256 lines, with each line containing the space-separated Red, Green, and Blue values for that entry in the color map.

*Note: The source code contains an infinite `goto retry` loop for interactive testing which appears to be a remnant; the primary functionality is the command-line-driven color map generation.*