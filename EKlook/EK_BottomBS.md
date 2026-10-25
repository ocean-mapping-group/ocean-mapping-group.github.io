---
layout: default
title: EK_BottomBS (Module within EKlook)
parent: Simrad EK60/EK80 Echosounder Suite (EKlook)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 3
tool_name: EK_BottomBS
source_path: code/EKlook/EK_BottomBS.c
category: EKlook
input_formats:
- In-Memory EKlook Trace & Phase Arrays
output_formats:
- Bottom Track Guide (.BottomTrackGuide)
- Angular Response Curves (.ARC_fullBW, .ARC_3D, .ARC_FFTbins, .ARC_FFT3D)
related_tools:
- EKlook
- BatchProcEK
- comboCalibEK_ARCs
- EK_funcs
---

# EK_BottomBS (Module within EKlook)

## Description
`EK_BottomBS` (`code/EKlook/EK_BottomBS.c`) is an interactive GUI module within the [`EKlook`](EKlook.html) application. It manages the **"BOTTOM Detect / ARC Window,"** allowing users to interactively tune bottom-detection parameters (`dBdrop`, `phaseOffZero`), toggle radiometric/geometric corrections (Transmission Loss, Beam Pattern, Ensonified Area), inspect sub-window FFT spectra across the seafloor echo envelope, and stack or export broadband Angular Response Curves (ARCs).

## Interactive Controls

| Control | Description | Related Variable |
|---|---|---|
| **Buttons (Toggle Corrections)** | | |
| `addTL` | Toggles Transmission Loss (TL) corrections in ARC calculations. | `BSaddTL` |
| `addBP` | Toggles Beam Pattern (BP) corrections in ARC calculations. | `BSaddBP` |
| `addArea` | Toggles Ensonified Area corrections in ARC calculations. | `BSaddArea` |
| `depthGuide` | Toggles the use of Nadir Depth as a guide for bottom detection. | `useNadirDepthGuide` |
| `mountGuide` | Toggles the use of Mount Angle as a guide for bottom detection. | `useMountAngleGuide` |
| **Buttons (ARC Operations)** | | |
| `dump BStrack` | Saves bottom track parameters to `<prefix>.BottomTrackGuide` for use in [`BatchProcEK`](BatchProcEK.html). | |
| `flushARC` | Clears the accumulated Angular Response Curves (ARCs). | `ARC_cummulative`, `ARC_byPing` |
| `dump ARC` | Writes the current accumulated ARC to disk. | `ARC_cummulative` |
| `stack all ARC` | Stacks all valid ping envelopes into a cumulative ARC and writes it to disk. | `ARC_cummulative` |
| `show Area/Grazing` | Toggles the display of ensonified area versus grazing angle. | `showAreaGrazing` |
| **Sliders** | | |
| `Angle Sensitivity` | Adjusts the split-beam angle sensitivity for along and across angles. | `Along_AngleSensitivity` |
| `Bulk Calibration` | Adjusts the bulk calibration offset (in dB) applied to backscatter. | `BulkCalibration` |
| `Nadir Depth` | Sets the nadir water depth guide (m). | `NadirDepth` |
| `Mount Angle` | Adjusts the transducer roll mount angle ($^\circ$). | `EKMountAngle.roll` |
| `Sub-Window FFT Length` | Sets the sample length of the sliding FFT sub-window (`64`, `32`, `16`, `8`, `4`, `2`). | `envWinSize` |

## Visualizations

*   **Matched-Filtered Echo Envelope (dB):** Displays the echo envelope and bottom detection bounds.
*   **Fore/Aft & Port/Starboard Phase:** Displays raw and low-pass filtered split-beam electrical phase ramps and zero crossings.
*   **Highlighted Envelope Subwindow Spectrum & I/Q:** Displays the FFT power spectrum and complex I/Q waveform of the selected envelope sub-window.
*   **Apparent Echo Envelope using Highlighted Frequency Slice:** Displays the echo envelope extracted at a single FFT frequency bin.
*   **ARC & ARC Count Windows:** Plots single-ping and cumulative Angular Response Curves ($BS$ vs. grazing angle) alongside normalized bin counts.

## Key Bindings

*   `KEY_Z`: Resets the active slider to its default value.
*   `KEY_Q` / `KEY_ESC`: Closes the "BOTTOM Detect / ARC window."
*   `KEY_UP` / `KEY_DOWN`: Adjusts the `BSmax` and `BSmin` display range in the ARC plot.
*   `KEY_LEFT` / `KEY_RIGHT`: Adjusts slider values or steps through envelope sub-windows and frequency slices.
*   `KEY_SPACE`: Toggles `whichARC` between full-bandwidth time-domain ARCs and FFT frequency-bin ARCs.
