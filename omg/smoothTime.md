---
layout: default
title: smoothTime
parent: OMG Tools
nav_order: 64
---
# smoothTime

## Description
`smoothTime` is a utility designed to apply a simple moving average filter to the `timeOffset` field within the profile headers of OMG-HDCS merged files. The goal is to smooth out any "jerky" or noisy time stamps, which can improve the accuracy of subsequent navigation interpolation or other time-sensitive processing.

The tool calculates an average `timeOffset` over a specified window (`noav`) of profiles and updates the central profile's `timeOffset` with this averaged value.

## Usage
```bash
smoothTime <OMG_HDCS_datafile(s)> [-noav <value>] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile(s)>` | **Required.** One or more paths to OMG-HDCS merged files to be processed. These files are modified in place. |
| `-noav <value>` | Specifies the number of profiles (window size) to use for the moving average. It should be an odd number to have a clear center. | `3` |
| `-v` | Enable verbose output. | |

## How It Works
1.  **File Processing:** The tool iterates through each specified merged file.
2.  **Summary Header Reading:** Reads the summary header to get `summary.numProfiles` and `summary.timeScale`.
3.  **Time Offset Extraction:**
    *   Allocates memory for two double arrays: `timeOffset` (to store original `profile.timeOffset` values) and `low_timeOffset` (for smoothed values).
    *   Iterates through all profiles in the merged file, extracting and storing each `profile.timeOffset` into the `timeOffset` array.
4.  **Moving Average Smoothing:**
    *   Copies the `timeOffset` array to `low_timeOffset`.
    *   Iterates through profiles from `filtlen` to `summary.numProfiles - filtlen - 1` (the range where a full window is available).
    *   For each profile `i`, it calculates the average of `timeOffset` values within the window `[i - filtlen, i + filtlen - 1]`.
    *   This average is then stored in `low_timeOffset[i]`.
    *   The `Tshift` (rescaled) is added to `low_timeOffset[i]`.
5.  **Writing Changes:**
    *   If `-test` is *not* used, the tool iterates through all profiles again.
    *   For each profile `i`, it reads the original profile, updates its `profile.timeOffset` with the (integer cast of) `low_timeOffset[i]`, and writes the modified profile back to the merged file.
6.  **Cleanup:** Closes files and frees dynamically allocated memory.

## Output Files
The input merged files are modified in-place.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
Smoothing timestamps can be beneficial for data from systems with imprecise time registration or for integrating data from multiple asynchronous sensors. The filter helps to remove high-frequency jitter while preserving the overall temporal trend. The tool modifies merged files in place, so backups are recommended. The `-test` option allows for previewing results before committing changes.