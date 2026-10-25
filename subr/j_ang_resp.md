---
layout: default
title: j_ang_resp
parent: Core Shared Libraries (subr)
module_name: j_ang_resp
source_path: code/subr/j_ang_resp.c
header_path: code/subr/j_ang_resp.h
category: Backscatter & Seafloor Classification
related_tools:
  - getBeamPattern
  - correctBS
  - weigh_grid
  - jview
---

# `j_ang_resp` — Acoustic Backscatter Angular Response & Sidescan Spectral Analysis Library

## Overview & Purpose in the OMG Architecture

`j_ang_resp` (`code/subr/j_ang_resp.c`, `code/subr/j_ang_resp.h`), written by John E. Hughes Clarke (February–September 1996), provides data structures, file I/O, curve-characterization algorithms, APL-UW Jackson model inversion, and 2D sidescan patch spectral analysis for **seafloor acoustic backscatter angular response (`AR`)** and **beam pattern (`BP`)** calibration.

In multibeam and sidescan seafloor characterization, the variation of backscatter strength with grazing/incidence angle ($0^\circ$ to $90^\circ$) carries distinct physical signatures of sediment impedance (nadir specular reflection), roughness (Kirchhoff / composite roughness regime), and critical-angle velocity ratio. `j_ang_resp` encapsulates stacked angular response records (`JEM_Angular_Response`), fits piecewise linear slopes and Jackson model geoacoustic parameters (`fit_jack_par`), detects inflection points (`find_inflexions`), manages empirical beam-pattern correction curves (`.bp`), and performs 2D Fast Fourier Transform (FFT) spectral slope analysis on 512 × 512 sidescan image patches (`Analyze_SSpatch`).

---

## Key Data Structures, Constants & Macros

### Constants
- `PORT_SIDE` (`-1`), `STBD_SIDE` (`1`), `BOTH_SIDE` (`0`), `WRAP_SIDE` (`2`): Side codes for `JEM_Angular_Response`.
- `BOTH_SIDES` (`0`), `PORT_ONLY` (`1`), `STBD_ONLY` (`2`): Side selection flags for `characterise_BS_curve()` and `find_inflexions()`.
- `AR_SIZE` (`1264`): Fixed byte size of a serialized `JEM_Angular_Response` record on disk.

### Core Structs (`code/subr/j_ang_resp.h`)

#### `JEM_Angular_Response`
Hold-all binary record (1264 bytes on disk) representing an along-track stacked angular response curve for one side of a swath:
- **Metadata & Timing**: `toolType`, `side`, `Start_Mode`, `End_Mode`, `no_pings`, `Start_Time`, `End_Time` (seconds since 1970), `time_interval`.
- **Geometry & Geographic Bounds**: `Start_azimuth`, `End_azimuth`, `transducer_depth`, `Start_inboard_depth`, `End_inboard_depth`, `Start_outboard_depth`, `End_outboard_depth`, and `Geo_Fix` (`lat`, `lon`) bounding corners (`Start_Outer`, `Start_Nadir`, `End_Outer`, `End_Nadir`).
- **Stacked Backscatter & Sidescan Arrays**: `attenuation_coeff`, `av_BSo`, `av_BSn`, `short av_BS[90]` (mean backscatter per $1^\circ$ bin in $0.01\text{ dB}$), `short sigma[90]` (standard deviation), `short av_ss[90]` (Lambertian-corrected sidescan), `unsigned short bcount[90]`, `sscount[90]`.
- **Sidescan Variability & Coefficients**: `changes_pixel`, `short ss_changes[10][10]`, and `float coeff[7]` (piecewise linear regression coefficients).

#### `GSparam` & `ARindex`
Sediment grain-size ground-truth record (`GSparam`) linking physical grab-sample statistics (`median`, `mean`, `sd`, `skew`, `kurtosis`, `percgrav`, `percsand`, `percsilt`, `percclay`, `nomodes`, `modephi[3]`, `phifreq[17]`) with up to 10 spatially proximate angular response records (`ARindex ar[10]`).

#### `SSpatch_Attribs` & `spect_stuff`
Structures for 2D sidescan texture and power-spectrum analysis on 512 × 512 patches:
- `unsigned char data[512][512]`, `FFT_PINGS`, `FFT_SAMPS`, `pixel`.
- `SS_Period[512]`, `SS_Amplitude[512][512]`, `AV_Amplitude[512]`: Log-transformed spatial frequencies and power spectra.
- `AV_ACROSS_intercept/slope/fit/profile[512]` & `AV_ALONG_intercept/slope/fit/profile[512]`: Linear regression detrending fits across and along track.
- `AV_Spectral_slope`, `AV_Spectral_intercept`, `AV_Spectral_fit`: Power-law spectral decay parameters.

---

## Public Functions & Signatures

### Angular Response Curve Characterization & Inversion
- `void characterise_BS_curve(float curve[180], float coeff[7], int kirk_incid, int crit_incid, int side_to_use)`
  Folds or selects port (`89..0`) and/or starboard (`90..179`) backscatter into a $0^\circ$–$89^\circ$ incidence profile and computes 7 characteristic coefficients:
  - `coeff[0]`: Mean nadir backscatter ($0^\circ$–$5^\circ$).
  - `coeff[1..2]`: Intercept and slope in the near-nadir Kirchhoff regime ($5^\circ$ to `kirk_incid`).
  - `coeff[3..4]`: Intercept and slope in the mid-angle plateau (`kirk_incid` to `crit_incid`).
  - `coeff[5..6]`: Intercept and slope beyond the critical angle (`crit_incid` to $75^\circ$).
- `void fit_jack_par(float nadir_bs, float middle_bs, float inner, float outer, double *params)`
  Estimates 7 APL-UW Jackson model parameters (`params[0..6]`: frequency, velocity ratio, density ratio, loss tangent, spectral strength, spectral exponent, volume parameter) from observed inner/outer inflection angles and nadir/mid-swath dB levels by iteratively calling `do_RG_simple_model()` (`rg_jack2.h`).
- `void find_inflexions(float curve[180], float *gradients, float *sec_deriv, int winsize, float *pick_P_low, float *pick_P_high, float *pick_S_low, float *pick_S_high, float *der2_picks, int side_to_use)`
  Computes sliding-window first and second derivatives (`get_delta_slopes`) of the angular response curve to automatically locate the inner (Kirchhoff-to-roughness transition) and outer (critical angle roll-off) inflection points on port and starboard sides.
- `void do_least_squares(float *x, float *y, int novals, float *intercept, float *slope, float *fit)`
  Computes ordinary linear least-squares regression ($y = \text{intercept} + \text{slope} \cdot x$) and correlation quality (`fit`), ignoring zero-valued entries.
- `void get_delta_slopes(float *x, float *y, int novals, int window, float *dydx)`
  Calculates local linear regression slopes over a moving window of width `window`.

### Beam Pattern & AR File I/O
- `int omg_read_AR(FILE *file, unsigned int rec_num, JEM_Angular_Response *side)` / `int omg_write_AR(FILE *file, unsigned int rec_num, JEM_Angular_Response *side)`
  Random-access binary reader and writer for `JEM_Angular_Response` records (`AR_SIZE = 1264` bytes), performing full endianness conversion via `swapio.h` (`get_swapped_*` / `put_swapped_*`).
- `void list_AR(JEM_Angular_Response *side)`
  Prints a human-readable summary of a `JEM_Angular_Response` record.
- `void print_BP_curve(char *name, float *bp)` / `void load_BP_curve(char *name, float *bp)`
  Saves and loads 180-element ($1^\circ$ increment, $-90^\circ$ to $+89^\circ$) ASCII beam pattern calibration tables (`.bp`).

### 2D Sidescan Patch Spectral Analysis
- `int Analyze_SSpatch(SSpatch_Attribs *pA)`
  Detrends radial traces in a `512 × 512` sidescan patch, applies a Hanning window, executes a 1D complex FFT (`four1`) along each ping, stacks the log-log power spectrum across all pings, and fits a least-squares spectral slope (`AV_Spectral_slope`, `AV_Spectral_intercept`, `AV_Spectral_fit`).

---

## How It Fits Into the OMG Architecture

`j_ang_resp` underpins backscatter normalization, beam-pattern extraction, and angular response analysis across `code/omg/` (`getBeamPattern`, `correctBS`, `weigh_grid`) and interactive inspection in `code/JV/` (`jview`). Its `do_least_squares()` routine is also widely called as a general-purpose linear regression utility by modules such as `j_SUB2K`.
