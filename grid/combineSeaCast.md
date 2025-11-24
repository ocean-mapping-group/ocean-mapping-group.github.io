---
layout: default
title: combineSeaCast
parent: Grid Tools
nav_order: 11
---
---
layout: default
title: combineSeaCast
parent: Grid Tools
nav_order: 11
---
# combineSeaCast

## Description
`combineSeaCast` is a command-line utility that processes gridded output from an oceanographic model (likely SeaCast, given the name) to derive current magnitude and azimuth. It takes four JHC-format 32-bit floating-point (`.r4`) grid files as input: latitude, longitude, U-velocity (eastward), and V-velocity (northward). It then calculates the vector magnitude and direction (azimuth) for the current at each grid node and outputs these as a series of JCU navigation records (latitude, longitude, magnitude, azimuth) to an ASCII file, suitable for plotting as vectors on a map.

## Usage
```bash
combineSeaCast -lat <file_lat.r4> -lon <file_lon.r4> -uvel <file_uvel.r4> -vvel <file_vvel.r4> -out <output.nav> [OPTIONS]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-lat <file_lat.r4>` | **Required.** Path to the JHC-format `.r4` grid file containing latitude values for each grid node. | `lat_grid.r4` |
| `-lon <file_lon.r4>` | **Required.** Path to the JHC-format `.r4` grid file containing longitude values for each grid node. | `lon_grid.r4` |
| `-uvel <file_uvel.r4>` | **Required.** Path to the JHC-format `.r4` grid file containing eastward (U) velocity components for each grid node. | `u_velocity.r4` |
| `-vvel <file_vvel.r4>` | **Required.** Path to the JHC-format `.r4` grid file containing northward (V) velocity components for each grid node. | `v_velocity.r4` |
| `-out <output.nav>` | **Required.** Path for the output JCU navigation format file, containing latitude, longitude, current magnitude, and azimuth for each grid node. | `current_vectors.nav` |
| `-v` | Enable verbose output during processing. | |

## How It Works
1.  **File Opening:** Opens the four input `.r4` grid files (latitude, longitude, U-velocity, V-velocity) and the output `.nav` file.
2.  **Header Reading:** Reads the `JHC_header` from the input files, ensuring their dimensions match.
3.  **Pixel Iteration:** Iterates through each corresponding pixel in the input grids:
    *   Reads `latitude`, `longitude`, `u_velocity`, and `v_velocity` for the current grid node.
    *   Calculates the `magnitude` of the current vector: `sqrt(u_velocity^2 + v_velocity^2)`.
    *   Calculates the `azimuth` of the current vector: `atan2(u_velocity, v_velocity)`.
    *   Populates a `jcu_nav_rec` structure with `latitude`, `longitude`, `magnitude`, and `azimuth`.
    *   Writes the `jcu_nav_rec` to the output `.nav` file.

## Output Files
*   `<output.nav>`: An ASCII file in JCU navigation format, where each record contains latitude, longitude, current magnitude, and azimuth.

## Dependencies
*   `array.h`: For `JHC_header` structure and related functions.
*   `support.h`: For general utility functions and error handling.
*   `jcu_nav.h`: For `jcu_nav_rec` structure and related functions.

## Notes
The output `.nav` file can be directly used by plotting tools that support the JCU navigation format to visualize current vectors overlaid on a map. This tool is valuable for converting model output into a readily plottable format for oceanographic analysis.
