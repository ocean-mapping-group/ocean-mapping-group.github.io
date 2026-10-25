---
layout: default
title: EK_Polar (Module within EKlook)
parent: EKlook Tools
nav_order: 6
tool_name: EK_Polar
source_path: code/EKlook/EK_Polar.c
category: EKlook
input_formats:
  - In-Memory Trace, Phase & Complex IQ Arrays
  - Sphere TS Reference (.dat)
output_formats:
  - Frequency Calibration File (.txt.r4)
related_tools:
  - EKlook
  - EK_FFT
  - comboCalibEK_ARCs
---

# EK_Polar (Module within EKlook)

## Description
`EK_Polar` (`code/EKlook/EK_Polar.c`) is an interactive GUI module within the [`EKlook`](EKlook.md) application. It manages the **"POLAR EK-Trace Window,"** which visualizes split-beam target detections in polar coordinates (Fore–Aft vs. Port–Starboard mechanical angles), models 2D transducer beam-pattern roll-off as a function of radial angle and frequency, and exports frequency-dependent calibration tables (`Dump Calib`) during tungsten-carbide calibration sphere deployments.

## Interactive Controls

| Control | Description | Related Variable |
|---|---|---|
| **Buttons** | | |
| `All Targets` | Toggles display of all ping target detections across the line in the polar bullseye plot. | `showAll_Targets` |
| `Peak or LowPass` | Switches target detection between raw peak and low-pass filtered envelope peak. | `WhichTraceforAmplitudeDetect` |
| `Calc all Target FFTs` | Computes and stacks windowed FFT spectra across all valid target detections. | |
| `Remove Ripple` | Toggles removal of matched-filter autocorrelation ripple during spectral analysis. | `RemoveRipple` |
| `Subtract Sphere` | Subtracts the theoretical sphere Target Strength curve (`-sphereTS`) from the observed target spectra. | `RemoveSphere` |
| `Apply Calib` | Applies the derived frequency-dependent calibration curve. | `ApplyFreqCalib` |
| `Dump Calib` | Writes the derived frequency-dependent calibration curve to disk for use in [`comboCalibEK_ARCs`](comboCalibEK_ARCs.md) `-calib`. | |
| **Sliders** | | |
| `Peak Plot dB Range` | Dynamic range (in dB) for the peak Target Strength plots. | `Peak_Plot_Range_dB` |
| `max beamwidth` | Angular diameter (in degrees) of the polar bullseye plot. | `POLAR_diameter_degrees` |
| `BP Width Scaler` | Scaling factor applied to the beam width in the beam-pattern model. | `BeamWidthPhaseScaler` |
| `BP Peak Offset (dB)` | Offset (in dB) applied to the modeled beam-pattern peak. | `BeamPatternPeak_dB` |
| `BP Cosine Power` | Exponent of the powered-cosine beam-pattern roll-off model. | `CosPower` |
| `Peak-FFT Offset dB` | Offset (in dB) between time-domain peak TS and spectral FFT values. | `PeakFFTOffsetdB` |

## Visualizations

*   **Polar Bullseye Plot:** Plots detected targets by Fore–Aft angle vs. Port–Starboard angle, color-coded by target strength.
*   **Peak Target Strength vs. Radial Angle:** Plots measured peak TS against off-axis radial angle overlaid with the powered-cosine beam-pattern model.
*   **Spectral Roll-Off Image:** 2D image of FFT power spectrum magnitude as a function of frequency (Y-axis) and off-axis radial phase angle (X-axis).
*   **Cross-Sections of Radial Drop-Off by Frequency & FFT Slice by Radial Angle:** 1D slices through the spectral roll-off matrix.
