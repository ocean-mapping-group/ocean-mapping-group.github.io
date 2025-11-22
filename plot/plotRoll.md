---
layout: default
title: plotRoll
parent: Plot Tools
nav_order: 144
---
# plotRoll

## Description
`plotRoll` is a specialized plotting utility designed to visualize the required roll accuracy of a multibeam sonar system as a function of either angle (grazing angle) or range. It generates a custom plot based on a predefined mathematical relationship, which likely models the sensitivity of bathymetric measurements to roll errors at different across-track positions.

This tool is useful for understanding the impact of motion sensor accuracy on sounding quality and for determining acceptable limits for roll compensation, particularly in the context of system calibration and survey planning.

## Usage
```bash
plotRoll [-range] [-outfile <filename.meta>] [-size <dx> <dy>] [-yrange <min> <max>]
```

## Arguments

| Option | Description |
|---|---|
| `-range` | Changes the X-axis from angle to range. |
| `-outfile <filename.meta>` | Specifies the output PostScript metafile name. | `plot.meta` |
| `-size <dx> <dy>` | Specifies the plot size in centimeters. | `18.0 15.0` |
| `-yrange <min> <max>` | (Present in `USAGE` but fixed to `0.0` to `1.0` in provided code) Sets the Y-axis range (required roll accuracy). | `0.0` to `1.0` |

## How It Works
1.  **Initialization:** Parses command-line arguments to set plotting options, plot size, and `range_flag`.
2.  **Plot Setup:** Initializes the `plotlib` PostScript output (`plot.meta`). Sets up the overall plot dimensions (`xlength`, `ylength`, `xoff`, `yoff`). Draws the main plot border.
3.  **Axis Ranges:**
    *   If `range_flag` is set: `xmin = 0.0`, `xmax = 9.0` (range).
    *   If `range_flag` is *not* set: `xmin = 0.0`, `xmax = 90.0` (angle).
    *   `ymin = 0.0`, `ymax = 1.0` (fixed for roll accuracy).
4.  **Axis Labels and Grid:** Draws X and Y axes with numerical labels and grid lines. The labels on the X-axis will correspond to angle (0-90 degrees) or range (0-9).
5.  **Data Plotting Loop:** Iterates for `j` from `18` to `78` (representing angles):
    *   **Calculation:**
        *   Calculates `xval` as either the angle `j` or a derived range `2.0 * tan(j * M_PI / 180.0)` if `range_flag` is set.
        *   Calculates `yval` using the formula `(180.0 / M_PI) * atan(0.005 / tan(xval * M_PI / 180.0))`. This formula relates a small angular error (0.005 radians) to the required roll accuracy as a function of the angle or range.
    *   Plots `xval` vs. `yval` as a continuous line.
6.  **Additional Lines (`line()` function):** Calls the `line()` function with various fixed `x` values. This function plots small vertical lines at `yval = 0.9` and `yval = 1.0` at the specified `x` positions, likely indicating specific thresholds or reference points for roll accuracy.
7.  **Cleanup:** Calls `plot_close` to finalize the PostScript output.

## Output
*   A PostScript metafile (`plot.meta` or specified by `-outfile`) visualizing the required roll accuracy.
```
```
```