# `JV_FFT2D.c` - 2D FFT Analysis Toolkit

This C file implements an X-windows-based graphical user interface (GUI) and underlying logic for performing 2D Fast Fourier Transform (FFT) analysis on Digital Terrain Model (DTM) data. It allows users to visualize and manipulate DTMs and their spectral representations interactively.

## Key Features and Functions

*   **GUI Management (`manage_FFT2D_widget_events`, `refresh_FFT2D_widget_window`, `make_FFT2D_widget`):**
    *   Handles user interactions (button clicks, key presses, mouse events) within the FFT2D Analysis Toolkit widget.
    *   Manages the state and display of various GUI elements, including buttons, sliders, and graphic windows.
    *   Configures FFT parameters through interactive sliders (e.g., taper width, maximum wavelength, window size based on powers of 2, filter thresholds, sun illumination angle).
    *   Provides toggle buttons for various processing steps and visualization modes:
        *   `deaverage`: Remove mean from DTM.
        *   `detrend`: Remove linear trends from DTM.
        *   `taper`: Apply tapering to DTM edges.
        *   `spectral dB`: Display spectrum in decibels.
        *   `phase view`: Show phase spectrum.
        *   `low pass`, `high pass`, `band pass`: Apply frequency domain filters.
        *   `azimuth filt`: Apply azimuthal filtering.
        *   `grey/col`: Toggle between grayscale and color display.
        *   `sun ill`: Apply sun illumination shading.
*   **DTM Extraction (`FFT2D_extract_DTM`):**
    *   Extracts a user-defined sub-section (patch) of a larger DTM for targeted FFT analysis.
*   **2D FFT Calculation and Processing (`calc_FFT2D`):**
    *   **Preprocessing:** Applies `d_detrend_patch` (linear trend removal), `d_taper_patch` (edge tapering), and `d_remove_patch_average` (mean subtraction) to the DTM patch.
    *   `calc_wavelength_or_period`: Derives wavelength and frequency information based on DTM pixel size.
    *   `d_fft_forward`: Executes the 2D forward FFT on the preprocessed DTM.
    *   **Filtering:** Applies various filters in the frequency domain using `d_patchfilter` (low-pass, high-pass, band-pass) and `d_azimuthfilter` (azimuthal filtering).
    *   `d_fft_amplitude`: Computes the amplitude spectrum from the FFT results.
    *   `d_fft_phase`: Computes the phase spectrum if `FFT2D_phase` is enabled.
    *   Converts amplitude to decibels (dB) if `FFT2D_dodB` is enabled.
    *   Optionally detrends the amplitude spectrum (`FFT2D_dTrendAm`) and smooths it (`FFT2D_smoothAm`).
    *   `d_get_patch_maxima_lamda_azimuth`: Identifies the principal peak in the amplitude spectrum to determine the dominant wavelength, amplitude, and azimuth.
    *   `d_fft_inverse`: Performs the 2D inverse FFT to reconstruct a filtered DTM for spatial domain visualization.
    *   `J_Sun_illuminate`: Applies sun illumination shading to DTMs for enhanced visual representation.
*   **Visualization (`draw_FFT2D`, `draw_allFFT2D`, `to8bit_FFT2D`, `zoom_in_8bit`, `collapse_and_zoom_and_display_FFT_image`):**
    *   Renders various graphical outputs across multiple X-windows, allowing side-by-side comparison:
        *   The original DTM patch.
        *   The processed DTM (detrended, tapered).
        *   The 2D FFT amplitude/phase spectrum, with features like zoom levels, dB conversion, and dominant peak indication.
        *   1D periodograms (spectral plots) showing average, user-defined azimuth, and default azimuth spectra, plottable by bin number, wavelength, or frequency.
        *   Slices of the DTM and FFT amplitude along specific azimuths.
    *   `to8bit_FFT2D` and `zoom_in_8bit` handle the conversion of floating-point data to 8-bit color for display and apply zoom functionality to the spectral images.
*   **Utility Functions (`init_FFT2D_variables`, `minVal`, `maxVal`, `meanVal`, `movingAv`, `make_file_for_dtm`):**
    *   `init_FFT2D_variables`: Initializes all global parameters and flags for the FFT2D module to their default states.
    *   `minVal`, `maxVal`, `meanVal`: Basic statistical functions to compute minimum, maximum, and mean values of 2D float arrays.
    *   `movingAv`: Computes a moving average over a 2D array (though its implementation appears to set all values to the overall mean).
    *   `make_file_for_dtm`: A debug function to write various DTM states (original, detrended/tapered, amplitude, dB spectrum, detrended spectrum) to text files for external analysis.

## Dependencies

This module relies on several internal libraries and header files within the project:

*   `JV_global.h`: Provides global variables and definitions shared across the `jview` (JV) suite of applications.
*   `JV_FFT2D.h`: The specific header file for this module, containing structure definitions (e.g., `FFT2D_widget`, `FFT2D_spec_anal`) and function prototypes.
*   **Graphics and GUI (`jX_`, `jhc_` prefixed functions):** Functions for X-windows GUI management (e.g., `jX_is_win`, `jX_redraw_slider`, `jX_setup_widget`), drawing primitives (`jhc_text`, `jhc_line`, `jhc_shape`), and color management (`do_colormap`).
*   **Signal Processing (`d_` prefixed functions):** Core numerical routines for DTM processing and FFT (e.g., `d_detrend_patch`, `d_taper_patch`, `d_fft_forward`, `d_patchfilter`).
*   **Image Processing:** `packto8bit` for color conversion.
*   **Mathematical/Utility:** `calc_wavelength_or_period`, `J_Sun_illuminate`, `vectangle`, `get_azi_profile`.

## Usage

The `JV_FFT2D.c` module creates an interactive environment for in-depth spectral analysis of bathymetric or topographic data, allowing users to apply various processing steps and visualize their impact in both spatial and frequency domains. This is particularly useful for identifying dominant wavelengths, orientations, and other spatial patterns within gridded data.