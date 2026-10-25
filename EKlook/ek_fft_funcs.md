---
layout: default
title: ek_fft_funcs (Internal FFT Functions for EKlook)
parent: EKlook Tools
nav_order: 12
tool_name: ek_fft_funcs
source_path: code/EKlook/ek_fft_funcs.c
category: EKlook
input_formats:
  - In-Memory Complex IQ Windows (fcomplex)
output_formats:
  - Complex & Power Spectra (jFFT_bundle)
related_tools:
  - EK_FFT
  - EKlook
  - BatchProcEK
  - EK_funcs
---

# ek_fft_funcs (Internal FFT Functions for EKlook)

## Description
`ek_fft_funcs.c` (`code/EKlook/ek_fft_funcs.c`) provides the internal Fast Fourier Transform (FFT) signal-processing routines used by [`EK_FFT`](EK_FFT.md), [`EKlook`](EKlook.md), and [`BatchProcEK`](BatchProcEK.md). It operates on `jFFT_bundle` structures containing complex In-Phase/Quadrature (`fcomplex`) time-domain windows, applying cosine tapering, computing power-of-2 complex FFTs via `four1`, unwrapping/shifting baseband frequencies to physical acoustic frequencies, applying frequency-dependent seawater absorption corrections, and detrending matched-filter autocorrelation spectral ripple.

## Key Functions

*   `calc_ACMF_FFT()` & `detrend_ACMF_ripple()`: Computes the FFT of the autocorrelation function of the matched filter (ACMF) and removes passband spectral ripple.
*   `calc_MF_FFT()` & `detrend_MF_ripple()`: Computes the FFT of the matched filter replica directly and removes spectral ripple.
*   `calc_FFT_variables()`: Prepares the complex time-domain trace window, applies cosine tapering and spherical spreading / frequency-dependent absorption corrections, and executes the forward FFT.
*   `get_jbun_mag_range(jFFT_bundle *jbun)`: Computes magnitude (`spec_mag`), phase (`spec_phase`), and logarithmic power spectra (`spec_power`) from the complex FFT output.
*   `do_jbun_fcomplex_four1(jFFT_bundle *jbun)`: Wrapper around the complex Radix-2 `four1` FFT algorithm.
*   `calc_FFT_shift(jFFT_bundle *jbun)` & `shift_FFT_freqs(jFFT_bundle *jbun)`: Unwraps and shifts FFT frequency bins (`freq_shift`, `spec_power_shift`) to align with the physical transducer passband.
*   `alloc_jFFT_bundle()` & `free_jFFT_bundle()`: Memory management for `jFFT_bundle` arrays.
