---
layout: default
title: reson_7K_utils
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/reson_7K_utils.c
category: Multibeam Vendor Parsers
related_tools:
- 7k2omg
- 7k2nav
- 7k2orientation
- getAngularResponse
- omg2gsf
module_name: reson_7K_utils
header_path: code/subr/reson_7K_utils.h
---

# `reson_7K_utils` — Reson 7K to OMG HDCS Conversion Utilities

## Overview & Purpose

The `reson_7K_utils` module (`code/subr/reson_7K_utils.c` and `code/subr/reson_7K_utils.h`) bridges low-level Teledyne Reson 7K Data Format records (`reson_7K.h`) and the internal Ocean Mapping Group (OMG) data structures (`OMG_HDCS_jversion.h`, `jcu_nav.h`, and `j_EM_watercol.h`).

It provides conversion functions that translate Reson 7K timestamps, navigation (Record 1003), roll/pitch/heave orientation (Record 1012), heading (Record 1013), attitude time series (Record 1016), and beamformed water-column/image data (Records 7011 and 7018) into standard OMG HDCS records. It also provides random-access loading of auxiliary `.sonar_settings` sidecar files via byte offsets stored in `OMG_HDCS_profile_header`.

---

## Public Functions & Signatures

### 1. Sidecar Settings & Time Conversion

- **`int load_7K_sonar_settings(FILE *sonar_settings_file, OMG_HDCS_profile_header *profile, Reson_7K_7000_Sonar_Settings *sonar_settings)`**
  Seeks to `profile->sonar_settings_offset` in the open `.sonar_settings` sidecar file and calls `read_Reson_7K_7000_Sonar_Settings()` to load the ping's full `Reson_7K_7000_Sonar_Settings` record. Returns `0` on success or `1` if `sonar_settings_file` is `NULL`.
- **`double convert_7K_time(Reson_7K_DRF *drf)`**
  Converts the Reson 7K Data Record Frame (`Reson_7K_DRF`) timestamp (`year`, `jday`, `hour`, `minute`, `seconds`) into double-precision Unix epoch seconds using `stdtime_from_jul_day()`.

### 2. Navigation & Attitude Conversion

- **`int convert_7K_position(Reson_7K_DRF *drf, Reson_7K_1003_Position *position, jcu_nav_rec *nav)`**
  Converts a Reson 7K 1003 Position record (when `position->type_flag == 0`, geographical coordinates in radians) into a `jcu_nav_rec` structure:
  - Converts `latitude` and `longitude` from radians to decimal degrees.
  - Stores `position->height` into `nav->azi`.
  - Computes integer seconds (`nav->time`) and hundredths of a second (`nav->centisecs`) from `convert_7K_time(drf)`.
- **`int convert_7K_orientation(Reson_7K_DRF *drf, Reson_7K_1012_Orientation *orientation, OMG_HDCS_summary_attitude *attitude_summary, OMG_HDCS_attitude *attitude)`**
  Converts a Reson 7K 1012 Roll/Pitch/Heave record into an `OMG_HDCS_attitude` structure:
  - Computes `timeOffset` relative to `attitude_summary->refTime` and `attitude_summary->timeScale`.
  - Converts `roll` and `pitch` from radians to hundredths of a degree (`short`), and `heave` from meters to centimeters (`short`).
- **`int convert_7K_heading(Reson_7K_DRF *drf, Reson_7K_1013_Heading *heading, OMG_HDCS_summary_attitude *heading_summary, OMG_HDCS_attitude *heading_out)`**
  Converts a Reson 7K 1013 Heading record from radians into hundredths of a degree (`heading_out->heading`) with corresponding HDCS `timeOffset`.
- **`int convert_7K_attitude(Reson_7K_DRF *drf, Reson_7K_1016_Attitude_sample *orientation, OMG_HDCS_summary_attitude *attitude_summary, OMG_HDCS_attitude *attitude)`**
  Converts a single sample from a Reson 7K 1016 Attitude record (adding `orientation->time_offset / 1000.0` seconds to the DRF timestamp) into an `OMG_HDCS_attitude` struct containing `roll`, `pitch`, `heave`, and `heading`.

### 3. Water Column Conversion

- **`int convert_7K_watercolumn(Reson_7K_DRF *drf, Reson_7K_7011_Image_Data *image, Reson_7K_7018_Beamformed_Data *watercolumn, OMG_HDCS_beam *beams, Reson_7K_7000_Sonar_Settings *settings, j_EM_watercolumn *watercolumn_out)`**
  Initializes and populates an OMG `j_EM_watercolumn` structure from either a Reson 7K 7018 Beamformed Data record (`watercolumn`) or a 7011 Image Data record (`image`), using `Reson_7K_7000_Sonar_Settings` for sound velocity, sampling rate, projector vertical steering, and center frequency, and `beams[beam].Rc_steer` for beam pointing angles. Converts 16-bit linear amplitudes from Record 7018 into half-dB `signed char` values via $2 \times 20 \log_{10}(\text{amplitude} + 1)$.
- **`int convert_7K_watercolumn_orig(Reson_7K_DRF *drf, Reson_7K_7018_Beamformed_Data *watercolumn, Reson_7K_7004_Beam_Geometry *geometry, Reson_7K_7000_Sonar_Settings *settings, j_EM_watercolumn *watercolumn_out)`**
  Earlier variant of `convert_7K_watercolumn` that derives beam pointing angles directly from a Reson 7K 7004 Beam Geometry record (`-1 * geometry->beams[beam].beam_horizontal_direction_angle` in hundredths of a degree) rather than an `OMG_HDCS_beam` array.

---

## How It Fits Into the OMG Architecture

- **7K Ingestion Tools (`reson/7k2omg.c`, `reson/7k2nav.c`, `reson/7k2orientation.c`)**: Use `convert_7K_position`, `convert_7K_orientation`, `convert_7K_heading`, `convert_7K_attitude`, and `convert_7K_watercolumn` to convert raw `.s7k` files into OMG `.merged`, `.nav`, `.orientation`, and `.wcd` files.
- **Sonar Geometry & Backscatter Calibration (`subr/sonar_geometry.c`, `subr/Echo_calib.c`, `omg/getAngularResponse.c`, `gsf/omg2gsf.c`)**: Call `load_7K_sonar_settings()` to retrieve per-ping 7K sonar settings from `.sonar_settings` sidecar files during beam footprint and backscatter calibration.
