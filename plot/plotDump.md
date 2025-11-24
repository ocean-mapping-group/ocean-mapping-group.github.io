---
layout: default
title: plotDump
parent: Plot Tools
nav_order: 138
---
# plotDump

## Description
`plotDump` is a versatile plotting utility designed to visualize time-series data dumps, typically from `DelayEditor` or other processing tools. It can plot various navigation, motion, and sonar-related parameters (e.g., heave, roll, pitch, depths, velocities, accelerations) against time or another parameter.

The tool supports plotting multiple data series on a single graph, filtering, applying squat models, and displaying ranges from multibeam merged files. It's highly interactive, prompting the user for plot choices and ranges.

## Usage
```bash
plotDump -infile <file1> [-infile <file2> ...] [-outfile <filename.meta>] [OPTIONS] <merged_file(s)...>
```

## Arguments

| Option | Description |
|---|---|
| `-infile <file1> ...` | **Required.** One or more input ASCII files containing time-series data. |
| `-outfile <filename.meta>` | Specifies the output PostScript metafile name. | `plot.meta` |
| `-size <dx> <dy>` | Specifies the plot size in centimeters. | `20.0 25.0` |
| `-xplot` | Enables plotting one parameter against another (X-Y plot) instead of against time. | |
| `-dofilt` | Enables interactive filtering of data before plotting. | |
| `-filtlen <val>` | Specifies the length of the boxcar filter (number of samples) if filtering is enabled. | `2` |
| `-squat <bias> <linear> <square>` | Overlays a squat model onto the plot (requires `-xplot`). | |
| `-filtdepth` | (Present in `USAGE`, but implementation not fully shown for plotting) Intended for filtering depth. | |
| `-label <string>` | Adds a custom title to the plot. | |
| `-sparse` | (Present in `USAGE`, but implementation not fully shown for plotting) Intended for sparse plotting. | |
| `-xrange <min> <max>` | Sets the X-axis range. | Auto-determined. |
| `<merged_file(s)...>` | (Optional) One or more merged files. Their time extents will be indicated on the plot. |

## Interactive Mode
After launching, `plotDump` will guide the user through a series of prompts:

1.  **Number of Plots (`noplots`):** Prompts for how many vertical subplots to create.
2.  **Y-axis Bounds (per plot):** For each plot, it prompts for Y-axis minimum (`ymin[i]`) and maximum (`ymax[i]`) values. It can auto-calculate a range around the average value if `ymin[i]` is set to `-999.0`.
3.  **Parameter Selection (Y-axis):** For each subplot, it presents a menu of 56 available parameters and prompts the user to choose which one to plot on the Y-axis.
4.  **Parameter Selection (X-axis, if `-xplot`):** If `-xplot` is enabled, it presents the same menu and prompts for the parameter to plot on the X-axis.
5.  **Filtering (`-dofilt`):** If `-dofilt` is enabled, it asks the user if they want to filter the current time series and applies a boxcar filter with `filtlen`.
6.  **Continue Plotting:** After plotting one line in a subplot, it asks if the user wants to plot another line in the same subplot.

## How It Works
1.  **Initialization:** Parses command-line arguments to set plotting options, input file names, and ranges. Initializes a `plotlib` PostScript output (`plot.meta`).
2.  **Input File Reading:**
    *   Opens all input ASCII files specified by `-infile`.
    *   Reads metadata from each file (file name, time range, X range, start/end records, `delay`, `lag`, `scale_factor`).
    *   Determines `total_mintime` and `total_maxtime` across all files.
    *   Allocates memory for `values[MAX_NOVALUES]` to store all data.
    *   Reads all data from all input files into the `values` array, normalizing time to a common start.
    *   Calculates `avvalue[i]` (average) and `valcount[i]` (number of valid points) for each parameter.
3.  **Plot Setup:** Initializes the `plotlib` PostScript output. Sets up the overall plot dimensions (`xlength`, `ylength`, `xoff`).
4.  **Plotting Loop:**
    *   Divides the plotting area into `noplots` vertical subplots.
    *   For each subplot:
        *   Draws the subplot border.
        *   Draws X-axis grid lines and labels (time in minutes) if not `xplot_flag`.
        *   Prompts for Y-axis range and the parameter to plot.
        *   If `xplot_flag`, prompts for the X-axis parameter.
        *   If `dofilt` is active, interactively asks to filter and applies `filt_TS()`.
        *   **Data Plotting:** Iterates through `nopoints` (records):
            *   Gets `xval` (time or chosen X-parameter) and `yval` (chosen Y-parameter).
            *   If `xval` and `yval` are within their respective plot bounds, it draws a line segment from the previous point to the current point.
        *   **Squat Model (`-squat`):** If `squat_flag` and `xplot_flag` are active, it overlays a calculated squat curve (bias + linear term * speed + quadratic term * speed^2) onto the plot.
        *   Adds labels for the chosen parameters.
5.  **Merged File Extent Plotting:** If merged files (`.merged`) are provided, it reads their summary headers, extracts their time extents, and indicates these extents as rectangular boxes on the plot.
6.  **Filtering Function:**
    *   `filt_TS(int novals, float *invals, float *outvals, int filtlen)`: Applies a boxcar (moving average) filter to `invals` and stores results in `outvals`.
7.  **Cleanup:** Frees allocated memory and closes all input files.

## Output Files
*   `<outfile_name>`: A PostScript metafile (`.meta`) containing time-series plots of the selected parameters.

## Dependencies
*   `plotlib.h`: For `plotlib` functions.
*   `support.h`: For general utility functions.
*   `math.h`: For mathematical functions.
*   `OMG_HDCS_jversion.h`: For merged file structures.

## Notes
`plotDump` is a highly flexible interactive tool for detailed analysis of time-series data. Its interactive nature allows users to quickly explore different parameters and visualize trends, relationships, and anomalies. It is particularly useful for debugging processing results or for quality control of motion, navigation, and other time-varying data. The integration of filtering and squat models provides additional analytical capabilities.