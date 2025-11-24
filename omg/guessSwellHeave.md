---
layout: default
title: guessSwellHeave
parent: OMG Tools
nav_order: 109
---
# guessSwellHeave

## Description
`guessSwellHeave` is a utility designed to estimate and apply swell heave data to OMG-HDCS merged files, particularly for cases where direct heave measurements are unavailable (e.g., some NMFS EK data). The core idea is to assume that heave is the difference between observed depth and a low-pass filtered version of the observed depth, under the assumption that the seafloor does not have significant undulations within the filter length.

The tool uses either a simple moving average or a cosine-squared tapered weighted average filter to derive a "smoothed" depth, and then calculates heave as the difference between the original and smoothed depths. It can also filter out improbable heave values.

## Usage
```bash
guessSwellHeave <OMG_HDCS_datafile(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile(s)>` | **Required.** One or more paths to OMG-HDCS merged files. These files are modified in place unless `-test` is used. |
| `-v` | Enable verbose output. |
| `-test` | Runs the process but does *not* write any changes back to the merged file. Useful for previewing results. |
| `-filtlen <value>` | Specifies the half-width of the simple moving average filter (number of pings on each side). | `10` |
| `-cos_taper <seconds>` | Uses a cosine-squared tapered weighted average filter. `<seconds>` is the half-width of the filter in seconds. |
| `-maxheave <val>` | Rejects heave values (sets to 0.0) if their absolute value exceeds `val` meters. | `0.0` (disabled) |
| `-maxdheave <val>` | Rejects heave values (sets to 0.0) if the absolute change in heave from ping to ping exceeds `val` meters. | `0.0` (disabled) |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Summary Header Reading:** Reads the summary header to determine `summary.numProfiles` and `summary.timeScale`.
3.  **Data Extraction:**
    *   Allocates memory for `Times`, `Depths`, `SmthDe` (smoothed depths), `Heaves`, and `HeavesOK` (final filtered heave).
    *   Iterates through all profiles, extracts the `time` (Unix timestamp) and `depth` (from `beams[0].observedDepth`, scaled by `positionScale`) for each ping, and stores them in `Times` and `Depths` arrays.
4.  **Heave Calculation:**
    *   **Cosine-Tapered Filter (`-cos_taper`):**
        *   If `cos_taper` is active, it applies a cosine-squared tapered weighted average filter to the `Depths` array to calculate `SmthDe`. The weights are determined by the time difference between pings and the `longperiod` parameter (filter half-width in seconds).
        *   Heave is then calculated as `Heaves[k] = Depths[k] - SmthDe[k]`.
    *   **Simple Moving Average (`-filtlen`):**
        *   If `cos_taper` is *not* active, it applies a simple moving average filter of width `filtlen * 2` to `Depths` to calculate `SmthDe`.
        *   Heave is then calculated as `Heaves[i] = Depths[i] - SmthDe[i]`.
5.  **Heave Filtering (`-maxheave`, `-maxdheave`):**
    *   If `maxdheave` is specified, it checks the absolute difference in `Heaves` between consecutive pings. If it exceeds `maxdheave`, `HeavesOK[i]` for that ping is set to `0.0`.
    *   If `maxheave` is specified, it checks the absolute value of `Heaves[i]`. If it exceeds `maxheave`, `HeavesOK[i]` is set to `0.0`.
6.  **Writing Changes:**
    *   If `-test` is *not* used, the tool iterates through all profiles again.
    *   For each profile `i`, it reads the original profile, updates its `profile.vesselHeave` with `HeavesOK[i]` (scaled to millimeters and inverted), and writes the modified profile back to the merged file.
7.  **Cleanup:** Frees allocated memory and closes files.

## Output Files
The input merged files are modified in-place (unless `-test` is used).

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
Estimating heave from observed depths can be a useful technique when direct heave measurements are unavailable, but it relies on the assumption of a relatively flat seafloor within the filter window. This method is often used in preliminary processing or for data from systems that do not log detailed motion data. The filtering options help to remove spurious heave values. The tool modifies merged files in place, so backups are recommended.