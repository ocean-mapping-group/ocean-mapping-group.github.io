---
layout: default
title: Echo_calib
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/Echo_calib.c
category: Acoustic Backscatter & Sidescan Calibration
related_tools:
- make_ss
- swathed
- RT
- RTLite
- DelayEditor
- EKlook
module_name: Echo_calib
header_path: code/subr/Echo_calib.h
---

# Echo_calib: Multibeam Backscatter Calibration & Sidescan Time-Series Generation

## Overview & Purpose
`Echo_calib` (`Echo_calib.c` / `Echo_calib.h`, ~2,000 lines of C) is the central radiometric and geometric calibration engine for converting raw multibeam echo amplitudes, beam snippets, and sidescan time series into calibrated seafloor backscatter strength and `jcu_glo` (GLORIA-compatible) sidescan scanlines. Originally authored by John Hughes Clarke in October 1992 for Simrad EM100 and EM1000 systems, it has evolved continuously through 2023 to support:

* **Kongsberg/Simrad:** EM100, EM1000, EM12, EM300, EM1002, EM3000, EM3002, EM710, EM122, EM302, EM2040 (`.all` and `.kmall` formats, including multi-sector transmit/receive beam pattern compensation).
* **Teledyne Reson:** SeaBat 9001, 8101, 8125, 8111, 8150, 8160, and 7k-series (`7125`, `7150`, `7111`, `7101`, `T20P`) snippets and sidescan records.
* **R2Sonic:** 2020, 2022, 2024 TruePix (magnitude + angle) and FTS snippet records.
* **WASSP & Teledyne MB1:** Calibrated bathymetric/backscatter packets.

The library accounts for Time-Varying Gain (TVG), spherical spreading, seawater absorption (including François-Garrison/CTD re-attenuation), instantaneous ensonified footprint area, 3D grazing angle, Lambertian de-normalization, and multi-sector transmit/receive beam patterns (both across-track and along-track steering).

---

## Key Constants, State Variables & Data Structures

### Constants & Processing Versions

```c
#define MAX_NUM_ECHO_CALIB_SCANS 100000
#define MAX_NUM_ECHO_CALIB_BEAMS 1440

#define Atten_coeff_95kHz  30.0   /* 30 dB per km */
#define Atten_coeff_455kHz 60.0   /* 60 dB per km */
#define Sound_Speed        1500.0

#define MAKESS_V1               1
#define MAKESS_V2               2
#define MAKESS_V3               3
#define MAKESS_V4               4
#define MAKESS_RESON_SNIPPET    5
#define MAKESS_RESON_SIDESCAN   6
#define MAKESS_R2SONIC_TRUEPIX  7
```

### Global Calibration Buffers & Control Flags
* **Scanline & Beam Arrays:** `range_codes[8192]`, `grz_codes[8192]`, `altr_codes[8192]` (along-track offsets), `all_data[8192]`, `beam_codes[8192]`, `near_range[1440]`, `far_range[1440]`, `depth_beam[1440]`, `launch_angle_beam[1440]`, `BP_gain[1440]`, `Rx_Along_Gain[1440]`.
* **Radiometric Correction Flags:** `apply_TVG_flag`, `apply_ATTEN_flag`, `apply_POWER_flag`, `apply_Sph_flag`, `apply_Path_flag`, `apply_Foot_flag`, `apply_Beam_flag`, `apply_Empr_flag`, `apply_inverse_Lambert_flag`.
* **KMALL Backscatter Debugging Flags:** `apply_bscal`, `remove_bscal`, `flip_bscal`, `show_bscal`, `show_slapp`, `show_rxsen`, `show_sl_rx`.
* **Multi-Sector Beam Pattern Storage:**
  * `The_tx_sectors[100]`, `The_Sector_Params[100]` (`OMG_HDCS_tx_sector`)
  * `The_Sector_Beam_Pattern[100][180]`
  * `The_Sector_Beam_Pattern_Across_SRBP[100][180]`, `The_Sector_Beam_Pattern_Along_SRBP[100][180]`
  * `estimated_Along_SRBP_ADH[16][180]` (modeled along-track receive beam pattern vs. steering angle)

---

## Public Functions & Signatures

### Radiometric Amplitude & TVG Conversion
* `double EM_convert_amplitude(signed char amplitude, int toolType, float depth, float offset, signed char pulse_length, signed char mode, signed char EM100_power, signed char EM100_atten, signed char EM100_TVG, float grazing_angle, float *beam_pattern, float *grazing_angle_function)`
  Converts raw 8-bit echo amplitudes into calibrated dB backscatter values by stripping hardware TVG/power/attenuation gains and applying spherical spreading, path attenuation, and footprint area normalization (`footprint()`).
* `unsigned char EM_to_8bit(double dB_value)` / `unsigned char SB_shift16to8bit(int value, char method, float factor, float offset)`
  Maps calibrated floating-point dB or 16-bit linear amplitudes into 8-bit unsigned display/storage values.
* `double footprint(double grazing_angle, double slant_range, float along_beam_width, float across_beam_width, float pulse_length)`
  Computes the instantaneous ensonified seafloor area ($m^2$) from the pulse-length-limited and beamwidth-limited geometry.
* `double calc_atten(double temp, double salinity, double depth, double pH, double freq)`
  Computes the seawater acoustic absorption coefficient (dB/km) as a function of temperature, salinity, depth, pH, and acoustic frequency.
* `double recalc_1994_BSvalue(double BSn_BSo, char *trace_data, int no_samples, int method, double Incidence_Angle, double Ri, double Ro)`
  Recalculates Simrad normal/oblique backscatter (`BSn`/`BSo`) from raw snippet trace samples.

### Sidescan Scanline Generation (`make_ss` Family)
* `void make_ss(FILE *datafile, FILE *pingfile, int ping_no, int hack_flag, int gainup, float pixel_size, gloria_all_rec *out_rec)`
  High-level dispatcher that reads an HDCS profile, beams, and raw image trace from disk and populates a `gloria_all_rec` sidescan scanline record.
* `void make_this_ss(...)`, `void make_this_ss2(...)`, `void make_this_ss3(...)`, `void make_this_ss4(...)`
  Generational implementations of Kongsberg/Simrad and dual-time-series sidescan scanline assembly, mapping snippet samples across-track by slant range and horizontal projection, applying multi-sector beam patterns, and interpolating gaps (`interpolate_record`, `collapse_record`).
* `void make_reson_snippet_ss(...)` & `void make_reson_sidescan(...)`
  Constructs calibrated sidescan scanlines from Reson 81xx/7k snippets or raw sidescan packets.
* `void make_r2sonic_truepix(...)`
  Constructs calibrated sidescan scanlines from R2Sonic TruePix magnitude and angle time series.
* `void make_grazing_angles(...)` & `void make_along_track_offset(...)`
  Generates companion across-track scanlines encoding per-pixel grazing angle (`grz_codes`) and multi-sector along-track offset (`altr_codes`) for 3D terrain-corrected mosaicking.

### Multi-Sector Beam Pattern Management
* `int load_MS_bp(char *multi_sector_name, float The_Sector[100][180], OMG_HDCS_tx_sector Params[100], int *how_many_sectors)`
* `int dump_MS_bp(char *multi_sector_name, float The_Sector[100][180], OMG_HDCS_tx_sector Params[100], int *how_many_sectors)`
* `int load_MS_bp_lin(...)`, `int which_MS_sector_is_this(...)`, `int Ignore_Nadir_MSbp(...)`
* `float estimate_Along_track_RBP(float sector_frequency, int this_beam_Along_SRA, float Sound_speed)`

---

## How It Fits Into the OMG Architecture
`Echo_calib` is the backbone of all sidescan and backscatter processing in the OMG suite:
* **Interactive Swath & Backscatter Editing (`swathed`, `SE_BSwindow.c`, `SE_omgIOwin.c`):** Uses `Echo_calib` to render calibrated sidescan strips, inspect beam pattern residuals, and test radiometric flags interactively.
* **Real-Time Acquisition & Display (`RT`, `RTLite`):** Calls `make_this_ss2`/`make_reson_snippet_ss` on incoming multibeam pings to build real-time waterfall and georeferenced sidescan mosaics.
* **Batch Backscatter & Beam Pattern Tools (`omg/applySectBP.c`, `omg/getSnippetBP.c`, `omg/get_ADH_SRA.c`):** Relies on `load_MS_bp`, `dump_MS_bp`, and `make_ss` to extract empirical sector beam patterns and produce normalized `.glo` sidescan files for `mos2`.
