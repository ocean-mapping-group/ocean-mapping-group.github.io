---
layout: default
title: omg_hypack
parent: Core Shared Libraries (subr)
module_name: omg_hypack
source_path: code/subr/omg_hypack.c
header_path: code/subr/omg_hypack.h
category: File Formats & Vendor Parsers
related_tools:
  - hypack2omg
---

# omg_hypack

## Overview & Purpose

`omg_hypack` parses ASCII HYPACK HYSWEEP (`HSX`) survey files for conversion into the Ocean Mapping Group (OMG) HDCS format. HYPACK HSX files consist of an ASCII header section terminated by an `EOH` (End of Header) tag, followed by line-oriented data records prefixed by 3-character record identifiers. `omg_hypack` validates the file signature (`FTP` and `HSX` records), parses device configurations, lever arms, multibeam/sidescan capabilities, survey parameters, and sound velocity profiles from the header, and provides a line-by-line record reader backed by `OMG_Buffer`.

## Key Data Structures, Constants & Macros

### Constants
- `HSX_MAX_NUM_DEVICES` (`100`): Maximum number of configured survey devices stored in `Hypack_HSX_Header`.
- `HSX_MAX_NUM_SVP_LAYERS` (`1000`): Maximum number of sound velocity profile depth layers.

### Data Structures
- `Hypack_HSX_Device`: Aggregates device metadata across multiple header record types:
  - From `DEV`: `char *name`, `unsigned short capability1` (bitmask for position, depth, heading, MRU, extended capabilities).
  - From `DV2`: `unsigned short capability2` (bitmask for multibeam, multiple transducer, GPS, sidescan, single-beam, gyro, MRU), `on_tow_fish`, `enabled`.
  - From `OF2`: `OMG_HDCS_motion_sensor offsets` (`Xloc`, `Yloc`, `Zloc`, `dHeading`, `dRoll`, `dPitch`, and latency `dTime`).
  - From `SSI`: Sidescan configuration (`sidescan_sonar_flags`, `number_port_samples`, `number_stbd_samples`).
  - From `MBI`: Multibeam configuration (`multibeam_sonar_type`, `multibeam_sonar_flags`, hex-encoded bitmask `multibeam_beam_data`, `number_beams`, `number_beams2`, `first_angle`, `angle_increment`).
- `Hypack_HSX_Sound_Velocity_Layer`: Represents a single `SVC` layer (`begin_depth`, `end_depth`, `sound_velocity`).
- `Hypack_HSX_Header`: Complete survey header state containing:
  - `format_version` (from `HSX` line)
  - Survey start date/time (`year`, `month`, `day`, `hour`, `minute`, `second`) and Unix epoch `basetime` (computed via `stdtime_from_jul_day` from the `TND` record)
  - `INF` fields: `initial_tide_correction`, `initial_draft_correction`, `sound_velocity`
  - `HSP` HYSWEEP parameters: `minimum_depth`, `maximum_depth`, `maximum_port_offset`, `maximum_stbd_offset`, `maximum_port_angle`, `maximum_stbd_angle`, `high_beam_quality`, `low_beam_quality`, `sonar_range`, `towfish_layback`, `work_units`, `dunno_HSP_12`
  - `PRI` primary navigation system index (`primary_navigation_system`)
  - `devices[HSX_MAX_NUM_DEVICES]` and `number_of_devices`
  - `svp[HSX_MAX_NUM_SVP_LAYERS]` and `number_svp_samples`
- `Hypack_HSX_Record`: Holds a single line-oriented HSX data record:
  - `char id[4]`: Null-terminated 3-character record identifier (e.g., `RMB`, `POS`, `GYR`, `HCP`).
  - `OMG_Buffer buffer`: Dynamically sized line buffer holding the raw ASCII record.

## Public Functions & Signatures

- `int init_HSX_header(Hypack_HSX_Header *header)`
  - Zero-initializes the `Hypack_HSX_Header` structure.
- `int read_HSX_header(FILE *infile, Hypack_HSX_Header *header)`
  - Rewinds `infile` to byte 0, verifies the mandatory `FTP` (line 1) and `HSX` (line 2) signatures, and loops over header lines using `getc_line_vlength` until `EOH` is encountered. Parses `TND`, `INF` (skipping 4 double-quoted text strings before reading tide, draft, and sound speed), `PRI`, `HSP`, `DEV`, `DV2`, `OF2`, `MBI`, `SSI`, and `SVC` records while ignoring planned line records (`LNN`, `LIN`, `VER`, `PTS`, `LBP`, `EOL`).
- `int print_HSX_header(Hypack_HSX_Header *header)`
  - Prints a formatted diagnostic summary of the parsed HSX header, decoding all device capability bitmasks (`capability1`, `capability2`), multibeam flags (roll/pitch/heading compensation, single/dual head, depth resolution), and available beam data bitfields (`0x0001` range through `0x2000` sounding-flags).
- `int init_HSX_Record(Hypack_HSX_Record *record)` / `int init_HSX_record(Hypack_HSX_Record *record)`
  - Zeroes the record struct and initializes its internal `OMG_Buffer`. (Note: defined as `init_HSX_record` in `omg_hypack.c` and declared as `init_HSX_Record` in `omg_hypack.h`.)
- `int read_HSX_Record(FILE *infile, Hypack_HSX_Record *record)` / `int read_HSX_record(FILE *infile, Hypack_HSX_Record *record)`
  - Reads the next variable-length ASCII line from `infile` into `record->buffer` and copies the 3-character tag into `record->id`. Returns `1` on EOF, `0` on success.
- `int free_HSX_Record(Hypack_HSX_Record *record)`
  - Frees the internal `OMG_Buffer` and resets the record structure.

## How It Fits Into the OMG Architecture

`omg_hypack` is the parsing engine behind **`hypack2omg`** (`code/hypack/hypack2omg.c`), which converts HYPACK HYSWEEP `.HSX` files into OMG HDCS bathymetry, navigation, and attitude files. It relies on `omg_buffer` (`getc_line_vlength`) for safe arbitrary-length line reading, `stdtime` for Julian day and epoch time conversion, and `OMG_HDCS_motion_sensor` from `OMG_HDCS_jversion.h` to store sensor lever arms and mounting angles directly in OMG conventions.
