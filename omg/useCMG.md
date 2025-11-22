---
layout: default
title: useCMG
parent: OMG Tools
nav_order: 76
---
# useCMG

## Description
`useCMG` is a utility designed to process and filter heading information from OMG-HDCS merged files, primarily to generate a more accurate Course Made Good (CMG) heading. It calculates CMG based on changes in vessel position, filters this CMG, and then optionally combines it with the high-frequency components of the logged gyro heading to produce a filtered heading that accounts for both long-term course and short-period vessel motions.

This tool is particularly useful for improving navigation accuracy, especially in situations where the raw gyro heading might be noisy or subject to long-term drift.

## Usage
```bash
useCMG <OMG_HDCS_datafile(s)> [-filtlen <value>] [-test] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile(s)>` | **Required.** One or more paths to OMG-HDCS merged files to be processed. These files are modified in place unless `-test` is used. |
| `-filtlen <value>` | Specifies the half-width of the filter (number of pings on each side) to use for smoothing. | `3` |
| `-test` | Runs the processing but does *not* write any changes back to the merged file. Useful for previewing potential changes. |
| `-v` | Enable verbose output. |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Summary Header Reading:** Reads the summary header to get `summary.numProfiles`, `summary.refLat`, `summary.timeScale`, and `summary.positionScale`. `coslat` is calculated from `summary.refLat` for position calculations.
3.  **Data Extraction & CMG Calculation:**
    *   Allocates memory for several double arrays: `CMG_x`, `CMG_y`, `CMG_azi` (Course Made Good components), `GYRO_x`, `GYRO_y`, `GYRO_azi` (raw gyro heading components), `NEW_GYRO_azi`, `NEW_GYRO_x`, `NEW_GYRO_y` (filtered heading components), and `SOG` (Speed Over Ground).
    *   Iterates through all profiles (pings) in the merged file:
        *   Reads the current profile.
        *   Extracts `profile.vesselHeading` to populate `GYRO_azi`, then converts `GYRO_azi` into X/Y components (`GYRO_x`, `GYRO_y`).
        *   Calculates the change in vessel position (`CMG_x`, `CMG_y`) between consecutive pings using `vesselLongOffset` and `vesselLatOffset`, scaled by `coslat`.
        *   Calculates the `CMG_azi` (azimuth) from `CMG_x` and `CMG_y`.
        *   Calculates Speed Over Ground (`SOG`) from `CMG_x`, `CMG_y`, `dT` (time difference between pings), and scaling factors. It includes a commented-out check to filter `SOG` values above `30` knots.
4.  **Filtering & Blending:**
    *   Iterates through profiles from `filtlen` to `summary.numProfiles - filtlen - 1` (the range where a full filter window is available):
        *   Calculates `low_cmg_x` and `low_cmg_y` by averaging `CMG_x` and `CMG_y` values within the filter window. This effectively smoothes the CMG. It also includes a check using `SOG` and a `MaxKnots` threshold (`20.0`) to avoid averaging in "insane" values.
        *   Calculates `low_gyro_x` and `low_gyro_y` by averaging `GYRO_x` and `GYRO_y` values within the filter window.
        *   Converts these averaged components back to azimuths (`low_cmg_azi`, `low_gyro_azi`).
        *   **Heading Blending (Commented Out in Nov 2020):** The original intent was to blend the low-frequency CMG with the high-frequency component of the raw gyro. The current implementation, however, primarily uses the smoothed CMG. `NEW_GYRO_x[i]` and `NEW_GYRO_y[i]` are set to `low_cmg_x` and `low_cmg_y` respectively, and `NEW_GYRO_azi[i]` is derived from them.
    *   For profiles at the start and end that don't have a full filter window, the `NEW_GYRO_azi` values are extrapolated from the nearest valid filtered value.
5.  **Writing Changes:**
    *   If `-test` is *not* used, the tool iterates through all profiles again.
    *   For each profile `i`, it reads the original profile, updates its `profile.vesselHeading` with the (integer cast and scaled) `NEW_GYRO_azi[i]`, and writes the modified profile back to the merged file.
6.  **Cleanup:** Frees allocated memory and closes files.
