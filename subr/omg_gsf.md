---
layout: default
title: omg_gsf
parent: Core Shared Libraries (subr)
module_name: omg_gsf
source_path: code/subr/omg_gsf.c
header_path: code/subr/omg_gsf.h
category: File Formats & Vendor Parsers
related_tools:
  - gsfTool
  - gsf2omg
  - gsf2orientation
  - gsf2svp
  - gsf2param
---

# omg_gsf

## Overview & Purpose

`omg_gsf` provides a native, big-endian binary reader and parser for the Generic Sensor Format (GSF, up to version 3.01) within the Ocean Mapping Group (OMG) software suite. Rather than depending on external third-party GSF libraries, `omg_gsf` implements direct binary packet inspection, dynamic buffer management, and sub-record unpacking for swath bathymetry pings, sound velocity profiles (SVPs), attitude time-series, sensor parameters, and processing parameters, including specialized support for Reson 8100-series subrecords and 12-bit/multi-byte beam intensity time-series (BRB intensity).

## Key Data Structures, Constants & Macros

### Record & Subrecord Identifiers

- **Top-Level Record IDs**:
  - `GSF_HEADER` (`1`), `GSF_SWATH_BATHYMETRY_PING` (`2`), `GSF_SOUND_VELOCITY_PROFILE` (`3`), `GSF_PROCESSING_PARAMETERS` (`4`), `GSF_SENSOR_PARAMETERS` (`5`), `GSF_COMMENT` (`6`), `GSF_HISTORY` (`7`), `GSF_NAVIGATION_ERROR` (`8`), `GSF_SWATH_BATHY_SUMMARY` (`9`), `GSF_SINGLE_BEAM_SOUNDING` (`10`), `GSF_HV_NAVIGATION_ERROR` (`11`), `GSF_ATTITUDE` (`12`).
  - `gsf_record_names[13]`: Static lookup array mapping record IDs to human-readable descriptions.
- **Swath Bathymetry Subrecord IDs**:
  - Array Subrecords (`1`–`21`): `GSF_MB_SUBREC_DEPTH_ARRAY` (`1`), `GSF_MB_SUBREC_ACROSS_TRACK_ARRAY` (`2`), `GSF_MB_SUBREC_ALONG_TRACK_ARRAY` (`3`), `GSF_MB_SUBREC_TRAVEL_TIME_ARRAY` (`4`), `GSF_MB_SUBREC_BEAM_ANGLE_ARRAY` (`5`), `GSF_MB_SUBREC_MEAN_CAL_AMPLITUDE_ARRAY` (`6`), `GSF_MB_SUBREC_MEAN_REL_AMPLITUDE_ARRAY` (`7`), `GSF_MB_SUBREC_ECHO_WIDTH_ARRAY` (`8`), `GSF_MB_SUBREC_QUALITY_FACTOR_ARRAY` (`9`), `GSF_MB_SUBREC_RECEIVE_HEAVE_ARRAY` (`10`), `GSF_MB_SUBREC_NOMINAL_DEPTH_ARRAY` (`14`), `GSF_MB_SUBREC_QUALITY_FLAGS_ARRAY` (`15`), `GSF_MB_SUBREC_BEAM_FLAGS_ARRAY` (`16`), `GSF_MB_SUBREC_SIGNAL_TO_NOISE_ARRAY` (`17`), `GSF_MB_SUBREC_BEAM_ANGLE_FORWARD_ARRAY` (`18`), `GSF_MB_SUBREC_VERTICAL_ERROR_ARRAY` (`19`), `GSF_MB_SUBREC_HORIZONTAL_ERROR_ARRAY` (`20`), `GSF_MB_SUBREC_INTENSITY_SERIES_ARRAY` (`21`).
  - `GSF_MB_SUBREC_SCALE_FACTORS` (`100`): Scale and offset descriptors for compressed integer beam arrays.
  - Sensor-Specific Subrecords (`102`–`276`): Includes `GSF_MB_SUBREC_RESON_8101_SPECIFIC` (`122`) through `GSF_MB_SUBREC_RESON_8160_SPECIFIC` (`127`), Simrad EM series (`103`–`107`, `111`, `118`–`120`, `128`), SeaBeam, Elac, and single-beam subrecords.

### Core Structs

- `GSF_Buffer`: Manages dynamically resized raw packet buffers (`unsigned char *buffer`, `size_buffer`, `size_record`).
- `GSF_Time`: Big-endian timestamp pair (`signed int seconds`, `signed int nanoseconds`).
- `GSF_Sound_Velocity_Profile`: Stores observation and application `GSF_Time`, scaled integer `longitude`/`latitude` ($10^7$), `num_points`, and dynamically allocated `depth` and `sound_speed` arrays (scaled by 100).
- `GSF_Attitude`: Contains `basetime`, `num_points`, and dynamically allocated arrays for `time_offset` (ms), `pitch`, `roll`, `heave`, and `heading` (scaled by 100).
- `GSF_Sensor_Parameters` / `GSF_Processing_Parameters`: Stores timestamp, parameter count, and dynamically allocated `char **parameters` string arrays (`KEY=VALUE` format).
- `GSF_Scale_Factor`: Stores `compression_flag`, `scale_factor`, and `offset` for decoding quantized beam fields.
- `GSF_Reson_8100`: Sensor-specific metadata for Reson 8101/8125 sonars (`latency`, `ping_number`, `sonar_id`, `sonar_model`, `frequency`, `surface_sound_speed`, `sample_rate`, `ping_rate`, `mode`, `range`, `tx_power`, `rx_gain`, `pulse_width`, TVG coefficients, beamwidths, projector type/angle, range/depth filters, `temperature`, and `valid` flag).
- `GSF_BRB_Intensity`: Bottom Return Bathymetry intensity header (`bits_per_sample`, `applied_corrections`, `spare[16]`, `reson_8100_spare[8]`).
- `GSF_Beam`: Per-beam data (`depth`, `across`, `along`, `travel_time`, `beam_angle`, `relative_amplitude`, `quality_factor`, `flag`) plus snippet imagery (`sample_count`, `detect_sample`, `intensity` array).
- `GSF_Swath_Bathymetry_Ping`: Master ping record combining navigation, attitude, version 3.01 ellipsoid/GPS tide fields (`height_above_ellipsoid`, `ellipsoid_datum_separation`, `gps_tide_corrector`), `scale_factors[255]`, `GSF_Reson_8100`, `GSF_BRB_Intensity`, and dynamically allocated `GSF_Beam *beams`.

## Public Functions & Signatures

### Buffer & Packet Navigation
- `int init_GSF_Buffer(GSF_Buffer *buffer)` / `int grow_GSF_Buffer(GSF_Buffer *buffer, unsigned int new_size)` / `int free_GSF_Buffer(GSF_Buffer *buffer)`
  - Initializes, dynamically reallocates, or frees the raw byte buffer.
- `int peek_GSF_packet(FILE *infile, int *record_id, int *record_size)`
  - Reads the 4-byte big-endian record size and 4-byte record ID field at the current file position. Checks bit 31 (`0x80000000`) for an optional 4-byte checksum and masks the lower 12 bits (`0x00000FFF`) to extract `*record_id`.
- `int seek_GSF_packet(FILE *infile, int desired_record_id, GSF_Buffer *buffer)`
  - Scans forward through `infile` using `peek_GSF_packet`, skipping non-matching records with `fseek` (checking against file size to avoid seeking past EOF), and reads the first matching packet payload into `buffer`. Warns if `record_size` is not a multiple of 4 bytes.

### Record Lifecycle (`init_*`, `parse_*`, `print_*`, `free_*`)
- `GSF_Sound_Velocity_Profile`:
  - `init_GSF_Sound_Velocity_Profile`, `parse_GSF_Sound_Velocity_Profile`, `print_GSF_Sound_Velocity_Profile`, `free_GSF_Sound_Velocity_Profile`
  - Unpacks big-endian observation/application timestamps, coordinates, and reallocates/populates depth and sound speed arrays.
- `GSF_Attitude`:
  - `init_GSF_Attitude`, `parse_GSF_Attitude`, `print_GSF_Attitude`, `free_GSF_Attitude`
  - Unpacks base time and arrays of 16-bit time offsets, pitch, roll, heave, and heading measurements.
- `GSF_Sensor_Parameters` & `GSF_Processing_Parameters`:
  - `init_GSF_Sensor_Parameters`, `parse_GSF_Sensor_Parameters`, `print_GSF_Sensor_Parameters`, `free_GSF_Sensor_Parameters`
  - `init_GSF_Processing_Parameters`, `parse_GSF_Processing_Parameters`, `print_GSF_Processing_Parameters`, `free_GSF_Processing_Parameters`
  - Unpacks length-prefixed ASCII parameter strings from the GSF buffer and appends null terminators.
- `GSF_Swath_Bathymetry_Ping`:
  - `init_GSF_Swath_Bathymetry_Ping`, `parse_GSF_Swath_Bathymetry_Ping`, `print_GSF_Swath_Bathymetry_Ping`, `free_GSF_Swath_Bathymetry_Ping`
  - Unpacks the fixed ping header (including v3.01 ellipsoid/GPS tide fields) and iterates through all 4-byte aligned subrecords in the packet (`sub_record_id = (field & 0xFF000000) >> 24`, `sub_record_size = field & 0x00FFFFFF`). Unpacks `SCALE_FACTORS`, beam arrays, Reson 8101/8125 specific parameters, and `INTENSITY_SERIES_ARRAY` (including 12-bit packed nibbles unpacked 3 bytes at a time into two 32-bit integers, as well as 1-, 2-, and 4-byte samples).

## How It Fits Into the OMG Architecture

`omg_gsf` underpins the `code/gsf/` conversion and inspection suite:
- **`gsf2omg`**: Converts GSF swath bathymetry and Reson 8100 series packets into OMG HDCS bathymetry and backscatter files.
- **`gsfTool`**: Inspects and dumps GSF packet summaries and record contents using the `print_GSF_*` routines.
- **`gsf2orientation`**, **`gsf2svp`**, and **`gsf2param`**: Extract attitude records, sound velocity profiles, and sensor/processing parameters into standalone OMG orientation, SVP, and parameter files.
