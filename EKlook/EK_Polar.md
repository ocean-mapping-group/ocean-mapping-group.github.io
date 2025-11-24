---
layout: default
title: EK_Polar (Module within EKlook)
parent: EKlook Tools
nav_order: 6
---
# EK_Polar (Module within EKlook)

## Description
`EK_Polar` is a module within the `EKlook` interactive application. Its primary role is to manage the "POLAR EK-Trace window," a graphical user interface element designed for visualizing and analyzing EK echosounder data in a polar coordinate system. This module focuses on understanding target strength (TS) and angular phase relationships, enabling users to interactively adjust parameters for beam pattern modeling, view individual and aggregated target detections, and analyze the spectral roll-off with respect to radial phase angle.

## Interactive Controls

This module exposes the following interactive controls within the `EKlook` application:

| Control | Description | Related Variable |
|---|---|---|
| **Buttons** | | |
| `All Targets` | Toggles the display of all detected targets in the polar plot. | `showAll_Targets` |
| `Peak or LowPass` | Switches the amplitude detection method used for target identification (Peak detection or LowPass filtered peak detection). | `WhichTraceforAmplitudeDetect` |
| `Calc all Target FFTs` | Triggers a recalculation and stacking of FFTs for all valid targets. | |
| `Remove Ripple` | Toggles the application of a ripple removal correction during spectral analysis. | `RemoveRipple` |
| `Subtract Sphere` | Toggles the subtraction of a theoretical sphere model from the observed spectrum. | `RemoveSphere` |
| `Apply Calib` | Toggles the application of frequency-dependent calibration. | `ApplyFreqCalib` |
| `Dump Calib` | Dumps calibration values to a file (likely a text file for external use). | |
| **Sliders** | | |
| `Peak Plot dB Range` | Sets the dynamic range (in dB) for the peak TS plots. | `Peak_Plot_Range_dB` |
| `max beamwidth` | Defines the diameter (in degrees) of the polar plot. | `POLAR_diameter_degrees` |
| `BP Width Scaler` | A scaling factor applied to the beam width for beam pattern modeling. | `BeamWidthPhaseScaler` |
| `BP Peak Offset (dB)` | Adjusts the offset (in dB) for the beam pattern peak. | `BeamPatternPeak_dB` |
| `BP Cosine Power` | Controls the power of the cosine function used in beam pattern modeling. | `CosPower` |
| `Peak-FFT Offset dB` | An arbitrary offset (in dB) applied to the peak FFT values. | `PeakFFTOffsetdB` |

## Visualizations

The module displays various graphical representations within the `EKlook` application:
*   **Polar Plot (Bulls-eye Plot):** Shows detected targets plotted by Fore/Aft angle (vertical axis) versus Port/Starboard angle (horizontal axis), with colors often representing intensity. Concentric circles may represent increasing radial angle.
*   **Peak Target Strength vs Radial Angle:** Plots the peak target strength (dB) against the radial incidence angle, allowing for visualization of the beam pattern. The modeled beam pattern roll-off can be overlaid.
*   **Spectral Roll-Off Image:** A 2D image showing the FFT power spectrum's magnitude as a function of both frequency (Y-axis) and radial phase angle (X-axis).
*   **Cross-sections of Radial Drop-off by Frequency:** Detailed plots showing how the backscatter varies with radial phase angle for specific frequency slices.
*   **FFT Slice by Radial Phase Angle:** Displays the FFT spectrum for a chosen radial phase angle.
*   **Information Window:** Provides details about the number of valid targets, total traces, and current calibration/correction settings.

## Key Bindings (within the module's graphic windows)

*   `KEY_Z`: Zeros or resets a selected slider's value to a default (e.g., `Peak_Plot_Range_dB` to 20, `POLAR_diameter_degrees` to 10, `BeamWidthPhaseScaler` to 1, `BeamPatternPeak_dB` to 0, `CosPower` to 1, `PeakFFTOffsetdB` to 0).
*   `KEY_Q` / `KEY_ESC`: Closes the "POLAR EK-Trace window."
*   `KEY_UP` / `KEY_DOWN` (in spectral roll-off image): Changes the selected frequency slice for the cross-section plot.
*   `KEY_LEFT` / `KEY_RIGHT` (in spectral roll-off image): Changes the selected radial phase angle slice for the cross-section plot.

## How It Works
The `EK_Polar` module interactively processes EK echosounder data to analyze target strength and angular phase relationships. It applies various filters and corrections based on user input from buttons and sliders. The module then generates and updates polar plots, spectral roll-off images, and cross-sections to visualize how acoustic energy is distributed in a polar coordinate system. This is crucial for understanding the directional response of targets and the seafloor.

## Notes
The `EK_Polar` module is an integral part of the `EKlook` graphical user interface, focusing on interactive analysis of EK echosounder data. It does not accept any command-line arguments. Its functionality is accessed and controlled entirely through the `EKlook` GUI.