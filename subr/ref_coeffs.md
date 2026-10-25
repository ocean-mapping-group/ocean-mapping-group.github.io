---
layout: default
title: ref_coeffs
parent: Core Shared Libraries (subr)
module_name: ref_coeffs
source_path: code/subr/ref_coeffs.c
header_path: code/subr/ref_coeffs.h
category: Acoustic & Bathymetric Processing
related_tools:
  - swathed (SE)
  - deRefract
  - dumpXYZ
  - rationalOMG
  - weigh_grid
---

# ref_coeffs

## Overview & Purpose

`ref_coeffs` (authored by John Hughes Clarke, May 1996) defines the data structures, global state variables, and function prototypes for empirical two-layer sound velocity refraction correction ("RefTool"). In hydrographic surveys where inadequate or unmeasured near-surface and thermocline sound velocity variations cause systematic "frowning" or "smiling" swath artifacts, `ref_coeffs` models a two-layer empirical correction consisting of a surface transducer draft/sound-speed error (`surf_draft`, `surf_sss_error`) and a sub-surface water-column layer depth/sound-speed error (`layer_depth`, `layer_ss_error`), accounting for transducer array geometry (flat horizontal, curved EM1000/EM1002, or twin $30^\circ$ tilted arrays).

## Key Data Structures, Constants & Macros

### Transducer Array Geometry Constants
- `HORIZ_LINE` (`0`): Flat horizontal transducer array (beam steering relative to horizontal).
- `EM1000_CURVED` (`1`): Curved cylindrical array (Simrad EM1000) where beam steering varies across the arc.
- `TWIN_30DEG_LINE` (`2`): Dual-head or V-mounted $30^\circ$ tilted linear arrays.
- `EM1002_CURVED` (`3`): Curved cylindrical array (Simrad EM1002).

### Data Structures & Global Variables
- `ref_coeff`: Represents a time/ping-indexed empirical refraction coefficient keyframe:
  - `int rec`: Profile (ping) record number in the HDCS file.
  - `float surf_draft`: Effective transducer draft (meters) for the surface layer.
  - `float surf_sss_error`: Surface sound speed error ($\Delta c_0$ in m/s) at the transducer face (affects beam steering angles for non-perpendicular beams).
  - `float layer_depth`: Depth of the empirical refraction interface/thermocline (meters).
  - `float layer_ss_error`: Sound speed contrast ($\Delta c_1$ in m/s) across the horizontal sub-surface layer (affects Snell's law ray bending below `layer_depth`).
- Global State (defined in `ref_coeffs.c`, declared `extern` in `ref_coeffs.h`):
  - `int array_type`: Active transducer array geometry (`HORIZ_LINE`, `EM1000_CURVED`, `TWIN_30DEG_LINE`, or `EM1002_CURVED`).
  - `float surf_draft`, `float surf_sss_error`, `float layer_depth`, `float layer_ss_error`: Active interpolated refraction parameters for the current ping.
  - `double actual_beam_steered_angle[900]`: Per-beam corrected launch angle after applying `surf_sss_error` to the transducer array geometry.
  - `double actual_beam_sublayer_angle[900]`: Per-beam refracted ray angle below `layer_depth` after applying Snell's law with `layer_ss_error`.
  - `int no_coeffs`: Number of empirical refraction keyframes loaded in `rcoeff`.
  - `ref_coeff rcoeff[400]`: Array of up to 400 ping-indexed refraction keyframes.

## Public Functions & Signatures

*(Note: `ref_coeffs.c` defines the shared global storage; the implementation routines declared in `ref_coeffs.h` are linked via `SE_REFTOOLwin.c` and the OMG refraction utilities.)*

- `int read_ref_coeff_file(char *name)` / `int write_ref_coeff_file(char *name)`
  - Reads or writes an ASCII/binary `.ref_coeff` file containing ping-indexed `(rec, surf_draft, surf_sss_error, layer_depth, layer_ss_error)` keyframes into/from `rcoeff[]` and `no_coeffs`.
- `int jREF_decide_array_type(int toolType)`
  - Maps an OMG HDCS `toolType` sonar identifier to one of the four transducer array geometries (`HORIZ_LINE`, `EM1000_CURVED`, `TWIN_30DEG_LINE`, `EM1002_CURVED`).
- `void get_coeffs(int recno, ref_coeff *rc)`
  - Interpolates `rcoeff[0..no_coeffs-1]` at ping number `recno` to populate `*rc`.
- `void set_up_ref_coefficients(ref_coeff *rc)`
  - Copies `*rc` into the active globals (`surf_draft`, `surf_sss_error`, `layer_depth`, `layer_ss_error`) and triggers `calc_BeamSteering_Errors()` and `calc_BeamTurning_Errors()`.
- `void calc_BeamSteering_Errors()` & `void calc_BeamTurning_Errors()`
  - Precomputes `actual_beam_steered_angle[]` and `actual_beam_sublayer_angle[]` across the swath from the active surface and sub-layer sound speed errors.
- `void get_refracted_location(float depth_in, float across_in, float *depth_out, float *across_out)`
  - Takes a nominal `(depth_in, across_in)` sounding and applies the precomputed beam steering and Snell's law layer refraction adjustments to output the corrected `(*depth_out, *across_out)`.

## How It Fits Into the OMG Architecture

`ref_coeffs` powers the interactive **RefTool** window in **SwathEd (`SE`)** (`SE_REFTOOLwin.c`, `SE_2Dwindow.c`, `SE_W_TimeSeries.c`, `SE_omgIOwin.c`, `swathed.c`) where operators visually flatten outer-beam refraction artifacts, and is used in batch processing by **`deRefract`**, **`dumpXYZ`**, **`rationalOMG`** (`code/omg/`), and **`weigh_grid`** (`code/grid/`).
