---
layout: default
title: plot2D
parent: Plot Tools
nav_order: 130
---
# plot2D

## Description
`plot2D` is a specialized plotting utility designed to visualize 2D data dumps from tools like `swatheditor` (specifically its 2D view and patch test tool). It reads ASCII data containing X and Y coordinates, along with associated attributes like color and shape, and generates a PostScript plot.

The tool can display general 2D scatter plots or specialized "patch test" plots, showing the results of calibration offsets. It's interactive for setting plot sizes and ranges.

## Usage
```bash
plot2D -infile <file1> [-outfile <filename.meta>] [-size <dx> <dy>] [-patch] [-xrange <min> <max>]
```

## Arguments

| Option | Description |
|---|---|
| `-infile <file1>` | **Required.** Specifies an input ASCII file containing 2D plot data. |
| `-outfile <filename.meta>` | Specifies the output PostScript metafile name. | `plot.meta` |
| `-size <dx> <dy>` | Specifies the total plot size in centimeters (X and Y dimensions). | `20.0 15.0` |
| `-patch` | Indicates that the input file contains "patch test" data. This changes the interpretation of input parameters (e.g., reads roll, pitch, gyro offsets, and time delay) and adds specific annotations to the plot. |
| `-xrange <min> <max>` | Sets the X-axis range for the plot. | Auto-determined from input. |
| `-label <string>` | (Present in `USAGE` but not implemented) Intended to add a string label. |

## Input File Format (ASCII)
The input ASCII file (from `swatheditor`'s 2D dump) is expected to contain:
*   `reg_left reg_right` (float, float): Global X range of the region.
*   `reg_bot reg_top` (float, float): Global Y range of the region.
*   `sub_left sub_right` (float, float): Sub-region X range.
*   `box_left box_right` (float, float): Box X range.
*   `box_bot box_top` (float, float): Box Y range.
*   `tide` (int): Tide correction flag.
*   `flag` (int): Flag for soundings (all or unflagged).
*   `obsproc` (int): Observed or processed soundings.
*   **If `-patch`:** `roll_offset pitch_offset gyro_offset time_delay` (float, float, float, float).
*   Else: `direction` (int).
*   `xmin xmax` (float, float): Plot X-axis data range.
*   `ymin ymax` (float, float): Plot Y-axis data range.
*   Then, for each data point: `xval yval col shape` (float, float, int, int).
    *   `col`: Color index for the point.
    *   `shape`: Shape index (0 for cross, 1 for diamond).

## How It Works
1.  **Initialization:** Parses command-line arguments to set plotting options, input file names, plot size, and `patch_flag`.
2.  **File Opening:** Opens the input ASCII data file (`-infile`) for reading and initializes the `plotlib` PostScript output (`plot.meta`).
3.  **Parameter Reading:** Reads various plot parameters (region bounds, sub-region bounds, box bounds, tide/flag settings, `xmin`, `xmax`, `ymin`, `ymax`) from the input ASCII file. If `patch_flag` is set, it also reads roll, pitch, gyro offsets, and time delay.
4.  **Plot Setup:**
    *   Sets up the overall plot dimensions (`xlength`, `ylength`, `xoff`).
    *   Draws the main plot border.
    *   **Region and Box Drawing:** Draws auxiliary rectangles on the plot representing the `reg`, `sub`, and `box` regions, using different colors.
    *   **Patch Test Annotations (`-patch`):** If `patch_flag` is set, it adds text annotations to the plot displaying the `roll_offset`, `pitch_offset`, `gyro_offset`, and `time_delay` values.
5.  **Data Plotting:**
    *   Iterates through each data point in the input file, reading `xval`, `yval`, `col`, and `shape`.
    *   If `xval` and `yval` are within their respective plot bounds and `yval` is not `0.0`:
        *   Calculates screen coordinates (`xpos`, `ypos`).
        *   Sets the pen color based on `col`.
        *   Draws the point using the specified `shape` (cross or diamond).
6.  **Axis Drawing:** Draws X and Y axes with labels and ticks based on data ranges.
7.  **Plot Metadata:** Adds labels for tide correction, flagging status, processing type (observed/processed), and view direction.
8.  **Cleanup:** Calls `plot_close` to finalize the PostScript output.

## Output Files
*   `<outfile.meta>`: A PostScript metafile (`.meta`) containing the 2D plot.

## Dependencies
*   `plotlib.h`: For `plotlib` functions.
*   `support.h`: For general utility functions.
*   `X_extra.h`: For X-windows related drawing utilities.

## Notes
`plot2D` is an essential tool for visualizing calibration results and data quality in multibeam hydrography. The "patch test" plots are particularly useful for identifying and correcting constant errors in roll, pitch, gyro, and latency. The tool's reliance on specific ASCII dump formats highlights its role within a broader processing workflow. The `label` option is listed but not implemented.