---
layout: default
title: reson_7K
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/reson_7K.c
category: File Formats & Vendor Parsers
related_tools:
- 7kTool
- 7k2omg
- 7k2nav
- 7k2orientation
- 7k2image
- 7kStrip
- 7kTVG
- 7k_reflectivity_check
- omg2gsf
- swathed (SE)
module_name: reson_7K
header_path: code/subr/reson_7K.h
---

# reson_7K

## Overview & Purpose

`reson_7K` is the primary binary parser and chronological packet indexer for Teledyne Reson 7K (`.s7k` and `.7k`) Data Format files produced by SeaBat 7101, 7111, 7125, 7150, 7160, and T20/T50 multibeam systems. Every 7K record is wrapped in a 64-byte Data Record Frame (`Reson_7K_DRF`) containing the little-endian sync pattern `0x0000FFFF`, packet size, timestamp, and record type ID (optionally preceded by a 36-byte Network Frame `Reson_7K_NF`). `reson_7K` provides full binary parsers for navigation, attitude, sonar settings, beam geometry, bathymetry, sidescan, snippets, TVG curves, water-column beamformed amplitude/phase, raw element I/Q data, and remote control settings, along with a binary-searchable file indexer (`Reson_7K_Index`).

## Key Data Structures, Constants & Macros

### Constants
- `RESON_7K_SYNC_PATTERN` (`0x0000FFFF`): 32-bit little-endian sync marker at byte offset 4 of every `Reson_7K_DRF`.
- Array & ID Limits: `MAX_7K_RECORD_ID` (`8000`), `RESON_7K_MAX_NUM_BEAMS` (`1000`), `RESON_7K_MAX_NUM_BEAM_SAMPLES` (`10000`), `RESON_7K_MAX_NUM_BACKSCATTER_SAMPLES` (`15000`).
- Fixed Record Header Sizes: `RESON_7K_NF_SIZE` (`36`), `RESON_7K_DRF_SIZE` (`64`), `RESON_7K_1003_SIZE` (`36`), `RESON_7K_1012_SIZE` (`12`), `RESON_7K_1013_SIZE` (`4`), `RESON_7K_1016_SIZE` (`4`), `RESON_7K_1016_SAMPLE_SIZE` (`18`), `RESON_7K_7000_SIZE` (`156`), `RESON_7K_7004_SIZE` (`12`), `RESON_7K_7006_SIZE` (`24`), `RESON_7K_7007_SIZE` (`64`), `RESON_7K_7008_SIZE` (`30`), `RESON_7K_7010_SIZE` (`50`), `RESON_7K_7011_SIZE` (`56`), `RESON_7K_7018_SIZE` (`44`), `RESON_7K_7027_SIZE` (`99`), `RESON_7K_7028_SIZE` (`46`), `RESON_7K_7038_SIZE` (`60`), `RESON_7K_7503_SIZE` (`260`).

### Core Structs
- **Framing & Indexing**:
  - `Reson_7K_NF`: 36-byte Network Frame header (`protocol_version`, `offset`, `total_packets`, `total_records`, `transmission_id`, `packet_size`, `total_size`, `sequence_number`, source/destination device IDs).
  - `Reson_7K_DRF`: 64-byte Data Record Frame (`protocol_version`, `offset`, `synch_header`, `size`, `optional_data_offset`, `optional_data_id`, `year`, `jday`, `seconds`, `hour`, `minute`, `record_type_id`, `device_id`, `system_enumerator`, `flags`, `total_records`, `fragment_number`, `check_sum`, `bytes_on_disk`).
  - `Reson_7K_Index_Element` & `Reson_7K_Index`: Per-record-type arrays of `(double time, unsigned long file_offset)` sorted chronologically for fast binary search.
- **Navigation & Attitude Records (1000-series)**:
  - `Reson_7K_1003_Position`: `datum_id`, `latency`, `latitude` (rad), `longitude` (rad), `height` (m), `type_flag`, `utm_zone`, `quality_flag`, `method`.
  - `Reson_7K_1012_Orientation`: `roll`, `pitch`, `heave` (radians/meters).
  - `Reson_7K_1013_Heading`: `heading` (radians).
  - `Reson_7K_1016_Attitude` & `Reson_7K_1016_Attitude_sample`: Up to 256 high-rate samples of `(time_offset, roll, pitch, heave, heading)`.
- **Sonar Settings, Bathymetry, Imagery & Water Column (7000-series)**:
  - `Reson_7K_7000_Sonar_Settings`: 156-byte operating parameters (`frequency`, `sample_rate`, `receiver_bandwidth`, `pulse_width`, `pulse_type_id`, `pulse_envelope_id`, `range`, `power`, `gain`, `control_flags`, projector steering/beamwidths/weighting, hydrophone weighting/beamwidth, range/depth gates, `absorption`, `sound_velocity`, `spreading`, plus verbatim `raw_buffer[156]` for `.sonar_settings` files).
  - `Reson_7K_7004_Beam_Geometry`: Per-beam vertical/horizontal direction angles and along/across-track beamwidths (`Reson_7K_7004_Beam_Data`).
  - `Reson_7K_7006_Bathymetry`: Processed two-way travel time `range`, `quality` bitmask, `intensity`, and min/max filters (`Reson_7K_7006_Beam_Data`).
  - `Reson_7K_7007_Backscatter`: Port/starboard 8-bit or 16-bit sidescan time-series (`port_samples_8/16`, `stbd_samples_8/16`).
  - `Reson_7K_7008_Generic_Data`: Legacy snippet/water-column record (`Reson_7K_7008_Record_Data` with `first_sample`, `last_sample`, `magnitude_16`).
  - `Reson_7K_7010_TVG`: Real-time Time Varying Gain curve (`num_samples`, `float *tvg_gain` in dB).
  - `Reson_7K_7011_Image_Data` & `Reson_7K_7018_Beamformed_Data`: 2D water-column image (`amplitude[][]`) and 16-bit beamformed `amplitude[beam][sample]` + `phase[beam][sample]`.
  - `Reson_7K_7027_Bathymetry`: Raw detection data in samples (`beam_descriptor`, `range`, `rx_angle`, `flags`, `quality`, `uncertainty`, `signal_strength`, `tx_angle`, `sampling_rate`).
  - `Reson_7K_7028_Snippet`: Snippet time-series per beam (`beam_descriptor`, `snippet_start`, `detection_sample`, `snippet_end`, `unsigned short *snippets`).
  - `Reson_7K_7038_RawIQ`: Raw hydrophone element quadrature (`real[][]`, `imaginary[][]`) samples.
  - `Reson_7K_7503_Remote_Control_Settings`: 260-byte remote control settings record.

## Public Functions & Signatures

- **Indexing & Synchronization**:
  - `int seek_next_7K_sync(FILE *infile)`: Scans for little-endian `0x0000FFFF` and rewinds 8 bytes to the start of the `Reson_7K_DRF`.
  - `char *get_7K_record_name(int rec)`: Returns human-readable name for record IDs `1003`–`7503`.
  - `init_Reson_7K_Index`, `build_Reson_7K_Index`, `search_Reson_7K_Index`, `print_Reson_7K_Index`, `free_Reson_7K_Index`, `compare_index_elements`: Builds a per-record-type offset index sorted by timestamp (`convert_7K_time`) and performs binary search (with linear fallback) for any record ID and target timestamp.
- **Record Parsers (`init_*`, `read_*`, `print_*`, `free_*`)**:
  - Framing: `Reson_7K_NF`, `Reson_7K_DRF`
  - Navigation/Motion: `Reson_7K_1003_Position`, `Reson_7K_1012_Orientation`, `Reson_7K_1013_Heading`, `Reson_7K_1016_Attitude`
  - Acoustic/Sonar: `Reson_7K_7000_Sonar_Settings`, `Reson_7K_7004_Beam_Geometry`, `Reson_7K_7006_Bathymetry`, `Reson_7K_7007_Backscatter`, `Reson_7K_7008_Generic_Data`, `Reson_7K_7010_TVG`, `Reson_7K_7011_Image_Data`, `Reson_7K_7018_Beamformed_Data`, `Reson_7K_7027_Bathymetry`, `Reson_7K_7028_Snippet`, `Reson_7K_7038_RawIQ`, `Reson_7K_7503_Remote_Control_Settings`.

## How It Fits Into the OMG Architecture

`reson_7K` is the foundation of the `code/reson/` toolset (`7kTool`, `7k2omg`, `7k2nav`, `7k2orientation`, `7k2image`, `7kStrip`, `7kTVG`, `7k_reflectivity_check`, `8kTool`), `code/gsf/` (`omg2gsf`, `gsf2omg_7101`), `code/SE/` (`swathed`), and the companion `subr/` modules `reson_7K_utils`, `reson_7K_TVG`, `reson_calibration`, `Echo_calib`, and `sonar_geometry`.
