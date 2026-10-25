---
layout: default
title: omg_mb1
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/omg_mb1.c
category: File Formats & Vendor Parsers
related_tools:
- mboneTool
- mbone2omg
- makess
- get_ADH_SRA
- swathed (SE)
module_name: omg_mb1
header_path: code/subr/omg_mb1.h
---

# omg_mb1

## Overview & Purpose

`omg_mb1` provides a binary parser, record inspector, and acoustic backscatter calibrator for Teledyne Odom MB1 (`.mb1` / `.tdy`) multibeam echosounder data files. Teledyne MB1 files contain a 61-byte file header (`Teledyn...`), ping packets (`TDYMB01`) composed of offset-indexed data segments (timing, raw sonar settings, real-time processing settings, angle/range bathymetry, quality/uncertainty, sidescan, snippets, and water column amplitude/phase), and real-time ancillary sensor packets (`TDYRTA1` subtypes for motion, position, heading, and sound speed). In addition to parsing, `omg_mb1` implements radiometric backscatter calibration (`calibrate_mb1`) to convert raw MB1 beam/snippet/sidescan samples into OMG logarithmic backscatter space.

## Key Data Structures, Constants & Macros

### Record Identifiers & Constants
- `MB1_ID_EOF` (`-1`), `MB1_ID_UNKNOWN` (`0`), `MB1_ID_FILE_HEADER` (`1`), `MB1_ID_TDYMB01` (`2`), `MB1_ID_TDYRTA1_0` (`3` - Motion), `MB1_ID_TDYRTA1_1` (`4` - Position), `MB1_ID_TDYRTA1_2` (`5` - Heading), `MB1_ID_TDYRTA1_4` (`6` - Sound Speed).
- `MB1_MAX_NUM_BEAMS` (`512`).
- Fixed Segment Header Sizes: `MB1_FILE_HEADER_SIZE` (`61`), `MB1_MB01_HEADER_SIZE` (`81`), `MB1_TDY_TIME_SIZE` (`20`), `MB1_TDY_RAW_SIZE` (`45`), `MB1_TDY_PROC_SIZE` (`26`), `MB1_TDY_AR_SIZE` (`12`), `MB1_TDY_QUAL_SIZE` (`8`), `MB1_TDY_SS_SIZE` (`15`), `MB1_TDY_SNIP_SIZE` (`11`), `MB1_TDY_WC_SIZE` (`9`), `MB1_RTA1_HEADER_SIZE` (`31`).

### Core Structs
- `MB1_File_Header`: 48-byte `header_id`, creation timestamp (`year`, `month`, `day`, `hour`, `minute`, `second`, `milliseconds`), and `reserved[4]`.
- `MB1_MB01_Header`: Master ping header containing `packet_size`, `version`, `sonar_head`, `model[8]`, `serial_number`, firmware/software versions (`DSP`, `COMM`, `RTA`, `TSPU`), `ping` number, `num_data_structures`, byte offsets to each sub-segment (`offset_TIME_segment`, `offset_RAW_segment`, `offset_IQ_segment`, `offset_PROC_segment`, `offset_AR_segment`, `offset_QUAL_segment`, `offset_SNIPPET_segment`, `offset_SNIPSS_segment`, `offset_SS_segment`, `offset_WC_segment`, `offset_RCAR_segment`), and embedded sub-segment structs:
  - `MB1_TDY_TIME`: Ping timestamp (`year`, `month`, `day`, `hour`, `minute`, `second`, `fractional_seconds` in $10\,\mu\text{s}$ ticks, `time_origin`).
  - `MB1_TDY_RAW`: Raw hardware settings (`sample_rate`, `num_samples_per_channel`, `ping_range_samples`, `transmit_power`, `pulse_width`, `max_depth`, `min_depth`, `max_range`, `min_range`, `max_ping_rate`, `start_frequency`, `stop_frequency`, `modulation_type`, and raw 45-byte `inbuffer` copy for `.sonar_settings` persistence).
  - `MB1_TDY_PROC`: Real-time processing gains (`display_gain`, `spreading`, `absorption`, `num_pings_stacked`, `stacking_method`, `head_tilt_angle`).
  - `MB1_TDY_AR`: Angle/Range bathymetry (`sound_speed`, `num_soundings`, and dynamic float arrays `angle_across`, `angle_along`, `range`).
  - `MB1_TDY_QUAL`: Quality metrics (`num_soundings`, dynamic float array `range_uncertainty`).
  - `MB1_TDY_SS`: Sidescan imagery (`gain_flag`, `num_port_samples`, `num_stbd_samples`, dynamic float arrays `port_ss`, `stbd_ss`).
  - `MB1_TDY_SNIP`: Snippet time-series (`gain_flag`, `num_beams`, dynamic arrays `angle`, `start_sample`, `num_samples`, and concatenated `amplitude`).
  - `MB1_TDY_WC`: Water-column data (`gain_flag`, `num_beams`, dynamic arrays `angle`, `start_sample`, `num_samples`, `amplitude`, and `phase`).
- `MB1_RTA1_Header`: Real-time ancillary sensor packet (`header_id`, `sub_id`, timestamp, `data_length`, and `OMG_Buffer buffer` holding the raw ASCII/binary sensor string).
- `MB1_Calibrator`: Context structure for radiometric calibration of MB1 backscatter (`data_in`, `data_out`, `ping_number`, `beam_number`, pointers to `OMG_HDCS_summary_header`, `OMG_HDCS_profile_header`, `OMG_HDCS_beam`, `MB1_TDY_RAW *sonar_settings`, `grazing_angles`, `dB_shift`, `dB_scale`, `rx_beamwidth`, `tx_beamwidth`, `attenuation_coefficient`, `skip_all_corrections`).

## Public Functions & Signatures

### Packet Discovery & Time Conversion
- `int get_next_MB1_rec_type(FILE *infile)`
  - Peeks at the next 7–8 bytes of `infile` (`"TDYMB01"`, `"TDYRTA1"` + `sub_id`, or `"Teledyn"`), rewinds the file pointer to the start of the packet, and returns the `MB1_ID_*` constant (or `MB1_ID_EOF`).
- `char *get_MB1_record_name(int i)`
  - Maps `MB1_ID_*` constants to human-readable strings.
- `double TDY_time_to_unix_time(MB1_TDY_TIME *header)`
  - Converts `MB1_TDY_TIME` into a Unix epoch timestamp (`double`) using `stdtime_dmy_to_jul_day` and `stdtime_from_jul_day` plus `fractional_seconds / 100000.0`.

### Segment Parsers (`init_*`, `parse_*`, `print_*`, `free_*`)
- `MB1_File_Header`, `MB1_MB01_Header`, `MB1_TDY_TIME`, `MB1_TDY_RAW`, `MB1_TDY_PROC`, `MB1_TDY_AR`, `MB1_TDY_QUAL`, `MB1_TDY_SS`, `MB1_TDY_SNIP`, `MB1_TDY_WC`, `MB1_RTA1_Header`:
  - `parse_MB1_MB01_Header` reads the 81-byte `TDYMB01` header, computes the packet end offset, and seeks to each non-zero segment offset (`offset_TIME_segment`, `offset_RAW_segment`, etc.) to invoke the corresponding segment parser before positioning `infile` at `end_packet`.

### Sonar Settings & Radiometric Backscatter Calibration
- `int load_MB1_sonar_settings(FILE *sonar_settings_file, OMG_HDCS_profile_header *profile, MB1_TDY_RAW *sonar_settings)`
  - Seeks to `profile->sonar_settings_offset` in an auxiliary `.sonar_settings` file and reads the 45-byte `MB1_TDY_RAW` record.
- `int init_MB1_Calibrator(MB1_Calibrator *calibrator)`
  - Initializes the calibrator with default `dB_scale = 2.0` (1 DN = 0.5 dB in OMG unsigned byte space), nominal `rx_beamwidth = 5.0` deg, and `tx_beamwidth = 3.0` deg (at 200 kHz).
- `int calibrate_mb1(MB1_Calibrator *calibrator)`
  - Computes slant range from two-way travel time and transducer sound speed, adjusts `rx_beamwidth` for beam steering ($\theta_{rx} / \cos(\text{steer})$), scales both transmit and receive beamwidths inversely with center frequency relative to 200 kHz ($\theta_f = \theta_{200} \cdot 200 / f_{\text{kHz}}$), computes the seafloor ensonified area via `ensonified_area()`, and applies source level, $-10\log_{10}(\text{area})$, $+40\log_{10}(R)$ spreading, $+2\alpha R/1000$ attenuation, and `dB_shift` to convert `20*log10(data_in[i])` into 8-bit `data_out[i]`.

## How It Fits Into the OMG Architecture

`omg_mb1` is used by **`mboneTool`** and **`mbone2omg`** (`code/mb1/`) to inspect and convert Teledyne MB1 files into OMG HDCS files (and `.sonar_settings` sidecars). Its `MB1_Calibrator` and `load_MB1_sonar_settings` interface with **`Echo_calib`** (`code/subr/Echo_calib.c`), **`makess`**, **`get_ADH_SRA`**, and **`swathed` (`SE`)** for sidescan generation and angular response extraction.
