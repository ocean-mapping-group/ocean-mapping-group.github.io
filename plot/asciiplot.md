---
layout: default
title: asciiplot
parent: Plot Tools
nav_order: 124
---
# asciiplot

## Description
`asciiplot` is a versatile plotting utility designed to visualize numerical data from ASCII files (or binary JHC `.r4` arrays if `omgbin_flag` is set). It generates plots using a custom `plotlib` library, creating PostScript output (`.meta` file) that can be viewed or converted.

The tool is highly configurable, allowing users to specify X and Y axis ranges, plot multiple datasets, control line and point styles, add labels, and highlight specific slices or plots. It supports various data formats, including simple columns, and specialized binary formats.

## Usage
```bash
asciiplot [-infile file1 ...] [-infilQ fileN QstringN] [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `-infile <file1>` | **Required.** Specifies an input ASCII file containing data to plot. Can be used multiple times for multiple plots on the same graph or different graphs (depending on `-multi`). |
| `-infilQ <fileN> <QstringN>` | Specifies an input ASCII file and an associated qualifier string (`QstringN`). Useful for distinguishing multiple datasets. |
| `-outfile <metafile_name>` | Specifies the output PostScript metafile name. | `plot.meta` |

### Plot Customization
| Option | Description |
|---|---|
| `-dumb` | Enables interactive input for plot parameters (e.g., plot size, X/Y bounds). |
| `-autoX` | Automatically determines X-axis bounds from the data. |
| `-centreX <val>` | Centers the X-axis around the given value. |
| `-timeX` | Interprets X-axis values as timestamps (Unix seconds) and prompts for date/time input for X bounds. |
| `-allY <ymin> <ymax>` | Sets a common Y-axis range for all plots. |
| `-force_plotsize` | Overrides default plot size and prompts for X, Y dimensions. |
| `-force_xrange` | Overrides default X-range and prompts for Xmin, Xmax. |
| `-add_bar` | Adds vertical bars from the X-axis to data points (for displaying deviations). |
| `-column` | Interprets the input as a column-major array (for `omgbin_flag`). |
| `-flipx` | Flips the X-axis of the plot. |
| `-flip_ascii_array` | Transposes the input ASCII array (swaps rows and columns). |
| `-skip_step <val>` | When `-flip_ascii_array` is used, processes every `val`-th row/column. | `1` |
| `-lineskip <val>` | Skips `val` lines from the beginning of the input file before reading data. | `0` |
| `-qualifier` | Adds qualifier strings (from `-infilQ`) to the plot legend. |
| `-noborder` | Suppresses plotting of the plot border. |
| `-axes` / `-labels` | Plots X and Y axes and labels. |
| `-plotjust <val>` | Plots only the specified plot number (1-indexed). | `0` (plots all) |
| `-xfrac <val>` | Sets the fraction of the plot width to use for the X-axis (e.g., `0.1` for 0.8 width, `0.05` for 0.9 width). | `0.1` |
| `-overshootok` | Allows Y values to overshoot specified Y-bounds without rejection. |
| `-points` | Plots data as points. |
| `-pointsandlines` | Plots data as points connected by lines. |
| `-point_size <val>` | Sets the size of plot points. | `0.025` |
| `-point_logo <val>` | Sets the shape of plot points (0: cross, 1: diamond, 2: box). | `0` |
| `-multi` | Plots multiple datasets on a single graph (overlapping). |
| `-grey_pen` | Uses a grayscale color scheme for multiple plots. |
| `-last_blue <val>` | (Used with `-grey_pen`) Last `val` plots use blue pens. |
| `-custom_pen <val>` | Uses a custom pen color specified by `val`. |
| `-rainbow` | (Not implemented) Intended for a rainbow color scheme. |
| `-new` | (Present in `USAGE` but not fully implemented) Likely for new plot type. |

### OMG Binary Input (`-omgbin`)
| Option | Description |
|---|---|
| `-omgbin` | Interprets the input file as a binary JHC `.r4` array. Requires `-dumb`. |
| `-Xfrom_zero` | For `omgbin` input, plots X-axis from zero instead of `arrayhead.xmin`. |
| `-scan_sequence <start> <step>` | For `omgbin` input, specifies a sequence of scanlines (rows/columns) to plot. |
| `-scan_av <val>` | For `omgbin` input, applies a moving average filter along the scan direction. | `1` |
| `-vert_av <val>` | For `omgbin` input, applies a moving average filter along the vertical (perpendicular to scan). | `1` |
| `-highlight_slice <val>` | For `omgbin` input, highlights a specific slice (row/column) number. |
| `-highlight_plot <val>` | For `omgbin` input, highlights a specific plot number. |

### Titles and Labels
| Option | Description |
|---|---|
| `-tit1 <string>` | Sets the main title (top center). |
| `-tit2 <string>` | Sets a secondary title (top left). |
| `-xlab <string>` | Sets the X-axis label. |
| `-ylab <string>` | Sets the Y-axis label. |

## How It Works
1.  **Initialization:** Parses command-line arguments to set plotting options, file names, and ranges.
2.  **File Reading Loop:** Loops through each input file specified by `-infile` or `-infilQ`:
    *   Opens the input ASCII file (or binary `.r4` for `-omgbin`).
    *   Reads plot dimensions (DX, DY) and number of plots (`noplots`).
    *   **X/Y Axis Bounds:** Determines X and Y axis bounds either interactively (if `-dumb`), automatically (`-autoX`), or from specified ranges.
    *   **Data Loading (`-omgbin` vs. ASCII):**
        *   If `-omgbin`: Reads a JHC header from the binary file. Based on `column_flag`, it loads either rows or columns as Y-data, using `scan_sequence`, `scan_av`, and `vert_av` for filtering/averaging.
        *   If ASCII: Reads `nopoints` X values and `noplots` corresponding Y values for each X from the ASCII file.
    *   **Data Manipulation (`-flipx`, `-flip_ascii_array`, `-centreX`):** Applies transformations to the loaded data.
3.  **Plot Generation (using `plotlib` library):**
    *   Calls `plot_open` to initialize the PostScript output.
    *   Calculates plot geometry (`xlength`, `ylength`, `xoff`, `yoff`).
    *   **Axes and Labels:** If `axes_flag` is set, calls `plot_axes` to draw and label X and Y axes.
    *   **Plotting Data:** Iterates through each plot:
        *   Sets pen color (normal, grayscale, custom, or highlighted).
        *   If `point_flag` is set, plots points (with specified logo and size).
        *   If `!point_flag` or `point_flag == 2`, plots lines connecting data points.
        *   If `add_bar` is set, plots vertical bars from the X-axis to data points.
        *   Adds qualifier labels if `qualifier_flag` is set.
    *   Adds titles if specified.
    *   **`plot_axes` Function:** A helper function that draws and labels axes with automatic tick generation and handling of flipped axes.
4.  **Cleanup:** Calls `plot_close` to finalize the PostScript output and closes the input file.

## Output
*   A PostScript metafile (`plot.meta` or specified by `-outfile`) containing the generated plot(s).
*   An optional `omgbin.dump.ascii` file if `-omgbin` is used (for debugging).
```