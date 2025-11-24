---
layout: default
title: multiplot
parent: Plot Tools
nav_order: 128
---
# multiplot

## Description
`multiplot` is an interactive plotting utility designed to create multiple plots within a single PostScript output file. It reads data from ASCII files, allowing users to define the plotting area, X and Y axis ranges, and plot several datasets on a single graph.

This tool is useful for comparing different datasets visually in a structured manner, where each dataset might represent a separate measurement or a different processing step of the same data.

## Usage
```bash
multiplot [-infile <asciiplotfile>] [-outfile <metafile_name>]
```

## Arguments

| Option | Description |
|---|---|
| `-infile <asciiplotfile>` | Specifies the initial input ASCII file containing data to plot. If not provided, it prompts for input. |
| `-outfile <metafile_name>` | Specifies the output PostScript metafile name. | `multiplot.meta` |

## Interactive Mode
After launching, `multiplot` will guide the user through a series of prompts:

1.  **Plotting Area Dimensions:** Prompts for the maximum dimensions of the plotting area (`dx`, `dy` in cm).
2.  **File Selection:** Prompts for the ASCII plot file name.
3.  **Plot Geometry:** Prompts for X and Y axes lengths (`xlength`, `ylength`) and X and Y offsets (`xoffset`, `yoffset`) for the current plot within the overall plotting area.
4.  **Number of Plots (`noplots`):** Reads the number of individual plots (`noplots`) to be drawn on the current graph from the input file.
5.  **X-Axis Bounds:** Reads X-axis minimum (`xmin`) and maximum (`xmax`) values from the input file.
6.  **Y-Axis Bounds (per plot):** For each of the `noplots`, it reads Y-axis minimum (`ymin[i]`) and maximum (`ymax[i]`) values from the input file.
7.  **Number of Data Points:** Reads the total number of data points (`nopoints`) for each plot from the input file.
8.  **Data Reading and Plotting:** Reads X values and corresponding Y values for each plot from the input file. It then draws lines connecting valid data points within the specified X and Y bounds.
9.  **Continue Plotting:** After plotting one graph, it asks "do you want to plot another graph?". If the user enters 'y' or 'Y', it loops back to prompt for another ASCII plot file name and continues.

## Input File Format (ASCII)
The input ASCII file for each graph is expected to contain:
*   `dx dy` (float, float): Maximum dimensions of the plotting area.
*   `noplots` (int): Number of individual plots on this graph.
*   `xmin xmax` (float, float): X-axis bounds.
*   For each plot `i` from `0` to `noplots - 1`: `ymin[i] ymax[i]` (float, float): Y-axis bounds for plot `i`.
*   `nopoints` (int): Number of data points for all plots.
*   For each data point `j` from `0` to `nopoints - 1`:
    *   `xval` (float): X-coordinate.
    *   For each plot `i` from `0` to `noplots - 1`: `yval` (float): Y-coordinate for plot `i`.

## How It Works
1.  **Initialization:** Opens the output PostScript metafile (`synname`) and initializes `plotlib`.
2.  **Interactive Graph Loop:** Enters a loop (`again:` and `goto again;`) for plotting multiple graphs.
3.  **File Input:** Prompts the user for an ASCII plot file and opens it.
4.  **Plot Area Setup:** Prompts for and sets the maximum plotting area dimensions (`dx`, `dy`).
5.  **Plotting Geometry:** Reads `xlength`, `ylength`, `xoffset`, `yoffset` for the current graph.
6.  **Data Range Reading:** Reads `noplots`, `xmin`, `xmax`, `ymin[]`, `ymax[]`, and `nopoints` from the input ASCII plot file.
7.  **Data Plotting Loop:** Iterates through each data point `j` and then through each plot `i`:
    *   Reads `xval` and `yval` from the input file.
    *   If `xval` and `yval` are within their respective plot bounds and `yval` is not `0.0`, it converts them to device coordinates (`xpos`, `ypos`).
    *   It then draws a line segment from the `oldxpos`/`oldypos` (previous data point) to the current point (`xpos`, `ypos`).
8.  **Continue/Exit:** After plotting a graph, it asks the user if they want to plot another.
9.  **Cleanup:** Calls `plot_close` to finalize the PostScript output.

## Output Files
*   `<outfile_name>`: A PostScript metafile (`.meta`) containing the generated plots.

## Dependencies
*   `plotlib.h`: For `plotlib` functions.
*   `support.h`: For general utility functions.

## Notes
`multiplot` is an interactive tool suitable for visually comparing multiple time-series or profile datasets. The input file format is highly specific, requiring explicit definition of plot geometry and data ranges within the ASCII file itself. The interactive nature allows users to build complex composite plots step-by-step.