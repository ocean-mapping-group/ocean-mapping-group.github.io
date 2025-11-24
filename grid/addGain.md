---
layout: default
title: addGain
parent: Grid Tools
nav_order: 4
---
---
layout: default
title: addGain
parent: Grid Tools
nav_order: 4
---
# addGain

## Description
`addGain` is a command-line utility that applies a gain correction to an 8-bit image (likely a sidescan mosaic or intensity map) based on depth information from a corresponding floating-point (`.r4`) depth grid. This effectively normalizes the image intensity with respect to the water depth, compensating for signal loss over longer ranges. The output is a new 8-bit image file.

## Usage
```bash
addGain [OPTIONS] <base_filename> <output_8bit_file>
```
The `<base_filename>` is expected to be a prefix that will be appended with `.r4` for the float depth file and `.mos` for the 8-bit mosaic file. The `<output_8bit_file>` will be the resulting gained 8-bit image.

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-normal <value>` | Specifies a "normal" depth value (in meters) around which the gain normalization is centered. Depths shallower than this value will receive less gain, and deeper values more gain. | `100.0` |
| `<base_filename>` | **Required.** The base name for the input files. The tool will look for `<base_filename>.r4` (for depth) and `<base_filename>.mos` (for the 8-bit mosaic to be gained). | `survey_area` (looks for `survey_area.r4` and `survey_area.mos`) |
| `<output_8bit_file>` | **Required.** The name of the output 8-bit grid file, which will contain the depth-gained image. | `gained_image.8bit` |

## How It Works
1.  **File Opening:** Opens the input 8-bit image (`.mos`), the input depth grid (`.r4`), and the output 8-bit image file.
2.  **Header Reading:** Reads the `JHC_header` from the input files, extracting dimensions and scaling information.
3.  **Gain Calculation:** A lookup table `gain_look` is pre-calculated. For each possible depth value (scaled from 0 to 255), it stores a gain factor based on the `-normal` depth. The gain factor is calculated as `(depth / normal_depth)^2`.
4.  **Pixel-wise Gain Application:** Iterates through each pixel in the input image and corresponding depth grid:
    *   Reads the 8-bit pixel value from the input image.
    *   Reads the float depth value from the depth grid.
    *   If the depth value is valid (not `0.0`):
        *   Determines the appropriate gain factor from `gain_look` based on the current depth.
        *   Multiplies the input image pixel value by this gain factor.
        *   Clamps the result to the 8-bit range (0-254) and writes it to the output image.
    *   If the depth value is `0.0`, the output pixel is set to `0`.
5.  **Output Header:** Updates the `JHC_header` for the output file and writes it to the output file.

## Output Files
*   `<output_8bit_file>`: A new JHC-format 8-bit grid file.

## Dependencies
*   `array.h`: For `JHC_header` structure and related functions.
*   `support.h`: For general utility functions and error handling.

## Notes
The gain correction is applied to compensate for the fact that a sonar signal loses intensity with increasing depth/range. By normalizing to a `normal_depth`, deeper areas receive more gain and shallower areas less, aiming for a more uniform image intensity across varying bathymetry.
