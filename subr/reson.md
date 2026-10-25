---
layout: default
title: reson
parent: Core Shared Libraries (subr)
module_name: reson
source_path: code/subr/reson.c
header_path: code/subr/reson.h
category: File Formats & Vendor Parsers
related_tools:
  - 8kTool
  - 8k2omg
  - xtf2omg_reson
  - xtfTool
  - extractSnippet
  - extractRI
  - getTVG
  - get8101BeamPattern
  - getAngularResponse
---

# reson

## Overview & Purpose

`reson` provides the big-endian binary packet parser, quality-flag unpacker, dynamic range scanner, and 16-bit-to-8-bit intensity converter for Teledyne Reson SeaBat 8100-series (8101, 8111, 8124, 8125, 8150, 8160) multibeam echosounder R-Theta (`0x13`, `0x17`) and RI-Theta (`0x14`, `0x18`) packets. It supports both raw SeaBat 8K serial/network streams and 8100-series bathymetry payloads embedded inside XTF files.

## Key Data Structures, Constants & Macros

### Constants & Macros
- `RESON_8K_SYNC_PATTERN` (`0xFFFF0000`): 4-byte synchronization header `{0xff, 0xff, 0x00, 0x00}` at the start of every SeaBat 8K packet.
- Fixed Header Sizes (preceding variable-length beam arrays):
  - `RESON_PEEKER_SIZE` (`5` bytes)
  - `RESON_0x13_0x14_SIZE` (`36` bytes for legacy R-Theta `0x13` and RI-Theta `0x14` packets)
  - `RESON_0x17_0x18_SIZE` (`68` bytes for extended R-Theta `0x17` and RI-Theta `0x18` packets)
- Quality Packing Flags:
  - `UNDEFINED_QUALITY` (`0`), `PACKED_QUALITY` (`1` - two 4-bit nibbles per byte), `UNPACKED_QUALITY` (`2` - one byte per beam).
- 16-bit Intensity Conversion Modes (`jb_fix_RESON_16bit`):
  - `JB_8101_LOG` (`0`), `JB_8101_LIN` (`1`), `JB_8101_REFL` (`2`), `JB_8101_TRACE` (`3`), `JB_8101_HALF_DB_LOG` (`4`), `JB_8101_FLOAT` (`5`).

### Core Structs
- `DATA_TIME`: Internal SeaBat clock timestamp (`unsigned long Seconds` since Jan 1, 1970; `unsigned long Millisecs`).
- `RESON_PEEKER`: 5-byte lookahead header (`int synch_header`, `char packet_type`).
- `RESON_BATHY`: Unified structure holding `0x13`, `0x14`, `0x17`, and `0x18` bathymetry packets:
  - Common Fields: `synch_header[4]`, `packet_type`, `packet_subtype` (bit 7 indicates head 1 vs. head 2 on dual-head systems), `DATA_TIME data_time`, `latency` (ms), `velocity` (m/s), `sample_rate` (Hz), `ping_rate` (mHz), `range_set` (m), `power` (bits 0–4 power 0–8, bit 15 auto), `gain` (bits 0–6 gain 1–45, bit 14 TVG, bit 15 auto), `tvg_spread` ($\times 4$), `tvg_absorp` (dB/km), `beam_count`, `pulse_width` ($\mu\text{s}$).
  - Extended `0x17`/`0x18` Fields: `ping_number`, `sonar_id` (IP/MAC lower 4 bytes), `sonar_model`, `frequency` (kHz), `projector_type` (stick, array face, ER; bit 7 pitch stabilization), `projector_beam_width`, receive beamwidth `beam_width_num` / `beam_width_denom`, `projector_angle`, range/depth filters (`min_range`, `max_range`, `min_depth`, `max_depth`, `filters_active`), `roll_stab`, `temperature` ($\text{deg C} \times 10$).
  - Dynamic Per-Beam Arrays: `unsigned short *range` ($\text{sample cells} \times 4$), `unsigned char *quality` (bit 0 brightness, bit 1 colinearity, bit 2 amplitude detect, bit 3 phase detect), `unsigned short *intensity` (for `0x14`/`0x18`), `unsigned char *intensity8bit`, and trailing `unsigned short checksum`.
  - In-Memory Housekeeping: `bytesOnDisk`, `persistent_packet_type`, `packedQualityFlag`.
- `resonDynamicRanges`: Tracks min, max, and span for `PulseWidth`, `Power`, `Gain`, `TVGSpread`, and `TVGAbsorp` across an indexed XTF file.

## Public Functions & Signatures

- `int seek_next_8K_sync(FILE *infile)`
  - Scans `infile` byte-by-byte until matching `RESON_8K_SYNC_PATTERN` (`0xFFFF0000`), `SNIPPET_ID_SNP0`, or `SNIPPET_ID_SNP1`, then rewinds 4 bytes to the packet start.
- `void readRESON_PEEKER(RESON_PEEKER *peeker, FILE *infile)`
  - Reads 5 bytes (`synch_header` and `packet_type`) and rewinds 5 bytes without advancing `infile`.
- `void resonInit(RESON_BATHY *bathy)` / `void freeRESON_BATHY(RESON_BATHY *bathy)`
  - Initializes pointers and state flags (`UNDEFINED_QUALITY`) before the first read, or frees allocated beam arrays.
- `int readRESON_BATHY(RESON_BATHY *bathy, FILE *infile)` / `void readRESON_0x13_0x14(RESON_BATHY *bathy, FILE *infile)` / `void readRESON_0x17_0x18(RESON_BATHY *bathy, FILE *infile)` / `void printRESON_BATHY(RESON_BATHY *bathy)`
  - Peeks at `packet_type`, reads the 36-byte (`0x13`/`0x14`) or 68-byte (`0x17`/`0x18`) fixed header, reads big-endian `range` values, auto-detects packed vs. unpacked quality bytes on the first ping via `checkPackedQuality()`, unpacks quality flags (`readPackedQualities`), reads 16-bit `intensity` values (for `0x14`/`0x18`), and reads the 2-byte `checksum`.
- `int checkPackedQuality(FILE *infile, int numBeams)` & `int readPackedQualities(unsigned char *qualityOut, int numBeams, FILE *infile)`
  - Inspects whether any upper nibbles (`0xF0`) are non-zero to distinguish 4-bit packed qualities from 8-bit unpacked qualities, and unpacks 2 beams per byte (padded to even byte counts).
- `void jb_fix_RESON_16bit(unsigned short *dataIn, unsigned char *dataOut, int numSamps, unsigned char power, unsigned char gain, int corr_flags, int source_flags)` & `void corrRESON_BATHY(RESON_BATHY *bathy)`
  - Converts 16-bit SeaBat intensity values into dB ($20\log_{10}(\text{DN}) - \text{gain} - 3 \cdot \text{power}$) and outputs 8-bit linear, 1-dB log, 0.5-dB log, or float values.
- `void getResonDynamicRanges(FILE *infile, XTFFileIndex *theIndex, resonDynamicRanges *dynamicRanges)` / `void printResonDynamicRanges(resonDynamicRanges *dynamicRanges)`
  - Iterates over all bathymetry frames in an indexed XTF file to report the dynamic range of power, gain, pulse width, and TVG settings.

## How It Fits Into the OMG Architecture

`reson` is used by **`8kTool`** and **`8k2omg`** (`code/reson/`), the XTF conversion tools (`xtf2omg_reson`, `xtfTool`, `extractSnippet`, `extractRI`, `stripSS`, `getTVG`), and the Reson radiometric calibration libraries (`reson_calibration.c`, `snippet.c`, `Echo_calib.c`).
