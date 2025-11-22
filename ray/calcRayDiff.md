---
layout: default
title: calcRayDiff
parent: Ray Tools
nav_order: 164
---
# calcRayDiff

## Description
`calcRayDiff` is a specialized utility designed to compare two sound velocity profiles (SVPs) by calculating the depth differences predicted by ray tracing through each SVP. It takes two SVP files (typically from a BOT MVP100/200/XXX profiler), builds Time-Angle (TA) lookup tables for each, differences their predicted depths, and then reprojects these differences into Across-track/Depth (XZ) space.

The primary purpose of this tool is to provide a graphical output (currently a PGM image) that quantifies the absolute scale of depth anomalies at every depth-across track position, which can be encountered by a shipboard sonar. This helps users understand the impact of using one SVP over another on multibeam bathymetry.

## Usage
```bash
calcRayDiff -pro1 <file1> -pro2 <file2> -outimage <image_file> [-tdcr_dep <val>] [-maxangle <val>] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `-pro1 <file1>` | **Required.** Path to the first SVP file (MVP format). |
| `-pro2 <file2>` | **Required.** Path to the second SVP file (MVP format). |
| `-outimage <image_file>` | **Required.** Output PGM (Portable Graymap) image file, showing depth differences. |
| `-tdcr_dep <val>` | Transducer depth (meters). | `2.5` |
| `-maxangle <val>` | Maximum beam angle to trace (degrees). | `75.0` |
| `-v` | Enable verbose output. |

## How It Works

1.  **Initialization:** Parses command-line arguments to get input/output filenames and ray tracing parameters (`transducer_depth`, `maxangle`).
2.  **SVP Reading (`read_MVP()`):**
    *   Opens the two input SVP files (`-pro1`, `-pro2`).
    *   Calls `read_MVP()` to parse the MVP-formatted SVP files. This function reads depth-velocity pairs (`ZVpair`) and stores them in `raw_zv1` and `raw_zv2` arrays. It skips initial header lines from the MVP format.
    *   Closes the SVP files.
3.  **Water Column Initialization (`jWC_init()`):**
    *   Initializes two `watercolumn` structures (`wc1`, `wc2`) using `jWC_init()` (an external function). These structures will hold the processed SVPs and ray trace results.
    *   Determines `max_depth` and `max_range` based on the input SVPs and `maxangle`.
4.  **SVP Interpolation (`jWC_interp_zv()`):**
    *   Interpolates the raw SVP data within `wc1` and `wc2` into a finely layered model (e.g., constant velocity layers). This prepares the water column for ray tracing.
5.  **Ray Tracing (`jWC_trace()`):**
    *   Performs ray tracing through `wc1` and `wc2` to generate internal Time-Angle (TA) lookup tables for depth.
6.  **Time Series Resampling (`jWC_resample_timeseries()`):**
    *   Resamples the ray trace results into a uniform time-angle grid for easier comparison.
7.  **Across-track/Depth (XZ) Interpolation (`jWC_interp_XZ()`):**
    *   Interpolates the ray trace results into an XZ grid (Across-track/Depth) for `wc1`.
8.  **Difference Calculation (`AT_difference()`):**
    *   Creates a new `farray` (`AT_diff`) to store the differences in depth between `wc1.AT_depth` and `wc2.AT_depth` in Time-Angle space.
9.  **Reprojection to XZ Space (`AT_to_XZ_reproject()`):**
    *   Creates a new `farray` (`XZ_diff`) to store the depth differences in Across-track/Depth space.
    *   Uses the XZ-interpolated time and angle grids from `wc1` (`wc1.XZ_time`, `wc1.XZ_angle`) to map the `AT_diff` values into the `XZ_diff` grid.
10. **Output to PGM (`write_out_PGM()`):**
    *   Writes the `XZ_diff` array as a PGM (Portable Graymap) image, where pixel intensity represents the magnitude of the depth difference.
11. **Cleanup:** Frees all allocated `farray` and `watercolumn` memory.

## Helper Functions

*   `read_MVP(FILE *grazfile, ZVpair *zvp, int *novals, int vflag)`: Reads depth-velocity pairs from an MVP-formatted SVP file.
*   `getc_line(FILE *file, char *string, int printit)`: Reads a line from a file.
*   `AT_difference(farray *at1z, farray *at2z, farray *atdiffz)`: Calculates the difference between two `farray` structures.
*   `AT_to_XZ_reproject(farray *xzdiff, farray *atdiff, farray *xztime, farray *xzangle)`: Reprojects data from Time-Angle space to Across-track/Depth space.
*   `write_out_PGM(farray *fa)`: Writes an `farray` to a PGM image file.

## Data Structures (from `j_watercolumn.h`, `j_farray.h`)

*   `watercolumn`: Stores SVP data and ray tracing results (TA and XZ lookup tables).
*   `ZVpair`: A pair of depth and sound velocity values.
*   `farray`: A generic 2D floating-point array structure with associated metadata.
```
```
---
layout: default
title: calcRayDiff
parent: Ray Tools
nav_order: 164
---
# calcRayDiff

## Description
`calcRayDiff` is a specialized utility designed to compare two sound velocity profiles (SVPs) by calculating the depth differences predicted by ray tracing through each SVP. It takes two SVP files (typically from a BOT MVP100/200/XXX profiler), builds Time-Angle (TA) lookup tables for each, differences their predicted depths, and then reprojects these differences into Across-track/Depth (XZ) space.

The primary purpose of this tool is to provide a graphical output (currently a PGM image) that quantifies the absolute scale of depth anomalies at every depth-across track position, which can be encountered by a shipboard sonar. This helps users understand the impact of using one SVP over another on multibeam bathymetry.

## Usage
```bash
calcRayDiff -pro1 <file1> -pro2 <file2> -outimage <image_file> [-tdcr_dep <val>] [-maxangle <val>] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `-pro1 <file1>` | **Required.** Path to the first SVP file (MVP format). |
| `-pro2 <file2>` | **Required.** Path to the second SVP file (MVP format). |
| `-outimage <image_file>` | **Required.** Output PGM (Portable Graymap) image file, showing depth differences. |
| `-tdcr_dep <val>` | Transducer depth (meters). | `2.5` |
| `-maxangle <val>` | Maximum beam angle to trace (degrees). | `75.0` |
| `-v` | Enable verbose output. |

## How It Works

1.  **Initialization:** Parses command-line arguments to get input/output filenames and ray tracing parameters (`transducer_depth`, `maxangle`).
2.  **SVP Reading (`read_MVP()`):**
    *   Opens the two input SVP files (`-pro1`, `-pro2`).
    *   Calls `read_MVP()` to parse the MVP-formatted SVP files. This function reads depth-velocity pairs (`ZVpair`) and stores them in `raw_zv1` and `raw_zv2` arrays. It skips initial header lines from the MVP format.
    *   Closes the SVP files.
3.  **Water Column Initialization (`jWC_init()`):**
    *   Initializes two `watercolumn` structures (`wc1`, `wc2`) using `jWC_init()` (an external function). These structures will hold the processed SVPs and ray trace results.
    *   Determines `max_depth` and `max_range` based on the input SVPs and `maxangle`.
4.  **SVP Interpolation (`jWC_interp_zv()`):**
    *   Interpolates the raw SVP data within `wc1` and `wc2` into a finely layered model (e.g., constant velocity layers). This prepares the water column for ray tracing.
5.  **Ray Tracing (`jWC_trace()`):**
    *   Performs ray tracing through `wc1` and `wc2` to generate internal Time-Angle (TA) lookup tables for depth.
6.  **Time Series Resampling (`jWC_resample_timeseries()`):**
    *   Resamples the ray trace results into a uniform time-angle grid for easier comparison.
7.  **Across-track/Depth (XZ) Interpolation (`jWC_interp_XZ()`):**
    *   Interpolates the ray trace results into an XZ grid (Across-track/Depth) for `wc1`.
8.  **Difference Calculation (`AT_difference()`):**
    *   Creates a new `farray` (`AT_diff`) to store the differences in depth between `wc1.AT_depth` and `wc2.AT_depth` in Time-Angle space.
9.  **Reprojection to XZ Space (`AT_to_XZ_reproject()`):**
    *   Creates a new `farray` (`XZ_diff`) to store the depth differences in Across-track/Depth space.
    *   Uses the XZ-interpolated time and angle grids from `wc1` (`wc1.XZ_time`, `wc1.XZ_angle`) to map the `AT_diff` values into the `XZ_diff` grid.
10. **Output to PGM (`write_out_PGM()`):**
    *   Writes the `XZ_diff` array as a PGM (Portable Graymap) image, where pixel intensity represents the magnitude of the depth difference.
11. **Cleanup:** Frees all allocated `farray` and `watercolumn` memory.

## Helper Functions

*   `read_MVP(FILE *grazfile, ZVpair *zvp, int *novals, int vflag)`: Reads depth-velocity pairs from an MVP-formatted SVP file.
*   `getc_line(FILE *file, char *string, int printit)`: Reads a line from a file.
*   `AT_difference(farray *at1z, farray *at2z, farray *atdiffz)`: Calculates the difference between two `farray` structures.
*   `AT_to_XZ_reproject(farray *xzdiff, farray *atdiff, farray *xztime, farray *xzangle)`: Reprojects data from Time-Angle space to Across-track/Depth space.
*   `write_out_PGM(farray *fa)`: Writes an `farray` to a PGM image file.

## Data Structures (from `j_watercolumn.h`, `j_farray.h`)

*   `watercolumn`: Stores SVP data and ray tracing results (TA and XZ lookup tables).
*   `ZVpair`: A pair of depth and sound velocity values.
*   `farray`: A generic 2D floating-point array structure with associated metadata.
```
```