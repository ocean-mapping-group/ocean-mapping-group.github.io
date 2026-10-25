---
layout: default
title: reson_calibration
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/reson_calibration.c
category: Acoustic Modeling, Backscatter & TVG
related_tools:
- makess
- getAngularResponse
- getSnippetBP
- get_ADH_SRA
- getSnippetVariance
- omg2gsf
module_name: reson_calibration
header_path: code/subr/reson_calibration.h
---

# `reson_calibration` — Reson 81xx and 7K Radiometric Backscatter Calibration

## Overview & Purpose

The `reson_calibration` module (`code/subr/reson_calibration.c` and `code/subr/reson_calibration.h`) implements radiometric calibration algorithms for multibeam snippet and sidescan time-series amplitudes recorded by Teledyne Reson SeaBat 81xx series (`SeaBat_8101`, `SeaBat_8111`, `SeaBat_8125`, `SeaBat_8150`, `SeaBat_8160`) and 7K series (`SeaBat_7125`, `SeaBat_7150`, `SeaBat_7160`, `Reson_T20P`) sonars.

Developed by Jonathan Beaudoin and Thomas Weber (following tank calibrations at UNH and field campaigns in the Bismarck Sea and PNG), the library converts raw 16-bit linear amplitudes (`unsigned short`) into calibrated 8-bit logarithmic backscatter (`unsigned char`) by:
1. Converting raw digital counts to dB ($20 \log_{10}(\text{count})$) and applying an empirical pressure conversion factor (`90.0 dB` for 81xx, `100.0 dB` for 7K) plus any user-specified `dB_shift`.
2. Removing the transmit source level (`txLevel` adjusted for power setting in 3 dB or 1.5 dB steps on 81xx, or `sonar_settings->power` on 7K).
3. Removing real-time receiver gain / hardware TVG (accounting for amplifier saturation ceilings such as `max_gain = 65.0 dB` on the SeaBat 8160) and applying post-processed spherical spreading ($40 \log_{10} R$) and two-way absorption ($2\alpha R$).
4. Normalizing by the instantaneous ensonified seafloor area ($10 \log_{10} A$) computed from pulse length, transmit/receive beamwidths (including $\cos\theta$ electronic beam-steering broadening), and grazing angle.
5. Optionally compensating for within-beam receive beam pattern scalloping (`build_scallop`) on snippet traces.

---

## Key Constants & Global Control Variables

### Source & Mode Constants (`reson_calibration.h`)

| Macro | Value | Description |
| :--- | :--- | :--- |
| `JB_8101_LOG` / `JB_8101_LIN` | `0` / `1` | Logarithmic vs. linear data flags |
| `JB_8101_REFL` | `2` | Calibrate per-beam average reflectivity values (`source_flags == 2`) |
| `JB_8101_TRACE` | `3` | Calibrate full port/starboard sidescan time series (`source_flags == 3`); negative or zero `source_flags` indicate snippet trace for beam `abs(source_flags)` |
| `TX`, `RX`, `TX_AND_RX` | `1`, `2`, `3` | Transducer directional flags |
| `SIMPLE`, `MODEL`, `BP`, `DUMP_ANGLES` | `1`, `2`, `3`, `4` | Scallop compensation modes for `scallop_type` |

### Global Calibration Flags

- `int calibration_kickout`: Diagnostic step-out selector (`1` through `7`) allowing callers to halt calibration at intermediate stages (raw log, pressure conversion, source level removal, TVG removal, area normalization).
- `int skip_pulse_length`, `skip_gain`, `skip_source_level`, `skip_conversion_factor`, `skip_all`: Flags to selectively bypass individual terms in the sonar equation.
- `int try_detvg_reson`, `int remove_reson_tvg`, `float max_gain`: Control removal of real-time Reson TVG and amplifier saturation clipping.
- `int apply_snippet_gain`, `int scallop_type`, `float snippet_bp[200]`: Control snippet beam-pattern scallop removal (`SIMPLE` sine approximation, `MODEL` $\text{sinc}^2$ array model, or empirical `BP` lookup table).

---

## Public Functions & Signatures

### `calibrate_reson`

```c
int calibrate_reson(
    unsigned short *dataIn, unsigned char *dataOut,
    int num_samples, float *grazing_angles,
    float *ensonified_beam_areas,
    OMG_HDCS_profile_header profile, OMG_HDCS_beam *beams,
    int source_flags, float new_attenuation,
    float dB_shift, int dB_scale, int toolType
);
```
Calibrates an array of `num_samples` 16-bit amplitudes from a Reson 81xx sonar (`SeaBat_8101`, `8111`, `8125`, `8150`, `8160`) into 8-bit unsigned integers scaled by `dB_scale` relative to `255` (where `255` represents `0 dB` or invalid data). Calls `interpolate_ensonified_areas()` and optionally `build_scallop()`.

### `calibrate_reson_7K`

```c
int calibrate_reson_7K(
    unsigned short *dataIn, unsigned char *dataOut,
    int num_samples, float *grazing_angles,
    OMG_HDCS_profile_header *profile, OMG_HDCS_beam *beams,
    Reson_7K_7000_Sonar_Settings *sonar_settings, Reson_7K_TVG *tvg,
    int source_flags, float new_attenuation, float dB_shift, int dB_scale,
    int toolType, float *final_corrector
);
```
Calibrates snippet (`source_flags < 0`) or sidescan (`source_flags == JB_8101_TRACE`) time series from Reson 7K systems (`SeaBat_7125`, `7150`, `7160`, `Reson_T20P`) using `Reson_7K_7000_Sonar_Settings` and `ensonified_area()`, accounting for $\cos(\text{Rc\_steer})$ receive beamwidth broadening on electronically steered arrays. Outputs the net scalar correction factor into `*final_corrector` if non-`NULL`.

### `build_scallop`

```c
int build_scallop(
    OMG_HDCS_profile_header profile, OMG_HDCS_beam *beams,
    float *grazing_angles, float *snippet_gain, int num_samples,
    int beam_to_do
);
```
Computes per-sample receive beam-pattern gain corrections (`snippet_gain`) across a snippet window for `beam_to_do` using one of four `scallop_type` modes (`SIMPLE`, `MODEL`, `BP`, or `DUMP_ANGLES`).

### `interpolate_ensonified_areas`

```c
int interpolate_ensonified_areas(
    OMG_HDCS_profile_header profile, OMG_HDCS_beam *beams,
    float *ensonified_beam_areas, int num_samples,
    int source_flags, float *interp_ensonified_areas
);
```
Maps per-beam ensonified areas (`ensonified_beam_areas`) onto sample indices across a sidescan trace (`JB_8101_TRACE`) or local snippet window (`source_flags <= 0`) and linearly interpolates/extrapolates across sample gaps.

---

## How It Fits Into the OMG Architecture

- **Sidescan & Backscatter Processing (`omg/makess.c`, `subr/Echo_calib.c`)**: Invoked to radiometrically calibrate Reson 81xx and 7K snippets and sidescan traces before mosaic generation.
- **Angular Response & Beam Pattern Analysis (`omg/getAngularResponse.c`, `omg/getSnippetBP.c`, `omg/get_ADH_SRA.c`, `omg/getSnippetVariance.c`)**: Used to extract calibrated seafloor angular response curves and empirical snippet beam patterns.
- **Format Conversion (`gsf/omg2gsf.c`, `knudsen/mergeOtherSonarData.c`)**: Used to calibrate Reson backscatter amplitudes during GSF export and multi-sonar merging.
