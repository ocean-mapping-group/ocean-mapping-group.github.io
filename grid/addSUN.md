---
layout: default
title: addSUN
parent: Grid Tools
nav_order: 6
---
---
layout: default
title: addSUN
parent: Grid Tools
nav_order: 6
---
# addSUN

## Description
`addSUN` is a command-line utility that takes a JHC-format floating-point (`.r4`) depth grid (a Digital Terrain Model) and generates a shaded relief image (or "sun" image) by calculating the cosine of the angle between an artificial light source (sun) and the normal to each surface facet. It can output either a floating-point sun image or an 8-bit greyscale image. It also supports calculating terrain derivatives (slopes) instead of shaded relief.

## Usage
```bash
addSUN [OPTIONS] <depth_input_file.r4> [sun_output_file]
```
If `sun_output_file` is not provided, a default name like `<input_file_prefix>.sun_<azi>` will be generated.

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-elev <value>` | Specifies the elevation angle (in degrees, from 0 to 90) of the simulated sun. 90 degrees is directly overhead. | `45.0` |
| `-azi <value>` | Specifies the azimuth angle (in degrees, 0-360, clockwise from North) of the simulated sun. | `315.0` |
| `-vert_exag <value>` | Sets the vertical exaggeration factor for the terrain when calculating slopes and normals. | `1.0` |
| `-ignore <value>` | Specifies a floating-point value in the input depth file to be treated as an "ignore" or null value. These points will typically be set to `0.0` in the output. | `0.0` |
| `-float` | Output a JHC-format 32-bit floating-point grid file for the sun illumination (cosine of incident angle). | (Default is 8-bit output) |
| `-8bit` | Explicitly specify 8-bit greyscale output. This is the default behavior if `-float` is not used. | |
| `-deriv` | Instead of shaded relief, calculate terrain derivatives (slopes). If this is used, `-elev` defaults to 90.0 (vertical illumination) and `-vert_exag` to 1.0. Default output range for 8-bit is -20.0 to 20.0. | |
| `-omni` | Used with `-deriv`. Calculates the slope in all directions (omnidirectional slope). | |
| `-magnitude` | Used with `-deriv`. Outputs the absolute magnitude of the slope. | |
| `-log` | Used with `-8bit`. Applies a logarithmic scaling to the output 8-bit intensity values. | |
| `-cossquared` | Applies a cosine-squared function to the output illumination values, potentially increasing contrast. | |
| `-range <min> <max>` | When outputting 8-bit, maps the calculated sun values within this floating-point range to the 0-254 8-bit range. If `-deriv` is used and no range is specified, defaults to -20.0 to 20.0. | `0.0 255.0` (for non-deriv 8bit) |
| `-xystep <value>` | Overrides the X and Y step values in the output JHC header with the specified float value. | |
| `<depth_input_file.r4>` | **Required.** The input JHC-format 32-bit floating-point depth grid file. The tool will also attempt to append `.r4` if the file is not found. | `bathymetry.r4` |
| `[sun_output_file]` | **Optional.** The name for the output sun illumination or derivative file. If not provided, a default name will be generated. | `bathymetry.sun_315` |

## How It Works
1.  **File Opening:** Opens the input `.r4` depth grid and the output file.
2.  **Header Reading:** Reads the `JHC_header` from the input file.
3.  **Slope and Normal Calculation:** Iterates through each pixel in the input grid:
    *   For each pixel, it accesses its own value and the values of its eight neighbors (using `get_map_value` and handling `ignore_val`).
    *   It calculates the local slope (derivatives in X and Y directions), accounting for `vert_exag`.
    *   From the slopes, it derives the normal vector to the surface facet.
4.  **Shaded Relief / Derivative Calculation:**
    *   If `-deriv` is set:
        *   If `-omni`, it calculates the slope magnitude in all directions.
        *   If `-magnitude`, it calculates the absolute magnitude of the slope.
        *   Otherwise, it calculates the slope in the direction of the sun (`azi`).
    *   Otherwise (default shaded relief):
        *   It calculates the cosine of the angle between the sun's direction vector (`azi`, `elev`) and the surface normal. This cosine value represents the shaded relief intensity.
        *   If `-cossquared` is set, it squares this value.
5.  **Output Scaling:**
    *   If `-float` is set, the raw calculated float value is written to the output.
    *   If `-8bit` (default) is set, the float value is scaled to an 8-bit unsigned char (0-254 range), potentially applying logarithmic scaling (`-log`) and mapping to a user-defined `range`.
6.  **Output Header:** Creates a `JHC_header` for the output file and writes it, followed by the processed pixel data.

## Output Files
*   `[sun_output_file]`: A JHC-format `.r4` (float) or `.8bit` (unsigned char) grid file containing the shaded relief image or terrain derivatives.

## Dependencies
*   `array.h`: For `JHC_header` structure and related functions (`get_JHC_map_value`).
*   `support.h`: For general utility functions and error handling.
*   `backscatter.h`: For `dget360offsets` and `dcosangle` functions (for angle calculations).

## Notes
Shaded relief images are commonly used in cartography and GIS to visually enhance topographic features, making them appear three-dimensional. The ability to calculate terrain derivatives directly can be useful for geomorphological analysis.
