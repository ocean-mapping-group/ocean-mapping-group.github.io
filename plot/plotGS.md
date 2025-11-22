---
layout: default
title: plotGS
parent: Plot Tools
nav_order: 141
---
# plotGS

## Description
`plotGS` is a specialized plotting utility designed to visualize grain size distribution data. It reads ASCII files containing grain size percentages (typically from laboratory analysis) and plots them as a bar graph or histogram. The tool can handle different input formats, including a custom format (likely from `DelayEditor` output) and data from the Pacific Geoscience Centre (PGC).

This tool is useful for rapidly visualizing sedimentological data, allowing for quick comparison of different samples or characterization of sediment types.

## Usage
```bash
plotGS <infile(s)> [-outfile <filename.meta>] [-size <dx> <dy>] [-yrange <min> <max>] [-pgc] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `<infile(s)>` | **Required.** One or more input ASCII files containing grain size data. |
| `-outfile <filename.meta>` | Specifies the output PostScript metafile name. | `plot.meta` |
| `-size <dx> <dy>` | Specifies the plot size in centimeters. | `15.0 15.0` |
| `-yrange <min> <max>` | Sets the Y-axis range (percentage). | `0.0` to `40.0` |
| `-pgc` | Indicates that the input file is in PGC (Pacific Geoscience Centre) format. This implies a different parsing and plotting approach, including extraction of mean, standard deviation, kurtosis, and skewness, and plotting against Phi units. |
| `-v` | Enable verbose output. |
| `-sparse` | (Present in `USAGE` but not implemented) Intended for sparse plotting. |

## Input File Formats
*   **Default (likely from `DelayEditor` output):** Contains a series of percentage values for predefined grain size bins (e.g., 25000um, 19000um down to 75um, and mud/pan).
*   **PGC (`-pgc`) format:** A more complex ASCII format that includes metadata like sample number, latitude, longitude, and then a list of Phi units and corresponding relative and cumulative percentages.

## How It Works
1.  **Initialization:** Parses command-line arguments to set plotting options, input file formats (`pgc_flag`), plot size, and ranges.
2.  **File Reading Loop:** Loops through each input file specified:
    *   Opens the input ASCII file.
    *   **Data Loading:**
        *   If `pgc_flag` is set: It parses the multi-line PGC format, extracting sample number, latitude, longitude, and then Phi values and percentages. It also calculates `mode`, `mean`, `stdev`, `kurt`, `skew` from the Phi data. It opens `.llz` and `.lln` files for writing coordinate and number data.
        *   If `pgc_flag` is *not* set: It reads a predefined sequence of percentage values for different grain size bins.
    *   **Plotting:** Calls `do_plot()` to generate the plot.
    *   Closes the input file.
3.  **`do_plot()` Function:**
    *   Draws the main plot border.
    *   Sets X-axis range (from `0.0` to `fractions` or Phi units if `pgc_flag` is set) and Y-axis range (percentage).
    *   **PGC Specific Plotting:** If `pgc_flag` is set:
        *   Draws vertical lines to delineate gravel, sand, silt, and clay boundaries in Phi units.
        *   Displays sample number, skewness, kurtosis, mean, mode, and standard deviation on the plot.
        *   Plots bars representing `perc_gs[j]` (percentages) against `phi[j]` (Phi units).
    *   **Default Plotting:** Plots bars representing percentages for each predefined grain size bin.
    *   Adds general plot title and labels.
4.  **Cleanup:** Calls `plot_close` to finalize the PostScript output.

## Output
*   A PostScript metafile (`plot.meta` or specified by `-outfile`) containing a bar graph or histogram of grain size distribution.
*   If `pgc_flag` is set:
    *   `<infile>.llz`: ASCII file containing latitude, longitude, mean, standard deviation for each sample.
    *   `<infile>.lln`: ASCII file containing latitude, longitude, sample number.
```
```
```
---
layout: default
title: plotGS
parent: Plot Tools
nav_order: 141
---
# plotGS

## Description
`plotGS` is a specialized plotting utility designed to visualize grain size distribution data. It reads ASCII files containing grain size percentages (typically from laboratory analysis) and plots them as a bar graph or histogram. The tool can handle different input formats, including a custom format (likely from `DelayEditor` output) and data from the Pacific Geoscience Centre (PGC).

This tool is useful for rapidly visualizing sedimentological data, allowing for quick comparison of different samples or characterization of sediment types.

## Usage
```bash
plotGS <infile(s)> [-outfile <filename.meta>] [-size <dx> <dy>] [-yrange <min> <max>] [-pgc] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `<infile(s)>` | **Required.** One or more input ASCII files containing grain size data. |
| `-outfile <filename.meta>` | Specifies the output PostScript metafile name. | `plot.meta` |
| `-size <dx> <dy>` | Specifies the plot size in centimeters. | `15.0 15.0` |
| `-yrange <min> <max>` | Sets the Y-axis range (percentage). | `0.0` to `40.0` |
| `-pgc` | Indicates that the input file is in PGC (Pacific Geoscience Centre) format. This implies a different parsing and plotting approach, including extraction of mean, standard deviation, kurtosis, and skewness, and plotting against Phi units. |
| `-v` | Enable verbose output. |
| `-sparse` | (Present in `USAGE` but not implemented) Intended for sparse plotting. |

## Input File Formats
*   **Default (likely from `DelayEditor` output):** Contains a series of percentage values for predefined grain size bins (e.g., 25000um, 19000um down to 75um, and mud/pan).
*   **PGC (`-pgc`) format:** A more complex ASCII format that includes metadata like sample number, latitude, longitude, and then a list of Phi units and corresponding relative and cumulative percentages.

## How It Works
1.  **Initialization:** Parses command-line arguments to set plotting options, input file formats (`pgc_flag`), plot size, and ranges.
2.  **File Reading Loop:** Loops through each input file specified:
    *   Opens the input ASCII file.
    *   **Data Loading:**
        *   If `pgc_flag` is set: It parses the multi-line PGC format, extracting sample number, latitude, longitude, and then Phi values and percentages. It also calculates `mode`, `mean`, `stdev`, `kurt`, `skew` from the Phi data. It opens `.llz` and `.lln` files for writing coordinate and number data.
        *   If `pgc_flag` is *not* set: It reads a predefined sequence of percentage values for different grain size bins.
    *   **Plotting:** Calls `do_plot()` to generate the plot.
    *   Closes the input file.
3.  **`do_plot()` Function:**
    *   Draws the main plot border.
    *   Sets X-axis range (from `0.0` to `fractions` or Phi units if `pgc_flag` is set) and Y-axis range (percentage).
    *   **PGC Specific Plotting:** If `pgc_flag` is set:
        *   Draws vertical lines to delineate gravel, sand, silt, and clay boundaries in Phi units.
        *   Displays sample number, skewness, kurtosis, mean, mode, and standard deviation on the plot.
        *   Plots bars representing `perc_gs[j]` (percentages) against `phi[j]` (Phi units).
    *   **Default Plotting:** Plots bars representing percentages for each predefined grain size bin.
    *   Adds general plot title and labels.
4.  **Cleanup:** Calls `plot_close` to finalize the PostScript output.

## Output
*   A PostScript metafile (`plot.meta` or specified by `-outfile`) containing a bar graph or histogram of grain size distribution.
*   If `pgc_flag` is set:
    *   `<infile>.llz`: ASCII file containing latitude, longitude, mean, standard deviation for each sample.
    *   `<infile>.lln`: ASCII file containing latitude, longitude, sample number.
```
```