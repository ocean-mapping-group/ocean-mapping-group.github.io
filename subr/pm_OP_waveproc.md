---
layout: default
title: pm_OP_waveproc
parent: Core Shared Libraries (subr)
module_name: pm_OP_waveproc
source_path: code/subr/pm_OP_waveproc.c
header_path: code/subr/pm_OP_waveproc.h
category: Acoustic & Bathymetric Processing
related_tools:
  - swathed (SE)
  - dumpWaveFormParams
  - processSHOALSdepths
  - make_Optech_prof
  - filterPPK
  - merge_PPK
---

# pm_OP_waveproc

## Overview & Purpose

`pm_OP_waveproc` (authored by Pim Kuus and Marketa, February 2006 – July 2008) implements airborne bathymetric LiDAR waveform processing, classification, water-column attenuation ($K$) extraction, and bottom reflectance characterization for Optech SHOALS (Scanning Hydrographic Operational Airborne Lidar Survey) waveforms. It processes all four SHOALS receiver channels—Photomultiplier Tube (`PMT`), Geiger-mode Avalanche Photodiode (`GAPD`), Infrared (`IR`), and `RAMAN`—to detect surface and seafloor returns, linearize log-compressed DN amplitudes, detrend exponential water-column volume backscatter, and recover weak/vegetated (algae/weed) bottom peaks.

## Key Data Structures, Constants & Macros

### Channel & Classification Constants
- Receiver Channel Types:
  - `PM_WAVE_PMT` (`0`): Deep green channel (Photomultiplier Tube).
  - `PM_WAVE_GAPD` (`1`): Shallow green channel (Avalanche Photodiode).
  - `PM_WAVE_IR` (`2`): Infrared water-surface channel.
  - `PM_WAVE_RAMAN` (`3`): Red Raman backscatter channel.
- Waveform Return Classifications:
  - `DEEP_WATER` (`4`): Extinction occurs before a bottom return is reached.
  - `WEAK` (`5`): Weak bottom return (e.g., submerged aquatic vegetation/kelp).
- `MAX_WAVEFORM_SAMPLES` (`500`): Maximum temporal bins per LiDAR waveform ($1\text{ ns}$ bins $\approx 0.115\text{ m}$ in water).
- SHOALS Decompression Polynomial Coefficients (`COEFF_A` through `COEFF_G`): 6th-order polynomial coefficients used by `uncompress_dn()` to linearize log-compressed receiver Digital Numbers (DNs).

### Core Struct (`pm_OP_wave`)
- `pm_OP_wave`: Encapsulates a single LiDAR waveform and its derived physical features:
  - **Traces & Derivatives**: `wave_type`, `valid` (`1` = passed 1st derivative check, `2` = passed 2nd residual check, `3` = passed 3rd height check, `9` = invalid), `no_samples`, raw `trace[500]`, 5-point moving average `smooth[500]`, 1st and 2nd derivatives (`d_trace`, `dd_trace`, `d_trace_smooth`, `dd_trace_smooth`), and 11-point decimated traces (`decimated`, `d_decimated`).
  - **Water Column & Attenuation ($K$)**: `water_surface`, `max_at_surface`, `start_of_watercolumn`, `end_of_watercolumn`,diffuse attenuation slope `float K`, `k_type` (`0` = exponential, `1` = linear), reference point `(s_Io, i_Io)` at 10 ns ($\approx 1.15\text{ m}$) below the surface peak.
  - **Surface & Bottom Peak Picks**: Intensities (`i_start_sur`, `i_start_bot`, `i_top_bot`, `i_end_bot`, `i_50_bot`, `i_50_sur`) and sample indices (`s_start_sur`, `s_start_bot`, `s_top_bot`, `s_end_bot`, `s_50_bot`, `s_50_sur`, `width_bot`, `bot_offset`).
  - **Pulse Shape & Reflectance Metrics**: `i_top_bot_k` (intensity on the extended $K$ decay line at the bottom peak), `i_top_bot_d` (depth-independent peak height above decay trend), `height_corrected`, linearized peak height `double height_lin`, derivatives (`d_start_bot`, `dd_start_bot`, `dd_top_bot`, `d_end_bot`), `seabed_rise_time`, `seabed_fall_time`, `seabed_rise_slope`, `seabed_fall_slope`, integrated pulse `area`, `height_of_seabed_above_trend`, `residual_to_log_fit_of_WC`.
  - **Deep/Weak Return Metrics**: Sinking point `(s_sink, i_sink)` ($5\sigma$ above tail noise), extinction point `(s_extinct, i_extinct)`, `return_type` (`DEEP_WATER` or `WEAK`), and `s_trailing_edge`.

## Public Functions & Signatures

- `int pm_Process_Wave(pm_OP_wave *A_Wave, int verbose)`
  - Top-level dispatcher validating `A_Wave->wave_type` (`PMT`, `GAPD`, `IR`, `RAMAN`) and invoking `get_bottom_char()`.
- `int get_bottom_char(pm_OP_wave *A_Wave, int verbose)`
  - Core waveform analysis pipeline:
    1. Computes smoothed trace (`window = 5`), 11-point decimated trace, and smoothed 1st/2nd derivatives.
    2. Locates the surface return peak (`s_start_sur`, `i_start_sur`) and 50% leading edge (`s_50_sur` for IR).
    3. Detects initial bottom onset (`s_start_bot` at 1st-derivative zero-crossing), peak (`s_top_bot`), and trailing edge (`s_end_bot`), computing rise/fall times, slopes, and area.
    4. Runs multi-stage quality control (`clean_results` runs 1, 2, and 3), attempting recovery of weak/vegetated returns via `improve_bot_peak()`, `get_K()`, and `detrend_wavefrom()`.
    5. Computes the 50% bottom leading edge (`s_50_bot`), depth-independent peak height `i_top_bot_d`, and linearized height `height_lin` via `uncompress_dn()`.
- `int classify_Wave(pm_OP_wave *A_Wave, int verbose)`
  - Estimates tail noise mean and standard deviation ($\sigma$), finds the sinking point `s_sink` ($5\sigma$ above noise), and classifies non-bottom waveforms into `WEAK` or `DEEP_WATER` based on positive residual ratios and trailing-edge derivatives.
- `int get_K(pm_OP_wave *A_Wave, int verbose)`
  - Extracts the water-column attenuation slope `A_Wave->K` via linear least squares (`do_least_squares` from `j_ang_resp.h`) between `s_Io` (`s_start_sur + 10`) and `s_start_bot - 5` (using $0.115\text{ m/sample}$).
- `int improve_bot_peak(pm_OP_wave *A_Wave, float the_level, int verbose)` & `int clean_results(pm_OP_wave *A_Wave, int cleaning_run)`
  - Recovers low-amplitude bottom peaks (e.g., over kelp/algae) by maximizing positive residuals above the surface-to-noise chord and validates peak widths and SNR across 3 cleaning passes.
- `double uncompress_dn(double dn_value, float baseline)`
  - Removes baseline noise and linearizes SHOALS log-compressed DN values using a piecewise 6th-order polynomial (`COEFF_A`..`COEFF_G` for $19 < \text{DN} \le 217$).
- `float correct_GAPD_for_k(pm_OP_wave *A_Wave)` / `float clac_reflectance(...)` / `double convert_DN_to_lin(float DN)` / `float convert_lin_to_DN(double lin_value)` / `double convert_DN_to_dB(float DN)` / `float convert_dB_to_DN(double dB_value)` / `float calc_corrected_height(float old_height, float k_value, float range)`
  - Radiometric conversion helpers between DN, linear power, and dB, plus water-column attenuation compensation for GAPD/PMT bottom reflectance.

## How It Fits Into the OMG Architecture

`pm_OP_waveproc` is integrated into **SwathEd (`SE`)** via `SE_Waveforms.c` / `SE_Waveforms.h` for interactive LiDAR waveform inspection, and powers the `code/Optech/` airborne LiDAR processing suite (`dumpWaveFormParams`, `processSHOALSdepths`, `make_Optech_prof`, `filterPPK`, `merge_PPK`).
