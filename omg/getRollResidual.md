---
layout: default
title: getRollResidual
parent: OMG Tools
nav_order: 106
---
# getRollResidual

## Description
`getRollResidual` is a utility designed to estimate and output the residual roll error (or, more generally, the across-track slope) present in multibeam sonar data. It does this by calculating the across-track slope of the seafloor for each ping using a least-squares fit to the observed depths and across-track positions of the beams. It then applies a moving average filter to these slopes to identify the long-term trend, and outputs both the raw slope and the filtered slope.

This tool is useful for identifying and quantifying residual roll biases in the data, which may be due to uncorrected vessel motion or misalignment.

## Usage
```bash
getRollResidual <filename.merged> [-testonly]
```

## Arguments

| Option | Description |
|---|---|
| `<filename.merged>` | **Required.** The path to the input OMG-HDCS merged file. |
| `-testonly` | (Present in `USAGE` but not implemented) This option likely suggests a test mode, but its functionality is not seen in `main`. |

## How It Works
1.  **File Opening:** Opens the input merged file for reading (`r+`).
2.  **Summary Header Reading:** Reads the summary header to determine `summary.numProfiles`.
3.  **Memory Allocation:** Allocates memory for arrays to store `across_track_slope` (raw slope per ping) and `slope_fit` (filtered slope).
4.  **Profile Iteration (Calculate Raw Slopes):** Loops through each profile (ping) in the merged file:
    *   Reads the current profile header and raw beams.
    *   Extracts valid `observedDepth` and `acrossTrack` values into `yvals` and `xvals` arrays, respectively.
    *   **Least-Squares Fit:** Performs a linear least-squares regression (`do_least_squares`) on `xvals` vs. `yvals` to calculate `intercept`, `slope`, and `fit` for the current ping.
    *   Stores the calculated `slope` (converted to degrees) in `across_track_slope[i]`.
    *   Calculates a `slope_fit[i]` based on the `fit` and `intercept` (a measure of how well the data fits the slope). If `intercept` is zero, `slope_fit[i]` is set to `999.0`.
5.  **Profile Iteration (Calculate Filtered Slopes and Output):** Loops through each profile again (or prints directly in the same loop if `filter_length` logic is applied to `across_track_slope`):
    *   For pings that are not near the edges of the file (to ensure a full `filter_length` window):
        *   Calculates a `filtered_slope` by averaging `across_track_slope` values within a moving window of `filter_length` (hardcoded to `40`) pings.
    *   Outputs the ping number, the raw `across_track_slope[i]`, and the `filtered_slope` to standard output.
6.  **Cleanup:** Closes the merged file and frees allocated memory.

## Output
The tool prints to standard output:
*   Ping number
*   Raw across-track slope (in degrees) for that ping
*   Filtered across-track slope (in degrees) for that ping
```