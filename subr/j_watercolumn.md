---
layout: default
title: j_watercolumn
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/j_watercolumn.c
category: Water Column & Acoustic Raytracing
related_tools:
- mergeAtt
- newMergeAtt
- makess
- getBeamPattern
- applySectBP
- LPFbeams
- gsf2svp
- SYN_internal_wave
- jview
module_name: j_watercolumn
header_path: code/subr/j_watercolumn.h
---

# `j_watercolumn` — Sound Velocity Profile (SVP) Management & Acoustic Raytracing Interface

## Overview & Purpose in the OMG Architecture

`j_watercolumn` (`code/subr/j_watercolumn.c`, `code/subr/j_watercolumn.h`), originally authored by John E. Hughes Clarke in August 1998 and expanded by Jonathan Beaudoin (2006) and JHC (2025), defines the core **OMG Water Column (`watercolumn`)** data structures, temporal/spatial profile interpolation rules, seawater sound-speed equations, and acoustic raytracing APIs used across the entire OMG software suite.

Accurate multibeam depth and cross-track positioning requires tracing acoustic rays through a vertically stratified (and temporally/spatially varying) ocean sound velocity profile (SVP). `j_watercolumn` defines the `ZVpair`, `Ray`, and `watercolumn` structures (supporting Version I and Version II `.jwc` / `.svp` formats with temperature, salinity, and 3D current velocity components) and declares the raytracing (`raytrace`, `quicktrace`, `raytrace_gradients`, `raypath`) and multi-cast interpolation (`interp_watercolumn`, `find_closest_wcs`, `load_watercolumns`) functions that are used by every bathymetric and sidescan processing tool in `code/omg/` and `code/JV/`.

---

## Key Data Structures, Constants & Macros (`code/subr/j_watercolumn.h`)

### Multi-Cast Interpolation Rule Constants
Used to specify `watercolumn.interpolation_method` and `wc_rule_names[]`:
- `WC_INITIAL` (`0`)
- `WC_LAST_OBSERVED_IN_TIME` (`1`): Uses the most recent prior cast (simulating real-time survey acquisition).
- `WC_NEXT_OBSERVED_IN_TIME` (`2`): Uses the next upcoming cast.
- `WC_CLOSEST_IN_TIME` (`3`): Nearest-neighbor cast in time.
- `WC_INTERPOLATED_IN_TIME` (`4`): Linear time-weighted interpolation between bracketing casts.
- `WC_CLOSEST_IN_DIST` (`5`): Nearest-neighbor cast in geographic distance.
- `WC_INTERPOLATED_IN_DIST` (`6`): Inverse-distance weighted interpolation between casts.
- `WC_INVALID` (`7`), `WC_DONT_INTERPOLATE` (`-1.0`).

### Raytracing Method & Cast Direction Constants
- **Raytracing Methods**: `CONST_LAYERS` (`0`), `CONST_GRADIENT` (`1`), `DUMB_TEST` (`2`), `QUICK_TRACE` (`3`).
- **Cast Sorting Modes**: `JWC_DOWNCAST` (`0`), `JWC_UPCAST` (`1`), `JWC_BOTHCAST` (`2`).
- **Lookup Criteria**: `BY_TIME` (`0`), `BY_DIST` (`1`).

### Core Structs

#### `ZVpair`
Represents a single vertical observation node in a water-column profile:
- `double depth`, `speed`: Depth (m) and sound speed (m/s).
- `double temperature`, `salinity`, `extra_field`, `int flag`: Version II JWC CTD parameters.
- `double cummulative_area`: Runtime harmonic-mean integration accumulator.
- `double uvel`, `vvel`, `wvel`: Runtime 3D ocean current velocity components (added November 2025).

#### `Ray`
Stores a point along a traced acoustic ray trajectory:
- `double across`, `depth`, `twtt`: Across-track radial distance (m), vertical depth (m), and two-way travel time (s).

#### `watercolumn`
Master structure managing raw and resampled vertical profiles, metadata, and runtime `soundscape` state:
- **File Header & Observation Metadata**: `short format_version`, `double time_of_obs`, `time_of_rec`, `time_since_last_obs`, `time_until_next_obs`, `lat_obs`, `lon_obs`, `lat_rec`, `lon_rec`.
- **Raw & Interpolated Profile Arrays**:
  - `int no_raw_zvs`, `size_raw_zvs`, `ZVpair *raw_zv`: Raw observed depth/speed/CTD layers.
  - `char got_interp`, `int no_interp_zvs`, `size_interp_zvs`, `float zv_interval`, `ZVpair *interp_zv`: Uniformly resampled and deep-extended layers used for fast raytracing.
- **Statistics & Dynamic Range**: `min_speed`, `mean_speed`, `max_speed`, `min_temperature`, `mean_temperature`, `max_temperature`, `min_salinity`, `mean_salinity`, `max_salinity`, `depth_of_first_obs`, `depth_of_first_valid_obs`, `depth_of_last_obs`, `depth_of_last_valid_obs`.
- **Runtime & Uncertainty Fields**: `filename`, `prefix`, `suffix`, `got_async`, `is_sorted`, `interpolation_method`, `status`, `deleted`, `edited`, `plot`, `marked`, `source`, `copy_count`, projected `(x, y)`, `angular_sector_in_spec`, `swath_in_spec`, and `ZVpair tail_error`.

---

## Public Functions & Signatures

### Lifecycle, I/O & Profile Preparation
- `int jWC_init(watercolumn *wc)` / `void jWC_free(watercolumn *wc)`
  Initializes a `watercolumn` structure to safe defaults and frees dynamically allocated `raw_zv`, `interp_zv`, and filename strings.
- `int jWC_read(char *wcname, watercolumn *wc)` / `int jWC_write(FILE *file, watercolumn *wc)` / `int jWC_print(watercolumn *wc)`
  Reads, writes, and prints OMG `.jwc` / `.svp` water-column files (supporting both Version I and Version II formats).
- `watercolumn jWC_copy(watercolumn *wc)` / `void jWC_copy_header(watercolumn *wc_source, watercolumn *wc_destination)`
  Deep-copies an entire `watercolumn` or copies its header metadata.
- `int jWC_sort_async(watercolumn *wc, int method)`
  Sorts asynchronous raw CTD/SVP casts by depth and extracts the downcast (`JWC_DOWNCAST`), upcast (`JWC_UPCAST`), or combined cast (`JWC_BOTHCAST`).
- `void jWC_interp_zv(watercolumn *wc, float maxdepth, float sv_at_maxdepth)`
  Resamples `wc->raw_zv` onto regular depth intervals (`wc->zv_interval`) in `wc->interp_zv` and extrapolates to `(maxdepth, sv_at_maxdepth)`.
- `void jWC_calc_means(watercolumn *wc)` / `int watercolumn_insert_sample(watercolumn *svp, ZVpair sample)`
  Updates min/mean/max profile statistics and inserts a new `ZVpair` sample in depth-sorted order.

### Acoustic Raytracing & Seawater Equations
- `void raytrace(watercolumn *wc, int method, int layers_to_use, float startdepth, float depression_angle, double TWTT, float surface_sound_speed, double *radial_dist, double *depth, float *final_depression_angle)`
  Primary Snell's Law raytracer: traces a ray launched at `startdepth` and `depression_angle` (adjusted by `surface_sound_speed` at the transducer face) for a given two-way travel time `TWTT`, returning horizontal `radial_dist`, vertical `depth`, and bottom `final_depression_angle`.
- `void quicktrace(...)` & `int raytrace_gradients(...)`
  Fast lookup-based and constant-velocity-gradient circular-arc raytracers.
- `Ray *raypath(...)`, `int raypath2(...)`, `int raypath3(...)`, `void resample_ray(...)`
  Computes and resamples the full trajectory array (`Ray *`) of an acoustic ray through all water-column layers.
- `double vsw(double t, double p, double s)` & `double vchemilli(double t, double p, double s)`
  Computes seawater sound speed (m/s) from temperature `t` (°C), pressure/depth `p`, and salinity `s` (PSU) using UNESCO / Chen & Millero equations.

### Multi-Cast Selection & Interpolation
- `int load_watercolumns(char **wcname, int nowcs, watercolumn wc[], float max_interp_depth, float max_interp_sv, float bin_thickness, int *num_valid_wcs)`
- `int find_closest_wcs(double pingtime, double latitude, double longitude, int nowcs, watercolumn wc[], int *wc_before, int *wc_after, int criteria, float maxtime, float maxdist)`
- `int interp_watercolumn(double image_time, double latitude, double longitude, float maxtime, float maxdist, int num_watercolumns, watercolumn *wc, watercolumn *interp_wc)`

---

## How It Fits Into the OMG Architecture

`j_watercolumn` is the foundational SVP and raytracing interface in `subr/`. It is paired with `jb_watercolumn` (which implements advanced SVP comparison, Douglas-Peucker thinning, and time-varying raytracing rule tables) and is linked by `mergeAtt`, `newMergeAtt`, `makess`, `getBeamPattern`, `applySectBP`, `LPFbeams`, `gsf2svp`, and `jview`.
