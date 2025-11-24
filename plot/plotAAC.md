---
layout: default
title: plotAAC
parent: Plot Tools
nav_order: 131
---
# plotAAC

## Description
`plotAAC` is an interactive plotting utility designed to visualize data from AAC (Applanix Attitude and Navigation Controller) Ring Laser Gyro (RLG) systems. It reads binary data files containing various navigation and motion parameters (e.g., time, position, velocity, acceleration, angular rates, roll, pitch, heading, heave errors) and generates time-series plots.

The tool allows users to select which parameters to plot, define plotting ranges, and can overlay data from multiple sources (e.g., primary RLG, HIPPY, TSSB systems). It also applies simple filtering for spike removal.

## Usage
```bash
plotAAC -infile <file1> [-outfile <filename.meta>] [-size <dx> <dy>] [-vref] [-sens] [-xrange <min> <max>]
```

## Arguments

| Option | Description |
|---|---|
| `-infile <file1>` | **Required.** Specifies the base name for the input binary data files (e.g., `bet` will look for `bet.out`, `hippmbet.out`, `tssbmbet.out`). |
| `-outfile <filename.meta>` | Specifies the output PostScript metafile name. | `plot.meta` |
| `-size <dx> <dy>` | Specifies the total plot size in centimeters (X and Y dimensions). | `20.0 25.0` |
| `-vref` | Selects a specific set of parameters for plotting (VREF, `noval`=17). |
| `-sens` | Selects a specific set of parameters for plotting (SENS, `noval`=5). |
| `-sparse` | (Present in `USAGE` but not fully implemented) Likely intended for sparse plotting. |
| `-xrange <min> <max>` | Sets the X-axis (time since start of window) range for the plot. | Auto-determined. |
| `-v` | Enable verbose output (not explicitly used). | |

## Interactive Mode
After launching, `plotAAC` will guide the user through a series of prompts:

1.  **Plotting Area Dimensions:** Prompts for the maximum dimensions of the plotting area (`dx`, `dy` in cm).
2.  **Number of Plots (`noplots`):** Prompts for how many plots (time series of different parameters) to create.
3.  **Y-axis Bounds (per plot):** For each plot, it prompts for Y-axis minimum (`ymin[i]`) and maximum (`ymax[i]`) values.
4.  **Parameter Selection:** For each plot, it presents a menu of available parameters from the RLG, HIPPY, and TSSB systems and prompts the user to choose which parameter to plot.
5.  **Continue Plotting:** After plotting the selected parameters for one plot, it asks if the user wants to plot another line in the current graph.

## How It Works
1.  **Initialization:** Parses command-line arguments to set plotting options and input filenames. Initializes a `plotlib` PostScript output (`plot.meta`).
2.  **Data Loading:**
    *   Opens three binary input files: `bet.out` (main RLG data), `hippmbet.out` (HIPPY data), and `tssbmbet.out` (TSSB data).
    *   Reads `range` (number of records) from the file sizes.
    *   Reads all data from these three files into a 2D array `values[parameter_index][record_index]`.
    *   Performs unit conversions (e.g., radians to degrees, m/s² to g's) on the loaded data.
    *   Applies a simple spike removal filter to TSSB roll error.
    *   Calculates `Clean Horizontal Velocity` and `Filtered TSSB Roll Error`.
3.  **Plot Generation (using `plotlib` library):**
    *   Calls `plot_open` to initialize the PostScript output.
    *   Sets up the overall plot dimensions (`xlength`, `ylength`, `xoff`).
    *   Iterates through each graph (`i` from `0` to `noplots - 1`):
        *   Draws the main plot border.
        *   Draws X and Y grid lines and labels.
        *   **Parameter Selection:** Prompts the user to choose a parameter to plot from a menu.
        *   **Data Plotting:** Iterates through `nopoints` (records):
            *   Extracts `xval` (time) and `yval` (chosen parameter).
            *   If `xval` and `yval` are within their respective plot bounds, it draws a line segment from the previous point to the current point.
        *   Adds labels for the plotted parameter.
4.  **Cleanup:** Calls `plot_close` to finalize the PostScript output and closes input files.

## Output Files
*   `<outfile_name>`: A PostScript metafile (`.meta`) containing time-series plots of the selected parameters.

## Dependencies
*   `plotlib.h`: For `plotlib` functions.
*   `support.h`: For general utility functions.
*   `math.h`: For mathematical functions.

## Notes
`plotAAC` is a valuable tool for quality control and detailed analysis of RLG/GNSS motion data, allowing for visual inspection of navigation and attitude parameters. The interactive mode enables flexible selection of parameters and plotting ranges. The tool applies some basic filtering to improve data quality for visualization. The input binary format is specific to AAC data.