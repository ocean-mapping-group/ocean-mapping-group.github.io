---
layout: default
title: extractVertSection
parent: Grid Tools
nav_order: 29
---
---
layout: default
title: extractVertSection
parent: Grid Tools
nav_order: 29
---
# extractVertSection

## Description
`extractVertSection` is a powerful utility for creating a 2D vertical cross-section from 3D oceanographic model data. The tool traces a path defined by a series of geographic waypoints and samples the full water column from the 3D model at regular intervals along this path. The result is a new 2D JHC grid (`.r4` file) where the X-axis represents the along-track distance and the Y-axis represents depth, with the pixel values being the model parameter at that location.

The tool supports both structured grids (like **SalishSeaCast**) and unstructured triangular-mesh grids (like **SSCOFS/FVCOM**).

## Usage
```bash
extractVertSection -wpts <waypointfile> -interval <meters> -param3D <param.r4> <model_geom_option> [OPTIONS]
```

### Example
```bash
# For a structured grid (SalishSeaCast)
extractVertSection -wpts track.txt -interval 100 -param3D temp.r4 -custom_Salish lat.r4 lon.r4 mask.r4 -maxdepth 300

# For an unstructured grid (SSCOFS)
extractVertSection -wpts track.txt -interval 100 -param3D temp.r4 -custom_SSCOFS quoddy_files/ elem.r4 -maxdepth 300
```

## Arguments

### Required Inputs
| Option | Description |
|---|---|
| `-wpts <waypointfile>` | An ASCII file containing the waypoints (`latitude longitude label`) that define the path for the cross-section. |
| `-interval <meters>` | The sampling distance in meters along the profile path. |
| `-param3D <param.r4>` | The 3D model parameter file to be sliced. This should be a JHC `.r4` grid file composed of multiple 2D layers stacked vertically. The tool expects a corresponding `.zvals` file (defining the depth of each layer) to exist in the same directory. |
| **Model Geometry** | You must specify one of the following options to define the model's grid geometry. |
| `-custom_Salish <lat.r4> <lon.r4> <mask.r4>` | For **structured** grids. Specifies the three geometry files: a grid of node latitudes, a grid of node longitudes, and a land/sea mask. |
| `-custom_SSCOFS <quoddy_prefix> <mapelem.r4>` | For **unstructured** grids. Specifies the prefix for the Quoddy node/element files and a `.r4` grid that maps geographic locations to element numbers. |

### Output and Resampling Options
| Option | Description | Default |
|---|---|---|
| `-maxdepth <meters>` | The maximum depth for the output vertical section grid. | `400.0` |
| `-mindepth <meters>` | The minimum depth for the output vertical section grid. | `0.0` |
| `-depthstep <meters>` | The vertical pixel size (resolution) of the output grid. | `1.0` |
| `-nointerp` | Disables horizontal interpolation. For structured grids, it will pick the value from the nearest node instead of bilinearly interpolating. For unstructured grids, it will pick the value from the first node of the containing triangle instead of performing barycentric interpolation. | Interpolation is on by default. |
| `-show_waypoints` | In the output `.r4` image, this option draws a vertical line to mark the location of each waypoint from the input file. | |
| `-v` | Enable verbose output. | |

## How It Works
1.  **Waypoint Loading:** Reads the waypoint file (`-wpts`), parsing latitude/longitude and converting them to projected Northing/Easting coordinates.
2.  **Model Geometry Loading:** Loads the specified 3D model geometry (either SalishSeaCast files or SSCOFS files).
3.  **Path Sampling:** Creates a series of sample points along the defined path at `interval` spacing.
4.  **Vertical Section Extraction:** For each sample point along the path:
    *   It identifies the corresponding model nodes (for structured grids) or elements (for unstructured grids) that cover the sample point.
    *   For each depth layer in the model:
        *   It extracts the parameter value (from `-param3D`) at that location and depth, using interpolation if `-nointerp` is not set.
        *   These values are then mapped to the appropriate `along-track distance` and `depth` in the output 2D grid.
5.  **Output Grid Creation:** Creates a new 2D JHC `.r4` grid where the X-axis is along-track distance and the Y-axis is depth. The pixel values are the extracted model parameter.
6.  **Waypoint Marking (`-show_waypoints`):** If enabled, draws vertical lines in the output grid at the location of the waypoints.

## Output Files
The tool generates two files based on the `<waypointfile>` name:
1.  **`<waypointfile>.VertSection.r4`**: The primary output. A 2D JHC float grid representing the vertical cross-section.
2.  **`<waypointfile>.VertSection`**: An ASCII log file containing the coordinates (`rx, ry`), parameter value at the surface, and along-track azimuth for each step of the profile.

## Dependencies
*   `array.h`: For `JHC_header` structure and grid data handling.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.

## Notes
This tool is invaluable for detailed analysis of 3D oceanographic model data along specific transects, allowing scientists to visualize vertical variations of parameters like temperature, salinity, or currents across a chosen path. The support for both structured and unstructured grids makes it versatile for different modeling approaches.

## Output Files
The tool generates two files based on the `<waypointfile>` name:
1.  **`<waypointfile>.VertSection.r4`**: The primary output. A 2D JHC float grid representing the vertical cross-section.
2.  **`<waypointfile>.VertSection`**: An ASCII log file containing the coordinates (`rx, ry`), parameter value at the surface, and along-track azimuth for each step of the profile.
