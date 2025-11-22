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
| `-v` | Enable verbose output. |

## How It Works
1.  **File Processing:** The tool iterates through each specified merged file.
2.  **Summary Header Reading:** Reads the summary header for basic file information.
3.  **Time Smoothing Loop:** For each profile `i` in the merged file (excluding profiles at the beginning and end that cannot accommodate the full `noav` window):
    *   It calculates the total `timeOffset` by summing the `timeOffset` values of `noav` profiles centered around `i`.
    *   The sum is then divided by `noav` to get the average `timeOffset`.
    *   The `timeOffset` of the current profile `i` is updated with this newly calculated average.
    *   The modified profile header is written back to the merged file.
4.  **In-Place Modification:** The merged file is modified in place, updating the `timeOffset` values for profiles within the processing range.
