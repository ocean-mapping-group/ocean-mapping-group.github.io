---
layout: default
title: r_atten
parent: Core Shared Libraries (subr)
module_name: r_atten
source_path: code/subr/r_atten.c
header_path: code/subr/r_atten.h
category: Acoustic & Bathymetric Processing
related_tools:
  - makess
  - getBeamPattern
  - newGetBP
  - get_ADH_SRA
---

# r_atten

## Overview & Purpose

`r_atten` (authored by Rodrigo Carvalho, August 2012) computes depth-dependent cumulative seawater sound absorption (attenuation in dB/km) on a **per-beam** basis from an observed CTD profile (`watercolumn`) and compares it against the single constant sector attenuation coefficient applied in real time by Kongsberg SIS. It then calculates the differential two-way transmission loss correction (`the_gain_corr_we_should_use[beam]`) required by **`makess`**, **`getBeamPattern`**, **`newGetBP`**, and **`get_ADH_SRA`** to remove water-column absorption artifacts from sidescan mosaics and empirical Angular Response Curves (ARCs).

## Key Data Structures, Constants & Macros

### Constants
- `MAX_NO_ATTEN_VALS` (`1000`): Maximum number of depth layers in an attenuation profile.
- `MAX_NO_ATTEN_SECTOR_FREQ` (`100`): Maximum number of distinct transmit sector center frequencies cached simultaneously.

### Data Structures & Global State
- `an_atten`: Represents seawater properties and attenuation at a single CTD depth sample:
  - `float depth`: Sample depth in meters.
  - `float temperature`: Temperature in $^{\circ}\text{C}$.
  - `float salinity`: Salinity in PSU.
  - `float pH`: Acidity (default `8.0`).
  - `double in_situ`: Local (in-situ) absorption coefficient (dB/km) at `depth`, computed via `calc_atten()` (`Echo_calib.h`, Francois & Garrison / Ainslie & McColm formulation).
  - `float cummulative`: Depth-integrated harmonic/trapezoidal mean absorption coefficient (dB/km) from the sea surface ($z = 0$) down to `depth`.
- `atten_profile`: Stores the complete cumulative attenuation curve for a single acoustic center frequency:
  - `int novalues`: Number of depth samples.
  - `float freq_kHz`: Acoustic frequency in kHz.
  - `an_atten the_atten[MAX_NO_ATTEN_VALS]`: Array of layered attenuation entries.
- Module Globals:
  - `float the_pH`: Seawater pH (initialized to `8.0` by `r_init_atten()`).
  - `atten_profile att_Fq[MAX_NO_ATTEN_SECTOR_FREQ]`: Cache of precalculated `atten_profile` curves indexed by sector frequency.
  - `int no_recognised_atten_freq` / `int currently_used_atten_freq_index`: Frequency cache counters.
  - `watercolumn the_CTD_for_atten`: Active CTD profile structure (`j_watercolumn.h`).
  - `float the_atten_we_should_use[1000]`: Per-beam cumulative attenuation (dB/km) interpolated at each beam's sounding depth.
  - `float the_gain_corr_we_should_use[1000]`: Per-beam two-way gain correction (in dB, or $0.5\text{ dB}$ steps) to apply during backscatter re-calibration.
  - `float atten_diff`: Difference between CTD-derived cumulative attenuation and the real-time SIS attenuation coefficient.

## Public Functions & Signatures

- `int r_init_atten()`
  - Initializes module state: sets `the_pH = 8.0`, `no_recognised_atten_freq = 0`, and `currently_used_atten_freq_index = 0`.
- `int r_calc_insitu_cummulative_atten(watercolumn *a_wc, float pH, float desired_freq_kHz, atten_profile *theprof)`
  - Iterates over all `a_wc->no_raw_zvs` layers in the CTD cast:
    1. Calls `calc_atten(T, S, Z, pH, freq_kHz)` to compute the local `in_situ` absorption (dB/km) at each depth.
    2. Integrates the cumulative layer-averaged absorption from the surface to each depth $z_i$ using trapezoidal integration over layer thickness $\Delta Z_i = (z_i - z_{i-1}) \times 0.001\text{ km}$:
       $$\alpha_{\text{cum}}(z_i) = \frac{\sum_{k=1}^{i} \frac{\alpha(z_k) + \alpha(z_{k-1})}{2} \Delta Z_k}{\sum_{k=1}^{i} \Delta Z_k}$$
- `float r_find_atten_to_use(double depth, int index_for_this_CF, int oldatten, int test_beam)`
  - Looks up `att_Fq[index_for_this_CF]` and linearly interpolates `cummulative` attenuation at the beam's sounding `depth` (clamping to the shallowest `in_situ` value if `depth < depth[0]`). Optionally logs `(depth, atten_to_use, oldatten, diff)` to `"attenuation_data_file1.txt"` when `test_beam` is true (beam 100).
- `int r_get_diff_atten(float the_CF, float the_old_atten, int j, double depth, double range)`
  - Checks whether `the_CF` (center frequency in kHz) is already cached in `att_Fq[]`; if not, calls `r_calc_insitu_cummulative_atten()` to populate a new cache slot. Interpolates `the_atten_we_should_use[j]` at the beam's `depth`, computes `atten_diff = the_atten_we_should_use[j] - the_old_atten / 100.0`, and stores the two-way slant-range correction `the_gain_corr_we_should_use[j] = atten_diff * 2.0 * range / 1000.0`.

## How It Fits Into the OMG Architecture

`r_atten` is called by **`Echo_calib`** (`code/subr/Echo_calib.c`), **`makess`**, **`getBeamPattern`**, **`newGetBP`**, and **`get_ADH_SRA`** (`code/omg/`) to replace coarse per-sector absorption coefficients with exact CTD-integrated per-beam absorption corrections in multi-sector multibeam systems (such as Kongsberg EM710, EM302, and EM122).
