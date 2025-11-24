---
layout: default
title: EK_init (Initialization Function within EKlook)
parent: EKlook Tools
nav_order: 11
---
# EK_init (Initialization Function within EKlook)

## Description
`EK_init` is a function (defined in `EK_init.c`) primarily responsible for initializing global variables and default settings for the `EKlook` application. This function sets up various parameters related to sound speed, display dimensions, ocean environment (pH, temperature, salinity, depth), backscatter display ranges, calibration, and bottom detection. When `EKlook` starts, `eklook_init()` ensures that the application environment is configured with a consistent set of default values before loading data or processing user input.

## Key Initialized Variables and Default Values

The `eklook_init()` function sets the following default values and configurations for the `EKlook` application:

*   **Environmental Parameters:**
    *   `meansoundspeed`: `1500.0` m/s
    *   `Ocean_pH`: `8.0`
    *   `Ocean_Temp`: `12.0` (Celsius)
    *   `Ocean_Sali`: `35.0` (PSU)
    *   `Ocean_AvDepth`: `5.0` (meters, average depth for some calculations)

*   **Display and Image Dimensions:**
    *   `sidebarX`: `40` pixels
    *   `thumbnailX`, `thumbnailY`: `500`, `700` pixels (dimensions for the whole file overview image)
    *   `zoomX`, `zoomY`: `1000`, `400` pixels (dimensions for the zoomed-in image section)

*   **Backscatter and Calibration Parameters:**
    *   `mindB`, `maxdB`: `-70`, `70` dB (default display range for overall backscatter)
    *   `BulkCalibration`: `-120.0` dB (a default global calibration offset)
    *   `trimdB`: Automatically set to `(mindB + maxdB) / 2.0`
    *   `maxPressure`: Calculated from `maxdB` (`10^(maxdB/20.0)`)
    *   `BSmax`, `BSmin`: `10.0`, `-40.0` dB (default display range for bottom/ARC backscatter)

*   **Angular Response Curve (ARC) Settings:**
    *   `BSaddTL`: `1` (Transmission Loss corrections are included by default)
    *   `BSaddBP`: `1` (Beam Pattern corrections are included by default)
    *   `BSaddArea`: `1` (Ensonified Area corrections are included by default)
    *   `use_area_model`: `AREA_BW` (Bandwidth-based model for ensonified area calculation)

*   **Bottom Detection and Phase Analysis:**
    *   `maxAcceptablePhaseFit`: `0.1`
    *   `maxBelievableAmplitudeElevation`: `20.0`
    *   `Along_AngleSensitivity`, `Across_AngleSensitivity`: `23.0` (default for 7-degree systems)
    *   `TwoWayBeamWidth`: `5.0` degrees
    *   `R_WBT_tx`, `R_WBT_rx`: `25` Ohms, `1000` Ohms (WBT internal resistances)
    *   `WhichTraceforAmplitudeDetect`: `USELOWPASS` (default amplitude detection method)
    *   `MinimumValidPhaseSamples`: `30`
    *   `dBdrop`: `10` (signal drop-off in dB for bottom detection)
    *   `phaseOffZero`: `90` (phase offset from zero for bottom detection)

*   **Other Flags and Debug Settings:**
    *   `verbose_flag`: `0` (off)
    *   `showTrack`: `2` (default tracking display mode)
    *   `gotSphereTS`, `sphereFshift`, `noSpherePts`: `0`
    *   `validNav`, `validMotion`, `validHeading`: `0`
    *   `gotBottomTrackGuide`: `0`
    *   `eklook_record`, `JEVENT_debug`: `0`
    *   `useWindows`, `useStart[0]`, `useStop[0]`: `1`, `0`, `MAXTRACES`

## How It Works
The `eklook_init()` function is automatically called when the `EKlook` application starts. Its primary role is to ensure a consistent and predictable operational environment by assigning default values to all critical global variables and flags. This prevents undefined behavior and prepares the application for loading user data and processing. Many of these initialized values can subsequently be modified interactively by the user within the `EKlook` GUI.

## Notes
The `eklook_init()` function is an internal initialization routine of the `EKlook` application. It does not accept any command-line arguments. Its purpose is to establish a foundational state for the GUI and its underlying data processing. Users can modify many of these parameters interactively within the `EKlook` application once it has started.