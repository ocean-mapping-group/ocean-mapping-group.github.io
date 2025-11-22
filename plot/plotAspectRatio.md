---
layout: default
title: plotAspectRatio
parent: Plot Tools
nav_order: 135
---
# plotAspectRatio

## Description
`plotAspectRatio` is a specialized plotting utility designed to visualize the distribution of ray angles or "aspect ratio" as a function of grazing angle. It generates a histogram-like plot showing how many times a particular angle is "stacked" given a simulated or theoretical water column height.

This tool is useful for understanding the geometric distribution of sound rays within a given water column and how it relates to aspect ratio or grazing angle.

## Usage
```bash
plotAspectRatio [-ar <ratio>] [-outfile <filename.meta>] [-size <dx> <dy>] [-yrange <min> <max>]
```

## Arguments

| Option | Description |
|---|---|
| `-outfile <filename.meta>` | Specifies the output PostScript metafile name. | `plot.meta` |
| `-size <dx> <dy>` | Specifies the total plot size in centimeters (X and Y dimensions). | `15.0 15.0` |
| `-yrange <min> <max>` | Sets the Y-axis range (count or percentage). | `0.0` to `25.0` |
| `-ar <ratio>` | Specifies the aspect ratio. This is multiplied by 1000 to get a simulated water column `height`. (e.g., `0.1` is a low aspect ratio). | `1000.0` (implied, as `height` initialized to `1000.0`) |

## How It Works
1.  **Initialization:** Parses command-line arguments to set plot size, Y-axis range, and `height` (which is derived from `-ar`).
2.  **Plot Area Setup:** Sets up the overall plot dimensions (`xlength`, `ylength`, `xoff`, `yoff`). Draws the main plot border.
3.  **Angle Stack Calculation:**
    *   Initializes a `stack[90]` array to zeros.
    *   Iterates from `i = 0` to `999` (simulating horizontal distance).
    *   For each `i`, it calculates an `angle` (grazing angle) using `atan(i / height)`.
    *   Increments `stack[(int)angle]` for each calculated angle.
    *   Scales the `stack` values by `(100.0 / 1000.0)` to represent a percentage or normalized count.
    *   Determines `maxstack` from the `stack` array.
4.  **Plotting Histogram:**
    *   Sets X-axis range from `0.0` to `90.0` (grazing angle).
    *   Sets Y-axis range from `ymin` to `ymax` (count/percentage).
    *   For each `j` from `0` to `89` (representing angle bins):
        *   Draws a vertical bar representing `stack[j]` as a filled rectangle.
5.  **Cleanup:** Calls `plot_close` to finalize the PostScript output.

## Output
*   A PostScript metafile (`plot.meta` or specified by `-outfile`) containing a histogram-like plot of angle distribution.
```
```
```