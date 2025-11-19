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
| `-interval <meters>` | **Required.** The sampling distance in meters along the profile path between waypoints. | `-interval 50.0` |
| `-topo <dtm.r4>` | **Required (can be used multiple times).** Specifies a JHC float grid file to extract data from. If multiple `-topo` files are provided, a profile will be extracted from each one (if the path intersects it). | `-topo survey_area.r4` |
| `-decdeg` | If specified, the tool will read the `<waypointfile>` as simple space-separated decimal degrees (`latitude longitude value`) instead of the default format. | |
| `-aplot` | Toggles the output format to a simple two-column file (`along-track_distance  value`), which is suitable for direct plotting. The default output is a three-column geographic file (`latitude longitude depth`). | |
| `-calc_along_slope` | Instead of extracting depth, this option calculates and outputs the along-track slope in degrees. | |

### Filtering Options
These options apply post-processing filters to the extracted profile data. A filtered output file named `<waypointfile>.filt_prof` will be created.

| Option | Description | Default / Example |
|---|---|---|
| `-filtlen <meters>` | Applies a running-average (boxcar) filter to the profile. `<meters>` specifies the full width of the filter. | `-filtlen 500.0` |
| `-domedian <samples>` | Applies a median filter. The filter window size is `(2 * samples) + 1`. | `-domedian 5` |
| `-doaverage <samples>` | Applies a mean (average) filter. The filter window size is `(2 * samples) + 1`. | `-doaverage 3` |

### Other Options
| Option | Description |
|---|---|
| `-use_xaxis_relative` | Used with `-aplot`. The output's X-axis will be the projected X-coordinate from the grid's projection, rather than the cumulative along-track distance. |
| `-v` | Enable verbose output. |

## Output Files
*   **`<waypointfile>.profile`**: The primary output file containing the extracted profile data.
*   **`<waypointfile>.filt_prof`**: Created only if a filtering option (`-domedian`, `-doaverage`, or `-filtlen`) is used. Contains the filtered profile.
