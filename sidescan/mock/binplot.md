---
layout: default
title: binplot
parent: Mock Tools
grand_parent: sidescan
nav_order: 4
---
# binplot

## Description
`binplot` is a utility designed to visualize binary data, specifically streams of 16-bit short integers, by plotting them onto a Metafile. It creates a 2D graph, where the x-axis typically represents the index (or time) and the y-axis represents the data value. The plot dimensions, ranges, and output file are configurable.

## Usage
```bash
binplot [-infile <file>] [-outfile <metafile>]
```

## Arguments

| Option | Description |
|---|---|
| `-infile <file>` | Specifies the input binary file containing 16-bit short integers. If not specified, data is read from standard input. |
| `-outfile <metafile>` | Specifies the output Metafile name. | `plot.meta` |

## How It Works
1.  **Input Reading:**
    *   The tool reads 16-bit short integers from either the specified input file (`-infile`) or standard input.
    *   The entire input stream is loaded into a `short *trace` array in memory.
2.  **Plot Initialization:**
    *   It determines the plot dimensions (`dx`, `dy`) and the number of plots (`noplots`, hardcoded to 1 in the provided source).
    *   A Metafile is opened (`plot_open`) with the specified dimensions.
    *   A basic bounding box is drawn on the plot area.
3.  **Axis Scaling:**
    *   The x-axis range (`xmin`, `xmax`) is set from 0 to the total number of points (`nopoints`).
    *   The y-axis range (`ymin`, `ymax`) is hardcoded to the full range of a 16-bit short integer (-32768 to 32767).
4.  **Data Plotting:**
    *   The tool iterates through the `trace` array.
    *   For each data point (`xval`, `yval`):
        *   It converts the `xval` and `yval` to screen coordinates (`xpos`, `ypos`) based on the defined plot area and ranges.
        *   It then draws a line segment from the previous point (`oldxpos`, `oldypos`) to the current point (`xpos`, `ypos`).
5.  **Output:** The generated plot is saved as a Metafile.
