---
layout: default
title: jb_watercolumn
parent: Core Shared Libraries (subr)
module_name: jb_watercolumn
source_path: code/subr/jb_watercolumn.c
header_path: code/subr/jb_watercolumn.h
category: Water Column Uncertainty, SVP Thinning & Raytracing Rules
related_tools:
  - soundscape
  - mergeAtt
  - newMergeAtt
  - testSV
---

# `jb_watercolumn` — SVP Uncertainty Wedge Comparison, Douglas-Peucker Thinning & Raytracing Rules Library

## Overview & Purpose in the OMG Architecture

`jb_watercolumn` (`code/subr/jb_watercolumn.c`, `code/subr/jb_watercolumn.h`), authored by Jonathan Beaudoin, extends the core `j_watercolumn` library with advanced **Sound Velocity Profile (SVP) management, uncertainty quantification, profile thinning, deep-water profile extension, harmonic mean sound-speed integration, and time-varying raytracing rule tables**.

During hydrographic multibeam processing (and within the interactive `soundscape` SVP analysis application), hydrographers need to:
1. **Quantify refraction uncertainty (`SVP_Comparator`)**: Raytrace two different SVPs (e.g., an active cast vs. a subsequent cast or climatological reference) across a full swath sector and generate 2D cross-track/depth error wedges (`do_error_wedge`) and vertical error profiles (`do_error_profile`) normalized by depth or IHO percentage standards.
2. **Thin dense CTD/SVP casts (`SVP_Thinner`)**: Reduce high-density raw CTD casts to a compact set of inflection points using 1D or 2D **Douglas-Peucker** polygonal simplification (`douglas_peucker_svp`) so they can be transmitted to real-time sonar controllers with limited SVP table slots.
3. **Schedule time-dependent interpolation rules (`raytracing_rules`)**: Define and query a chronological schedule of SVP selection/interpolation strategies (`Last observed`, `Closest in time`, `Interpolated in time/distance`) across a survey.

---

## Key Data Structures, Constants & Macros (`code/subr/jb_watercolumn.h`)

### Constants
- **Wedge Output Formats**: `WEDGE_OUT_FORMAT_UNDEFINED` (`0`), `WEDGE_OUT_FORMAT_PPM` (`1`), `WEDGE_OUT_FORMAT_OLD` (`2`), `WEDGE_OUT_FORMAT_NEW` (`3`).
- **Raytracing Depth Source Rules (`raytracing_depth_source`)**:
  - `DEPTH_SOURCE_SHALLOWEST` (`0`): Raytrace down to the shallower of the two casts.
  - `DEPTH_SOURCE_DEEPEST` (`1`): Raytrace down to the deeper of the two casts.
  - `DEPTH_SOURCE_CAST1` (`2`), `DEPTH_SOURCE_CAST2` (`3`), `DEPTH_SOURCE_USER` (`4`).
- **Thinning Constants**: `THIN_DOUGLAS_PEUCKER` (`1`), `DOUGLAS_PEUCKER_1D` (`1`), `DOUGLAS_PEUCKER_2D` (`2`).

### Core Structs

#### `raytracing_rules`
Manages a chronological table of SVP interpolation rules over a survey:
- `int number_of_rules`: Total rules in the schedule.
- `double *time`: Array of Unix epoch timestamps when each rule takes effect.
- `int *interpolation_method`: Rule code at each timestamp (`WC_LAST_OBSERVED_IN_TIME` .. `WC_INTERPOLATED_IN_DIST`).
- `int *max_times`, `float *max_distances`: Maximum time (s) and distance (m) thresholds for each rule.
- `int current_rule`, `current_rule_number`: Runtime state trackers.

#### `SVP_Comparator`
Configuration and output container for two-profile raytracing uncertainty analysis:
- **Inputs & Geometry**: `filename1[500]`, `filename2[500]`, `outname[500]`, `latitude`, `longitude`, `time`, `draft`, `angular_sector`, `use_common_surface_speed`, `user_specified_ssp`, `surface_sound_speed_1`, `surface_sound_speed_2`, `raytrace_method`, `layers_to_use`, `resolution`, `raytracing_depth`, `raytracing_depth_source`, `max_raytracing_depth`.
- **Normalization & Mode Flags**: `normalize_by_percent`, `normalize_by_depth`, `just_outer`, `do_error_profile`, `do_error_wedge`.
- **Outputs**:
  - `watercolumn wc_out`: Vertical error profile vs. depth.
  - `int width`, `height`, `width_achieved`, `wedge_output_format`.
  - `float *depth`, `*across`, `*error_depth`, `*error_across`, `char *valid`: 2D spatial swath wedge buffers.
  - `double nadir_depth_error`, `outer_depth_error`, `outer_radial_error`: Terminal depth/radial errors at maximum depth.
  - `double time_diff`, `distance`: Temporal and geographic separation between the two casts.

#### `SVP_Thinner`
Configuration struct for SVP simplification:
- `int method` (`THIN_DOUGLAS_PEUCKER`), `int do_2ndpass`, `float DP_tolerance`, `int DP_dimension` (`DOUGLAS_PEUCKER_1D` or `DOUGLAS_PEUCKER_2D`).

---

## Public Functions & Signatures

### Raytracing Rule Schedule Management
- `int initialize_raytracing_rules(raytracing_rules *rules)` / `int free_raytracing_rules(raytracing_rules *rules)`
- `int load_raytracing_rules(FILE *infile, raytracing_rules *rules)` / `int write_raytracing_rules(FILE *outfile, raytracing_rules *rules)`
- `int get_raytracing_rule(double time, raytracing_rules *rules, int *rule, int *max_time, float *max_dist)`
  Looks up the active interpolation rule and time/distance thresholds for a ping at `time`.
- `int add_raytracing_rule(double time, raytracing_rules *rules, int rule, int max_time, float max_dist)` / `int remove_raytracing_rule(int rule_number, raytracing_rules *rules)`

### SVP Comparison & Uncertainty Wedges
- `int init_Comparator(SVP_Comparator *comparator)` / `int free_Comparator(SVP_Comparator *comparator)`
- `int do_compare(SVP_Comparator *comparator, watercolumn *svp1, watercolumn *svp2)`
  Executes comparative raytracing across the specified `angular_sector` and depth range using `svp1` (reference) and `svp2` (test), populating the 2D swath error wedge (`error_depth`, `error_across`), the 1D vertical error profile (`wc_out`), and terminal outer-beam/nadir error metrics.
- `int Comparator_Write(SVP_Comparator *comparator)`
  Writes the resulting error wedge or profile to disk.

### Profile Lookup, Extension, Thinning & Harmonic Sound Speed
- `double gimme_speed(watercolumn *wc, float depth)` & `ZVpair gimme_ZV_pair(watercolumn *wc, float depth)`
  Interpolates sound speed or all `ZVpair` attributes (speed, temperature, salinity) at an arbitrary `depth`.
- `float gimme_binsize(float depth)`
  Returns the standard vertical bin thickness appropriate for a given water depth.
- `int extend_profile(watercolumn *extendee, watercolumn *extender)`
   Splices the deep tail of `extender` (e.g., a deep climatological cast or deeper neighbouring cast) onto the bottom of a shallower `extendee` cast.
- `int init_Thinner(SVP_Thinner *thinner)` / `int free_Thinner(SVP_Thinner *thinner)`
- `watercolumn thin_watercolumn(SVP_Thinner *thinner, watercolumn *svp)` & `int douglas_peucker_svp(ZVpair *data, int from, int to, float tol, int method)`
  Applies recursive Douglas-Peucker line simplification to reduce an SVP to key inflection points within tolerance `tol`.
- `float compute_harmonic_sound_speed(watercolumn *svp, float draft)` & `watercolumn compute_harmonic_svp(watercolumn *svp, float draft)`
  Integrates cumulative slowness from `draft` downward to compute harmonic mean sound speed.
- `float get_minimum_required_sampling_depth(watercolumn *sv, float sv_tol)`
  Determines the shallowest surface sampling depth required to keep surface sound speed uncertainty within `sv_tol`.

---

## How It Fits Into the OMG Architecture

`jb_watercolumn` is the analytical engine behind `soundscape` and the automated SVP refraction uncertainty tools in the OMG codebase, working directly on `watercolumn` structs defined in `j_watercolumn.h`.
