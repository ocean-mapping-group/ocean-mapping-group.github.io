---
layout: default
title: simrad_utils
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/simrad_utils.c
category: Multibeam Vendor Parsers
related_tools:
- RT
- RTlite
- RTlite_unravel
- xtfTool
- xtf2omg_simrad
- simrad_reader
- EM_unpack
module_name: simrad_utils
header_path: code/subr/simrad_utils.h
---

# `simrad_utils` — Kongsberg Simrad `.all` Byte-Order & Sonar Model Detection

## Overview & Purpose

The `simrad_utils` module (`code/subr/simrad_utils.c` and `code/subr/simrad_utils.h`) provides non-destructive file-header inspection utilities for Kongsberg Maritime (Simrad) `.all` multibeam raw datagram files.

Because Kongsberg EM-series multibeam echosounders have historically logged `.all` datagrams in both big-endian (older Sun/Motorola operator stations such as EM12, EM950, EM1000) and little-endian (x86 Windows/Linux SIS operator stations such as EM300, EM1002, EM3000, EM710, EM2040, EM302, EM122) byte orders, downstream parsers must determine the file's endianness and EM model number before unpacking telegrams. Both `guess_simrad_byte_order()` and `get_model()` preserve and restore the caller's `FILE *` stream offset via `ftell()` and `fseek()`.

---

## Key Constants

Defined in `code/subr/simrad_utils.h`:

| Macro | Value | Description |
| :--- | :--- | :--- |
| `SIMRAD_UNKNOWN_BYTE_ORDER` | `-1` | Endianness could not be determined from the datagram header |
| `SIMRAD_BIG_ENDIAN` | `0` | File datagrams are stored in big-endian (MSB-first) byte order |
| `SIMRAD_LITTLE_ENDIAN` | `1` | File datagrams are stored in little-endian (LSB-first) byte order |

---

## Public Functions & Signatures

### `guess_simrad_byte_order`

```c
int guess_simrad_byte_order(FILE *infile);
```
- **Purpose**: Determines whether a Kongsberg `.all` file is encoded in little-endian or big-endian byte order without altering the file position of `infile`.
- **Algorithm**:
  1. Saves the current stream offset (`initial_file_position = ftell(infile)`).
  2. Seeks to byte offset `8` from the start of the file (`SEEK_SET`), which corresponds to the 4-byte integer `date` field (`YYYYMMDD`) inside the first Kongsberg datagram header (following the 4-byte telegram length, 1-byte `STX` `0x02`, 1-byte datagram type, and 2-byte EM model number).
  3. Reads the 4-byte date field as both a little-endian integer (`fread_LE_int`) and a big-endian integer (`fread_BE_int`), then restores `initial_file_position`.
  4. Checks which interpretation falls within the valid calendar date range `[19700000, 20500000]` (`1970-00-00` to `2050-00-00`):
     - Returns `SIMRAD_LITTLE_ENDIAN` (`1`) if only `datefield_LE` is within bounds.
     - Returns `SIMRAD_BIG_ENDIAN` (`0`) if only `datefield_BE` is within bounds.
     - Returns `SIMRAD_UNKNOWN_BYTE_ORDER` (`-1`) otherwise.

### `get_model`

```c
int get_model(FILE *infile, int byte_order);
```
- **Purpose**: Reads and returns the 16-bit unsigned Kongsberg EM model number (e.g., `300`, `1002`, `3000`, `710`, `2040`, `122`, `302`) from the first datagram header in `infile`.
- **Algorithm**:
  1. Saves `initial_file_position = ftell(infile)`.
  2. Seeks to byte offset `6` from the start of `infile` (`SEEK_SET`).
  3. Reads a 2-byte `unsigned short` using `fread_BE_short()` if `byte_order == SIMRAD_BIG_ENDIAN` or `fread_LE_short()` otherwise.
  4. Restores `initial_file_position` and returns `model`.

### `old_guess_simrad_byte_order`

```c
int old_guess_simrad_byte_order(FILE *infile);
```
- **Purpose**: Legacy heuristic byte-order detector retained in `simrad_utils.c`. Scans up to 10 consecutive datagrams under both `SIMRAD_BIG_ENDIAN` and `SIMRAD_LITTLE_ENDIAN` hypotheses by reading the 4-byte `telegram_length` preceding each `0x02` (`STX`) byte and checking whether advancing by `telegram_length + 4` lands on the next datagram's `0x02` (`STX`) byte.

---

## How It Fits Into the OMG Architecture

- **Kongsberg `.all` Converters (`RT/RT.c`, `RTLite/RTlite.c`, `RTLite/RTlite_unravel.c`)**: Call `guess_simrad_byte_order()` and `get_model()` immediately upon opening a `.all` file to configure endian-swapping and sonar-specific beam/attitude handling.
- **XTF & Simrad Utilities (`xtf/xtfTool.c`, `xtf/xtf2omg_simrad.c`, `subr/xtf_utils.c`, `jonnyb/simrad_code/*`)**: Used across `simrad_reader`, `EM_unpack`, `km2nav`, `km2orientation`, `km2report`, `get_watercolumn`, `compress_watercolumn`, `get_stave`, `get_seeps`, and `get_centralbeams` to auto-detect `.all` endianness and sonar model numbers.
