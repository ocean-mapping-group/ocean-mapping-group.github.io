---
layout: default
title: EK_ZoomImage (Module within EKlook)
parent: EKlook Tools
nav_order: 8
tool_name: EK_ZoomImage
source_path: code/EKlook/EK_ZoomImage.c
category: EKlook
input_formats:
  - In-Memory Trace, Phase & Complex IQ Arrays (.MF_dB, .Raw_dB, .PS_phase, .FA_phase, .MF_IQ)
output_formats:
  - Bottom Track Guide (.BottomTrackGuide)
  - Ping Parameters (.ping_Params)
related_tools:
  - EKlook
  - EK_BottomBS
  - BatchProcEK
---

# EK_ZoomImage (Module within EKlook)

## Description
`EK_ZoomImage` (`code/EKlook/EK_ZoomImage.c`) is an interactive GUI module within the [`EKlook`](EKlook.md) application. It manages the **"ZOOM EK-Trace Window,"** providing a high-resolution zoomed echogram of selected ping ranges alongside single-ping vertical profiles of uncompressed power (`.Raw_dB`), matched-filtered power (`.MF_dB`), complex I/Q waveforms (`.MF_IQ`), and Fore–Aft / Port–Starboard split-beam phase angles. It also allows interactive adjustment of bottom-detection parameters (`dBdrop`, `phaseOffZero`, `maxAcceptablePhaseFit`) and bottom-track guide curves.

## Interactive Controls

| Control | Description |
|---|---|
| **Buttons** | |
| `full trace` | Resets the vertical zoom window to encompass the full range of the current trace. |
| `Power or IQ` | Toggles the single-ping trace plot between logarithmic power (dB) and linear In-Phase / Quadrature (I/Q) components. |
| `Power or Phase` | Toggles the 2D zoomed echogram image between backscatter intensity (dB) and split-beam phase angle. |
| `add TL` | Toggles Transmission Loss (TL) correction on the displayed power traces. |
| `record on/off` | Toggles frame recording mode. |
| `before/after MF` | Toggles the envelope display between uncompressed (`.Raw_dB`) and matched-filtered (`.MF_dB`) traces. |
| **Sliders** | |
| `dB drop (beam pattern roll off)` | Adjusts the envelope amplitude drop threshold (in dB below peak) used to bound the seabed footprint. |
| `max Phase off Zero deg.` | Sets the maximum allowed electrical phase offset from zero (degrees) for split-beam bottom detection. |
| `max Acceptable Phase Fit` | Sets the linear regression goodness-of-fit threshold for phase ramp detection across the beam footprint. |

## Visualizations

*   **Zoomed Image Window (`graphic_window[0]`):** High-resolution 2D echogram (power or phase) of the rubber-banded ping/sample sub-window.
*   **Matched-Filtered Envelope & Trace I/Q Plots:** Vertical profiles of the current ping's dB envelope and complex $(I, Q)$ samples with bottom-pick markers.
*   **Fore–Aft & Port–Starboard Phase Plots:** Vertical profiles of split-beam electrical phase angles and fitted zero-crossing ramps.
*   **Vertical Profile of Motion Parameters (`graphic_window[4]`):** Along-track profile of Roll, Pitch, Heave, Heading, Peak TS, or Radial Phase across the zoomed ping window.
