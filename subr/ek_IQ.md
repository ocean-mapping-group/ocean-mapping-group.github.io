---
layout: default
title: ek_IQ
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/ek_IQ.c
category: Broadband Echosounder & Split-Beam Signal Processing
related_tools:
- readEA600
- EKlook
module_name: ek_IQ
header_path: code/subr/ek_IQ.h
---

# ek_IQ: Complex I/Q Phasor Arithmetic, Chirp Synthesis & Fast FFT Convolution

## Overview & Purpose
`ek_IQ` (`ek_IQ.c` / `ek_IQ.h`, 469 lines) provides standalone complex In-Phase and Quadrature ($I/Q$) signal processing primitives for broadband scientific echosounders (Simrad EK80) and multibeam sonars (SM2000). Consolidated into `subr/` by John Hughes Clarke in November 2023 (and expanded in March 2025 with fast radix-2 FFT overlap-padding convolution), `ek_IQ` implements:

* Complex phasor magnitude, phase angle, cross-correlation, and inter-vector phase lag calculations.
* Linear Frequency Modulated (LFM) chirp synthesis (`make_chirp`) matching MATLAB's `chirp()` phase trajectory.
* Time-domain complex convolution (`cmplx_convolve`) and high-speed frequency-domain FFT convolution (`cmplx_fft_convolve`) with cached matched-filter spectra.
* Radiometric conversion from raw EK80 Wideband Transceiver (WBT) complex voltages to calibrated linear acoustic power (`calcEK80_volt2power`) and Frobenius norm calculation (`calc_array_norm_squared`).

---

## Key Data Structures & Global Variables

### Complex Phasor Structure (`fcomplex`)

```c
typedef struct {
    float I, Q;   /* In-phase (real) and Quadrature (imaginary) components */
} fcomplex;
```

### Fast FFT Convolution State Globals

```c
int       doFFTConv;        /* Flag to select cmplx_fft_convolve (1) vs time-domain cmplx_convolve (0) */
int       pulseFFTlen;      /* Cached sample length of the current matched-filter pulse */
int       traceFFTlen;      /* Cached sample length of the current raw trace */
int       padsams;          /* Next power-of-2 FFT buffer length >= (no_sams + pulsesams) */
fcomplex *padMFpulse;       /* Zero-padded time-domain matched-filter pulse buffer */
fcomplex *padrawtrace;      /* Zero-padded time-domain raw acoustic trace buffer */
fcomplex *padFFT_MFpulse;   /* Cached forward FFT spectrum of the matched-filter pulse */
```

---

## Public Functions & Signatures

### Complex Phasor & Cross-Correlation Primitives
* `float fc_get_amplitude(fcomplex vect)`
  Returns the Euclidean magnitude $\sqrt{I^2 + Q^2}$ using `hypot(vect.I, vect.Q)`.
* `float fc_get_phase(fcomplex vect)`
  Returns the phase angle in **degrees** ($-180^\circ \dots +180^\circ$) via `atan2(vect.Q, vect.I) * 180.0 / M_PI`.
* `void fc_get_cmplxXcorr(fcomplex A, fcomplex B, fcomplex *out, float *magnitude, float *phase_lag)`
  Computes the complex conjugate product $\text{out} = A \cdot B^* = (A_I B_I + A_Q B_Q) + j(A_Q B_I - A_I B_Q)$, storing its magnitude in `*magnitude` and phase angle (in degrees) in `*phase_lag`.
* `float angle_between_vectors(fcomplex A, fcomplex B)`
  Computes the wrapped phase angle difference $\Delta\phi = \text{atan2}(A_Q, A_I) - \text{atan2}(B_Q, B_I)$ in **radians** ($-\pi < \Delta\phi \le \pi$), used for split-beam Fore-Aft and Port-Starboard electrical angle determination.

### LFM Chirp Generation
* `int make_chirp(float *chirp, float *envelope, int no_samples, float samp_interval, float start_freq, float stop_freq, float pulse_level)`
  Synthesizes a linear frequency-modulated (LFM) chirp of `no_samples` samples at sampling interval `samp_interval` ($\Delta t$, in seconds) sweeping from `start_freq` ($f_0$) to `stop_freq` ($f_1$) over duration $T = N \Delta t$:
  $$\phi(t) = 2\pi \left( f_0 t + \frac{f_1 - f_0}{2 T} t^2 \right), \quad \text{chirp}[i] = \text{pulse\_level} \cdot \text{envelope}[i] \cdot \cos(\phi(t_i))$$

### Time-Domain & Fast FFT Complex Convolution
* `int cmplx_convolve(fcomplex *in_signal2, int pulsesams, fcomplex *in_signal1, int no_sams, fcomplex *out_signal)`
  Computes the direct $O(N \cdot M)$ time-domain complex discrete convolution of trace `in_signal1` (`no_sams`) with pulse filter `in_signal2` (`pulsesams`), writing `pulsesams + no_sams - 1` complex samples to `out_signal`.
* `int cmplx_fft_convolve(fcomplex *in_signal2, int pulsesams, fcomplex *in_signal1, int no_sams, fcomplex *out_signal)`
  Computes fast $O(N \log N)$ frequency-domain complex convolution:
  1. Finds the smallest power of two `padsams` $\ge \text{no\_sams} + \text{pulsesams}$.
  2. On the first call (or whenever `pulsesams` or `no_sams` changes), zero-pads `in_signal2`, computes its forward FFT via `four1((float *)padMFpulse - 1, padsams, 1)`, and caches the spectrum in `padFFT_MFpulse`.
  3. Zero-pads `in_signal1` into `padrawtrace` and computes its forward FFT via `four1()`.
  4. Performs point-wise complex multiplication of `padrawtrace` and `padFFT_MFpulse`.
  5. Computes the inverse FFT via `four1((float *)out_signal - 1, padsams, -1)` and normalizes by `1.0 / padsams` to produce results numerically identical to `cmplx_convolve`.

### Radiometric Power & Norm Calculations
* `float calcEK80_volt2power(int notraces, fcomplex voltIQ, float R_wbt_rx, float Ztrd)`
  Converts an average complex voltage phasor `voltIQ` across `notraces` split-beam quadrants into linear received power (Watts) given the WBT receiver impedance `R_wbt_rx` (typically $1000\,\Omega$) and transducer impedance `Ztrd` (typically $75\,\Omega$):
  $$P_{\text{lin}} = N_{\text{traces}} \left(\frac{|V_{IQ}|}{2\sqrt{2}}\right)^2 \left(\frac{|R_{\text{wbt}} + Z_{\text{trd}}|}{R_{\text{wbt}}}\right)^2 \frac{1}{Z_{\text{trd}}}$$
* `double calc_array_norm_squared(fcomplex *signal, int nosams)`
  Computes the squared Frobenius (Euclidean 2-norm) energy $\sum_{i=0}^{N-1} (I_i^2 + Q_i^2)$ of a matched-filter pulse array.

---

## How It Fits Into the OMG Architecture
`ek_IQ` is directly included by `ek80_parse_proc.h` and linked by `readEA600` (`code/knudsen/readEA600.c`) and `EKlook` (`code/EKlook/`). The addition of `cmplx_fft_convolve` in `ek_IQ` accelerates broadband EK80 matched-filter deconvolution by orders of magnitude on long water-column traces.
