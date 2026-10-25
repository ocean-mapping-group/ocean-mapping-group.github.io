---
layout: default
title: sonar_geometry
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/sonar_geometry.c
category: Raytracing, Sound Speed & Geolocation
related_tools:
- newMergeAtt
- svp_tool
- j_watercolumn
- jb_watercolumn
- orientation
- OMG_HDCS_jversion
module_name: sonar_geometry
header_path: code/subr/sonar_geometry.h
---

# sonar_geometry

## Overview
`sonar_geometry` (`sonar_geometry.c` / `sonar_geometry.h`, >3,100 lines) is the master 3D multibeam and single-beam **sounding reduction and geolocation engine** of the Ocean Mapping Group suite. Given an OMG-HDCS `.merged` file (and its companion `.orientation`, `.param`, `.sectors`, `.surf_ss`, `.sonar_settings`, `.mech_pitch`, `.watercol`, and optional delayed-heave files), `sonar_geometry` reconstructs the full transmit (`tx`) and receive (`rx`) geometry for any `(ping_number, beam_number)` pair and reduces raw two-way travel time (`TWTT`) and array steering angles into 3D vessel-referenced (`x, y, z`) and geographic (`latitude, longitude, depth`) coordinates.

It handles over 25 distinct sonar architectures—including Mills Cross systems, dual-head tilted systems (EM3000D, EM2040D, R2Sonic), barrel arrays (Reson 8101/8111, 7101/7111), multi-sector deep-water systems (EM120, EM300, EM302, EM710, EM1002), interferometric staves (SEA SwathPlus, Submetrix ISIS), and single-beam sounders—while accounting for separate TX and RX epochs, 3D lever-arm rotations, non-orthogonal cone intersections, Snell's law beam repointing, and stratified water-column raytracing (including the Hamilton-Beaudoin iterative Harmonic Sound Speed method, `-travis`).

---

## Core Data Structure: `Sounding_Geometry`

`Sounding_Geometry` encapsulates both the **configuration controls** and the **intermediate/final solutions** for a sounding:

### File Handles & Configuration State
- **Companion Streams**: `merged_file`, `attitude_file` (`.orientation` or alternate GP102 file), `delayed_heave_file` (POS/MV GP111), `sector_file` (`.sectors`), `surf_ss_file` (`.surf_ss`), `sonar_settings_file` (`.sonar_settings` for Reson 7K / R2Sonic), `mech_pitch_file`, `watercol_file`.
- **HDCS Headers & Vessel Params**: `OMG_HDCS_summary_header summary`, `OMG_HDCS_profile_header profile`, `OMG_rational_profile rational_profile`, `OMG_HDCS_sonar_params sonar_parameters` (`.param`), `OMG_HDCS_tx_sector tx_sectors[100]`, `OMG_rational_beam rational_beams[1000]`.
- **Timing & Attitude**: `tx_time`, `rx_time`, `orientation_delay`, `drift` (clock drift), `tx_orientation`, `rx_orientation`, `tx_align`, `rx_align`, `align_tweak`, `uncrosstalk` / `gyro_offset`.
- **3D Lever Arms**: `tx_lever_arms`, `rx_lever_arms`, `tx_rotated_lever_arms`, `rx_rotated_lever_arms`, `tx_internal_sonar_offsets`, `rx_internal_sonar_offsets`, `heave_lever_arms` (for migrating heave from IMU to RP).
- **Steering & Draft**: `tx_steer`, `rx_steer`, `flip_tx_steer`, `flip_rx_steer`, `tx_steer_tweak`, `rx_steer_tweak`, `draft`, `nominal_draft`, `OWTT` ($\mu\text{s}$), `OWTT_scaler`.
- **Raytracing & Sound Speed**: `watercolumn svp`, `watercolumn svp_harmonic`, `raytrace_method`, `try_quicktrace`, `surface_sound_speed`, `use_ssp_on_raytrace`, `repoint_beams`, `repoint_from_wc`, `repoint_ssp`.
- **Hamilton-Beaudoin (`travis`) Extended Reduction**: `travis`, `travisRx`, `owttCorrected`, `Ray *hssRay`, `tx_draft`, `rx_draft`, `rx_along_extra`, `rx_across_extra`, `northSpeed`, `eastSpeed`, `trig_QT`, `sector_shotDelay`.

### Output Solutions
- **Cone Intersection Outputs**: `beamDepression` (degrees below horizontal), `beamAzimuth` (degrees relative to `reference_heading`).
- **Raytrace Outputs**: `depth` (m), `radial` (horizontal range, m), `final_depression_angle`.
- **Final Geolocation**: `x`, `y`, `z` (meters relative to vessel Reference Point), `latitude`, `longitude` (decimal degrees).

---

## Public Functions

| Function | Signature | Description |
|---|---|---|
| `init_sounding_geometry` | `int init_sounding_geometry(Sounding_Geometry *geometry)` | Zeroes the `Sounding_Geometry` struct, initializes the embedded `j_EM_watercolumn` (`wc_in`), sets `current_ping = -1`, and sets `OWTT_scaler = 1.0`. |
| `get_sounding_geometry` | `int get_sounding_geometry(Sounding_Geometry *geometry, char *filename, unsigned int ping_number, unsigned int beam_number)` | Lazily opens/caches companion files for `filename`, reads ping/beam records, interpolates `tx_orientation` (at transmit + sector offset) and `rx_orientation` (at transmit + sector offset + `2 * OWTT`), rotates 3D TX/RX/heave lever arms, and extracts sonar-specific `tx_steer`, `rx_steer`, `draft`, and `surface_sound_speed`. |
| `intersect_cones` | `int intersect_cones(Sounding_Geometry *geometry)` | Rotates ideal TX (`[1,0,0]`) and RX (`[0,1,0]`) array axis vectors by mount alignment (`tx_align`, `rx_align`) and vessel attitude (`tx_orientation`, `rx_orientation`), computes the non-orthogonality angle between TX at transmit and RX at receive, intersects the TX and RX steering cones, and populates `beamAzimuth` and `beamDepression`. |
| `intersect_cones_travis` | `int intersect_cones_travis(Sounding_Geometry *geometry)` | Implements the Hamilton-Beaudoin iterative 3D hyperbolic cone intersection and reverse Harmonic Sound Speed (HSS) raytracing algorithm (`-travis`), accounting for translational displacement (`dx, dy, dz`) of the receiver array between TX and RX epochs. |
| `reduce_sounding` | `int reduce_sounding(Sounding_Geometry *geometry)` | Executes the full reduction pipeline: optional Snell's law beam repointing (`repoint_angle`), cone intersection (`intersect_cones` or `intersect_cones_travis`), water-column raytracing (`raytrace` or harmonic `try_quicktrace`), lever-arm/heave/tide summation into `(x, y, z)`, and geographic projection into `(latitude, longitude)`. |
| `repoint_angle` | `float repoint_angle(float ssp1, float ssp2, float theta1)` | Applies Snell's law $\theta_2 = \arcsin\left(\frac{c_2}{c_1}\sin\theta_1\right)$ (in degrees) to re-steer array angles when substituting transducer sound speed. |
| `gimme_sector_offset` | `double gimme_sector_offset(int toolType, int mode, double reduced_angle)` | Returns empirical multi-sector transmit firing time offsets (in ms) for legacy Kongsberg EM300 and EM1002 depth modes when `.sectors` files are absent. |
| `print_sounding_geometry` | `int print_sounding_geometry(Sounding_Geometry *geometry)` | Prints a detailed diagnostic report of TX/RX epochs, alignments, attitudes, steering angles, rotated lever arms, draft, OWTT, depression, and azimuth. |
| `free_sounding_geometry` | `int free_sounding_geometry(Sounding_Geometry *geometry)` | Closes open file pointers and releases dynamically allocated buffers. |

---

## Architectural Role
`sonar_geometry` is the core physics engine behind [`newMergeAtt`](../omg/newMergeAtt.html) and [`svp_tool`](../JV/JV_svpedit.html). Centralizing all sonar-specific array geometries, sector firing delays, attitude interpolations, and cone intersections in `sonar_geometry.c` guarantees identical bathymetric reduction across interactive refraction editors and batch processing pipelines.
