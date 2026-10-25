---
layout: default
title: omg_fmgt
parent: Core Shared Libraries (subr)
module_name: omg_fmgt
source_path: code/subr/omg_fmgt.c
header_path: code/subr/omg_fmgt.h
category: Backscatter Mosaicking & Fledermaus FMGT Interoperability
related_tools:
  - makess
  - correctBS
  - FMGT / geocoder interoperability utilities
---

# `omg_fmgt` — QPS Fledermaus Geocoder Toolbox (FMGT) Backscatter Structure Definitions

## Overview & Purpose in the OMG Architecture

`omg_fmgt` (`code/subr/omg_fmgt.c`, `code/subr/omg_fmgt.h`) defines the binary data structures required to read, write, and interoperate with **Fledermaus Geocoder Toolbox (FMGT)** backscatter project files, sonar offset configurations, ping headers, and angular response / beam-pattern tables.

Originally developed by Luciano Fonseca (UNH/CCOM) and integrated into IVS3D/QPS Fledermaus, FMGT/Geocoder uses specific binary structures to store per-ping radiometric metadata (`fmgt_ping_header`), file-level backscatter indexing (`fmgt_backscatter_header`), dual-head sonar lever arms and calibration parameters (`fmgt_sonar_offsets`), line-level mosaic bounds and angular averages (`fmgt_sonar_header`), and 181-angle ($-90^\circ$ to $+90^\circ$) beam-pattern correction tables (`fmgt_beam_pattern`). `omg_fmgt` exposes these exact C structs to the OMG codebase so OMG backscatter tools can inspect or exchange calibration and time-series data with FMGT.

---

## Key Constants & Data Structures (`code/subr/omg_fmgt.h`)

### Constants
- `FGT_ANGLES` (`181`): Number of discrete $1^\circ$ incidence angle bins ($-90^\circ$ through $0^\circ$ to $+90^\circ$) stored in FMGT angular response and beam-pattern arrays.

### Core Structs

#### `fmgt_ping_header`
Per-ping navigation, geometry, and radiometric gain header for a backscatter trace:
- **Position & Timing**: `unsigned short ok`, `npels` (number of pixels), `double secs1970` (Unix epoch timestamp), `utm_n`, `utm_e` (UTM Northing and Easting in m), `utm_azi` (heading in radians).
- **Sonar & Radiometric Parameters**: `float fishdepth`, `alt`, `sound_vel`, `unsigned short gain`, `short power`, `unsigned short pw` (pulse width), `tvg_applied`, `gain_auto`, `signed int ping_number`, `float slant`, `spreading`, `absorption`, `layback`, `row`, `short roll`.
- **Mosaic & Editing State**: `unsigned short tile`, `data_type`, `signed int patchId`, `short pad1`, `signed char pingOffset`, `userEditFlag`.

#### `fmgt_backscatter_header`
File-level header describing an FMGT backscatter data file and coordinate reference system:
- `unsigned int marker`, `version`, `flagMask`, `preProcessMask`.
- `unsigned int numBathyPings`, `numBackscatterPings`, `numPatches`, `patchDecimation`, `numRangeAngle`.
- `unsigned int bathyDatagramId`, `backscatterDatagramId`, `rangeAngleDatagramId`.
- `unsigned int numAllocatedPings`, `numAllocatedNavigation`.
- `char filename[1024]`, `wktIn[1024]`, `wktOut[1024]`: Source file path and input/output Well-Known Text (WKT) coordinate system strings.

#### `fmgt_sonar_offsets`
Comprehensive dual-head sonar mounting lever arms, angular offsets, and radiometric calibration constants:
- **Identification**: `device_type`, `packetModelNumber`, `dual_head`, `sonarName[128]`, `default_sonar_id`, `head1SerialNumber`, `head2SerialNumber`.
- **Head 1 & Head 2 Lever Arms & Attitude Offsets**: `S1X`, `S1Y`, `S1Z`, `S1H`, `S1R`, `S1P`, `P1X`, `P1Y`, `P1Z` and `S2X`, `S2Y`, `S2Z`, `S2H`, `S2R`, `S2P`, `P2X`, `P2Y`, `P2Z`.
- **Acoustic & Radiometric Calibration**: `absorbcoef`, `absorbcorr`, `db_reference_head_1`, `db_reference_head_2`, `gain_port`, `gain_stbd`, `power`, `gain`, `spreading`, `pulseWidth`, `mosaicPixelSize`, `surfaceSoundSpeed`, `mbPixel`, `maxbeams`, `freq_1`, `freq_2`, `max_angle`, `x_beam_width`, `a_beam_width`, `samp_freq_1`, `samp_freq_2`, `default_samp_freq`, `min_pulse_width`.
- **Backscatter TVG Crossover Parameters**: `ob_bs1`, `ob_bs2` (oblique backscatter dB), `ni_bs1`, `ni_bs2` (normal incidence backscatter dB), `r_ni1`, `r_ni2`, `tvg_xover1`, `tvg_xover2`.

#### `fmgt_sonar_header`
Survey line summary header containing spatial bounds, processing flags (`apply_avg`, `lambert`, `swap_bytes`, `apply_gains`, `apply_area`, `apply_spreading`), and 181-bin angular response accumulators (`total_avg[181]`, `count_avg[181]`, `total_avg_hard[181]`, `total_avg_soft[181]`).

#### `fmgt_beam_pattern`
Stores a 181-bin (`FGT_ANGLES`) beam pattern curve (`double total[181]`, `unsigned int count[181]`, `back_mean`, `back_count`), ping range (`ping_ini`, `ping_fin`), AVO/histogram flags, roll/pitch gates (`minRoll`, `maxRoll`, `minPitch`, `maxPitch`), and angle cutoffs (`initAngle`, `cutoffAngle`).

---

## Public Functions & Signatures

- `int dummy_fmgt_function()`
  Placeholder linkage symbol in `code/subr/omg_fmgt.c` (returns `0`) so `omg_fmgt.o` compiles cleanly into the shared `libsubr` archive alongside the header definitions in `omg_fmgt.h`.

---

## How It Fits Into the OMG Architecture

`omg_fmgt` provides binary layout compatibility with QPS Fledermaus FMGT / Geocoder files for OMG backscatter research and cross-comparison tools.
