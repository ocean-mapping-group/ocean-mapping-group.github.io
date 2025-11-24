---
layout: default
title: plotDelayHeave
parent: Plot Tools
nav_order: 137
---
# plotDelayHeave

## Description
`plotDelayHeave` is a specialized plotting utility designed to visualize delayed heave data, typically generated from post-processing POS/MV output (e.g., Applanix). It processes various time-series heave data (real-time, post-processed, high-pass filtered, and their differences) and plots them, along with indicating the extent of associated multibeam merged files.

The tool calculates and displays differences between different heave measurements, performs trend removal, and can apply high-pass filters, all crucial for analyzing and correcting vertical motion in hydrographic surveys. It is designed to handle large datasets by dumping intermediate results to disk.

## Usage
```bash
plotDelayHeave -infile <base_name> [-outfile <filename.meta>] [-size <dx> <dy>] [-start <yr> <jday> <hr> <min>] [-end <yr> <jday> <hr> <min>] [-xrange <min> <max>] [-dep] [-atten <val>] [-delay <val>] [-skip <val>] <merged_file(s)...>
```

## Arguments

| Option | Description |
|---|---|
| `-infile <base_name>` | **Required.** Specifies a base name for binary time series files (e.g., `rt_hv_base_name.out`, `vp_base_name.out`, etc.). |
| `-outfile <filename.meta>` | Specifies the output PostScript metafile name. | `plot.meta` |
| `-size <dx> <dy>` | Specifies the plot size in centimeters. | `20.0 18.0` |
| `-start <yr> <jday> <hr> <min>` | Sets the start time (X-axis minimum) for the plot. |
| `-end <yr> <jday> <hr> <min>` | Sets the end time (X-axis maximum) for the plot. |
| `-xrange <min> <max>` | Sets the X-axis range (seconds from epoch). Overrides `-start` and `-end`. |
| `-dep` | (Present in `USAGE`, but not used in provided snippet.) Intended for displaying depths. |
| `-atten <val>` | Attenuation factor to apply to heave data. | `1.0` |
| `-delay <val>` | Time delay in minutes to apply to heave data. | `0.0` |
| `-skip <val>` | Skip factor for plotting data points. | `5` |
| `<merged_file(s)...>` | (Optional) One or more merged files. Their time extents will be indicated on the plot. |

## Data Files Generated/Used by `-infile <base_name>`
*   `rt_hv_<base_name>.out`: Real-time heave data.
*   `vp_<base_name>.out`: Vertical position data.
*   `pp_hv_<base_name>.out`: Post-processed heave data.
*   `deri_<base_name>.rt-pp`: Difference between real-time and post-processed heave.
*   `deri_<base_name>.rt-pp_detrend`: Detrended difference between real-time and post-processed heave.
*   `deri_<base_name>.hpf_of_vp`: High-pass filtered vertical position.
*   `deri_<base_name>.rt-hpf_of_vp`: Real-time heave minus high-pass filtered vertical position.
*   `deri_<base_name>.vp_detrend`: Detrended vertical position.

## How It Works
1.  **Initialization:** Parses command-line arguments, setting input/output filenames, plot ranges, and processing flags.
2.  **File Naming:** Constructs filenames for various heave data streams based on the `-infile` base name.
3.  **Plot Setup:** Initializes the `plotlib` PostScript output (`plot.meta`). Sets up the overall plot dimensions (`xlength`, `ylength`, `xoff`).
4.  **Plot Areas:** Divides the plotting area into 8 vertical subplots, each for a different heave data type.
5.  **Heave Data Processing Loop:** For each of the 8 plots:
    *   **Data Loading (`suck_in_data`):** Reads binary time-series data (timestamp and value) from the respective file into `heave_data[i]`.
    *   **Data Derivation:**
        *   **Plot 3 (`deri_...rt-pp`):** Calculates the difference between `heave_data[0]` (real-time heave) and `heave_data[2]` (post-processed heave). Applies a least-squares detrending to `heave_data[2]` before differencing.
        *   **Plot 4 (`deri_...rt-pp_detrend`):** Calculates the difference between `heave_data[3]` (detrended post-processed heave) and `heave_data[0]` (real-time heave), with an alignment shift.
        *   **Plot 5 (`deri_...hpf_of_vp`):** Applies a simple 1500-point boxcar high-pass filter to `heave_data[1]` (vertical position).
        *   **Plot 6 (`deri_...rt-hpf_of_vp`):** Calculates the difference between `heave_data[5]` (high-pass filtered vertical position) and `heave_data[0]` (real-time heave).
        *   **Plot 7 (`deri_...vp_detrend`):** Applies a least-squares detrending to `heave_data[1]` (vertical position).
    *   **Data Dumping (`dump_out_data`):** Writes processed data to intermediate binary files.
    *   **X-axis Range Determination:** Sets `xmin` and `xmax` based on the time extents of the data, or user-provided `-start`, `-end`, or `-xrange`.
    *   **Y-axis Range Determination:** Calculates `ymin[i]` and `ymax[i]` from the loaded data and then prompts the user for interactive input.
    *   **Plotting Data:** Plots the time-series data for the current plot `i`.
6.  **Merged File Extent Plotting:** If merged files (`.merged`) are provided, it reads their summary headers, extracts their time extents, and indicates these extents as rectangular boxes on the plot.
7.  **Cleanup:** Frees allocated memory and closes all files.

## Output Files
*   `<outfile_name>`: A PostScript metafile (`.meta`) containing time-series plots of heave data.
*   Multiple intermediate binary files (e.g., `rt_hv_<base_name>.out`, `deri_<base_name>.rt-pp`, etc.) storing processed heave data.

## Helper Functions
*   `suck_in_data(int i, int *num)`: Reads a binary time-series (double timestamp, double value) from `name[i]` into `heave_data[i]`.
*   `suck_in_quarter_data(int i, int *num)`: Reads data from `name[i]`, taking only every 4th record (not actively used in `main` as written).
*   `dump_out_data(int i, int num)`: Writes a binary time-series (double timestamp, double value) from `heave_data[i]` to `name[i]`.

## Dependencies
*   `plotlib.h`: For `plotlib` functions.
*   `support.h`: For general utility functions.
*   `stdtime.h`: For time conversion.
*   `OMG_HDCS_jversion.h`: For merged file structures.

## Notes
`plotDelayHeave` is a critical tool for quality control and analysis of vertical motion data, particularly for assessing the performance of different heave measurement systems (e.g., real-time vs. post-processed). The ability to visualize differences and apply filters helps in identifying residual errors that can affect bathymetric accuracy. The tool relies on specific binary data formats for the heave components.