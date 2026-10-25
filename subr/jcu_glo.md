---
layout: default
title: jcu_glo
parent: Core Shared Libraries (subr)
module_name: jcu_glo
source_path: code/subr/jcu_glo.c
header_path: code/subr/jcu_glo.h
category: Sidescan & Sub-Bottom Format I/O
related_tools:
  - knud2glo
  - xtf2gloria
  - j_SUB2K
  - jview
---

# `jcu_glo` — JCU / GLORIA Sidescan & Sub-Bottom Image Record Format I/O Library

## Overview & Purpose in the OMG Architecture

`jcu_glo` (`code/subr/jcu_glo.c`, `code/subr/jcu_glo.h`), written by John E. Hughes Clarke in November 1989 at the Marine Geophysical Laboratory, James Cook University (JCU), defines the fixed-length 1160-byte **JCU GLORIA (`gloria_rec`)** sidescan/sub-bottom image record format and its random-access binary I/O and binary time-search routines.

Originally designed to merge 8-bit dual-channel GLORIA long-range sidescan imagery (512 samples port, 512 samples starboard) with 19-beam SeaBeam swath bathymetry (`cb_depth[19]`, `cb_offset[19]`) and navigation in a single 136-byte header + 1024-byte image record (`GLORIA_RECLEN = 1160`), the `gloria_rec` format became a universal fixed-record 8-bit trace container across the OMG suite. It is used not only for legacy GLORIA sidescan, but also as the target output format for Knudsen sub-bottom profilers (`knud2glo`), XTF sidescan converters (`xtf2gloria`), and 1024-sample trace viewers.

---

## Key Data Structures, Constants & Macros (`code/subr/jcu_glo.h`)

### Record Dimension & Processing Flag Constants
- `GLORIA_SIDESIZE` (`512`): Number of 8-bit pixels per side (port or starboard).
- `GLORIA_SIDESIZE_X2` (`1024`): Total pixels across the full swath (`stbd_data` + `port_data`).
- `HEADER_LENGTH` (`136`): Fixed byte size of the serialized `jcu_all_rec` header on disk.
- `GLORIA_RECLEN` (`1160`): Total byte size of one `gloria_rec` on disk (`136 + 512 + 512`).
- `RAW_SIDE` (`496`): Sample count per side in raw Institute of Oceanographic Sciences (`ios_rec`) GLORIA tape records.
- **Bitwise Processing Flags (`process_flag`)**:
  - `MERGED` (`1`): Navigation/bathymetry merged.
  - `SLANTR` (`2`): Slant-range to ground-range corrected.
  - `BEAMPT` (`4`): Beam-pattern / grazing-angle corrected.
  - `DESTRP` (`8`): Along-track destriped.

### Core Structs

#### `jcu_all_rec`
The 136-byte ping header containing navigation, towfish geometry, 19-beam bathymetry, and transceiver settings:
- **Timing & Navigation**: `int time` (Unix epoch seconds since 1970), `short centisecs` (hundredths of a second), `float azi` (heading/azimuth in **radians**), `double lat`, `double lon` (decimal degrees).
- **Sampling & Towfish Geometry**: `unsigned char ping_rate` (s), `unsigned char pixel_size` (integer meters), `float small_pixel` (fractional pixel size in meters), `float fishdepth` (m), `float altitude` (m above seafloor).
- **Co-Registered Swath Bathymetry**: `short cb_depth[19]` (1500 m/s SeaBeam depths) and `short cb_offset[19]` (refraction-corrected cross-track offsets).
- **Processing & Sonar Settings**: `char process_flag`, `unsigned char tx_power_reduction`, `rx_beam_width`, `rx_bandwidth`, `unsigned short tx_pulse_len`, `tx_beam_width`, `absorp_coeff`, `unsigned char rx_gain_reduction`, `mode`.

#### `gloria_rec`, `gloria_real_rec` & `gloria_all_rec`
- `gloria_rec`: Standard 1160-byte record combining `jcu_all_rec header`, `unsigned char stbd_data[512]`, and `unsigned char port_data[512]`.
- `gloria_real_rec`: In-memory floating-point variant with `float stbd_data[512]` and `float port_data[512]`.
- `gloria_all_rec`: Continuous 1024-byte buffer variant with `unsigned char all_data[1024]`.

#### `ios_rec`
Raw UK Institute of Oceanographic Sciences (IOS) GLORIA magnetic tape record layout (`passno`, `lineno`, `heading`, `port[496]`, `stbd[496]`, `jday`, `hour`, `minutes`, `seconds`, `checksum`).

---

## Public Functions & Signatures

### Random-Access Binary I/O
- `int jcu_readgloria(FILE *file, unsigned int rec_num, gloria_rec *rec)`
  Seeks to byte offset `GLORIA_RECLEN * rec_num` (`1160 * rec_num`), reads the 1160-byte raw record buffer, unpacks all `jcu_all_rec` header fields at their exact Big-Endian byte offsets using `get_swapped_*()` (`swapio.h`), and copies the 512-byte `stbd_data` and 512-byte `port_data` arrays. Returns `1` on success or `0` on seek/EOF failure.
- `int jcu_writegloria(FILE *file, unsigned int rec_num, gloria_rec *rec)`
  Packs `rec->header` into the 136-byte header layout using `put_swapped_*()`, appends `stbd_data[512]` and `port_data[512]`, seeks to `1160 * rec_num`, and writes the 1160-byte record to `file`.

### Binary Search & ASCII Header Printers
- `int jcu_time_search(FILE *file, int wanttime, int *recnum)`
  Performs an $O(\log N)$ binary search over a `gloria_rec` file to find the record index `*recnum` whose `header.time` matches or brackets `wanttime` (seconds since 1970).
- `char *jcu_datestring(gloria_rec *data)`
  Returns a formatted UTC date/time string (`asctime(gmtime(&secs))`) for `data->header.time`.
- `int jcu_write_verbose_head(FILE *file, gloria_rec *rec)`
  Prints a detailed multi-line dump of all header fields in `rec->header` to `file`.
- `int jcu_write_compact_head(FILE *file, gloria_rec *rec)`
  Prints a single-line tabular summary (`time`, `centisecs`, `azi`, `ping_rate`, `pixel_size`, `lat`, `lon`, `fishdepth`, `altitude`, `cb_depth[9]`, `process_flag`).
- `int jcu_write_swath_head(FILE *file, gloria_rec *rec)`
  Prints the 19 `cb_depth` values and 19 `cb_offset` values on two lines.

---

## How It Fits Into the OMG Architecture

`jcu_glo` is linked by sidescan and sub-bottom conversion tools (`code/knudsen/knud2glo`, `code/xtf/xtf2gloria`), interferometric processors (`j_SUB2K.h`), and OMG image display utilities.
