---
layout: default
title: JV_FFT2D (Module within jview)
parent: JV Tools
nav_order: 2
---
# JV_FFT2D (Module within jview)

## Description
`JV_FFT2D.c` implements an X-windows-based graphical user interface (GUI) and underlying logic for performing 2D Fast Fourier Transform (FFT) analysis on Digital Terrain Model (DTM) data. It allows users to visualize and manipulate DTMs and their spectral representations interactively within the `jview` application.

## Key Features and Functions

*   **GUI Management (`manage_FFT2D_widget_events`, `refresh_FFT2D_widget_window`, `make_FFT2D_widget`):**
    *   Handles user interactions (button clicks, key presses, mouse events) within the FFT2D Analysis Toolkit widget.
    *   Manages the state and display of various GUI elements, including buttons, sliders, and graphic windows.
    *   Configures FFT parameters through interactive sliders (e.g., taper width, maximum wavelength, window size based on powers of 2, filter thresholds, sun illumination angle).
    *   Provides toggle buttons for various processing steps and visualization modes: `deaverage`, `detrend`, `taper`, `spectral dB`, `phase view`, `low pass`, `high pass`, `band pass`, `azimuth filt`, `grey/col`, `sun ill`.
*   **DTM Extraction (`FFT2D_extract_DTM`):**
    *   Extracts a user-defined sub-section (patch) of a larger DTM for targeted FFT analysis.
*   **2D FFT Calculation and Processing (`calc_FFT2D`):**
    *   **Preprocessing:** Applies `d_detrend_patch` (linear trend removal), `d_taper_patch` (edge tapering), and `d_remove_patch_average` (mean subtraction) to the DTM patch.
    *   `calc_wavelength_or_period`: Derives wavelength and frequency information.
    *   `d_fft_forward`: Executes the 2D forward FFT.
    *   **Filtering:** Applies various filters in the frequency domain using `d_patchfilter` (low-pass, high-pass, band-pass) and `d_azimuthfilter` (azimuthal filtering).
    *   `d_fft_amplitude`: Computes the amplitude spectrum.
    *   `d_fft_phase`: Computes the phase spectrum.
    *   Converts amplitude to decibels (dB) if `FFT2D_dodB` is enabled.
    *   Optionally detrends (`FFT2D_dTrendAm`) and smooths (`FFT2D_smoothAm`) the amplitude spectrum.
    *   `d_get_patch_maxima_lamda_azimuth`: Identifies the principal peak in the amplitude spectrum.
    *   `d_fft_inverse`: Performs the 2D inverse FFT to reconstruct a filtered DTM.
    *   `J_Sun_illuminate`: Applies sun illumination shading.
*   **Visualization (`draw_FFT2D`, `draw_allFFT2D`, `to8bit_FFT2D`, `zoom_in_8bit`, `collapse_and_zoom_and_display_FFT_image`):**
    *   Renders various graphical outputs across multiple X-windows: original DTM, processed DTM, 2D FFT amplitude/phase spectrum, 1D periodograms, and slices of the DTM and FFT amplitude.
    *   `to8bit_FFT2D` and `zoom_in_8bit` handle the conversion of floating-point data to 8-bit color for display and apply zoom functionality.
*   **Utility Functions (`init_FFT2D_variables`, `minVal`, `maxVal`, `meanVal`, `movingAv`, `make_file_for_dtm`):**
    *   `init_FFT2D_variables`: Initializes all global parameters and flags for the FFT2D module.
    *   `minVal`, `maxVal`, `meanVal`: Basic statistical functions.
    *   `movingAv`: Computes a moving average.
    *   `make_file_for_dtm`: A debug function to write various DTM states to text files.

## How It Works
The `JV_FFT2D` module provides an interactive environment within `jview` for spectral analysis of DTM data. It takes a selected DTM patch, applies preprocessing steps like detrending and tapering, and then performs a 2D FFT. Various filters can be applied in the frequency domain. The results (amplitude and phase spectra) are visualized in real-time. The module allows users to interactively adjust parameters for both spatial and spectral processing, with visual feedback. It also includes functions to reconstruct filtered DTMs using inverse FFT and to apply sun illumination for enhanced visualization.

## Dependencies

*   `JV_global.h`: Provides global variables and definitions shared across the `jview` suite of applications.
*   `JV_FFT2D.h`: The specific header file for this module, containing structure definitions (e.g., `FFT2D_widget`, `FFT2D_spec_anal`) and function prototypes.
*   **Graphics and GUI (`jX_`, `jhc_` prefixed functions):** Functions for X-windows GUI management (e.g., `jX_is_win`, `jX_redraw_slider`, `jX_setup_widget`), drawing primitives (`jhc_text`, `jhc_line`, `jhc_shape`), and color management (`do_colormap`).
*   **Signal Processing (`d_` prefixed functions):** Core numerical routines for DTM processing and FFT (e.g., `d_detrend_patch`, `d_taper_patch`, `d_fft_forward`, `d_patchfilter`).
*   **Image Processing:** `packto8bit` for color conversion.
*   **Mathematical/Utility:** `calc_wavelength_or_period`, `J_Sun_illuminate`, `vectangle`, `get_azi_profile`.

## Notes
The `JV_FFT2D` module creates an interactive environment for in-depth spectral analysis of bathymetric or topographic data, allowing users to apply various processing steps and visualize their impact in both spatial and frequency domains. This is particularly useful for identifying dominant wavelengths, orientations, and other spatial patterns within gridded data.