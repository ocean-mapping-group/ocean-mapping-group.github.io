---
layout: default
title: omg_wassp
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/omg_wassp.c
category: File Formats & Vendor Parsers
related_tools:
- wasspTool
- wassp2omg
- makess
- get_ADH_SRA
- swathed (SE)
module_name: omg_wassp
header_path: code/subr/omg_wassp.h
---

# omg_wassp

## Overview & Purpose

`omg_wassp` provides a binary packet parser, stream synchronizer, and backscatter calibrator for ENL WASSP (Wide Angle Sonar Seafloor Profiler) multibeam echosounder data files. WASSP network/disk streams consist of little-endian packets framed by a 32-bit sync pattern (`0x77f9345a`), a 32-bit byte size, and an 8-character ASCII packet type identifier (such as `"GENBATHY"` for generic bathymetry/backscatter pings and `"GEN_SENS"` for serial navigation/attitude sensor records).

## Key Data Structures, Constants & Macros

### Constants
- `WASSP_MAX_NUM_BEAMS` (`256`): Maximum nominal beam count per WASSP ping.
- Fixed Header & Record Sizes:
  - `WASSP_PACKET_HEADER_SIZE` (`16` bytes: 4B `sync_pattern`, 4B `size`, 8B `header`).
  - `WASSP_GEN_BATHY_HEADER_SIZE` (`88` bytes).
  - `WASSP_GEN_BATHY_BEAM_SIZE` (`16` bytes).
  - `WASSP_GEN_SENS_HEADER_SIZE` (`29` bytes).

### Core Structs
- `WASSP_Packet_Header`: 16-byte framing header (`sync_pattern`, `size`, and null-terminated `header[9]`).
- `WASSP_Gen_Bathy_Header`: 88-byte `GENBATHY` ping header containing:
  - Framing & Version: `sync_pattern`, `size`, `header[9]`, `version`.
  - Timing & Identity: `utc_milliseconds`, `utc_day`, `utc_month`, `utc_year`, `ping_number`, `sonar_model`, 64-bit serial number (`serial_number1`, `serial_number2`).
  - Acoustic Settings: `num_beams`, `flags`, `sampling_rate` (Hz), `frequency` (Hz), `source_level` (volts/dB), `pulse_width` (ms), `absorption` (dB/km), `spreading` (dB), `sample_type`, `sound_speed` (m/s).
  - `unsigned char inbuffer[88]`: Raw byte copy preserved for writing to `.sonar_settings` sidecar files.
- `WASSP_Gen_Bathy_Beam`: 16-byte per-beam record (`float range` in samples, `float angle` in degrees, `unsigned int flags`, `float backscatter`).
- `WASSP_Gen_Bathy`: Complete `GENBATHY` packet (`WASSP_Gen_Bathy_Header header`, dynamically allocated `WASSP_Gen_Bathy_Beam *beams`, `checksum`, and capacity `size_beams`).
- `WASSP_Gen_Sensor`: Complete `GEN_SENS` packet (`sync_pattern`, `size`, `header[9]`, `version`, `double time` in ms, `port_number`, dynamically allocated ASCII `char *serial_data`, and `checksum`).
- `WASSP_Calibrator`: Backscatter calibration context (`ping_number`, `beam_number`, pointers to `OMG_HDCS_summary_header`, `OMG_HDCS_profile_header`, `OMG_HDCS_beam`, `WASSP_Gen_Bathy_Header *sonar_settings`, `grazing_angles`, `dB_shift`, `dB_scale`, `rx_beamwidth`, `tx_beamwidth`, `attenuation_coefficient`, `skip_all_corrections`, `debug`).

## Public Functions & Signatures

### Packet Synchronization & Parsing
- `int init_WASSP_Header(WASSP_Packet_Header *data)` / `int read_WASSP_Header(WASSP_Packet_Header *data, FILE *infile)`
  - Initializes or reads the 16-byte packet framing header.
- `int seek_next_WASSP_Packet(FILE *infile, int file_size, WASSP_Packet_Header *header)`
  - Scans `infile` byte-by-byte until finding the little-endian magic word `0x77f9345a`, rewinds 16 bytes to leave `infile` positioned at the start of the packet, and populates `header`. Returns `0` on match, `1` on EOF.
- `int init_WASSP_Gen_Bathy(WASSP_Gen_Bathy *data)` / `int read_WASSP_Gen_Bathy_Header(WASSP_Gen_Bathy_Header *header, FILE *infile)` / `int read_WASSP_Gen_Bathy(WASSP_Gen_Bathy *data, FILE *infile)` / `int print_WASSP_Gen_Bathy(WASSP_Gen_Bathy *data)`
  - Reads the 88-byte `GENBATHY` header, reallocates `data->beams` for `num_beams`, unpacks each 16-byte beam record (`range`, `angle`, `flags`, `backscatter`), and reads the trailing 4-byte checksum.
- `int init_WASSP_Gen_Sensor(WASSP_Gen_Sensor *data)` / `int read_WASSP_Gen_Sensor(WASSP_Gen_Sensor *data, FILE *infile)` / `int print_WASSP_Gen_Sensor(WASSP_Gen_Sensor *data)`
  - Reads the 29-byte `GEN_SENS` header, computes the payload length `size_serial = data->size - (WASSP_GEN_SENS_HEADER_SIZE + 4)`, reads the NMEA/serial string into `data->serial_data`, and unpacks the 4-byte checksum.

### Sonar Settings & Calibration
- `int load_WASSP_sonar_settings(FILE *sonar_settings_file, OMG_HDCS_profile_header *profile, WASSP_Gen_Bathy_Header *sonar_settings)`
  - Seeks to `profile->sonar_settings_offset` in `.sonar_settings` and loads the 88-byte `WASSP_Gen_Bathy_Header`.
- `int init_WASSP_Calibrator(WASSP_Calibrator *calibrator)` / `int calibrate_WASSP(WASSP_Calibrator *calibrator)`
  - Initializes default beamwidths and `dB_scale = 2.0`, and computes ensonified area (`ensonified_area`), source level, spreading ($40\log_{10}R$), and attenuation adjustments to populate `calibrator->beam->calibratedBackscatter`.

## How It Fits Into the OMG Architecture

`omg_wassp` supports **`wasspTool`** and **`wassp2omg`** (`code/wassp/`) for inspecting and converting raw WASSP data streams into OMG HDCS files, and integrates with **`Echo_calib`**, **`makess`**, **`get_ADH_SRA`**, and **`swathed` (`SE`)** for backscatter processing.
