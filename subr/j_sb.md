---
layout: default
title: j_sb
parent: Core Shared Libraries (subr)
module_name: j_sb
source_path: code/subr/j_sb.c
header_path: code/subr/j_sb.h
category: Sonar Format I/O (SeaBeam)
related_tools:
  - sb2omg
  - weigh_grid
---

# `j_sb` — Scripps Institution of Oceanography (SIO) SeaBeam 2000 Format I/O Library

## Overview & Purpose in the OMG Architecture

`j_sb` (`code/subr/j_sb.c`, `code/subr/j_sb.h`), authored by John E. Hughes Clarke on November 1, 1993, provides the binary data structures, file readers, and diagnostic print routines for the **Scripps Institution of Oceanography (SIO) SeaBeam 2000 (`SB2K`)** multibeam echosounder data format.

Early deep-water multibeam surveys conducted aboard academic research vessels (such as R/V *Melville* and R/V *Thomas Washington*) logged SeaBeam 2000 swath bathymetry and sound velocity profiles in the binary SIO format. `j_sb` defines the exact memory layout of SIO headers, attitude/transceiver profiles, depth/cross-track sounding pairs, and sound velocity profiles (SVPs), enabling OMG conversion and gridding utilities (`URI_SEABEAM` format in `j_dtm.h`) to ingest historical SeaBeam 2000 datasets.

---

## Key Data Structures (`code/subr/j_sb.h`)

### `SIO_header`
Ping or record framing header containing navigation, timing, and payload lengths:
- `short year`, `jday`, `min`, `sec`: Record timestamp (year, Julian day, minute of day, seconds).
- `long lat`, `lon`: Vessel latitude and longitude in scaled integer units.
- `short heading`, `course`: Vessel heading and course made good.
- `short speed_fa`, `speed_ps`: Fore-aft and port-starboard vessel speed components.
- `short quality`: Navigation/record quality indicator.
- `short sensor_len`, `data_len`: Byte lengths of the following sensor profile and sounding data blocks.
- `char speed_ref[2]`, `sens_type[2]`, `data_type[2]`: 2-character ASCII codes identifying speed reference, sensor type, and data block type.

### `SIO_profile`
Transceiver and motion sensor settings for a swath ping:
- `short pitch`, `roll`: Vessel pitch and roll angles.
- `short ping_gain`, `sssv`, `tmtr_pulse_wid`, `tmtr_atten`: Receiver gain, surface sound speed (`sssv`), transmitter pulse width, and transmitter attenuation.
- `short dummy` and `char op_mode`: Padding and sonar operating mode character.

### `SIO_XZ_pair` & `SIO_soundings`
- `SIO_XZ_pair`: Individual beam sounding consisting of `short depth` and `short xtrack` (across-track distance).
- `SIO_soundings`: Swath sounding block containing `short no_points`, `short scale_factor`, and `SIO_XZ_pair pairs[151]` (supporting up to 151 beams per ping).

### `SIO_ZV_pair`, `SIO_VR_quad` & `SIO_svp`
- `SIO_ZV_pair`: Depth (`short depth`) and sound velocity (`short ssv`) node.
- `SIO_VR_quad`: Vertical reference device lever-arm offsets (`short id`, `port_loc`, `forw_loc`, `vert_loc`).
- `SIO_svp`: Complete Sound Velocity Profile record containing `int mean_sv`, `short no_points`, `short scale_factor`, `SIO_ZV_pair ssv_data[30]` (up to 30 depth-velocity layers), `SIO_VR_quad vert_ref_data[2]`, and `char vert_ref_dev[8]`.

---

## Public Functions & Signatures

### Binary Record Readers
- `int jSIO_read_swath_header(FILE *file, SIO_header *sio_head)`
  Reads a `sizeof(SIO_header)` block from `file` into `sio_head` via `fread()`. Returns `1` on success.
- `int jSIO_read_swath_profile(FILE *file, SIO_profile *sio_prof)`
  Reads a `sizeof(SIO_profile)` sensor block from `file` into `sio_prof`.
- `int jSIO_read_swath_soundings(FILE *file, SIO_soundings *sio_sound)`
  Reads the 4-byte header (`no_points` and `scale_factor`) of a sounding block, followed by `sio_sound->no_points * sizeof(SIO_XZ_pair)` bytes into `sio_sound->pairs[]`.
- `int jSIO_read_svp(FILE *file, SIO_svp *sio_svp)`
  Reads a complete `SIO_svp` sound velocity and lever-arm record from `file`.

### Diagnostic Printers
- `void jSIO_print_swath_header(SIO_header sio_head)`
  Prints all timestamp, position, course, speed, block length, and 2-character descriptor fields of `sio_head` to `stdout`.
- `void jSIO_print_swath_profile(SIO_profile sio_prof)`
  Prints pitch, roll, gain, surface sound velocity, pulse width, attenuation, and operating mode.
- `void jSIO_print_swath_soundings(SIO_soundings sio_sound)`
  Prints `no_points`, `scale_factor`, and a table of `(depth, xtrack)` values for all active beams.
- `void jSIO_print_svp(SIO_svp sio_svp)`
  Prints `mean_sv`, `no_points`, `scale_factor`, the 30 `ssv_data` pairs, the 2 `vert_ref_data` lever-arm quads, and the 8-character vertical reference device name.

---

## How It Fits Into the OMG Architecture

`j_sb` provides legacy SeaBeam 2000 support for OMG format converters and inspection tools, working alongside `j_sb2100` (which handles the newer SeaBeam 2100 series ASCII/binary hybrid format).
