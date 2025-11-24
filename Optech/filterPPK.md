---
layout: default
title: filterPPK
parent: Optech Tools
nav_order: 113
---
# filterPPK

## Description
`filterPPK` is a utility designed to process and filter RTK (Real-Time Kinematic) heave data, specifically the `RTK_at_RP` (RTK height at Reference Point) field stored in OMG-HDCS merged files. It applies a low-pass filter (cosine-squared tapered weighted average) to this RTK height data to extract the long-period heave component.

The tool aims to separate the short-period heave (swell) from the long-period heave (tide and any residual vertical datum issues) for more accurate data processing. The filtered long-period heave is then outputted, and the high-pass filtered component could theoretically represent the swell heave.

## Usage
```bash
filterPPK <OMG_HDCS_datafile(s)> [-out <ASCII_filename>] [-longperiod <val>] [-verbose]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `<OMG_HDCS_datafile(s)>` | **Required.** One or more paths to input OMG-HDCS merged files. | `survey_data.merged` |
| `-out <ASCII_filename>` | **Required.** The path for the output ASCII file (contains filtered RTK heights and timestamps). | `filtered_rtk.txt` |
| `-longperiod <val>` | Specifies the half-width of the cosine-squared tapered low-pass filter (in seconds). This effectively controls the cutoff frequency of the filter. | `15.0` |
| `-verbose` | Enable verbose output. | |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Summary Header Reading:** Reads the summary header from the merged file.
3.  **Memory Allocation:** Allocates memory for `longperiod_heave`, `RTK_at_RP`, `filtRTKatRP`, `heave`, `highpassHeave`, `TtimE` (timestamps), and `weight` arrays.
4.  **Data Extraction & Filtering:** Loops through each profile (ping) in the merged file:
    *   Reads the `profile` header.
    *   Extracts `profile.RTK_at_RP` (scaled by 100.0) into `RTKatRP[k]`.
    *   Extracts the Unix timestamp (`TtimE[k]`) from the profile.
    *   **Low-Pass Filter Application:** Applies a cosine-squared tapered weighted average filter to `RTKatRP` values:
        *   For each ping `k`, it calculates a weighted sum of `RTKatRP` values from surrounding pings within the `longperiod` (time window) using a cosine-squared taper.
        *   This weighted sum, divided by the total weight, gives the `filtRTKatRP[k]`, which represents the low-pass filtered (long-period) heave.
        *   The `highpassHeave[k]` (swell component) is calculated as `heave[k] - longperiod_heave[k]` (though `heave[k]` and `longperiod_heave[k]` aren't clearly populated from original merged file data in the provided snippet, implying they might be internal calculations or zero-initialized).
5.  **Output to ASCII File:** For each ping, it prints the Unix timestamp (`TtimE[k]`) and the low-pass filtered RTK height (`filtRTKatRP[k]`) to the output ASCII file.
6.  **Cleanup:** Frees allocated memory and closes files.

## Output Files
*   `<ASCII_filename>`: An ASCII file containing timestamps and filtered RTK heights.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.
*   `math.h`: For mathematical functions.

## Notes
The `RTK_at_RP` field often contains high-frequency heave noise along with the desired long-period tide component. This tool separates these components using a spectral filter, which is crucial for applying accurate vertical datum corrections in hydrographic surveys. The terms `heave` and `highpassHeave` in the code are noted as potentially confusing; `RTKatRP` (from `profile.RTK_at_RP`) is the primary input.