---
layout: default
title: EK_ZoomImage (Module within EKlook)
parent: EKlook Tools
nav_order: 8
---
# EK_ZoomImage (Module within EKlook)

## Description
`EK_ZoomImage` is a module within the `EKlook` interactive application. Its primary role is to manage the "ZOOM EK-Trace window," a graphical user interface element that provides a detailed, zoomed-in view of selected EK echosounder traces. This module allows users to closely examine individual pings, their envelopes, and phase information. It enables interactive adjustment of bottom detection parameters, visualization of matched-filtered data, and analysis of various trace attributes.

## Interactive Controls

This module exposes the following interactive controls within the `EKlook` application:

| Control | Description |
|---|---|
| **Buttons** | |
| `full trace` | Resets the zoomed view to encompass the entire length of the current trace. |
| `Power or IQ` | Toggles the display mode in the time series plots between power (logarithmic intensity in dB) and I/Q (in-phase/quadrature) components of the trace. |
| `Power or Phase` | Toggles the display in the main zoom image window between a power image (backscatter intensity) and a phase image (showing phase trends). |
| `add TL` | Toggles the application of Transmission Loss (TL) corrections to the displayed power data. |
| `record on/off` | Toggles a recording mode, potentially for capturing interactive sessions or debug information. |
| `before/after MF` | Toggles the display of the trace envelope before or after the matched filtering process. |
| **Sliders** | |
| `dB drop (beam pattern roll off)` | Adjusts the signal drop-off (in dB) from the peak in the envelope, a key parameter for bottom detection algorithms. |
| `max Phase off Zero deg.` | Controls the maximum allowed phase offset from zero (in degrees) for a valid bottom phase detection. |
| `max Acceptable Phase Fit` | Sets the threshold for the goodness-of-fit statistic for phase detection, influencing the validity of phase-based bottom detects. |

## Visualizations

The module provides several integrated visualization panels within `EKlook`:

*   **Zoomed Image Window (`graphic_window[0]`):** A high-resolution image of the selected trace segment. This can display either the power (intensity) or the phase information, depending on the `Power or Phase` setting.
*   **Matched-Filtered Envelope Plot:** A time series plot showing the matched-filtered envelope of the trace (in dB), with various indicators for bottom detection.
*   **Trace I/Q Plot:** A time series plot displaying the in-phase (I) and quadrature (Q) components of the trace.
*   **Fore-Aft Phase Plot:** A time series plot showing the fore-aft phase trend, crucial for angle-of-arrival estimation.
*   **Port-Starboard Phase Plot:** A time series plot showing the port-starboard phase trend.
*   **Vertical Profile of Motion Parameters (`graphic_window[4]`):** A vertical plot displaying a selected motion parameter (Roll, Pitch, Heave, or Heading) over the range of traces currently visible in the zoomed image.

## Key Bindings (within the module's graphic windows)

*   `KEY_Z`: Zeros or resets a selected slider's value (e.g., `dB drop` to 10, `phaseOffZero` to 90, `maxAcceptablePhaseFit` to 0.1).
*   `KEY_Q` / `KEY_ESC`: Closes the "ZOOM EK-Trace window."
*   `KEY_UP` / `KEY_DOWN` (in zoomed image window): Scrolls through the traces, incrementing/decrementing the `currenttrace`.
*   `KEY_UP` / `KEY_DOWN` (in power plot window): Adjusts the `mindB` or `maxdB` display range.
*   `KEY_LEFT` / `KEY_RIGHT` (on sliders): Adjusts the selected slider's value.
*   `KEY_SPACE` (in zoomed image window): Toggles `showTrack` to display target locations or phase trends.
*   `KEY_SPACE` (in vertical profile of motion parameters): Cycles through the motion parameters (`WhattoShow`: Roll, Pitch, Heave, Heading, Peak TS, Radial Phase).
*   `+` / `-` (Keypad): Adjusts the display range of the vertical motion profile.
*   **Left Mouse Drag (Rubber Banding):** Defines a new zoom region within the main zoom image.
*   **Middle Mouse Click (in main zoom image):** Sets the `currenttrace` to the clicked trace.
*   **Middle Mouse Click (in power plot window):** Sets the `trimdB` (amplitude threshold for target detection) to the clicked value.

## How It Works
The `EK_ZoomImage` module provides a detailed, trace-level view of EK echosounder data. It processes individual echo traces, applying matched filtering and displaying the results as envelopes and I/Q components. User interactions via buttons and sliders allow for real-time adjustment of bottom detection parameters and visualization of various data attributes. The module updates its graphical outputs instantly, enabling users to fine-tune processing and inspect data quality closely.

## Notes
The `EK_ZoomImage` module is an integral part of the `EKlook` graphical user interface, focusing on interactive analysis and fine-tuning of EK echosounder data at the trace level. It does not accept any command-line arguments. Its functionality is accessed and controlled entirely through the `EKlook` GUI.