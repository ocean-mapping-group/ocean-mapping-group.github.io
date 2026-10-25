---
layout: default
title: EK_init (Initialization Function within EKlook)
parent: Simrad EK60/EK80 Echosounder Suite (EKlook)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 11
tool_name: EK_init
source_path: code/EKlook/EK_init.c
category: EKlook
input_formats:
- Internal Default Parameters
output_formats:
- Initialized EKlook Global State
related_tools:
- EKlook
- EK_funcs
---

# EK_init (Initialization Function within EKlook)

## Description
`EK_init` (`code/EKlook/EK_init.c`) defines `eklook_init()`, which initializes global oceanographic, electrical, radiometric, and GUI window parameters when [`EKlook`](EKlook.html) starts up.

## Key Initialized Variables and Default Values

*   **Environmental Parameters:**
    *   `meansoundspeed`: `1500.0` m/s
    *   `Ocean_pH`: `8.0`
    *   `Ocean_Temp`: `12.0` $^\circ\text{C}$
    *   `Ocean_Sali`: `35.0` PSU
    *   `Ocean_AvDepth`: `5.0` m
*   **Display and Image Dimensions:**
    *   `sidebarX`: `40` pixels
    *   `thumbnailX`, `thumbnailY`: `500`, `700` pixels (main file overview)
    *   `zoomX`, `zoomY`: `1000`, `400` pixels (zoomed echogram section)
*   **Backscatter and Calibration Parameters:**
    *   `mindB`, `maxdB`: `-70.0`, `70.0` dB
    *   `BulkCalibration`: `-120.0` dB
    *   `BSmax`, `BSmin`: `10.0`, `-40.0` dB (ARC display range)
*   **Angular Response Curve (ARC) Settings:**
    *   `BSaddTL = 1`, `BSaddBP = 1`, `BSaddArea = 1` (Transmission Loss, Beam Pattern, and Ensonified Area corrections enabled by default)
    *   `use_area_model`: `AREA_BW` (bandwidth-based ensonified area model)
*   **Bottom Detection and WBT Transceiver Settings:**
    *   `maxAcceptablePhaseFit`: `0.1`
    *   `Along_AngleSensitivity`, `Across_AngleSensitivity`: `23.0` (standard $7^\circ$ split-beam transducer sensitivity)
    *   `TwoWayBeamWidth`: `5.0` degrees
    *   `R_WBT_tx`, `R_WBT_rx`: `25` $\Omega$, `1000` $\Omega$ (Kongsberg Wide Band Transceiver internal impedances)
    *   `dBdrop`: `10` dB, `phaseOffZero`: `90` degrees
