---
layout: default
title: ensonification
parent: Core Shared Libraries (subr)
module_name: ensonification
source_path: code/subr/ensonification.c
header_path: code/subr/ensonification.h
category: Acoustic Backscatter & Sidescan Calibration
related_tools:
  - Echo_calib
  - swathed
  - applySectBP
  - get8101BeamPattern
  - getAngularResponse
  - getSnippetBP
  - getSnippetVariance
  - get_ADH_SRA
---

# ensonification: Instantaneous Seafloor Ensonified Area & Minimum Slant Range Interface

## Overview & Purpose
`ensonification` (`ensonification.h` / `ensonification.c`) defines the public interface and global control flags for computing the instantaneous seafloor area ensonified by a multibeam transmit/receive beam pair and for determining the Minimum Slant Range (normal-incidence specular distance) between a transducer and a gridded Digital Terrain Model (DTM).

In quantitative seafloor backscatter processing, raw echo intensity must be normalized by the instantaneous ensonified area $A$ ($10 \log_{10} A$) to convert received echo level into surface scattering strength ($S_b$). Near nadir (high grazing angles), the ensonified footprint is bounded by the intersection of the transmit along-track beamwidth ($\phi_T$) and receive across-track beamwidth ($\theta_R$); away from nadir (moderate to low grazing angles), the across-track footprint is bounded by the projected acoustic pulse length ($c \tau / (2 \cos \theta_g)$).

---

## Global Control Flags

```c
extern int debug_ensonification;
extern int invert_heave_for_ensonification;
```
* **`debug_ensonification`**: Defined in `ensonification.c`; enables diagnostic console output during footprint area and minimum slant-range calculations.
* **`invert_heave_for_ensonification`**: Defined in `ensonification.c`; flips the sign convention of vessel heave when computing transducer Z-elevation above the reference datum/DTM.

---

## Public Functions & Signatures

### `int find_min_range(OMG_HDCS_summary_header *summary, OMG_HDCS_profile_header *profile, OMG_HDCS_beam *beams, OMG_HDCS_sonar_params *sonar_parameters, JHC_header *dtm_header, float *dtm, float *min_range)`
Determines the minimum slant range (`*min_range`, in meters) from the active multibeam transducer to the seafloor for a given ping `profile`, using either the underlying bathymetric `dtm` grid (`dtm_header`, `dtm`) or the valid observed depths across `beams` along with lever-arm offsets in `sonar_parameters`.

### `float ensonified_area(float range, float sound_speed, float grazing_angle, float tx_beamwidth, float rx_beamwidth, float pulse_length)`
Computes the instantaneous seafloor area ($m^2$) ensonified at slant `range` (meters), local `sound_speed` ($c$, in m/s), `grazing_angle` (degrees), transmit along-track beamwidth `tx_beamwidth` (degrees), receive across-track beamwidth `rx_beamwidth` (degrees), and effective transmit `pulse_length` ($\tau$, in seconds):
* **Beamwidth-limited regime (near nadir):**
  $$A_{\text{beam}} \approx R^2 \, \phi_T \, \theta_R$$
* **Pulse-length-limited regime (oblique incidence):**
  $$A_{\text{pulse}} \approx R \, \phi_T \, \frac{c \tau}{2 \cos \theta_g}$$

### `int calc_ensonified_area(OMG_HDCS_profile_header *profile, OMG_HDCS_beam *beams, OMG_HDCS_sonar_params *sonar_parameters, float *grazing_angles, float *ensonified_areas, int toolType, int source_flags, float min_range_metres)`
Computes an array of `ensonified_areas` across an entire ping profile (`beams` or sidescan trace bins) for sonar model `toolType`, accounting for per-beam or per-sample slant ranges, precomputed `grazing_angles` (from `grazing_angle.c`), and `min_range_metres`.

### `int calculate_ensonified_area_ADH(int k, simrad_TVG *tvg, BS_data *a_BS_data)`
Added January 1, 2015 by Anand Hiroji (ADH); computes the ensonified area correction specifically tailored to Kongsberg/Simrad TVG laws (`simrad_tvg.h`) when stripping and re-applying radiometric corrections during sector beam-pattern extraction.

---

## How It Fits Into the OMG Architecture
`ensonification.h` is directly included by `Echo_calib.h` and is a core dependency of the OMG backscatter normalization and beam-pattern calibration pipeline:
* **`Echo_calib` (`code/subr/Echo_calib.c`):** Uses `ensonified_areas_trace` and `ensonified_areas_beam_avg` to normalize multibeam snippet and sidescan traces.
* **Backscatter & Beam Pattern Utilities (`code/omg/applySectBP.c`, `get8101BeamPattern.c`, `getAngularResponse.c`, `getSnippetBP.c`, `getSnippetVariance.c`, `get_ADH_SRA.c`):** Calls `calc_ensonified_area` and `calculate_ensonified_area_ADH` to isolate true angular backscatter response from geometric footprint variations.
