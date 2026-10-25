---
layout: default
title: omg_jsf
parent: Core Shared Libraries (subr)
module_name: omg_jsf
source_path: code/subr/omg_jsf.c
header_path: code/subr/omg_jsf.h
category: File Formats & Vendor Parsers
related_tools:
  - jsfTool
  - jsf2omg
  - jsf2nav
  - jsf2orientation
---

# omg_jsf

## Overview & Purpose

`omg_jsf` implements a little-endian binary parser for EdgeTech JSF (JStar Format) sonar and ancillary sensor files. EdgeTech sub-bottom profilers, sidescan sonars, and interferometric/bathymetric systems record packetized binary streams prefixed by a 16-byte message header (`0x1601` magic marker). `omg_jsf` decodes the message header and provides parsers and diagnostic printers for acoustic trace data (message 80), orientation/MRU data (message 2020), processed interferometric bathymetry (message 3000), attitude (message 3001), pressure/CTD sensors (message 3002), and navigation position (message 3004).

## Key Data Structures, Constants & Macros

### Constants
- `JSF_SONAR_MESSAGE_HEADER_START` (`0x1601`): Sync word marking the start of every JSF packet.
- Fixed Packet Header Sizes:
  - `JSF_MESSAGE_HEADER_SIZE` (`16` bytes)
  - `JSF_SONAR_DATA_SIZE` (`240` bytes fixed header preceding trace samples)
  - `JSF_ORIENTATION_DATA_SIZE` (`44` bytes)
  - `JSF_BATHYMETRY_3000_DATA_SIZE` (`80` bytes fixed header preceding bathymetric samples)
  - `JSF_ATTITUDE_3001_DATA_SIZE` (`32` bytes)
  - `JSF_PRESSURE_3002_DATA_SIZE` (`36` bytes)
  - `JSF_POSITION_3004_DATA_SIZE` (`56` bytes)

### Core Structs
- `JSF_Message_Header`: 16-byte packet framing header (`start`, `protocol_version`, `session_id`, `message_type`, `command_type`, `subsystem_id`, `channel`, `sequence_number`, `reserved`, `message_size`).
- `JSF_Sonar_Data` (Message 80): Contains 240 bytes of ping metadata (`ping_time`, `start_depth`, `ping_number`, `MSBs`, `id`, `validity_flag`, `data_format`, `towpoint_dist_aft`/`stbd`, `km_of_pipe`, `position_x`/`y`, `coordinate_units`, `annotation_string[24]`, `num_samples`, `sampling_interval`, `adc_gain_factor`, `transmit_level`, `start_frequency`, `end_frequency`, `sweep_length`, `pressure`, `depth`, `sample_frequency`, `pulse_id`, `altitude`, CPU and NMEA timestamps/course/speed, `compass_heading`, `pitch`, `roll`, `temperature`, `weighting_factor`, `layback`, `cable_out`) plus dynamically allocated `unsigned short *trace_data` and a copy of the 240-byte `rawdata` header.
- `JSF_Orientation_Data` (Message 2020): 3-axis accelerations (`acceleration_x/y/z`), rate gyros (`rate_gyro_x/y/z`), `pitch`, `roll`, `heave`, `heading`, `temperature`, `device_info`, and `data_flags`.
- `JSF_Bathymetric_Sample` & `JSF_Bathymetric_3000_Data` (Message 3000): Header (`time`, `nanoseconds`, `ping_number`, `num_samples`, `channel`, `algorithm_type`, `pulse_amplitude`, `start_frequency`, `end_frequency`, `mixer_frequency`, `sample_rate`, `time_to_first_sample`, scale factors for time/angle/amplitude, `time_to_first_bottom_return`) and dynamically allocated array of `JSF_Bathymetric_Sample` (`time_delay`, `angle`, `amplitude`, `quality`).
- `JSF_Attitude_3001_Data` (Message 3001): Timestamp, `data_validity_flags` bitmask, and floating-point `heading`, `heave`, `pitch`, `roll`, and `yaw`.
- `JSF_Pressure_3002_Data` (Message 3002): Timestamp, `data_validity_flags`, `pressure`, `water_temperature`, `salinity`, `conductivity`, `sound_speed`, and `depth`.
- `JSF_Position_3004_Data` (Message 3004): Timestamp, `data_validity_flags`, `utm_zone`, `easting`, `northing`, `latitude`, `longitude`, `speed`, `heading`, and `altitude`.

## Public Functions & Signatures

- `char *get_JSF_message_name(unsigned short message_type)`
  - Translates numeric JSF message IDs (`80`, `82`, `182`, `426`, `428`, `2002`, `2020`, `2060`, `2080`, `2090`, `2100`, `2111`, `3000`–`3004`) into descriptive strings.
- `int parse_JSF_Message_Header(JSF_Message_Header *header, FILE *infile)` / `int print_JSF_Message_Header(JSF_Message_Header *header)`
  - Reads 16 bytes from `infile` and unpacks the little-endian header fields using `jb_endian` helpers (`get_LE_short`, `get_LE_int`, `get_LE_char`). Returns `-1` on EOF.
- `int parse_JSF_Sonar_Data(JSF_Sonar_Data *ping, FILE *infile)` / `int print_JSF_Sonar_Data(JSF_Sonar_Data *ping)`
  - Reads the 240-byte fixed header into `ping->rawdata`, unpacks all fields, determines trace byte count from `ping->data_format` (`0` = 16-bit envelope at 2 bytes/sample; `1` = 16-bit I/Q analytic signal at 4 bytes/sample), dynamically grows `ping->trace_data`, and reads the sample array via `fread_LE_short`.
- `int parse_JSF_Orientation_Data(JSF_Orientation_Data *data, FILE *infile)` / `int print_JSF_Orientation_Data(JSF_Orientation_Data *data)`
  - Unpacks and prints the 44-byte orientation/MRU record.
- `int parse_JSF_Bathymetric_3000_Data(JSF_Bathymetric_3000_Data *data, FILE *infile)` / `int print_JSF_Bathymetric_3000_Data(JSF_Bathymetric_3000_Data *data)`
  - Unpacks the 80-byte bathymetric header, reallocates `data->bathy_data` for `num_samples`, and reads `num_samples * 4` little-endian shorts directly into the `JSF_Bathymetric_Sample` array.
- `int parse_JSF_Attitude_3001_Data(JSF_Attitude_3001_Data *data, FILE *infile)` / `int print_JSF_Attitude_3001_Data(JSF_Attitude_3001_Data *data)`
  - Unpacks and prints message 3001 attitude records, checking bitflags `0x01`–`0x10` when printing valid fields.
- `int parse_JSF_Pressure_3002_Data(JSF_Pressure_3002_Data *data, FILE *infile)` / `int print_JSF_Pressure_3002_Data(JSF_Pressure_3002_Data *data)`
  - Unpacks and prints message 3002 pressure/CTD/SVP records, honoring validity flags `0x01`–`0x20`.
- `int parse_JSF_Position_3004_Data(JSF_Position_3004_Data *data, FILE *infile)` / `int print_JSF_Position_3004_Data(JSF_Position_3004_Data *data)`
  - Unpacks and prints message 3004 navigation/position records, honoring validity flags `0x01`–`0x80`.

## How It Fits Into the OMG Architecture

`omg_jsf` powers the `code/jsf/` conversion utilities:
- **`jsfTool`**: Scans `.jsf` files, tallying and printing packet headers and sensor payloads.
- **`jsf2omg`**: Converts JSF acoustic trace data (message 80) and interferometric bathymetry (message 3000) into OMG HDCS format.
- **`jsf2nav`** and **`jsf2orientation`**: Extract navigation (`JSF_Sonar_Data` / `JSF_Position_3004_Data`) and attitude (`JSF_Orientation_Data` / `JSF_Attitude_3001_Data`) streams into OMG navigation and orientation files.
