---
layout: default
title: omg_sbet
parent: Core Shared Libraries (subr)
module_name: omg_sbet
source_path: code/subr/omg_sbet.c
header_path: code/subr/omg_sbet.h
category: Navigation, Attitude & Geodesy
related_tools:
  - sbet2nav
---

# omg_sbet

## Overview & Purpose

`omg_sbet` reads and converts Applanix POSPac SBET (Smoothed Best Estimate of Trajectory) binary files into Ocean Mapping Group (OMG) navigation (`jcu_nav_rec`) and HDCS attitude (`OMG_HDCS_attitude`) structures. Post-processed inertial/GNSS trajectory files in SBET format consist of packed 136-byte records of 17 IEEE-754 little-endian double-precision floats representing high-rate time, position, ellipsoidal height, 3D velocities, Euler attitude angles, wander angle, body accelerations, and angular rates.

## Key Data Structures, Constants & Macros

### Constants
- `OMG_SBET_SIZE` (`136` bytes): Exact on-disk byte size of a single binary SBET record ($17 \times 8$-byte `double` fields).

### Data Structures
- `OMG_SBET`: Unpacked in-memory representation of a single SBET epoch:
  - `double gps_time`: GPS seconds of the week.
  - `double latitude`: Latitude in radians.
  - `double longitude`: Longitude in radians.
  - `double altitude`: Ellipsoidal height (meters).
  - `double x_velocity`, `double y_velocity`, `double z_velocity`: North, East, and Down velocities (m/s).
  - `double roll`, `double pitch`, `double platform_heading`, `double wander_angle`: Attitude and wander angles in radians.
  - `double x_acceleration`, `double y_acceleration`, `double z_acceleration`: Body frame accelerations ($\text{m/s}^2$).
  - `double x_angular_rate`, `double y_angular_rate`, `double z_angular_rate`: Angular rates ($\text{rad/s}$).

## Public Functions & Signatures

- `int init_OMG_SBET(OMG_SBET *sbet)`
  - Zero-initializes an `OMG_SBET` structure using `memset`.
- `int read_OMG_SBET(OMG_SBET *sbet, FILE *infile)`
  - Reads `OMG_SBET_SIZE` (136) bytes from `infile` and unpacks all 17 little-endian `double` fields into `sbet` via `get_LE_double()` from `jb_endian.h`.
- `int print_OMG_SBET(OMG_SBET *sbet)`
  - Prints a single-line summary of the SBET record (`gps_time`, `latitude`, `longitude`, `altitude`, `roll`, `pitch`, `platform_heading`) to `stdout`.
- `int convert_OMG_SBET(double base_time, OMG_SBET *sbet, jcu_nav_rec *nav, OMG_HDCS_attitude *orientation, OMG_HDCS_summary_attitude *orientation_header)`
  - Converts a raw `OMG_SBET` record into OMG navigation and attitude records:
    1. **Time**: Adds `sbet->gps_time` (GPS seconds of week) to `base_time` (Unix epoch of the start of the GPS week). Splits the result into integer seconds (`nav->time`) and truncated centiseconds (`nav->centisecs = (int)((time - (int)time) * 100.0)`), ensuring compatibility with `thin_nav`.
    2. **Position & Ellipsoidal Height**: Converts `latitude` and `longitude` from radians to decimal degrees ($\times 180/\pi$) and stores ellipsoidal `altitude` in `nav->azi` (the convention expected by `mergeTide` for GPS tide/height processing).
    3. **Attitude**: Computes `orientation->timeOffset` relative to `orientation_header->refTime * 100.0` scaled by `orientation_header->timeScale`. Converts `roll`, `pitch`, and `platform_heading` from radians to hundredths of a degree ($\times 100 \times 180/\pi$), wrapping heading into $[0^\circ, 360^\circ]$.

## How It Fits Into the OMG Architecture

`omg_sbet` is used by **`sbet2nav`** (`code/jonnyb/gom_stuff/sbet2nav.c`) to ingest post-processed Applanix SBET trajectories and simultaneously generate `.nav` (`jcu_nav` format for `mergeNav` and `mergeTide`) and `.orientation` (OMG HDCS attitude format for `newMergeAtt`) files.
