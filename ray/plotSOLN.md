---
layout: default
title: plotSOLN
parent: Ray Tools
nav_order: 168
---
# plotSOLN

## Description
`plotSOLN` is a plotting utility designed to visualize ray trace solutions. It reads ASCII data, typically containing across-track distance (`across`) and depth difference (`dep_diff`) values for multiple layers and rays. The tool then generates a 2D plot, often displaying the `dep_diff` (error) as a function of `across` distance, for various depths.

This tool is useful for analyzing the results of ray tracing, especially when comparing different sound velocity profiles or understanding the spatial distribution of depth errors caused by sound speed variations.

## Usage
```bash
plotSOLN -infile <file1> [-infile <file2> ...] [-outfile <filename.meta>] [-size <dx> <dy>] [-xrange <min> <max>] [-yrange <min> <max>] [-tit1 <string>] [-tit2 <string>] [-v] [-sparse] [-together]
```

## Arguments

| Option | Description |
|---|---|
| `-infile <file1> ...` | **Required.** One or more input ASCII files containing ray trace solution data. |
| `-outfile <filename.meta>` | Specifies the output PostScript metafile name. | `plot.meta` |
| `-size <dx> <dy>` | Specifies the plot size in centimeters. | `20.0 10.0` |
| `-xrange <min> <max>` | Sets the X-axis range (across-track distance). | `0` to `375` |
| `-yrange <min> <max>` | Sets the Y-axis range (depth difference or error). | `-20` to `20` |
| `-tit1 <string>` / `-tit2 <string>` | Sets plot titles. | |
| `-v` | Enable verbose output. | |
| `-sparse` | (Present in `USAGE` but not implemented) Intended for sparse plotting. | |
| `-together` | (Present in `USAGE` but not implemented) Intended for plotting multiple datasets on one graph. | |

## Input File Format (ASCII)
The input ASCII file for ray trace solutions is expected to contain:
*   `novals` (int): Number of across-track values per layer.
*   `nolayers` (int): Number of depth layers.
*   For each layer `j` from `0` to `nolayers - 1`:
    *   `depth` (double): Current depth of the layer.
    *   `across[k]` (double) for `k` from `0` to `novals - 1`: Across-track distance for each ray.
    *   `depth` (double): (repeated depth).
    *   `dep_diff[k]` (double) for `k` from `0` to `novals - 1`: Depth difference for each ray.

## How It Works
1.  **Initialization:** Parses command-line arguments to set input/output filenames, plot size, X/Y ranges, and titles. Initializes `plotlib` PostScript output (`plot.meta`).
2.  **Plot Setup:** Initializes the `plotlib` PostScript output (`plot.meta`). Sets up the overall plot dimensions (`xlength`, `ylength`, `xoff`, `yoff`). Draws the main plot border and a zero line for reference.
3.  **Title and Labels:** If titles are provided, they are added to the plot.
4.  **File Reading Loop:** Loops through each input file specified by `-infile`:
    *   Opens the input ASCII file.
    *   Reads `novals` (number of across-track values) and `nolayers` (number of depth layers).
    *   **Layer and Ray Iteration:**
        *   For each layer `j`:
            *   Reads the `depth` for the current layer.
            *   Reads `across[k]` and `dep_diff[k]` for all `k` rays within the layer.
            *   **Plotting:**
                *   Sets pen color (alternating to distinguish layers).
                *   Iterates through `k` rays:
                    *   Converts `across[k]` to `xpos` and `dep_diff[k]` to `ypos` (screen coordinates).
                    *   If `dep_diff[k]` is valid and within the Y-range, it draws a line segment from the previous point to the current point, representing the depth difference curve for that layer.
5.  **Cleanup:** Closes all open files and `plotlib` output.

## Output Files
*   `<outfile_name>`: A PostScript metafile (`.meta`) visualizing the ray trace solutions.

## Dependencies
*   `plotlib.h`: For `plotlib` functions.
*   `support.h`: For general utility functions.
*   `math.h`: For mathematical functions.

## Notes
`plotSOLN` is useful for visualizing the output of ray tracing computations, particularly for comparing different sound velocity profiles or understanding the spatial distribution of depth errors caused by sound speed variations. The PostScript output allows for high-quality figures. The `-sparse` and `-together` options are listed in the usage but not implemented.