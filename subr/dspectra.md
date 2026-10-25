---
layout: default
title: dspectra
parent: Core Shared Libraries (subr)
module_name: dspectra
source_path: code/subr/dspectra.c
header_path: code/subr/dspectra.h
category: 2D Spectral Analysis & Image Processing
related_tools:
  - fft2dimage
  - jview
---

# dspectra: 2D Fast Fourier Transform (FFT) DTM Bedform Wavelength & Azimuth Analysis

## Overview & Purpose
`dspectra` (`dspectra.c` / `dspectra.h`, 1,251 lines) is a 2D spatial frequency-domain processing library authored by Danar G. Pratomo in October 2012 for analyzing submarine sand waves, ripples, and periodic bedforms in Digital Terrain Models (DTMs). Given a square power-of-two ($N \times N$) bathymetric grid patch, `dspectra` provides the complete signal conditioning and 2D spectral analysis pipeline:

1. **Mean Removal & Detrending:** Strips mean depth (`d_remove_patch_average`) or regional planar/quadratic seafloor tilt (`d_detrend_patch` via `dmatrix`).
2. **Radial Edge Tapering:** Applies a radially symmetric cosine/sine taper window (`d_taper_patch`) to suppress spectral leakage from patch boundaries.
3. **2D Forward & Inverse FFT:** Wraps the Numerical Recipes multidimensional FFT (`fourn` from `four1.c`) to compute 2D complex spectra, centered amplitude/power spectra (`d_fft_shift`, `d_spectral_dB`), phase spectra (`d_fft_phase`), and spatial reconstructions (`d_fft_inverse`).
4. **Directional & Wavenumber Filtering:** Supports bandpass/lowpass/highpass radial wavenumber filtering (`d_patch_filter`, `d_patchfilter`) and directional wedge filtering (`d_azimuthfilter`).
5. **Automated Bedform Crest Extraction:** Identifies dominant spectral peaks (`d_get_patch_maxima_lamda_azimuth`, `d_getmax`) to extract bedform wavelength ($\lambda$, in meters) and crest orientation azimuth (degrees), and extracts 1D directional profiles (`get_azi_profile`).

---

## Key Constants & Data Structures

### Spectral Peak & Cluster Structures (`d_wave_cluster`, `d_spectra_analysis`)
```c
#define MAX_CLUSTERS  10
#define MAX_FFT_WIDTH 1024

typedef struct {
    int   peak_x, peak_y;        /* 2D FFT grid coordinates of the spectral peak */
    float peak_frequency;        /* Spatial frequency (cycles per meter) */
    float peak_wavelength_m;     /* Dominant bedform wavelength (meters) */
    float peak_azimuth_deg;      /* Dominant propagation azimuth (degrees, 0..360) */
    float peak_amplitude;        /* Spectral peak magnitude */
    float wavelength_variance;   /* Cluster variance in wavelength */
    float azimuth_variance;      /* Cluster variance in azimuth */
} d_wave_cluster;

typedef struct {
    int            no_clusters;
    d_wave_cluster cluster[MAX_CLUSTERS];
} d_spectra_analysis;
```

### 1D Azimuthal Slice Structure (`custom_slices`)
```c
typedef struct {
    float dtm_peak_azi[MAX_FFT_WIDTH]; /* DTM profile along dominant peak azimuth */
    float dtm_user_azi[MAX_FFT_WIDTH]; /* DTM profile along user-selected azimuth */
    float fft_peak_azi[MAX_FFT_WIDTH]; /* FFT spectrum profile along peak azimuth */
    float fft_user_azi[MAX_FFT_WIDTH]; /* FFT spectrum profile along user azimuth */
    float wavelength[MAX_FFT_WIDTH];   /* Wavelength axis for slice */
    float frequency[MAX_FFT_WIDTH];    /* Spatial frequency axis for slice */
    float step_size;                   /* Spatial step size along slice (meters) */
    int   dimension;                   /* Number of samples in slice */
} custom_slices;

extern custom_slices slice;
```

---

## Public Functions & Signatures

### Spatial Pre-Conditioning (Detrending & Windowing)
* `int d_remove_patch_average(int rows, int cols, float *indata, float *outdata)`
  Computes the mean of all non-zero pixels in `indata` and subtracts it to produce a zero-mean patch in `outdata`.
* `int d_detrend_patch(int rows, int cols, float *indata, float *detrend_data, float *residual_data, int trendtype)`
  Promotes `indata` to double precision and calls `dTrend` (`trendtype == 1`, planar) or `dTrendPoly` (`trendtype == 2`, quadratic dome/trough) from `dmatrix.c`, outputting the detrended bathymetry in `detrend_data` and the fitted regional trend surface in `residual_data`.
* `int d_taper_patch(int rows, int cols, float frac_OK, float *indata, float *outdata)`
  Applies a circular window of radius `rows / 2`: pixels within normalized radius $r < \text{frac\_OK}$ retain weight `1.0`, pixels in $\text{frac\_OK} \le r < 1.0$ are smoothly tapered to zero with a half-sine roll-off, and corners outside $r \ge 1.0$ are zeroed.

### 2D FFT & Spectral Transformation Functions
* `int d_do_patch_spectra(int rows, int cols, float *indata, float *ampdata, float *phasedata, float *invdata, int doinverse)`
  Executes a 2D forward (`doinverse == 1`) or inverse (`doinverse == -1`) FFT via `fourn(indata - 1, nn, 2, doinverse)` and quadrants-shifts the normalized magnitude spectrum into `ampdata`.
* `int d_fft_forward(int rows, int cols, float *indata, float *outdata1, float *outdata2)`
  Interleaves real array `indata` into complex pairs (`d_spaced`), runs `fourn(..., 1)`, writes the 2D amplitude spectrum to `outdata1` (`d_fft_amplitude`), and preserves the raw complex spectrum in `outdata2` for frequency-domain filtering.
* `int d_fft_inverse(int rows, int cols, float *indata, float *outdata)`
  Executes inverse 2D FFT `fourn(indata - 1, nn, 2, -1)` and scales the real part by $1 / (\text{rows} \times \text{cols})$.
* `int d_fft_amplitude(...)`, `int d_fft_phase(...)`, `int d_fft_shift(...)`, `int d_spectral_dB(...)`
  Extracts magnitude, phase angle, DC-centered quadrant shift, and $20 \log_{10}$ decibel spectra.

### Spectral Filtering & Bedform Peak Picking
* `int d_patch_filter(...)` / `int d_patchfilter(int rows, int cols, float frac_filter, float *indata, float *outdata, int dofilt)`
  Applies radial frequency-domain lowpass or highpass masks.
* `int d_azimuthfilter(int rows, int cols, float azimuth, float frac_azi, float *indata, float *outdata)`
  Filters the 2D spectrum within an angular sector (`frac_azi`) around `azimuth` to isolate bedforms propagating in a specific direction.
* `int d_get_patch_maxima_lamda_azimuth(int rows, int cols, float wave_len, float size_pixel, float *amp_data, d_spectra_analysis *spec_anal)` & `int d_getmax(...)`
  Searches the upper half-plane of the shifted 2D amplitude spectrum `amp_data` for local maxima, converting peak wavenumber coordinates $(k_x, k_y)$ and grid cell size `size_pixel` into wavelength $\lambda$ (meters) and propagation azimuth (degrees).
* `int get_azi_profile(float *indata, float azimuth, int xdim, int ydim, float *theslice)` & `int calc_wavelength_or_period(custom_slices *slices)`
  Extracts a 1D cross-sectional slice through the DTM or 2D FFT along `azimuth`.

---

## How It Fits Into the OMG Architecture
`dspectra` powers the interactive 2D FFT analysis window in `jview` (`code/JV/JV_FFT2D.h`) and the command-line spectral tool `fft2dimage` (`code/image/fft2dimage.c`), allowing researchers to select a DTM sub-patch, inspect its 2D wavenumber spectrum, filter directional artifacts or sand waves, and automatically measure sand-wave wavelengths and migration directions.
