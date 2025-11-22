---
layout: default
title: plotTides
parent: Plot Tools
nav_order: 147
---
# plotTides

## Description
`plotTides` is a comprehensive plotting utility designed to visualize time-series data, primarily tidal observations or motion data (heave, roll, pitch, heading), alongside the temporal extents of multibeam merged files. It can also analyze and display statistical information, perform linear regression, and generate raster plots of data distributions.

This tool is invaluable for quality control of tidal corrections, assessing vessel motion, and understanding the temporal coverage of multibeam surveys. It supports various input formats (binary tide files, attitude files, navigation files) and offers extensive customization for plot appearance and data analysis.

## Usage
```bash
plotTides -infile <file1> [-infile <file2> ...] [-outfile <filename.meta>] [OPTIONS] [<merged_file(s)...>]
```

## Arguments

| Option | Description |
|---|---|
| `-infile <file1> ...` | **Required.** One or more input binary tide files (JCU_BINNAV_RECLEN format). |
| `-outfile <filename.meta>` | Specifies the output PostScript metafile name. | `plot.meta` |
| `<merged_file(s)...>` | (Optional) One or more merged files. Their time extents will be indicated on the plot. |

### Data Source & Type
| Option | Description |
|---|---|
| `-dep` | Plot depth from the tide file. |
| `-vel` | Plot velocity from the tide file. |
| `-lat` | Plot latitude from the tide file. |
| `-lon` | Plot longitude from the tide file. |
| `-flag <val>` | Plot a specific flag field (`flag[val]`) from the tide file. |
| `-isatt` | Input files are attitude files (OMG_HDCS_attitude format). |
| `-roll` / `-pitch` / `-heading` / `-heave` | For `-isatt`, specifies which attitude parameter to plot. | `roll` |
| `-attskip <val>` | For `-isatt`, skips `val` records when reading attitude data. | `10` |
| `-isnav` | Input files are navigation files (JCU_BINNAV_RECLEN format). |
| `-addGPSrolloverwraps <val>` | Adjusts timestamps for GPS week rollovers by `val` * 1024 weeks (e.g., for POS dated EM data). | `0` |

### Time Range & Display
| Option | Description |
|---|---|
| `-start <yr> <jday> <hr> <min>` | Sets the plot's X-axis start time. |
| `-end <yr> <jday> <hr> <min>` | Sets the plot's X-axis end time. |
| `-xrange <min> <max>` | Sets the plot's X-axis range (Unix seconds). Overrides `-start` and `-end`. |
| `-yrange <val>` | Sets the total Y-axis range (in meters or degrees). The plot's Y-axis will be centered around the data's mean. |
| `-wrap <val>` | Wraps the X-axis (time) display with a period of `val` hours (e.g., `12.42` for semi-diurnal tides). |
| `-dtmax <val>` | Maximum time jump (in seconds) allowed before breaking a line. | `3601.0` |
| `-dotimeofday <start_hr> <end_hr>` | Highlights time-of-day intervals on the plot. |
| `-usetime1970` | Use Unix timestamps (seconds since 1970) for time markers. |
| `-time_marker <markerfile>` | Plots vertical lines from an ASCII file of time markers. Can be used multiple times. |
| `-cenmark` | Centers time markers (used with `-time_marker`). |
| `-scalemark <min> <max>` | Scales time markers. |
| `-isrange` | (Present in `USAGE`, but logic suggests it is tied to `-dotimeofday` and `-time_marker`.) |
| `-doyears` | Labels years on the X-axis. |
| `-domonths` | Labels months on the X-axis. |

### Data Filtering & Processing
| Option | Description |
|---|---|
| `-atten <val>` | Attenuation factor to apply to Y-values. | `1.0` |
| `-delay <val>` | Time delay (in minutes) to apply to X-values. | `0.0` |
| `-dozero` | Plots zero values in the data. |
| `-fit_line` | Performs linear regression on the plotted data. |
| `-fitwin <min> <max>` | Defines time windows (in minutes since SOF) for linear regression. Can be used multiple times. |
| `-calcwin <min> <max>` | Defines time windows (in minutes since SOF) for calculating average RTK bias. Can be used multiple times. |

### Plotting Style & Annotations
| Option | Description |
|---|---|
| `-raster` | Generates a raster image of the plot (instead of line plots). |
| `-rasterXY <dx> <dy>` | Specifies raster image dimensions. | `300 100` |
| `-label1 <string>` / `-label2 <string>` | Sets plot titles. |
| `-label_stats` | Adds mean and standard deviation of the plotted data as text labels. |
| `-show_stats` | (Present in `USAGE`, but tied to `label_stats` in code logic). |
| `-fill_plot` | Fills the area under the curve to the X-axis baseline. |
| `-highlight_last` | Highlights the last plotted line from `-infile`. |
| `-highlight_last_merged` | Highlights the last merged file extent. |
| `-seq` | (Present in `USAGE`, but its effect on plotting merged files is not fully shown). |
| `-bounds_from <otherfile>` | Derives X-axis bounds from another navigation file. |

## How It Works
1.  **Initialization:** Parses command-line arguments to set input/output filenames, plot options, and ranges. Initializes a `plotlib` PostScript output (`plot.meta`).
2.  **Raster Setup (`-raster`):** If `raster_flag` is set, it initializes an `unsigned char` array `raster` and a JHC header for the raster output.
3.  **Bounds From (`-bounds_from`):** If specified, reads X-axis bounds from another navigation file.
4.  **Tide Data Loading & Processing Loop:** For each input tide file specified by `-infile`:
    *   Opens the tide file.
    *   **Data Reading:**
        *   If `-isatt`: Reads OMG_HDCS_attitude records, extracts the specified attitude parameter (`att_choice`), and stores timestamp and value in `tides[0]` and `tides[1]`.
        *   Otherwise: Reads JCU_BINNAV_RECLEN records, extracts the specified parameter (tide, depth, velocity, lat, lon, or flag), and stores timestamp and value in `tides[0]` and `tides[1]`.
    *   Applies `atten` and `delay`.
    *   **Linear Regression (`-fit_line`):** If `fit_line` is set, it performs a least-squares linear regression on the data within specified `fitwin` intervals.
    *   **Calibration Difference (`-calcwin`):** If `calcwin` is specified, it calculates the average difference between the data and the regression line within these intervals.
    *   Calculates `average`, `RMS`, `plausible_average`, `plausible_RMS` for statistical analysis.
5.  **Plot Setup:** Sets up plot dimensions, labels years/months on the X-axis (if `doyears`/`domonths`), and draws time-based grid lines.
6.  **Y-axis Range:** Prompts the user for Y-axis bounds (`ymin`, `ymax`) for the primary plot. Can auto-calculate a range around the mean if `yrange` is provided.
7.  **Data Plotting:**
    *   Iterates through the `tides` data.
    *   **Wrap-around (`-wrap`):** If `wrap_flag` is set, it wraps the time values to fit within a specified period.
    *   Plots `xval` (time) vs. `yval` (tide/motion data).
    *   Handles line breaks for large time gaps (`dtmax`).
    *   **Fill Plot (`-fill_plot`):** Fills the area between the curve and a baseline.
    *   **Raster Plot (`-raster`):** If `raster_flag` is set, it updates a raster image instead of drawing lines.
    *   **Time Markers (`-time_marker`, `-dotimeofday`):** Plots vertical lines or rectangular regions for specified time markers or times-of-day.
    *   **Merged File Extents (`<merged_file(s)...>`):** Plots rectangular boxes indicating the time extents of merged files, with optional highlighting of the last merged file.
8.  **Output Stats:** If `label_stats` is set, prints `plausible_average` and `plausible_RMS` on the plot.
9.  **Cleanup:** Frees allocated memory, closes files, and finalizes PostScript/raster output.

## Output
*   A PostScript metafile (`plot.meta` or specified by `-outfile`) visualizing the time-series data.
*   If `-raster` is used: A binary JHC `.r4` array file (`<infile_prefix>.tide.raster`) containing the rasterized plot.
*   `plottide.range`: A temporary file (seems unused by `main` except for writing plausible averages/RMS).
```
```
---
layout: default
title: plotTides
parent: Plot Tools
nav_order: 147
---
# plotTides

## Description
`plotTides` is a comprehensive plotting utility designed to visualize time-series data, primarily tidal observations or motion data (heave, roll, pitch, heading), alongside the temporal extents of multibeam merged files. It can also analyze and display statistical information, perform linear regression, and generate raster plots of data distributions.

This tool is invaluable for quality control of tidal corrections, assessing vessel motion, and understanding the temporal coverage of multibeam surveys. It supports various input formats (binary tide files, attitude files, navigation files) and offers extensive customization for plot appearance and data analysis.

## Usage
```bash
plotTides -infile <file1> [-infile <file2> ...] [-outfile <filename.meta>] [OPTIONS] [<merged_file(s)...>]
```

## Arguments

| Option | Description |
|---|---|
| `-infile <file1> ...` | **Required.** One or more input binary tide files (JCU_BINNAV_RECLEN format). |
| `-outfile <filename.meta>` | Specifies the output PostScript metafile name. | `plot.meta` |
| `<merged_file(s)...>` | (Optional) One or more merged files. Their time extents will be indicated on the plot. |

### Data Source & Type
| Option | Description |
|---|---|
| `-dep` | Plot depth from the tide file. |
| `-vel` | Plot velocity from the tide file. |
| `-lat` | Plot latitude from the tide file. |
| `-lon` | Plot longitude from the tide file. |
| `-flag <val>` | Plot a specific flag field (`flag[val]`) from the tide file. |
| `-isatt` | Input files are attitude files (OMG_HDCS_attitude format). |
| `-roll` / `-pitch` / `-heading` / `-heave` | For `-isatt`, specifies which attitude parameter to plot. | `roll` |
| `-attskip <val>` | For `-isatt`, skips `val` records when reading attitude data. | `10` |
| `-isnav` | Input files are navigation files (JCU_BINNAV_RECLEN format). |
| `-addGPSrolloverwraps <val>` | Adjusts timestamps for GPS week rollovers by `val` * 1024 weeks (e.g., for POS dated EM data). | `0` |

### Time Range & Display
| Option | Description |
|---|---|
| `-start <yr> <jday> <hr> <min>` | Sets the plot's X-axis start time. |
| `-end <yr> <jday> <hr> <min>` | Sets the plot's X-axis end time. |
| `-xrange <min> <max>` | Sets the plot's X-axis range (Unix seconds). Overrides `-start` and `-end`. |
| `-yrange <val>` | Sets the total Y-axis range (in meters or degrees). The plot's Y-axis will be centered around the data's mean. |
| `-wrap <val>` | Wraps the X-axis (time) display with a period of `val` hours (e.g., `12.42` for semi-diurnal tides). |
| `-dtmax <val>` | Maximum time jump (in seconds) allowed before breaking a line. | `3601.0` |
| `-dotimeofday <start_hr> <end_hr>` | Highlights time-of-day intervals on the plot. |
| `-usetime1970` | Use Unix timestamps (seconds since 1970) for time markers. |
| `-time_marker <markerfile>` | Plots vertical lines from an ASCII file of time markers. Can be used multiple times. |
| `-cenmark` | Centers time markers (used with `-time_marker`). |
| `-scalemark <min> <max>` | Scales time markers. |
| `-isrange` | (Present in `USAGE`, but logic suggests it is tied to `-dotimeofday` and `-time_marker`.) |
| `-doyears` | Labels years on the X-axis. |
| `-domonths` | Labels months on the X-axis. |

### Data Filtering & Processing
| Option | Description |
|---|---|
| `-atten <val>` | Attenuation factor to apply to Y-values. | `1.0` |
| `-delay <val>` | Time delay (in minutes) to apply to X-values. | `0.0` |
| `-dozero` | Plots zero values in the data. |
| `-fit_line` | Performs linear regression on the plotted data. |
| `-fitwin <min> <max>` | Defines time windows (in minutes since SOF) for linear regression. Can be used multiple times. |
| `-calcwin <min> <max>` | Defines time windows (in minutes since SOF) for calculating average RTK bias. Can be used multiple times. |

### Plotting Style & Annotations
| Option | Description |
|---|---|
| `-raster` | Generates a raster image of the plot (instead of line plots). |
| `-rasterXY <dx> <dy>` | Specifies raster image dimensions. | `300 100` |
| `-label1 <string>` / `-label2 <string>` | Sets plot titles. |
| `-label_stats` | Adds mean and standard deviation of the plotted data as text labels. |
| `-show_stats` | (Present in `USAGE`, but tied to `label_stats` in code logic). |
| `-fill_plot` | Fills the area under the curve to the X-axis baseline. |
| `-highlight_last` | Highlights the last plotted line from `-infile`. |
| `-highlight_last_merged` | Highlights the last merged file extent. |
| `-seq` | (Present in `USAGE`, but its effect on plotting merged files is not fully shown). |
| `-bounds_from <otherfile>` | Derives X-axis bounds from another navigation file. |

## How It Works
1.  **Initialization:** Parses command-line arguments to set input/output filenames, plot options, and ranges. Initializes a `plotlib` PostScript output (`plot.meta`).
2.  **Raster Setup (`-raster`):** If `raster_flag` is set, it initializes an `unsigned char` array `raster` and a JHC header for the raster output.
3.  **Bounds From (`-bounds_from`):** If specified, reads X-axis bounds from another navigation file.
4.  **Tide Data Loading & Processing Loop:** For each input tide file specified by `-infile`:
    *   Opens the tide file.
    *   **Data Reading:**
        *   If `-isatt`: Reads OMG_HDCS_attitude records, extracts the specified attitude parameter (`att_choice`), and stores timestamp and value in `tides[0]` and `tides[1]`.
        *   Otherwise: Reads JCU_BINNAV_RECLEN records, extracts the specified parameter (tide, depth, velocity, lat, lon, or flag), and stores timestamp and value in `tides[0]` and `tides[1]`.
    *   Applies `atten` and `delay`.
    *   **Linear Regression (`-fit_line`):** If `fit_line` is set, it performs a least-squares linear regression on the data within specified `fitwin` intervals.
    *   **Calibration Difference (`-calcwin`):** If `calcwin` is specified, it calculates the average difference between the data and the regression line within these intervals.
    *   Calculates `average`, `RMS`, `plausible_average`, `plausible_RMS` for statistical analysis.
5.  **Plot Setup:** Sets up plot dimensions, labels years/months on the X-axis (if `doyears`/`domonths`), and draws time-based grid lines.
6.  **Y-axis Range:** Prompts the user for Y-axis bounds (`ymin`, `ymax`) for the primary plot. Can auto-calculate a range around the mean if `yrange` is provided.
7.  **Data Plotting:**
    *   Iterates through the `tides` data.
    *   **Wrap-around (`-wrap`):** If `wrap_flag` is set, it wraps the time values to fit within a specified period.
    *   Plots `xval` (time) vs. `yval` (tide/motion data).
    *   Handles line breaks for large time gaps (`dtmax`).
    *   **Fill Plot (`-fill_plot`):** Fills the area between the curve and a baseline.
    *   **Raster Plot (`-raster`):** If `raster_flag` is set, it updates a raster image instead of drawing lines.
    *   **Time Markers (`-time_marker`, `-dotimeofday`):** Plots vertical lines or rectangular regions for specified time markers or times-of-day.
    *   **Merged File Extents (`<merged_file(s)...>`):** Plots rectangular boxes indicating the time extents of merged files, with optional highlighting of the last merged file.
8.  **Output Stats:** If `label_stats` is set, prints `plausible_average` and `plausible_RMS` on the plot.
9.  **Cleanup:** Frees allocated memory, closes files, and finalizes PostScript/raster output.

## Output
*   A PostScript metafile (`plot.meta` or specified by `-outfile`) visualizing the time-series data.
*   If `-raster` is used: A binary JHC `.r4` array file (`<infile_prefix>.tide.raster`) containing the rasterized plot.
*   `plottide.range`: A temporary file (seems unused by `main` except for writing plausible averages/RMS).
```
```