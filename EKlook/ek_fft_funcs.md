---
layout: default
title: ek_fft_funcs (Internal FFT Functions for EKlook)
parent: EKlook Tools
nav_order: 111
---
# ek_fft_funcs (Internal FFT Functions for EKlook)

## Description
`ek_fft_funcs.c` provides a suite of specialized internal functions for performing Fast Fourier Transform (FFT) analysis on EK series echosounder data within the `EKlook` application. These functions are designed to process complex-valued (I and Q) time-series data, calculate power spectra, handle frequency shifting, and apply various corrections (e.g., ripple removal, frequency-dependent attenuation). They are integral to the `EK_FFT` module, enabling interactive spectral visualization and analysis of echo envelopes and matched filter characteristics.

This module is not a standalone executable; its functions are called internally by other `EKlook` components, particularly those related to the "FFT EK-Trace window".

## Data Structures

### `jFFT_bundle` (Implicit from usage)
A structure (presumably defined in `EK_global.h` or `ek_fft_funcs.h`) that bundles together all data related to an FFT calculation, including:
*   `win`: Input complex time-domain window data (`fcomplex`).
*   `spec`: Output complex frequency-domain spectrum data (`fcomplex`).
*   `win_mag`: Magnitude of the time-domain window.
*   `spec_mag`: Magnitude of the frequency-domain spectrum.
*   `spec_phase`: Phase of the frequency-domain spectrum.
*   `spec_power`: Power spectrum (logarithmic intensity).
*   `freq`: Original frequency bins.
*   `freq_shift`: Shifted frequency bins.
*   `spec_power_shift`: Shifted power spectrum.
*   `FFT_power2`: Power of 2 representing FFT size.
*   `nosamples`: Number of samples in the FFT.
*   `sampinterval`: Sampling interval.
*   `FFT_bandwidth`: Bandwidth of the FFT.
*   `FFT_perc_taper`: Percentage of tapering applied.
*   `FFT_centre_sample_no`: Center sample number for FFT window.
*   `FFT_shift`: Calculated frequency shift.
*   `FFT_bin_wrap`: Bin wrap value.
*   `range_to_centre_m`: Range to the center of the FFT window.
*   `atten_dBperkm`: Frequency-dependent attenuation.
*   `Fdep_atten_dB`: Total frequency-dependent attenuation.
*   `alloced`: Flag indicating memory allocation status.
*   `normalized`: Flag for normalization of the spectrum.

## Functions

### `void calc_ACMF_FFT()`
Calculates the FFT of the autocorrelation function of the matched filter (ACMF).
*   **Purpose:** Used to derive spectral characteristics of the sonar pulse's autocorrelation, which is valuable for understanding system response and for ripple removal. It handles window sizing, zero-padding, or subsetting the ACMF to match the desired FFT window size.

### `void detrend_ACMF_ripple()`
Attempts to remove ripple components from the spectrum of the autocorrelation function of the matched filter (ACMF).
*   **Purpose:** By identifying and subtracting an average in-band spectral power from the ACMF spectrum, this function aims to correct for artifacts introduced by the pulse shape in subsequent spectral analyses.

### `void calc_MF_FFT()`
Calculates the FFT of the matched filter (MF) directly.
*   **Purpose:** Analyzes the spectral content of the actual matched filter pulse itself, which can be compared against echo spectra. It pads the MF to the next power of two for efficient FFT calculation.

### `void detrend_MF_ripple()`
Attempts to remove ripple components from the spectrum of the matched filter (MF).
*   **Purpose:** Similar to `detrend_ACMF_ripple()`, this function aims to correct for artifacts in the MF's spectrum by analyzing its average in-band power.

### `void calc_FFT_variables()`
Orchestrates the process of preparing time-domain data, calculating its FFT, and deriving various spectral properties for a given trace window.
*   **Purpose:** Sets up the FFT window (size, centering), applies spherical spreading correction (`TL_40logR`), and can inject a test signal. It then performs the FFT, calculates magnitudes, and applies frequency-dependent attenuation.

### `int get_jbun_mag_range(jFFT_bundle *jbun)`
Calculates magnitudes, phases, and power spectra from the results of an FFT stored in a `jFFT_bundle`.
*   **Purpose:** Populates `win_mag`, `spec_mag`, `spec_phase`, and `spec_power` fields within the `jFFT_bundle` and determines the frequency step (`Fstep`) and overall spectral range.

### `int do_jbun_fcomplex_four1(jFFT_bundle *jbun)`
A wrapper function that calls the `four1` (Numerical Recipes) FFT routine for complex data.
*   **Purpose:** Performs the core FFT computation on the complex time-domain data in `jbun->win`, storing the result in `jbun->spec`. Includes an option for normalization.

### `int shift_FFT_freqs(jFFT_bundle *jbun)`
Shifts and wraps the FFT frequency bins and their corresponding power spectrum for correct interpretation and display.
*   **Purpose:** Adjusts the frequency axis to be physically meaningful, typically centering the zero frequency and wrapping the negative frequencies.

### `int calc_FFT_shift(jFFT_bundle *jbun)`
Calculates the necessary frequency shift and bin wrap parameters for FFTs.
*   **Purpose:** Determines how the FFT output needs to be rearranged to align with the expected frequency range of the sonar pulse, considering the pulse's bandwidth and center frequency.

### `int alloc_jFFT_bundle(jFFT_bundle *jfft, int size)`
Allocates memory for all arrays within a `jFFT_bundle` structure.
*   **Purpose:** Initializes the memory resources required for storing time-domain data, frequency-domain results, and associated metadata for an FFT computation.

### `int free_jFFT_bundle(jFFT_bundle *jfft)`
Frees memory allocated for all arrays within a `jFFT_bundle` structure.
*   **Purpose:** Releases memory resources when they are no longer needed.
