---
layout: default
title: omg_r2sonic
parent: Core Shared Libraries (subr)
module_name: omg_r2sonic
source_path: code/subr/omg_r2sonic.c
header_path: code/subr/omg_r2sonic.h
category: File Formats & Vendor Parsers
related_tools:
  - r2sonicTool
  - r2sonic2omg
  - r2sonic2image
  - r2sonic_extract_truepix
  - xtf2omg_r2sonic
  - xtfTool
  - omg2gsf
  - swathed (SE)
---

# omg_r2sonic

## Overview & Purpose

`omg_r2sonic` is the comprehensive binary parser, packet indexer, and radiometric backscatter calibrator for R2Sonic Sonic 2020/2022/2024/2026 multibeam echosounder data streams (both standalone `.r2s` files and packets embedded within XTF files). It supports all four major R2Sonic big-endian packet families—Bathymetry (`BTH0`), Footprints/Snippets (`SNI0`/`FTS`), TruePix sidescan/3D angle+magnitude time-series (`TPX0`), and Water Column Data (`WCD0`)—including fragmented packet reassembly, fast multi-packet ping indexing (with dual-head serial number awareness), and full radiometric calibration (`calibrate_r2sonic`) of both snippets and TruePix imagery.

## Key Data Structures, Constants & Macros

### Constants & Packet Types
- `R2SONIC_MAX_NUM_BEAMS` (`512`), `R2SONIC_MAX_NUM_SNIPPET_SAMPLES` (`100`), `R2SONIC_MAX_NUM_WCD_SAMPLES` (`65535`).
- Fixed Header Sizes: `R2SONIC_WCD_HEADER_SIZE` (`12`), `R2SONIC_WCD_H0_SIZE` (`116`), `WCD_CHUNK_SIZE` (`36`), `R2SONIC_FTS_HEADER_SIZE` (`12`), `R2SONIC_FTS_H0_SIZE` (`140`), `FTS_SNIPPET_SIZE` (`32`), `R2SONIC_BATHY_HEADER_SIZE` (`12`), `R2SONIC_BATHY_H0_SIZE` (`116`), `R2SONIC_TRUEPIX_HEADER_SIZE` (`12`), `R2SONIC_TRUEPIX_H0_SIZE` (`140`).
- Index Packet Type IDs (`R2SONIC_MAX_NUM_PACKET_TYPES` = `5`):
  - `R2SONIC_ID_BTH0` (`0`), `R2SONIC_ID_SNI0` (`1`), `R2SONIC_ID_TPX0` (`2`), `R2SONIC_ID_WCD0` (`3`), `R2SONIC_ID_AIM0` (`4`).

### Core Structs
- **Bathymetry (`BTH0`)**:
  - `R2SONIC_BATHY_H0`: 116-byte `H0` section containing `model_number`, `serial_number`, `time_seconds`, `time_nanoseconds`, `ping_number`, `ping_period`, `sound_speed`, `frequency`, `tx_power`, `tx_pulse_width`, vertical/horizontal beamwidths and steering angles, `tx_misc_info`, `tx_voltage_error`, `rx_bandwidth`, `rx_sample_rate`, `rx_range`, `rx_gain`, `rx_spreading`, `rx_absorption`, `rx_mount_tilt`, `rx_misc_info`, `num_beams`, and verbatim `rawdata[116]` buffer.
  - `R2SONIC_Beam`: Per-beam decoded `range`, `twtt`, `angle`, `quality`, and `intensity`.
  - `R2SONIC_BATHY`: Top-level `BTH0` packet combining `R2SONIC_BATHY_H0`, dynamic `R2SONIC_Beam *beam`, and section parameters from `R0` (range scaling), `A0` (equi-angle), `A2` (equi-distant), `G0` (depth gates), and `I1` (intensity scaling).
- **Snippets (`SNI0` / `FTS`)**:
  - `R2SONIC_FTS_H0`: 140-byte `H0` section (adds `num_snippets` and `float more_info[6]`).
  - `R2SONIC_FTS_Beam`: `S1` snippet section (`ping_number`, `snippet_number`, `num_samples`, `first_sample`, `angle`, `scaling_factor_first`, `scaling_factor_last`, and `unsigned short *samples`).
  - `R2SONIC_FTS`: Top-level snippet packet supporting fragmented packet reassembly across multiple `S1` blocks.
- **TruePix (`TPX0`)**:
  - `R2SONIC_TRUEPIX_H0`: 140-byte `H0` header.
  - `R2SONIC_TRUEPIX`: Unpacks `D0` (magnitude-only port/stbd time-series) and `D1` (magnitude + angle port/stbd time-series with `D1_MagnitudeScaling[8]` and `D1_AngleScalingFactor`).
- **Water Column (`WCD0`)**:
  - `R2SONIC_WCD_H0`, `R2SONIC_WCD_Chunk` (`M1` amplitude-only or `M2` amplitude + phase chunk), `R2SONIC_WCD_Beam`, and `R2SONIC_WCD` (including `A1` beam angle array).
- **Packet Indexer & Calibrator**:
  - `R2SONIC_INDEX_ELEMENT` & `R2SONIC_INDEX`: Stores file offsets, packet types, serial numbers, timestamps, and ping numbers across all 5 packet streams, detecting dual-head configurations (`got_dual_head`).
  - `R2Sonic_Calibrator`: State for snippet and TruePix backscatter calibration (`data_in`, `data_out`, `ensonified_areas`, `sonar_settings_snippets`, `sonar_settings_truepix`, `do_truepix`, `do_snippets`, `grazing_angles`, `dB_shift`, `dB_scale`, `new_attenuation_coefficient`, `min_gain`, `max_gain`, `conversion_factor`, `skip_all_corrections`, `apply_snippet_bp`).

## Public Functions & Signatures

- **Packet Readers (`init_*`, `read_*`, `print_*`)**:
  - `init_R2SONIC_BATHY`, `read_R2SONIC_BATHY`, `print_R2SONIC_BATHY`, `read_R2SONIC_BATHY_H0`
  - `init_R2SONIC_FTS`, `read_R2SONIC_FTS`, `print_R2SONIC_FTS`, `read_R2SONIC_FTS_H0`, `init_R2SONIC_FTS_Beam`, `read_R2SONIC_FTS_Beam`
  - `init_R2SONIC_TRUEPIX`, `read_R2SONIC_TRUEPIX`, `print_R2SONIC_TRUEPIX`, `read_R2SONIC_TRUEPIX_H0`
  - `init_R2SONIC_WCD`, `read_R2SONIC_WCD`, `print_R2SONIC_WCD`, `read_R2SONIC_WCD_H0`, `init_R2SONIC_WCD_Chunk`, `read_R2SONIC_WCD_Chunk`, `init_R2SONIC_WCD_Beam`
- **Sonar Settings & Calibration**:
  - `void load_R2Sonic_sonar_settings(FILE *sonar_settings_file, OMG_HDCS_profile_header *profile, R2SONIC_BATHY_H0 *sonar_bathy_settings, R2SONIC_FTS_H0 *sonar_fts_settings, R2SONIC_TRUEPIX_H0 *sonar_tpx_settings)`
    - Seeks to `sonar_settings_offset_BTH0`, `FTS0`, and `TPX0` in `.sonar_settings` and loads the respective `H0` records.
  - `int init_R2Sonic_Calibrator(R2Sonic_Calibrator *calibrator)` / `int calibrate_r2sonic(R2Sonic_Calibrator *calibrator)`
    - Radiometrically calibrates R2Sonic snippet (`do_snippets`) or TruePix (`do_truepix`) time-series by removing real-time receiver gain, spreading (`rx_spreading`), and absorption (`rx_absorption`), correcting for frequency-dependent and steered beamwidths, computing sample-by-sample ensonified area (`ensonified_area`), and scaling into 8-bit OMG dB space.
  - `int interpolate_data(float *data, int num_recs)` & `int get_truepix_center_beam(OMG_HDCS_profile_header *profile, OMG_HDCS_beam *beams)`
    - Linearly interpolates across zero gaps in grazing angle/area arrays and identifies the nadir/sector-center beam accounting for vessel roll.
- **Indexing & Synchronization**:
  - `init_R2SONIC_INDEX`, `build_R2SONIC_INDEX`, `insert_R2SONIC_INDEX_ELEMENT`, `free_R2SONIC_INDEX`, `find_R2SONIC_PING_MATCH`, `compare_r2sonic_index_elements`
    - Scans an R2Sonic file to index all `BTH0`, `SNI0`, `TPX0`, `WCD0`, and `AIM0` packets and matches asynchronous packets by `ping_number` and `serial_number`.

## How It Fits Into the OMG Architecture

`omg_r2sonic` is a central subsystem used across `code/r2sonic/` (`r2sonicTool`, `r2sonic2omg`, `r2sonic2image`, `r2sonic_extract_truepix`), `code/xtf/` (`xtf2omg_r2sonic`, `xtfTool`), `code/gsf/` (`omg2gsf`, `gsf2omg_7101`), `code/SE/` (`swathed`), and `code/subr/` (`Echo_calib`, `sonar_geometry`).
