---
layout: default
title: EK_FFT (Module within EKlook)
parent: EKlook Tools
nav_order: 5
tool_name: EK_FFT
source_path: code/EKlook/EK_FFT.c
category: EKlook
input_formats:
  - In-Memory Complex Matched-Filtered Trace (.MF_IQ)
  - Pulse Replica (.pulse)
  - Sphere TS Reference (.dat)
output_formats:
  - Interactive Spectral Plots
related_tools:
  - EKlook
  - ek_fft_funcs
  - EK_Polar
---

# EK_FFT (Module within EKlook)

## Description
`EK_FFT` (`code/EKlook/EK_FFT.c`) is an interactive GUI module within the [`EKlook`](EKlook.md) application. It manages the **"FFT EK-Trace Window,"** enabling users to perform windowed Fast Fourier Transform (FFT) spectral analysis on selected segments of complex matched-filtered EK80 traces (`.MF_IQ`), inspect the transmit pulse replica and its autocorrelation spectrum, remove pulse-compression spectral ripple, and compare observed target spectra against theoretical tungsten-carbide calibration sphere curves (`-sphereTS`).

## Interactive Controls

| Control | Description | Related Variable |
|---|---|---|
| **Buttons** | | |
| `Test Signal` | Toggles generation and analysis of a synthetic test signal for FFT verification. | `do_FFT_test_signal` |
| `Show Pulse` | Toggles between the current echo trace's FFT and the FFT of the matched filter replica (or its autocorrelation). | `show_Pulse`, `lookatAutoCorrel` |
| `Remove Ripple` | Toggles removal of matched-filter autocorrelation spectral ripple. | `RemoveRipple` |
| `Limit Window` | Limits the FFT window to `[mBefore, mAfter]` meters around the detected target peak. | `LimitWindow` |
| **Sliders** | | |
| `FFT (power of 2)` | Sets the power-of-2 FFT window length ($2^8, 2^9, \dots$). | `FFTwin.FFT_power2` |
| `FFT cosine taper (perc)` | Sets the cosine taper percentage applied to the time-domain window before FFT. | `FFTwin.FFT_perc_taper` |
| `Bulk Calibration dB` | Adjusts the bulk calibration offset (in dB) applied to the spectrum. | `BulkCalibration` |
| `dB per kHz` | Sets a linear spectral slope correction (dB/kHz). | `dBperkHz` |
| `meters Before target` / `meters After target` | Defines the window boundaries (in meters) before and after the target when `LimitWindow` is active. | `mBefore`, `mAfter` |

## Visualizations

*   **Trace in Linear Amplitudes (I, Q, and Magnitude):** Displays the windowed complex time-domain waveform (or transmit replica).
*   **Raw FFT (before shifting window):** Displays the unshifted complex FFT magnitude spectrum.
*   **Shifted FFT Log Spectra:** Displays the unwrapped logarithmic power spectrum (in dB vs. kHz), with optional ripple removal and theoretical sphere TS overlay.
*   **Calibration Difference Plot:** Displays the residual spectral difference (in dB vs. frequency) between the measured sphere echo and the theoretical sphere TS model.
