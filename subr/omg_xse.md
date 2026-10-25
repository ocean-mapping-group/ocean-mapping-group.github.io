---
layout: default
title: omg_xse
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/omg_xse.c
category: File Formats & Vendor Parsers
related_tools:
- xseTool
- xse2omg
module_name: omg_xse
header_path: code/subr/omg_xse.h
---

# omg_xse

## Overview & Purpose

`omg_xse` implements a binary frame and group parser for the L-3 Communications SeaBeam Instruments / Hydrostar Data Exchange Format (XSE, Revision 1.6 / 1.8.7). XSE files are structured as hierarchical big-endian binary "Frames" (`$HSF` ... `#HSF`) containing one or more typed "Groups" (`$HSG` ... `#HSG`). `omg_xse` handles frame synchronization, converts XSE timestamps (seconds since `1901-01-01 00:00:00` UTC) into standard Unix epoch time (seconds since `1970-01-01`), and decodes Multibeam, Navigation, Sound Velocity, Sidescan, Ship Configuration, and SeaBeam-specific frames.

## Key Data Structures, Constants & Macros

### Constants & Magic Delimiters
- Frame/Group Magic Markers:
  - `START_FRAME` (`0x24485346`, ASCII `"$HSF"`), `END_FRAME` (`0x23485346`, ASCII `"#HSF"`).
  - `START_GROUP` (`0x24485347`, ASCII `"$HSG"`), `END_GROUP` (`0x23485347`, ASCII `"#HSG"`).
- Header Sizes & Capacities:
  - `OMG_XSE_FRAME_HEADER_SIZE` (`24` bytes), `OMG_XSE_GROUP_HEADER_SIZE` (`12` bytes).
  - `NUM_FRAME_TYPES` (`200`), `NUM_GROUP_TYPES` (`200`).
  - `frame_names[NUM_FRAME_TYPES]`: Lookup table mapping XSE frame IDs (`1` = Navigation, `2` = Sound Velocity, `3` = Tide, `4` = Ship, `5` = Sidescan, `6` = Multibeam, `7` = Singlebeam, `8` = Control, `9` = Bathymetry, `10` = Product, `11` = Native, `12` = Geodetic, `13` = SeaBeam, `14` = Message, `17` = Digital I/O).
- `XSE_TIME_OFFSET` (`-2177452800.0l`): Seconds offset between the XSE epoch (`1901-01-01 00:00:00` UTC) and the Unix epoch (`1970-01-01 00:00:00` UTC).

### Core Structs
- `Frame_Header`: 24-byte header (`start`, `size`, `ID`, `source`, `timeSec`, `timeMicros`) plus computed Unix timestamp `double time`.
- `Group_Header`: 12-byte group header (`start`, `size`, `ID`).
- `Multibeam_Frame` (Frame ID 6) & `Multibeam_Frame_Beam`:
  - General Group (1): `ping_number`, `frequency`, `pulse`, `power`, `bandwidth`, `sample`, `swath`.
  - Collapses Groups 2–19 into per-beam `Multibeam_Frame_Beam` records (`beam_number`, `travel_time`, `quality`, `amplitude`, `delay`, `across`, `along`, `depth`, `angle`, `heave`, `roll`, `pitch`, `angle2`, `start_gate`, `end_gate`, `noise`, `echo_length`, `hits`, `heave_rx`, `azimuth`), tracking present groups in `valid_group[NUM_GROUP_TYPES]`.
- `Navigation_Frame` (Frame ID 1): Unpacks Point Group 2 (`description`, `x` lon, `y` lat, `z` height in radians/meters), Accuracy Group 3 (`quality_indicator`, `num_satellites`, `hdop`, `differential_age`, `differential_ref_stn`), Motion Ground Truth Group 4 (`sog`, `cog`), Motion Through Water Group 5 (`sow`, `cow`), HRP Group 7 (`heave`, `roll`, `pitch`), and Heading Group 11 (`heading`).
- `Sound_Velocity_Frame` (Frame ID 2) & `Sound_Velocity_Sample`: Collapses depth, velocity, conductivity, salinity, temperature, and pressure groups into `Sound_Velocity_Sample *samples`.
- `Sidescan_Frame` (Frame ID 5): Unpacks General Group 1, Amplitude vs. Lateral Group 4 (`bin_size`, `offset`, `num_amplitude`, `short *amplitude`), Signal Group 6 (`ping_number2`, `channel_id`, `offset_sig_grp`, `interval`, `num_phase`, `short *phase`), and Weighting Group 9 (`factor_left`, `samples_left`, `factor_right`, `samples_right`).
- `Ship_Frame` (Frame ID 4) & `Transducer`: Unpacks General Group 1 (vessel dimensions/name), Sensors Group 4, Navigation & Motion Offsets Group 9 (`roll`, `pitch`, `heave`, `gyro`, `delay`, `nav_x/y/z`, `hrp_x/y/z`), Transducer Group 10 (`Transducer *transducer`), and Extended Mounting Group 11.
- `SeaBeam_Frame` (Frame ID 13): Unpacks Properties Group 1 (`ping_number`, `gain`, `pulse`, `power`, `sidescan_pixel_size`, `swath_width`, `interval`, `depth_mode`, `beam_mode`, `ssp`, `frequency`, `bandwidth`), HRP Group 2, Signal Group 9 (`beam`, `num_amplitude`, `float *amplitude`), and Message Group 21 (`message`).

## Public Functions & Signatures

- **Buffer & Frame Framing**:
  - `int grow_data_buffer(unsigned int new_size)`: Dynamically expands the shared `data_buffer` used for group payload reads.
  - `int seek_start_frame(FILE *infile)`: Scans `infile` for the big-endian `START_FRAME` (`0x24485346`) marker and rewinds 4 bytes to the frame start.
  - `int read_frame_header(FILE *infile, Frame_Header *header)` / `int print_frame_header(Frame_Header *header)`: Reads the 24-byte `Frame_Header` and computes `header->time = (double)timeSec + XSE_TIME_OFFSET + (double)timeMicros / 1.0E6`.
  - `int read_group_header(FILE *infile, Group_Header *header)` / `int print_group_header(Group_Header *header)`: Reads the 12-byte `Group_Header`.
- **Frame Lifecycle Functions (`init_*`, `clean_*`, `read_*`, `free_*`, `print_*`)**:
  - `Multibeam_Frame`: `init_multibeam_frame`, `read_multibeam_frame`, `free_multibeam_frame`, `print_multibeam_frame`
  - `Navigation_Frame`: `init_navigation_frame`, `clean_navigation_frame`, `read_navigation_frame`, `free_navigation_frame`, `print_navigation_frame`
  - `Sound_Velocity_Frame`: `init_sound_velocity_frame`, `clean_sound_velocity_frame`, `read_sound_velocity_frame`, `free_sound_velocity_frame`, `print_sound_velocity_frame`
  - `Sidescan_Frame`: `init_sidescan_frame`, `clean_sidescan_frame`, `read_sidescan_frame`, `free_sidescan_frame`, `print_sidescan_frame`
  - `Ship_Frame`: `init_ship_frame`, `clean_ship_frame`, `read_ship_frame`, `free_ship_frame`, `print_ship_frame`
  - `SeaBeam_Frame`: `init_seabeam_frame`, `clean_seabeam_frame`, `read_seabeam_frame`, `free_seabeam_frame`, `print_seabeam_frame`

## How It Fits Into the OMG Architecture

`omg_xse` is the core library for **`xseTool`** and **`xse2omg`** (`code/xse/`), converting Elac / SeaBeam 2100 / 1180 / 3000 series Hydrostar `.xse` files into OMG HDCS bathymetry, sidescan, navigation, orientation, sound velocity, and vessel parameter files.
