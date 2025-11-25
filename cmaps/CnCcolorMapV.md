---
layout: default
title: CnCcolorMapV
parent: Colormap Tools
nav_order: 2
---

# CnCcolorMapV

## Description
`CnCcolorMapV` is a command-line utility for generating a custom-sized color map. It is a variant of `CnCcolorMap`. This tool interpolates between a specified beginning and ending color in the HSV (Hue, Saturation, Value) color space. It then converts the interpolated colors to the RGB (Red, Green, Blue) color space and outputs the resulting RGB triplets.

Unlike `CnCcolorMap`, which always generates 256 colors, this version generates a number of color entries equal to the number of intervals specified by the user.

## Usage
```bash
CnCcolorMapV -b <h:s:v> -e <h:s:v> -i <intervals> [ -o <outfile> ]
```

## Arguments

| Option | Description | Example |
|---|---|---|
| `-b <h:s:v>` | **Required.** Specifies the beginning color in HSV format, with values separated by colons. <br> - `h` (Hue): 0-360 <br> - `s` (Saturation): 0.0-1.0 <br> - `v` (Value): 0.0-1.0 | `-b 0:1.0:1.0` (for red) |
| `-e <h:s:v>` | **Required.** Specifies the ending color in HSV format. | `-e 240:1.0:1.0` (for blue) |
| `-i <intervals>` | **Required.** The number of intervals to use for the interpolation. This will also be the number of colors in the output map. | `-i 16` |
| `-o <outfile>` | Specifies an optional output file to write the color map to. If not provided, the output is written to standard output. | `-o my_colormap.txt` |

## How It Works

1.  **Parse Arguments:** The tool reads the beginning and ending HSV colors and the number of interpolation intervals from the command line.
2.  **Calculate Steps:** It calculates the step size for the Hue, Saturation, and Value components needed to transition from the start color to the end color over the specified number of intervals.
3.  **Interpolate and Convert:** It loops a number of times equal to the `intervals` argument. In each iteration, it:
    a. Calculates the current interpolated HSV color.
    b. Converts the HSV color to its RGB equivalent.
    c. Prints the resulting integer R, G, and B values (ranging from 0 to 255) to the output.
4.  **Output:** The final output is a list containing `<intervals>` lines, with each line containing the space-separated Red, Green, and Blue values for that entry in the color map.