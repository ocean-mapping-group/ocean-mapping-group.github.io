---
layout: default
title: testChirp
parent: Acoustic & Mathematical Test Harnesses (tests)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 19
tool_name: testChirp
source_path: code/tests/testChirp.c
category: Chirp Waveforms, Matched Filtering & Signal Processing (tests)
input_formats:
- Command-line pulse, sweep, Doppler, heave, noise, and harmonic parameters
output_formats:
- pulse.ascii (Transmit chirp waveform in OMG ASCII plot format)
- impulse.ascii (Synthetic 12-target seafloor reflection impulse series)
- autocorrel.plot (Chirp autocorrelation & optional Doppler cross-correlation)
- chirp.plot (5-curve summary: chirp, autocorrelation, ref_coeff, convolved echo, deconvolved/compressed output)
- fft.plot (Power/amplitude spectrum or multi-harmonic dB spectrum)
- doppler.plot (Optional Doppler-shifted waveform comparison)
- heave.plot (Optional vessel heave cycle & vertical velocity profile)
- noise.plot (Optional additive white noise time series)
related_tools:
- testNormConv
- testFIR
- example
- EKlook
---

# testChirp

## Overview
`testChirp` (`code/tests/testChirp.c`, authored by John Hughes Clarke in December 2000 and expanded through November 2025) is a comprehensive acoustic waveform, pulse-compression (matched filtering), Doppler shift, and spectral harmonic simulator used for both research and OMG acoustic signal-processing coursework.

Given a pulse duration (`-pulse_length` or `-pulse_length_ms`) and frequency sweep (`-start_freq_kHz` / `-stop_freq_kHz` or `-cen_freq_kHz` / `-bandwidth_kHz`), `testChirp`:
1. Synthesizes a Continuous Wave (CW, when $f_{\text{start}} = f_{\text{stop}}$) or Linear Frequency Modulated (LFM chirp) pulse tapered by a configurable cosine/Hanning envelope (`-perc_tapered`) and optional high-frequency sweep attenuation ramp (`-pulse_atten`).
2. Optionally simulates vessel heave motion (`-heave_period`, `-heave_amplitude`, `-want_phase`) and platform transmit/receive vertical velocities (`-velocity_tx`, `-velocity_rc`), stretching or compressing the received waveform via time-domain linear interpolation (`get_chirp_at`) to model **Range-Doppler coupling** and matched-filter loss.
3. Convolves the transmit pulse with a synthetic 12-spike seafloor reflection coefficient series (`ref_coeff`, consisting of four groups of 3 positive/negative targets spaced at $0.5\text{ ms}$, $0.25\text{ ms}$, $0.125\text{ ms}$, and $0.0625\text{ ms}$), optionally adds uniform white noise (`-noise_level`), and performs matched-filter pulse compression (`do_convolve`) to demonstrate range resolution $\Delta R = \frac{c}{2B}$.
4. Computes the radix-2 Fast Fourier Transform (`four1`) of the transmitted (and Doppler-shifted) pulse, with a November 2025 mode (`-doharmonics`) that models 1st, 2nd, and 3rd nonlinear acoustic harmonics for CW vs. FM pulses.

---

## Syntax & CLI Options

```bash
testChirp [-v] (-pulse_length <s_val> | -pulse_length_ms <ms_val>) \
          [-start_freq <Hz> -stop_freq <Hz> | -start_freq_kHz <kHz> -stop_freq_kHz <kHz> | \
           -cen_freq_kHz <kHz> -bandwidth_kHz <kHz>] \
          [-perc_tapered <0..50>] [-pulse_level <amp>] [-pulse_atten <val>] \
          [-velocity_tx <m/s>] [-velocity_rc <m/s>] \
          [-heave_period <s> -heave_amplitude <m> [-want_phase <deg>]] \
          [-noise_level <amp>] [-just_make_pulse] [-add_edges] \
          [-doharmonics [-harm_log_drop <dB>] [-minharmdB <dB>]] \
          [-duration <s> | -duration_ms <ms>] [-samp_interval <s>] \
          [-fftplotrange <min_Hz> <max_Hz> | -fftplotbw <Hz>] [-plotsize <dx_cm> <dy_cm>]
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-pulse_length <s>` | **Required** (or `-pulse_length_ms`). Transmit pulse duration $T_p$ in seconds. | None |
| `-pulse_length_ms <ms>` | Transmit pulse duration $T_p$ in milliseconds (divided by `1000.0`). | None |
| `-start_freq <Hz>` / `-start_freq_kHz <kHz>` | Starting instantaneous frequency $f_0$ of the LFM sweep. | `100000.0 Hz` (`100 kHz`) |
| `-stop_freq <Hz>` / `-stop_freq_kHz <kHz>` | Ending instantaneous frequency $f_1$ of the LFM sweep. | `10000.0 Hz` (`10 kHz`) |
| `-cen_freq_kHz <kHz>` | Center frequency $f_c$ in kHz; sets $f_0 = f_c - B/2$ and $f_1 = f_c + B/2$. | `0` |
| `-bandwidth_kHz <kHz>` | Sweep bandwidth $B$ in kHz (used with `-cen_freq_kHz`). | `0` |
| `-perc_tapered <pct>` | Percentage of pulse length tapered with a raised-cosine (Hanning) window at each end (`0.0` to `50.0`). | `16.6667%` ($1/6$th) |
| `-pulse_level <amp>` | Peak amplitude multiplier of the transmitted pulse. | `1.0` |
| `-pulse_atten <val>` | High-frequency sweep amplitude roll-off across the pulse (`< 1.0` applies a linear ramp; `>= 1.0` applies a non-linear cosine roll-off). | `0.0` (Flat) |
| `-velocity_tx <m/s>` | Downward vertical velocity of the transducer at transmission ($+\text{ve}$ towards target). Enables Doppler calculation (`calc_doppler++`). | `0.0` |
| `-velocity_rc <m/s>` | Downward vertical velocity of the transducer at reception. Enables Doppler calculation. | `0.0` |
| `-heave_period <s>` | Vessel sinusoidal heave period in seconds (generates `heave.plot` when paired with `-heave_amplitude`). | `0.0` |
| `-heave_amplitude <m>` | Vessel heave amplitude in meters. | `1.0` |
| `-want_phase <deg>` | Phase angle (degrees, $0^\circ\text{–}360^\circ$) within the heave cycle at which the ping occurs; scales `velocity_diff *= sin(want_phase * pi / 180)`. | `0.0` |
| `-noise_level <amp>` | Peak uniform white noise amplitude added to the convolved echo series `sig_conv` (writes `noise.plot`). | `0.0` (Disabled) |
| `-just_make_pulse` | Exit immediately after writing `pulse.ascii` and `impulse.ascii` (skipping convolutions and FFT). | `0` |
| `-add_edges` | Pad `pulse.ascii` before and after the active pulse using `extra_fraction = ((duration/pulse_length) - 1.0) / 2.0`. | `0` |
| `-doharmonics` | Model primary, 1st ($2f$), 2nd ($3f$), and 3rd ($4f$) spectral harmonics in dB in `fft.plot` (automatically ensures FFT length $\ge 2048$). | `0` |
| `-harm_log_drop <dB>` | Decibel drop per harmonic order in `-doharmonics` mode. | `-10.0 dB` |
| `-minharmdB <dB>` | Floor dB clipping level in `-doharmonics` mode. | `-50.0 dB` |
| `-duration <s>` / `-duration_ms <ms>` | Total window duration used to compute `extra_fraction` when `-add_edges` is active. | `0.0` |
| `-samp_interval <s>` | Discrete sampling interval $\Delta t$ in seconds. If omitted, defaults to $0.1 / f_{\max}$ ($10\times$ highest frequency). | $0.1 / f_{\max}$ |
| `-fftplotrange <fmin> <fmax>` | Explicit frequency axis bounds (Hz) for `fft.plot`. | $[0.8 f_c, 1.2 f_c]$ |
| `-fftplotbw <Hz>` | Frequency axis bandwidth around $f_c$ for `fft.plot` ($[f_c - B_{\text{plot}}/2, f_c + B_{\text{plot}}/2]$). | `0` |
| `-plotsize <dx> <dy>` | Plot width and height in cm written to `pulse.ascii` and `fft.plot` headers. | `20.0 10.0` |
| `-v` | Enable verbose mode (`verbose_flag++`). | `0` |

---

## Mathematical & Signal Processing Formulation

### 1. Instantaneous Phase & Tapered LFM Synthesis
For sample index $i \in [\text{first\_sample}, \text{last\_sample}]$ within a pulse of width $N_p = T_p / \Delta t$ samples, the normalized position $w_1 = (i - \text{first\_sample}) / N_p \in [0, 1]$ and $w_2 = 1 - w_1$ define the linear instantaneous frequency and cumulative phase:

$$f_{\text{inst}}(w_1) = w_2\, f_{\text{start}} + w_1\, f_{\text{stop}}, \qquad \phi_i = \phi_{i-1} + 2\pi\,\Delta t\, f_{\text{inst}}(w_1)$$

$$s_{\text{chirp}}[i] = A(w_1)\, W_{\text{Hanning}}[i]\, \cos(\phi_i)$$

### 2. Doppler Time-Scaling (`calc_doppler`)
Given combined vertical velocity $\Delta v = (v_{\text{tx}} + v_{\text{rx}}) \sin(\theta_{\text{phase}})$ and sound speed $c = 1500\text{ m/s}$, the received echo time axis is scaled by the Doppler factor:

$$t' = t \cdot \left(\frac{c - \Delta v}{c}\right)$$

and resampled via linear interpolation (`get_chirp_at(start_time + t')`) before cross-correlating against the unshifted replica `chirp` (`Dopp_Autocorrel`).

### 3. Multi-Target Impulse Response & Matched Filtering
`testChirp` populates `ref_coeff` with four triplets of point reflectors to test range resolution:
* **$1.0\text{ ms}$, $1.5\text{ ms}$, $2.0\text{ ms}$ ($0.5\text{ ms}$ / $0.375\text{ m}$ spacing):** amplitude $+1.0$
* **$3.0\text{ ms}$, $3.25\text{ ms}$, $3.5\text{ ms}$ ($0.25\text{ ms}$ / $0.1875\text{ m}$ spacing):** amplitude $-0.7$
* **$4.0\text{ ms}$, $4.125\text{ ms}$, $4.25\text{ ms}$ ($0.125\text{ ms}$ / $0.0938\text{ m}$ spacing):** amplitude $+0.5$
* **$5.0\text{ ms}$, $5.0625\text{ ms}$, $5.125\text{ ms}$ ($0.0625\text{ ms}$ / $0.0469\text{ m}$ spacing):** amplitude $-0.5$

It convolves `chirp` with `ref_coeff` to form the raw echo `sig_conv`, adds optional white noise `noise_ts`, and correlates `sig_conv` with `chirp` to produce the pulse-compressed matched-filter output `deconvol`.

---

## Output Files Generated

| Filename | Description |
| :--- | :--- |
| `pulse.ascii` | OMG ASCII plot file of the transmitted chirp pulse $s_{\text{chirp}}(t)$ (time in $\mu\text{s}$). |
| `impulse.ascii` | Two-column ASCII file (`time_us ref_coeff`) of the 12-spike target impulse series. |
| `autocorrel.plot` | OMG plot file of the chirp autocorrelation (`Autocorrel`) and optional `Dopp_Autocorrel`. |
| `chirp.plot` | 5-curve OMG plot file containing: (1) `chirp`, (2) `Autocorrel`, (3) `ref_coeff`, (4) `sig_conv`, and (5) `deconvol`. |
| `fft.plot` | OMG plot file of the FFT amplitude spectrum (`Freq` vs. `Spectra`), or 4-harmonic dB spectrum when `-doharmonics` is set. |
| `doppler.plot` | Generated when `-velocity_tx` or `-velocity_rc` is used; compares `chirp` and `doppler_chirp`. |
| `heave.plot` | Generated when `-heave_period` and `-heave_amplitude` are used; plots one full heave cycle and marks `-want_phase`. |
| `noise.plot` | Generated when `-noise_level` is used; plots the uniform random noise series `noise_ts`. |

---

## Example Usage

```bash
# 1. Simulate a 2 ms, 50-100 kHz LFM chirp with Doppler heave velocity and noise
testChirp -pulse_length_ms 2.0 -start_freq_kHz 50 -stop_freq_kHz 100 \
          -velocity_tx 1.2 -velocity_rc 1.2 -want_phase 90 -noise_level 0.2

# 2. Simulate a 0.5 ms, 70 kHz FM chirp with 20 kHz bandwidth and plot harmonics
testChirp -pulse_length_ms 0.5 -cen_freq_kHz 70 -bandwidth_kHz 20 \
          -doharmonics -harm_log_drop -12 -minharmdB -60 -fftplotrange 0 350000
```
