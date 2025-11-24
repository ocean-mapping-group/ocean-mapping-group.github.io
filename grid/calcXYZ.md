---
layout: default
title: calcXYZ
parent: Grid Tools
nav_order: 10
---
---
layout: default
title: calcXYZ
parent: Grid Tools
nav_order: 10
---
# calcXYZ

## Description
`calcXYZ` is a command-line utility designed to generate XYZ coordinate data (suitable for gridding with `surface.c`) from stereo imagery or other parallax-derived inputs. It takes a correlation coefficient map (indicating data quality) and a parallax map as input. For valid points, it calculates the 3D position based on camera geometry parameters (focal length, camera separation) and outputs them as an ASCII XYZ file. It can also process sub-pixel parallax solutions.

## Usage
```bash
calcXYZ [OPTIONS] -coeff <coeff_map.8bit> -parallax <parallax_map.8bit> -out <output.xyz>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-coeff <coeff_map.8bit>` | **Required.** Specifies the path to the 8-bit JHC-format correlation coefficient map. Only pixels above a minimum coefficient threshold will be processed. | `corr_coeff.8bit` |
| `-parallax <parallax_map.8bit>` | **Required.** Specifies the path to the 8-bit JHC-format parallax map. This map typically contains encoded X-parallax values. | `x_parallax.8bit` |
| `-out <output.xyz>` | **Required.** Specifies the path for the output ASCII XYZ file. Each line in this file will contain X, Y, and Z coordinates. | `3d_points.xyz` |
| `-spix <subpixel_input_file.txt>` | If specified, the tool will read sub-pixel parallax solutions from this ASCII file instead of the 8-bit parallax map. The format of this file is assumed to be: `i j xpar ypar Xpar Ypar coeff`. | `subpix_data.txt` |
| `-mincoeff <value>` | Sets the minimum correlation coefficient threshold. Pixels with a coefficient below this value will be ignored. | `50` |
| `-flen <value>` | Specifies the camera's focal length in millimeters, used in the 3D reconstruction calculations. | `50.0` |
| `-csep <value>` | Specifies the camera separation (baseline) in millimeters, used in the 3D reconstruction calculations. | `220.0` |
| `-v` | Enable verbose output, printing detailed information during processing. | |

## How It Works
1.  **File Opening:** Opens the input correlation coefficient map (`-coeff`), parallax map (`-parallax`), and the output XYZ file. If `-spix` is used, it opens the sub-pixel input file instead of the parallax map.
2.  **Header Reading:** Reads the `JHC_header` from the correlation coefficient map.
3.  **Parameter Setup:** Initializes `focal_length`, `camera_separation`, and `min_coefficient` from command-line arguments.
4.  **Pixel Iteration:** Iterates through each pixel in the input image grids:
    *   Reads the correlation coefficient and parallax value for the current pixel.
    *   If the coefficient is above `min_coefficient` (and the parallax value is valid):
        *   **3D Coordinate Calculation:** Uses the `focal_length`, `camera_separation`, and parallax value to calculate the 3D X, Y, Z coordinates for that pixel. This involves trigonometric calculations based on stereo geometry.
        *   Writes the X, Y, Z coordinates to the output ASCII file.
5.  **Sub-pixel Mode (`-spix`):** If this option is used, the tool reads pre-computed sub-pixel solutions (X, Y, Z coordinates) directly from the specified ASCII file, bypassing the image processing steps.

## Output Files
*   `<output.xyz>`: An ASCII file containing `X Y Z` coordinates for each valid point.

## Dependencies
*   `array.h`: For `JHC_header` structure.
*   `support.h`: For general utility functions and error handling.
*   `math.h`: For mathematical functions.

## Notes
This tool is fundamental for generating 3D point clouds from stereo imagery, which can then be used for terrain modeling or other spatial analyses. The quality of the output point cloud heavily depends on the accuracy of the input parallax and correlation coefficient maps, as well as the calibration parameters (`-flen`, `-csep`).
