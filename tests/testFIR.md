---
layout: default
title: testFIR
parent: tests (Test, Simulation & Diagnostic Suite)
nav_order: 20
tool_name: testFIR
source_path: code/tests/testFIR.c
category: Chirp Waveforms, Matched Filtering & Signal Processing (tests)
input_formats:
  - Command-line synthetic heave wave (-sine), step offset (-step), and accelerometer bias (-bias) parameters
output_formats:
  - timedom.ascii (9-curve or 4-curve OMG ASCII time-domain plot file)
  - fft.ascii (OMG ASCII period-domain FFT amplitude spectrum plot file)
related_tools:
  - DelayEditor
  - mergeHeave
  - interpMRU
  - testChirp
---

# testFIR

## Overview
`testFIR` (`code/tests/testFIR.c`, authored by John Hughes Clarke in January 1997) is a vessel heave-compensation and digital filter simulator created to study **heave drift**, **accelerometer bias integration**, and the phase/transient response of **Finite Impulse Response (FIR)** vs. **FFT high-pass filters** in hydrographic motion reference units (MRUs / VRUs).

Over a 4,096-sample time series (`NOVALS = 4096`) at $\Delta t = 0.10\text{ s}$ ($409.6\text{ s}$ duration), `testFIR`:
1. Constructs a true vertical displacement profile `v_prof[i]` from a superposition of up to 10 cosine swell waves (`-sine <period_s> <amp_m>`) and up to 10 linear ramp/step offsets (`-step <metres_up> <over_n_secs> <start_sample>`).
2. Numerically differentiates `v_prof` twice to obtain vertical velocity `v_vel[i]` and vertical acceleration `v_accel[i]`.
3. Corrupts the acceleration by adding a constant sensor DC bias (`-bias`, `calc_v_accel[i] = bias + accel_scale * v_accel[i]`) and double-integrates back in time to produce a quadratically drifting vertical profile `calc_v_prof[i]`.
4. Applies two competing drift-removal algorithms:
   * **Causal Hanning-Weighted Linear Least-Squares FIR Filter (`do_FIR_filter`):** Slides a half-window of length `no_weights / 2` (default `512` samples = $51.2\text{ s}$), fits a Hanning-weighted linear trend to estimate the low-pass drift `low_pass[i]`, and extracts the high-pass heave `high_pass[i]`.
   * **Global Linear Detrend + FFT Brick-Wall High-Pass Filter (`four1`):** Detrends `calc_v_prof`, applies a 20-sample cosine taper at both ends, runs a forward 4,096-point FFT (`four1`), zeroes all spectral components with period $|T| > \text{fft\_cutoff\_period}$, and runs an inverse FFT (`four1(..., -1)`) to recover zero-phase `delay_heave[i]`.

---

## Syntax & CLI Options

```bash
testFIR [-v] [-accels] -sine <period_s> <amp_m> [-sine <p2> <a2> ...] \
        [-step <metres_up> <over_n_secs> <start_sample> ...] \
        [-bias <m/s2>] [-filtlen <N_weights>] [-fft_cutoff_period <s>] \
        [<dummy_inname> [<outname>]]
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-sine <T_s> <A_m>` | **At least one required.** Adds a cosine wave component of period $T_s$ (seconds) and amplitude $A_m$ (meters) to the true vertical profile `v_prof` (up to 10 components). | None |
| `-step <dz> <dur_s> <idx>` | Adds a ramp/step displacement of `<dz>` meters over `<dur_s>` seconds starting at sample index `<idx>` (up to 10 steps). Simulates a sudden squat, settlement, or datum jump. | `0` steps |
| `-bias <val>` | Constant DC accelerometer bias (in $\text{m/s}^2$) added to `v_accel` before double integration (`calc_v_accel[i] = bias + v_accel[i]`). Produces a parabolic $\frac{1}{2} b t^2$ heave drift. | `0.0` |
| `-filtlen <N>` | Total length `no_weights` of the Hanning weight array built by `build_weights()` (`do_FIR_filter` uses a causal window of `no_weights / 2` samples). | `1024` (`512`-sample window) |
| `-fft_cutoff_period <s>` | Cutoff period in seconds for the frequency-domain FFT high-pass filter; spectral bins with $|T| > \text{fft\_cutoff\_period}$ are zeroed before IFFT. | `10000.0` |
| `-accels` | Switch `timedom.ascii` output (`plot_flag = 1`) from the 9-curve filter comparison to the 4-curve kinematics view (`v_prof`, `v_vel`, `v_accel`, `calc_v_prof`). | `0` (9-curve mode) |
| `-v` | Print least-squares trend slope/intercept, taper width, and maximum spectral amplitude to `stdout`. | `0` |
| `<inname> <outname>` | Optional positional arguments; the second positional argument overrides the output time-domain filename (`timedom.ascii`). | `timedom.ascii` |

---

## Mathematical & Filtering Algorithms

### 1. Double Differentiation & Biased Double Integration
With sampling interval $\Delta t = 0.10\text{ s}$:

$$v[i] = \frac{z[i+1] - z[i]}{\Delta t}, \qquad a[i] = \frac{v[i+1] - v[i]}{\Delta t}$$

Adding accelerometer bias $b$ (`-bias`) and integrating twice via forward Euler recurrence from exact initial conditions ($\hat{v}[0] = v[0]$, $\hat{z}[0] = z[0]$):

$$\hat{a}[i] = a[i] + b, \qquad \hat{v}[i] = \hat{v}[i-1] + \hat{a}[i-1]\,\Delta t, \qquad \hat{z}[i] = \hat{z}[i-1] + \hat{v}[i-1]\,\Delta t$$

accumulates a quadratic vertical drift $\Delta\hat{z}(t) \approx \frac{1}{2} b t^2$.

### 2. Hanning-Weighted Causal Least-Squares FIR Filter (`do_FIR_filter`)
At each sample $i \ge M$ (where $M = \text{no\_weights}/2$), `do_FIR_filter()` fits a weighted straight line $y(k) = \alpha + \beta k$ over the trailing $M$ samples $k \in [0, M-1]$ using flat-topped Hanning weights $w_k$:

$$\beta = \frac{\sum w_k k \hat{z}_k - \frac{(\sum w_k k)(\sum w_k \hat{z}_k)}{\sum w_k}}{\sum w_k k^2 - \frac{(\sum w_k k)^2}{\sum w_k}}, \qquad \alpha = \frac{\sum w_k \hat{z}_k - \beta \sum w_k k}{\sum w_k}$$

Evaluating the fitted trend at the leading edge $k = M - 1$ gives the low-pass drift and high-pass heave:

$$z_{\text{low}}[i] = \alpha + (M - 1)\beta, \qquad z_{\text{high}}[i] = \hat{z}[i] - z_{\text{low}}[i]$$

---

## Output Files

1. **`timedom.ascii`** (or custom `<outname>`):
   * **Default 9-curve mode:** Writes `(time, v_prof, calc_v_prof, low_pass, high_pass, diff, delay_heave, v_prof - delay_heave, show_weight, calc_detrend)`.
   * **`-accels` 4-curve mode:** Writes `(time, v_prof, v_vel, v_accel, calc_v_prof)`.
2. **`fft.ascii`**: OMG ASCII plot file of `Period[i]` (seconds) vs. `Amplitude[i]` across all 4,095 non-DC FFT bins.

---

## Example Usage

```bash
# Simulate a 6 s swell (1.0 m) + 12 s swell (0.5 m), a 0.2 m step over 5 s at sample 1000,
# an accelerometer bias of 0.00005 m/s^2, and a 60 s FFT high-pass cutoff
testFIR -v -sine 6.0 1.0 -sine 12.0 0.5 -step 0.2 5 1000 -bias 0.00005 -fft_cutoff_period 60.0
```
For production heave drift filtering on multibeam `.merged` files, see [`DelayEditor`](../DE/DelayEditor.md) (`-heave_drift -avpings`).
