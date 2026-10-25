---
layout: default
title: four1
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/four1.c
category: Signal Processing, FFT & Spectral Analysis
related_tools:
- dspectra
- ek_IQ
- Echo_calib
- EKlook
- jview
- DelayEditor
module_name: four1
header_path: code/subr/four1.h
---

# `four1` — 1D and Multi-Dimensional Fast Fourier Transform (FFT) Routines

## Overview & Purpose
The `four1` module (`code/subr/four1.c` and `code/subr/four1.h`) provides in-place radix-2 Cooley-Tukey Fast Fourier Transform (FFT) routines adapted from *Numerical Recipes in C* (Press et al.). Originally integrated into the Ocean Mapping Group (`subr/`) codebase in the early 1990s for 1D spectral analysis (`four1`) and expanded in 2012 with the $N$-dimensional transform (`fourn`), it underpins frequency-domain matched filtering (pulse compression), power spectral density estimation, cross-spectral coherence analysis, and acoustic calibration across the OMG suite.

---

## Key Conventions & Macros (`four1.c`)

### 1-Based Indexing Convention
Both `four1` and `fourn` use the classic *Numerical Recipes* **1-based indexing convention** for complex interleaved `float` arrays:
- A complex series of $N$ points is stored in a `float` array of length $2N$ indexed from `data[1]` to `data[2*N]`, where odd indices (`data[1], data[3], ...`) hold real parts and even indices (`data[2], data[4], ...`) hold imaginary parts.
- Standard 0-based C callers pass a decremented pointer (`four1(complex_buf - 1, nn, isign)`).

### Helper Macro
- `#define SWAP(a,b) tempr=(a);(a)=(b);(b)=tempr`: Used during the in-place bit-reversal permutation stage to swap real and imaginary sample pairs.

---

## Public Functions & Signatures

### 1. One-Dimensional Radix-2 FFT

```c
void four1(float data[], int nn, int isign);
```
- **Purpose:** Replaces the 1-indexed interleaved complex array `data[1..2*nn]` by its discrete Fourier transform (when `isign == 1`) or by `nn` times its inverse discrete Fourier transform (when `isign == -1`).
- **Parameters:**
  - `data`: 1-based array of `2 * nn` single-precision floats containing `nn` interleaved complex samples $(\text{Re}_k, \text{Im}_k)$.
  - `nn`: Number of complex samples; **must** be an integer power of 2 ($2^m$).
  - `isign`: Transform direction (`+1` for forward FFT, `-1` for unnormalized inverse IFFT).
- **Algorithm:**
  1. **Bit-Reversal Permutation:** Iterates through indices $i = 1, 3, \dots, 2\text{nn}-1$ and maintains the bit-reversed index $j$, swapping complex pairs whenever $j > i$.
  2. **Danielson-Lanczos Butterfly Stages:** Repeatedly combines sub-transforms of length `mmax = 2, 4, 8, ..., nn` using double-precision trigonometric recurrences (`wtemp = sin(0.5 * theta)`, `wpr = -2.0 * wtemp * wtemp`, `wpi = sin(theta)`) to prevent cumulative floating-point phase drift across large transforms.
  3. **Inverse Scaling Note:** When `isign == -1`, the output is unnormalized and must be divided by `nn` by the caller to recover exact amplitudes.

### 2. Multi-Dimensional Radix-2 FFT

```c
void fourn(float data[], unsigned long nn[], int ndim, int isign);
```
- **Purpose:** Computes the in-place $N$-dimensional discrete Fourier transform (`isign == 1`) or unnormalized inverse transform (`isign == -1`) of a multi-dimensional complex array.
- **Parameters:**
  - `data`: 1-based interleaved complex `float` array of total length $2 \times \prod_{idim=1}^{ndim} \text{nn}[idim]$.
  - `nn`: 1-based array `nn[1..ndim]` specifying the complex dimension lengths along each axis (each dimension must be a power of 2).
  - `ndim`: Number of dimensions (e.g., `2` for 2D wavenumber/wavenumber-frequency transforms).
  - `isign`: Transform direction (`+1` forward, `-1` unnormalized inverse).
- **Algorithm:** Loops over each dimension `idim = ndim ... 1`, performing multi-dimensional stride-aware bit-reversal followed by Danielson-Lanczos butterfly stages along the stride `nprev` of the current axis.

---

## How It Fits Into the OMG Architecture
`four1` is the foundational FFT engine throughout the OMG signal-processing stack:
- **FM Chirp Pulse Compression (`ek_IQ`):** `matched_filter_one_trace()` in `code/subr/ek_IQ.c` calls `four1(..., 1)` on zero-padded complex basebanded transceiver traces and replica chirp pulses, multiplies by the complex conjugate in the frequency domain, and calls `four1(..., -1)` to recover compressed range profiles.
- **1D Spectral & Coherence Estimation (`dspectra`):** `code/subr/dspectra.c` calls `four1()` inside `spectrum()`, `cross_spectra()`, and `coherence()` to compute Welch-style windowed periodograms and transfer functions.
- **Acoustic Calibration & Split-Beam Diagnostics (`Echo_calib`, `EKlook`, `jview`, `DelayEditor`):** Used in `EK_FFT.c`, `ek_fft_funcs.c`, and `JV_play_WAV.c` for passband spectral inspection, Doppler shift analysis, and acoustic target frequency response characterization.
