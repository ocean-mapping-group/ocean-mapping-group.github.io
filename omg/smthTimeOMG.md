---
layout: default
title: smthTimeOMG
parent: OMG Tools
nav_order: 66
---
# smthTimeOMG

## Description
`smthTimeOMG` is a utility designed to smooth the `timeOffset` values stored in the profile headers of OMG-HDCS merged files. This is particularly useful for data derived from sources like SEGY, where time information might only be accurate to the integer second, but fractional second precision is needed for blending with other data (like heave).

The tool applies a moving average filter to the `timeOffset` values and can also apply a constant time shift.

## Usage
```bash
smthTimeOMG <OMG_HDCS_datafile(s)> [-v] [-test] [-filtlen <value>] [-Tshift <value>]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile(s)>` | **Required.** One or more paths to OMG-HDCS merged files to be processed. These files are modified in place unless `-test` is used. |
| `-v` | Enable verbose output. |
| `-test` | Runs the smoothing operation but does *not* write any changes back to the merged file. Useful for previewing potential changes. |
| `-filtlen <value>` | Specifies the half-width of the moving average filter (number of pings on each side to average over). The total window size will be `filtlen * 2`. | `3` |
| `-Tshift <value>` | Applies a constant time shift (in seconds) to the smoothed `timeOffset` values. | `0` |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Summary Header Reading & Time Scale Adjustment:** Reads the summary header to get `summary.numProfiles` and `summary.timeScale`. The `Tshift` value is rescaled internally to match the units of `timeOffset` (microseconds * `timeScale`).
3.  **Time Offset Extraction:**
    *   Allocates memory for two double arrays: `timeOffset` (to store original `profile.timeOffset` values) and `low_timeOffset` (for smoothed values).
    *   Iterates through all profiles in the merged file, extracting and storing each `profile.timeOffset` into the `timeOffset` array.
4.  **Moving Average Smoothing:**
    *   Copies the `timeOffset` array to `low_timeOffset`.
    *   Iterates through profiles from `filtlen` to `summary.numProfiles - filtlen - 1` (to ensure a full window is available).
    *   For each profile `i`, it calculates the average of `timeOffset` values within the window `[i - filtlen, i + filtlen - 1]`.
    *   This average is then stored in `low_timeOffset[i]`.
    *   The `Tshift` (rescaled) is added to `low_timeOffset[i]`.
5.  **Writing Changes:**
    *   If `-test` is *not* used, the tool iterates through all profiles again.
    *   For each profile `i`, it reads the original profile, updates its `profile.timeOffset` with the (integer cast of) `low_timeOffset[i]`, and writes the modified profile back to the merged file.
6.  **Cleanup:** Closes files and frees dynamically allocated memory.
