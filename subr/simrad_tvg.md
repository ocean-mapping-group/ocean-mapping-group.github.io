---
layout: default
title: simrad_tvg
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/simrad_tvg.c
category: Acoustic Modeling, Backscatter & TVG
related_tools:
- SE_AnandBS
- SE_WaterColumn
- newGetBP
- understand_KM_BS
- compress_OMG_watercolumn
- deTVG
module_name: simrad_tvg
header_path: code/subr/simrad_tvg.h
---

# `simrad_tvg` — Kongsberg Simrad EM Backscatter TVG & BTS De-Ramping Interface

## Overview & Purpose

The `simrad_tvg` module (`code/subr/simrad_tvg.h` and `code/subr/simrad_tvg.c`) defines the data structures and function prototypes for reconstructing and removing the real-time Time-Varying Gain (TVG) and Bottom Target Strength (`BTS`) backscatter corrections applied by Kongsberg (Simrad) EM-series multibeam echosounders (`.all` and `.kmall` formats).

Originally developed by Jonathan Beaudoin (2007–2011) and extended by Anand Hiroji (2013–2015) and John Hughes Clarke (2022–2024), the module models Kongsberg's three-segment real-time backscatter law across one-way travel time (`owtt`):
1. **Water Column Domain (`WC_Spec_Lamb == 1`)**: Before normal incidence (`owtt < owtt_to_normal_incidence`), where beamwidth-limited spreading applies.
2. **Specular / Nadir Ramp Domain (`WC_Spec_Lamb == 2`)**: Between normal incidence and the TVG crossover angle (`owtt_to_normal_incidence <= owtt < owtt_to_crossover`), where Kongsberg transitions from normal-incidence backscatter `BSn` to oblique backscatter `BSo` using a $\sqrt{t - 1}$ ramp to suppress the specular nadir peak.
3. **Lambertian Domain (`WC_Spec_Lamb == 3`)**: Beyond the crossover range (`owtt >= owtt_to_crossover`), where a flat-seafloor $\cos^2\theta$ Lambertian law around `BSo` and a pulse-length-limited ensonified area are assumed by the sonar in real time.

> **Implementation Note**: In the current UNB SwathEd source tree, `code/subr/simrad_tvg.c` contains only the global variable definition `int has_snippet;` (while the full header contract remains in `code/subr/simrad_tvg.h` for `SE_AnandBS.c`, `ensonification.h`, `newGetBP.c`, `understand_KM_BS.c`, and `deTVG.c`).

---

## Key Data Structures

### `simrad_TVG` (`simrad_tvg.h`)

```c
typedef struct simrad_TVG {
    /* Pulled directly from OMG data structures */
    float BSn;
    float BSo;
    float range_to_normal_incidence;
    int used_sample_rate;
    float crossover_angle;
    float tx_beamwidth, rx_beamwidth;
    float sound_speed;
    float pulse_length;

    /* Computed when above are loaded */
    float crossover_range;
    float owtt_to_normal_incidence;
    float owtt_to_crossover;

    /* Housekeeping flags controlling BTS computation */
    int try_new_BTS;
    int try_new_BTS_per_beam;
    int try_only_pulse_length_correction;
} simrad_TVG;
```

### `BS_data` (`simrad_tvg.h`)

Per-beam backscatter and snippet sample workspace structure:
- **Metadata & Angles**: `memory_allocated`, `no_of_samples`, `unique_sector`, `Beam_status`, `centre_sample_no`, `grazing_angles`, `sonar_relative_angle`, `Verticaly_Referenced_Angle`, `rx_beamwidth`, `pulse_length`, `owtt_to_centre_sample`, `WC_Spec_Lamb` (`1` = water column, `2` = specular domain, `3` = Lambertian domain).
- **Dynamic Sample Arrays**:
  - `float *original_BS`: Raw snippet/beam backscatter intensities (dB) as recorded by the Kongsberg sonar.
  - `float *BTS`: Reconstructed Kongsberg real-time Bottom Target Strength correction (dB) per sample.
  - `float *BSn_BSo`: Isolated near-nadir `BSn`-to-`BSo` ramp suppression term (added March 2024).
  - `float *BS`: Predicted Kongsberg backscatter coefficient (`BTS + BSo`).
  - `int *ensoni_area_descriptor`: Flag indicating how area was calculated (`0` = pulse-length limited, `1` = beamwidth limited, `2` = none).
  - `float *ensoni_area`: True slope-corrected ensonified area ($10 \log_{10} A$) computed from actual seafloor grazing angle.
  - `float *ensoni_area_flat_seafloor`: Flat-seafloor ensonified area ($10 \log_{10} A_{\text{flat}}$) assumed by the Kongsberg real-time processor.
  - `float *deTVG_BS`: Final de-ramped and true-area-normalized backscatter (`original_BS + BTS - ensoni_area`).
  - `double *owtt`: One-way travel time (seconds) for each snippet sample.

---

## Public Functions & Signatures

- **`int get_TVG_params(OMG_HDCS_profile_header *profile, simrad_TVG *tvg)`**
  Extracts `BSn`, `BSo` (from `profile->BSn_f`/`BSo_f` or `profile->TVG` and `profile->power`), `range_to_normal_incidence`, `crossover_angle` (`profile->tvg_crossover`), `tx_beamwidth`, `rx_beamwidth`, `sound_speed`, and `pulse_length` (supporting both legacy `.all` and `.kmall` `maxEffTxPulseLength_sec`), and computes `crossover_range`, `owtt_to_normal_incidence`, and `owtt_to_crossover`.
- **`int print_TVG_params(simrad_TVG *tvg)`**
  Prints a formatted diagnostic summary of all fields in a `simrad_TVG` struct.
- **`void compute_BTS(int k, simrad_TVG *tvg, BS_data *a_BS_data)`**
  Evaluates the Kongsberg real-time `BTS`, `BSn_BSo`, `WC_Spec_Lamb`, and `ensoni_area_flat_seafloor` at sample index `k` (supporting both legacy `try_new_BTS == 0` and modern `try_new_BTS == 1` formulations).
- **`int adh_take_out_BTS_and_correct_for_area(int k, simrad_TVG *tvg_array, int do_pulse_length_correction, BS_data *a_BS_data)`**
  Removes the Kongsberg real-time `BTS` and flat-seafloor area assumption from `original_BS[k]` and normalizes by the true grazing-angle-dependent ensonified area (`calculate_ensonified_area_ADH`), storing the result in `deTVG_BS[k]`.
- **`double adh_find_range_to_center_sample(unsigned int range, OMG_HDCS_profile_header *profile)`**
  Rescales a beam's two-way range from the bathymetry sampling rate (`profile->samp_rate`) to the seabed image sampling rate (`profile->snippet_sample_rate`) when they differ (e.g., EM2040 multi-mode operation).
- **`float adh_find_sector_pulse_length(OMG_HDCS_tx_sector *tx_sectors, unsigned char TxSector)`**
  Returns the effective transmit pulse length for sector `TxSector`: `signal_length` for CW pulses (`waveform_id == 0`) or compressed pulse length `1.0 / signal_bandwidth` for FM chirp pulses (`waveform_id == 1` or `2`).
- **`int adh_get_OWTT_for_each_sample(...)` / `int adh_get_OWTT_for_each_sample_from_twtt(...)`**
  Computes the one-way travel time `a_BS_data->owtt[k]` for sample `k` relative to the beam center detection sample, accounting for pre-EM710 (`has_snippet == 1`) vs. post-EM710 (`has_snippet == 0`) snippet sample spacing.
- **`int adh_get_RX_beamwidth(simrad_TVG *tvg, BS_data *a_BS_data)`**
  Computes the steered receive beamwidth broadened by the sonar-relative steering angle: `tvg->rx_beamwidth / cos((90.0 - sonar_relative_angle) * M_PI / 180.0)`.
- **`int adh_recalc_range_to_normal_incidence(OMG_HDCS_profile_header *profile, OMG_HDCS_beam *beams)`**
  Recomputes `profile->range_to_normal_incidence` as twice the minimum valid beam `range` across the swath.
- **`int recalc_owtt_normal_incidence_crossover(simrad_TVG *tvg, OMG_HDCS_beam *beams, int nobeams)`**
  Overrides `tvg->owtt_to_normal_incidence` and `tvg->owtt_to_crossover` using floating-point beam `twtt` values (added March 2024 for `.kmall` precision).
- **`int adh_allocate_memory_for_BS_data(int no_samples, BS_data *a_BS_data)` / `int adh_free_memory_for_BS_data(BS_data *a_BS_data)`**
  Allocates and frees the dynamic sample arrays inside a `BS_data` struct.

---

## How It Fits Into the OMG Architecture

- **Interactive Backscatter & Water Column Analysis (`SE/SE_AnandBS.c`, `SE/SE_WaterColumn.c`)**: `SE_AnandBS.c` uses `simrad_TVG` and `BS_data` to interactively inspect and de-TVG Kongsberg multibeam backscatter in SwathEd.
- **Beam Pattern & Backscatter Calibration (`omg/newGetBP.c`, `omg/understand_KM_BS.c`, `jonnyb/gom_stuff/deTVG.c`, `subr/ensonification.h`)**: Rely on `simrad_tvg.h` structures and routines to strip Kongsberg's real-time `BSn`/`BSo` ramp and flat-seafloor area assumptions so true angular response and transmit/receive beam patterns can be recovered.
