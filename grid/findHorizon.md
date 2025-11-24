---
layout: default
title: findHorizon
parent: Grid Tools
nav_order: 31
---
---
layout: default
title: findHorizon
parent: Grid Tools
nav_order: 31
---
# findHorizon

## Description
`findHorizon` is a specialized image processing utility that performs a transform on a JHC float grid (`.r4` file), likely to detect linear or near-linear features (horizons) that exhibit a known curvature. The tool transforms the input image from a standard (x, y) spatial domain into a (roll, y) domain.

The output is a new grid where peaks indicate the presence, vertical position, and "roll" (or tilt) of features in the original image that match the specified curvature. This process is analogous to a slant stack or Radon transform tailored for a specific feature shape, and is likely intended for use with geophysical data like seismic or sidescan sonar profiles where sedimentary layers or other horizons need to be tracked.

## Usage
```bash
findHorizon [-curvature <pixels>] [-roll_step <degrees>] <input_floatfile.r4> <output_filterfile.r4>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `<input_floatfile.r4>` | **Required.** The input JHC-format 32-bit floating-point grid file to be analyzed. | |
| `<output_filterfile.r4>`| **Required.** The name for the output transformed `.r4` grid file. | |
| `-curvature <pixels>` | The amplitude, in pixels, of a sinusoidal shape that defines the curvature of the feature being searched for. | `20.0` |
| `-roll_step <degrees>` | The angular step size used when testing different tilts or "rolls" for the curved feature. This controls the resolution of the output's roll axis. | `0.1` |

## How It Works
1.  **File Opening:** Opens the input `.r4` grid file and creates the output `.r4` file.
2.  **Header Reading:** Reads the `JHC_header` from the input file.
3.  **Output Grid Setup:** Determines the dimensions of the output grid. The Y-dimension will be the same as the input grid (`head.dy`), while the X-dimension will be determined by `roll_step` and the range of possible "roll" angles (e.g., -45 to 45 degrees).
4.  **Transformation Loop:** Iterates through each possible "roll" angle (column in the output grid) and each vertical position (row in the output grid):
    *   For each "roll" angle, it constructs a curved integration path across the width of the input image. This path has a sinusoidal shape defined by `curvature` and `roll_angle`.
    *   It then sums all the pixel values from the input image that lie along this path.
    *   This sum becomes a single pixel value in the output grid.
5.  **Output Header:** Creates a `JHC_header` for the output file and writes it.
6.  **Output Data:** Writes the processed float data to the output file.

## Output Files
*   `<output_filterfile.r4>`: A new JHC-format 32-bit floating-point grid file representing the transformed image (roll vs. vertical position).

## Dependencies
*   `array.h`: For `JHC_header` structure and grid data handling.
*   `support.h`: For general utility functions and error handling.
*   `math.h`: For trigonometric functions.

## Notes
This tool implements a specialized image transform (similar to a slant stack or Radon transform) that can highlight specific linear features within image data, particularly those with a characteristic curvature. This is useful in applications such as seismic interpretation or geological feature detection. Peaks in the output grid indicate the presence and parameters of such features.

## How It Works
For each possible "roll" angle, the tool creates a curved integration path across the width of the input image. This path has a sinusoidal shape defined by the `-curvature` parameter and is tilted according to the current roll angle. It then sums all the pixel values from the input image that lie along this path. This sum becomes a single pixel value in the output grid.

The output grid's X-axis represents the "roll" angle, and its Y-axis corresponds to the vertical position (rows) of the input grid. A bright spot at coordinates `(roll, y)` in the output image signifies that a feature with the defined curvature and a tilt matching `roll` is likely present at vertical position `y` in the input image.
