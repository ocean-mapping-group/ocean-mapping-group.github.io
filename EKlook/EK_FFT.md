---
layout: default
title: EK_FFT (Module within EKlook)
parent: EKlook Tools
nav_order: 5
---
# EK_FFT (Module within EKlook)

## Description
`EK_FFT` is a module within the `EKlook` interactive application. Its primary role is to manage the "FFT EK-Trace window," a graphical user interface element that allows users to perform and visualize Fast Fourier Transform (FFT) analysis on selected sections of EK series echosounder traces. This module provides controls for adjusting FFT parameters, applying signal processing techniques like ripple removal, and comparing observed spectra against a theoretical sphere model. It helps in identifying and analyzing frequency-dependent characteristics of the backscatter within the `EKlook` application.

## Interactive Controls

This module exposes the following interactive controls within the `EKlook` application:

| Control | Description | Related Variable |
|---|---|---|
| **Buttons** | | |
| `Test Signal` | Toggles the generation and analysis of a test signal for FFT. | `do_FFT_test_signal` |
| `Show Pulse` | Toggles the display between the current trace's FFT and the FFT of the matched filter pulse (or its autocorrelation). | `show_Pulse`, `lookatAutoCorrel` |
| `Remove Ripple` | Toggles the application of a ripple removal correction to the spectrum. | `RemoveRipple` |
| `Limit Window` | Toggles whether the FFT window is limited to a specific range around the target. | `LimitWindow` |
| **Sliders** | | |
| `FFT (power of 2)` | Adjusts the power-of-2 size for the FFT (e.g., 2^8, 2^9, ..., up to 2^MAX_FFT_POW2). | `FFTwin.FFT_power2` |
| `FFT cosine taper (perc)` | Sets the percentage of cosine tapering applied to the FFT window. | `FFTwin.FFT_perc_taper` |
| `Bulk Calibration dB` | Adjusts a bulk calibration value (in dB) applied to the spectrum. | `BulkCalibration` |
| `dB per kHz` | Sets a slope value (dB per kHz) for spectral analysis, used in filtering or comparison. | `dBperkHz` |
| `meters Before target` | When `LimitWindow` is active, defines the window boundary in meters before the target. | `mBefore` |
| `meters After target` | When `LimitWindow` is active, defines the window boundary in meters after the target. | `mAfter` |

## Visualizations

The module displays various graphical representations within the `EKlook` application:
*   **Trace in Linear Amplitudes (I, Q, and Magnitude):** Displays the original signal (or matched filter/autocorrelation pulse) in its time-domain representation.
*   **Raw FFT (before shifting window):** Shows the raw frequency spectrum.
*   **Shifted FFT Log Spectra:** Displays the logarithmic power spectrum after frequency shifting, with options for ripple removal and comparison against a sphere model.
*   **Calibration Difference Plot:** If a sphere model is loaded, it shows the difference between the observed spectrum and the model, potentially with ripple and beam pattern removal applied.

## Key Bindings (within the module's graphic windows)

*   `KEY_Z`: Zeros or resets a selected slider's value (e.g., FFT power to 8, taper to 0).
*   `KEY_Q` / `KEY_ESC`: Closes the "FFT EK-Trace window."
*   `KEY_LEFT` / `KEY_RIGHT`: Adjusts slider values or, in specific contexts (like when `LimitWindow` is active or comparing with a sphere model), can shift frequency ranges or window limits.
*   `KEY_SPACE` (on "Show Pulse" button): Toggles between showing the matched filter's FFT and its autocorrelation's FFT.

## How It Works
The `EK_FFT` module processes the raw or matched-filtered echo trace data within a selected time window. It performs a Fast Fourier Transform (FFT) on this data, allowing users to view the spectral content. Interactive controls enable adjustments to FFT parameters (like window size and tapering), and the module can apply corrections such as ripple removal. The visualizations update dynamically to show the effect of these parameter changes, helping users analyze the frequency-dependent characteristics of the echosounder data.

## Notes
This module functions as a specialized analytical tool within the `EKlook` graphical user interface. It does not accept direct command-line arguments for its operation, as its sole purpose is to manage and respond to interactive input within the running `EKlook` application. Its behavior is entirely dependent on the user's actions within the GUI.