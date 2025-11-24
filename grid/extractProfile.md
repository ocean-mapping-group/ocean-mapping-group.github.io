--- 
layout: default
title: extractProfile
parent: Grid Tools
nav_order: 27
---
# extractProfile

## Description
`extractProfile` is a command-line utility that extracts 2D depth profiles from one or more JHC-format 32-bit floating-point grid files (`.r4` DTMs). The tool traces a path defined by a series of geographic waypoints, samples the DTM(s) at a regular interval along this path, and outputs the resulting profile. It also includes options for filtering (median, average) and calculating the along-track slope.

## Usage
```bash
extractProfile -wpts <waypointfile> -interval <meters> -topo <dtm1.r4> [-topo <dtm2.r4> ...] [OPTIONS]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-wpts <waypointfile>` | **Required.** An ASCII file containing the waypoints that define the profile path. The default format is `LABEL DEG MIN DEG MIN`. | `-wpts my_track.txt` |
| `-interval <meters>` | **Required.** The sampling distance in meters along the profile path between waypoints. | `50.0` |
| `-topo <dtm.r4>` | **Required (can be used multiple times).** Specifies a JHC float grid file to extract data from. If multiple `-topo` files are provided, a profile will be extracted from each one (if the path intersects it). | `-topo survey_area.r4` |
| `-decdeg` | If specified, the tool will read the `<waypointfile>` as simple space-separated decimal degrees (`latitude longitude value`) instead of the default format. | |
| `-aplot` | Toggles the output format to a simple two-column file (`along-track_distance  value`), which is suitable for direct plotting. The default output is a three-column geographic file (`latitude longitude depth`). | |
| `-calc_along_slope` | Instead of extracting depth, this option calculates and outputs the along-track slope in degrees. | |

### Filtering Options
These options apply post-processing filters to the extracted profile data. A filtered output file named `<waypointfile>.filt_prof` will be created.

| Option | Description | Default / Example |
|---|---|---|
| `-filtlen <meters>` | Applies a running-average (boxcar) filter to the profile. `<meters>` specifies the full width of the filter. | `500.0` |
| `-domedian <samples>` | Applies a median filter. The filter window size is `(2 * samples) + 1`. | `5` |
| `-doaverage <samples>` | Applies a mean (average) filter. The filter window size is `(2 * samples) + 1`. | `3` |

### Other Options
| Option | Description |
|---|---|
| `-use_xaxis_relative` | Used with `-aplot`. The output's X-axis will be the projected X-coordinate from the grid's projection, rather than the cumulative along-track distance. |
| `-v` | Enable verbose output. | |

## How It Works
1.  **Waypoint Loading:** Reads the waypoint file (`-wpts`), parsing latitude/longitude and converting them to projected Northing/Easting coordinates.
2.  **DTM Loading:** Loads all specified DTMs (`-topo`) into memory.
3.  **Path Interpolation:** Interpolates between waypoints to create a series of sample points along the defined path at `interval` spacing.
4.  **Profile Extraction:** For each sample point along the path:
    *   It determines the geographic coordinates.
    *   For each DTM, it projects the geographic coordinates to pixel coordinates on the DTM.
    *   It bilinearly interpolates the DTM to get the depth (or slope if `-calc_along_slope`) at that location.
    *   The extracted value is stored.
5.  **Filtering (`-filtlen`, `-domedian`, `-doaverage`):** If any filtering options are specified, the extracted profile data is smoothed using the chosen filter.
6.  **Output:** Writes the processed profile data to either a geographic ASCII file (`.profile`) or a two-column plotting file (`.aplot`) if `-aplot` is specified. If filtering is applied, a `filt_prof` file is also generated.

## Output Files
*   **`<waypointfile>.profile`**: The primary output file containing the extracted profile data (geographic or raw values).
*   **`<waypointfile>.aplot`**: Two-column ASCII file for plotting (if `-aplot` is used).
*   **`<waypointfile>.filt_prof`**: Filtered profile data (if a filtering option is used).

## Dependencies
*   `array.h`: For `JHC_header` structure and DTM data handling.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.

## Notes
This tool is invaluable for creating cross-sectional views of gridded data, which are often used for geological interpretation, engineering design, or habitat mapping. The filtering options allow for noise reduction or highlighting of specific features. The `-calc_along_slope` option provides insight into the terrain's gradient along the profile.

