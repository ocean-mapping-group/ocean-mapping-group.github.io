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