---
layout: default
title: ek_fft_funcs (Internal FFT Functions for EKlook)
parent: EKlook Tools
nav_order: 105
---
# ek_fft_funcs (Internal FFT Functions for EKlook)

## Description
`ek_fft_funcs.c` provides a suite of specialized internal functions for performing Fast Fourier Transform (FFT) analysis on EK series echosounder data within the `EKlook` application. These functions are designed to process complex-valued (I and Q) time-series data, calculate power spectra, handle frequency shifting, and apply various corrections (e.g., ripple removal, frequency-dependent attenuation). They are integral to the `EK_FFT` module, enabling interactive spectral visualization and analysis of echo envelopes and matched filter characteristics.

This module is not a standalone executable; its functions are called internally by other `EKlook` components, particularly those related to the "FFT EK-Trace window".

## Data Structures

### `jFFT_bundle` (Implicit from usage)
A structure (presumably defined in `EK_global.h` or `ek_fft_funcs.h`) that bundles together all data related to an FFT calculation, including:

| Field | Description |
|---|---|
| `win` | Input complex time-domain window data (`fcomplex`). |
| `spec` | Output complex frequency-domain spectrum data (`fcomplex`). |
| `win_mag` | Magnitude of the time-domain window. |
| `spec_mag` | Magnitude of the frequency-domain spectrum. |
| `spec_phase` | Phase of the frequency-domain spectrum. |
| `spec_power` | Power spectrum (logarithmic intensity). |
| `freq` | Original frequency bins. |
| `freq_shift` | Shifted frequency bins. |
| `spec_power_shift` | Shifted power spectrum. |
| `FFT_power2` | Power of 2 representing FFT size. |
| `nosamples` | Number of samples in the FFT. |
| `sampinterval` | Sampling interval. |
| `FFT_bandwidth` | Bandwidth of the FFT. |
| `FFT_perc_taper` | Percentage of tapering applied. |
| `FFT_centre_sample_no` | Center sample number for FFT window. |
| `FFT_shift` | Calculated frequency shift. |
| `FFT_bin_wrap` | Bin wrap value. |
| `range_to_centre_m` | Range to the center of the FFT window. |
| `atten_dBperkm` | Frequency-dependent attenuation. |
| `Fdep_atten_dB` | Total frequency-dependent attenuation. |
| `alloced` | Flag indicating memory allocation status. |
| `normalized` | Flag for normalization of the spectrum. |

## Functions

*   `void calc_ACMF_FFT()`: Calculates the FFT of the autocorrelation function of the matched filter (ACMF). Used to derive spectral characteristics of the sonar pulse's autocorrelation, handling window sizing and zero-padding.
*   `void detrend_ACMF_ripple()`: Attempts to remove ripple components from the spectrum of the autocorrelation function of the matched filter (ACMF) to correct for artifacts.
*   `void calc_MF_FFT()`: Calculates the FFT of the matched filter (MF) directly, padding it to the next power of two for efficient FFT.
*   `void detrend_MF_ripple()`: Attempts to remove ripple components from the spectrum of the matched filter (MF) to correct for artifacts.
*   `void calc_FFT_variables()`: Orchestrates the process of preparing time-domain data, calculating its FFT, and deriving various spectral properties for a given trace window. Sets up the FFT window, applies spherical spreading correction, and handles frequency-dependent attenuation.
*   `int get_jbun_mag_range(jFFT_bundle *jbun)`: Calculates magnitudes, phases, and power spectra from the results of an FFT stored in a `jFFT_bundle`. Populates `win_mag`, `spec_mag`, `spec_phase`, and `spec_power` fields.
*   `int do_jbun_fcomplex_four1(jFFT_bundle *jbun)`: A wrapper function that calls the `four1` (Numerical Recipes) FFT routine for complex data. Performs the core FFT computation.
*   `int shift_FFT_freqs(jFFT_bundle *jbun)`: Shifts and wraps the FFT frequency bins and their corresponding power spectrum for correct interpretation and display. Adjusts the frequency axis to be physically meaningful.
*   `int calc_FFT_shift(jFFT_bundle *jbun)`: Calculates the necessary frequency shift and bin wrap parameters for FFTs. Determines how the FFT output needs to be rearranged to align with the expected frequency range.
*   `int alloc_jFFT_bundle(jFFT_bundle *jfft, int size)`: Allocates memory for all arrays within a `jFFT_bundle` structure. Initializes the memory resources required.
*   `int free_jFFT_bundle(jFFT_bundle *jfft)`: Frees memory allocated for all arrays within a `jFFT_bundle` structure. Releases memory resources when they are no longer needed.

## How It Works
The `ek_fft_funcs` module provides the computational backbone for the interactive FFT analysis within `EKlook`. It manages the data structures (`jFFT_bundle`) to hold complex time-domain and frequency-domain data. The functions handle the entire FFT pipeline: preparing the input window, performing the FFT using optimized routines, shifting and wrapping frequencies for correct display, and calculating various spectral properties like magnitude, phase, and power. These internal functions are invoked by the `EK_FFT` module (or other `EKlook` components) in response to user interactions, enabling real-time spectral visualization and manipulation.

## Notes
This module is not a standalone executable; its functions are called internally by other `EKlook` components, particularly those related to the "FFT EK-Trace window". It leverages mathematical libraries (like Numerical Recipes' `four1`) for efficient FFT computations.
