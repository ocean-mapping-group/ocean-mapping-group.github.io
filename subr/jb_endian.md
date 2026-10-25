---
layout: default
title: jb_endian
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/jb_endian.c
category: Binary I/O & Byte Swapping
related_tools:
- jb_utils
- omg_buffer
- Reson / Kongsberg / GSF / XTF binary parsers
module_name: jb_endian
header_path: code/subr/jb_endian.h
---

# `jb_endian` — Explicit Big-Endian & Little-Endian Binary Serialization Library

## Overview & Purpose in the OMG Architecture

`jb_endian` (`code/subr/jb_endian.c`, `code/subr/jb_endian.h`), written by Jonathan Beaudoin (adapted and generalized from John Hughes Clarke's `swapio.h`, with 64-bit `__x86_64` / `__amd64` updates by JHC in May 2016), provides explicit, endian-aware memory unpacking/packing (`get_BE_*`, `put_BE_*`, `get_LE_*`, `put_LE_*`), runtime-selectable byte-order accessors (`get_*`, `put_*` with `MSB`/`LSB` flags), scalar byte-swapping primitives, and array stream readers/writers (`fread_BE_*`, `fwrite_BE_*`, `fread_LE_*`, `fwrite_LE_*`).

While OMG's original `swapio.h` assumed that all OMG disk files were stored in Big-Endian (Motorola/Sun/SGI) format and only swapped bytes when compiled on Little-Endian (`INTEL`) architectures, modern hydrographic sonar formats (such as Kongsberg `.all`/`.kmall`, Reson `.s7k`, Triton `.xtf`, and Seatex/POS MV binary datagrams) frequently mix Big-Endian and Little-Endian packets—or include a runtime byte-order flag inside each packet header. `jb_endian` solves this by letting callers explicitly request Big-Endian (`BE` / `MSB`) or Little-Endian (`LE` / `LSB`) serialization regardless of host CPU architecture.

---

## Key Macros & Constants (`code/subr/jb_endian.h`)

### Compile-Time Architecture Detection
- `INTEL`: Defined as `1` on Little-Endian architectures (`__alpha`, `ultrix`, `__ultrix`, `i386`, `__x86_64`, `__amd64`), or `0` otherwise.
- `MOTOROLA`: Defined as `1` on Big-Endian architectures (`mc68000`, `sony`, `sgi`, `sun`), or `0` otherwise.

### Runtime Byte-Order Selectors
- `MSB` (`0`): Most Significant Byte first (Big-Endian).
- `LSB` (`1`): Least Significant Byte first (Little-Endian).

---

## Public Functions & Signatures

### 1. Explicit Big-Endian (`BE`) Memory Buffer Unpacking & Packing
Automatically swaps bytes when `INTEL && !MOTOROLA`, or copies directly on Big-Endian hosts:
- `void get_BE_short(unsigned char *data, unsigned short *sht)` / `void put_BE_short(unsigned char *data, unsigned short *sht)` (2 bytes)
- `void get_BE_int(unsigned char *data, unsigned int *anint)` / `void put_BE_int(unsigned char *data, unsigned int *anint)` (4 bytes)
- `void get_BE_long(unsigned char *data, unsigned long *along)` / `void put_BE_long(unsigned char *data, unsigned long *along)` (4 bytes)
- `void get_BE_float(unsigned char *data, float *afloat)` / `void put_BE_float(unsigned char *data, float *afloat)` (4 bytes)
- `void get_BE_double(unsigned char *data, double *adouble)` / `void put_BE_double(unsigned char *data, double *adouble)` (8 bytes)
- `void get_BE_char(unsigned char *data, unsigned char *achar, int count)` / `void put_BE_char(unsigned char *data, unsigned char *achar, int count)` (`count` bytes via `memcpy`)

### 2. Explicit Little-Endian (`LE`) Memory Buffer Unpacking & Packing
Copies directly on Little-Endian (`INTEL`) hosts, or swaps bytes when `!INTEL && MOTOROLA`:
- `void get_LE_short(unsigned char *data, unsigned short *sht)` / `void put_LE_short(unsigned char *data, unsigned short *sht)`
- `void get_LE_int(unsigned char *data, unsigned int *anint)` / `void put_LE_int(unsigned char *data, unsigned int *anint)`
- `void get_LE_long(unsigned char *data, unsigned long *along)` / `void put_LE_long(unsigned char *data, unsigned long *along)`
- `void get_LE_float(unsigned char *data, float *afloat)` / `void put_LE_float(unsigned char *data, float *afloat)`
- `void get_LE_double(unsigned char *data, double *adouble)` / `void put_LE_double(unsigned char *data, double *adouble)`
- `void get_LE_char(unsigned char *data, unsigned char *achar, int count)` / `void put_LE_char(unsigned char *data, unsigned char *achar, int count)`

### 3. Runtime Byte-Order Dispatchers (`byte_order == MSB` or `LSB`)
Allows packet parsers whose endianness is determined dynamically at runtime to unpack/pack values without branching in user code:
- `void get_short(unsigned char *data, unsigned short *sht, int byte_order)` / `void put_short(...)`
- `void get_int(unsigned char *data, unsigned int *anint, int byte_order)` / `void put_int(...)`
- `void get_long(unsigned char *data, unsigned long *along, int byte_order)` / `void put_long(...)`
- `void get_float(unsigned char *data, float *afloat, int byte_order)` / `void put_float(...)`
- `void get_double(unsigned char *data, double *adouble, int byte_order)` / `void put_double(...)`
- `void get_char(unsigned char *data, unsigned char *achar, int count, int byte_order)` / `void put_char(...)`

### 4. Low-Level Scalar Byte-Swapping Primitives & Diagnostics
- `unsigned short short_swap(unsigned short value)`
- `unsigned int int_swap(unsigned int value)`
- `unsigned long long_swap(unsigned long value)`
- `float float_swap(float value)`
- `double double_swap(double value)`
- `void endianTest()`: Prints whether `INTEL` or `MOTOROLA` is defined at runtime.

### 5. Bulk Array File Stream Readers & Writers (`FILE *stream`)
Reads or writes `num_items` elements of `size` bytes, performing in-place byte-swapping across the entire array when host endianness differs from target stream endianness:
- **Big-Endian File I/O**: `fread_BE_short`, `fwrite_BE_short`, `fread_BE_int`, `fwrite_BE_int`, `fread_BE_long`, `fwrite_BE_long`, `fread_BE_float`, `fwrite_BE_float`.
- **Little-Endian File I/O**: `fread_LE_short`, `fwrite_LE_short`, `fread_LE_int`, `fwrite_LE_int`, `fread_LE_long`, `fwrite_LE_long`, `fread_LE_float`, `fwrite_LE_float`.

---

## How It Fits Into the OMG Architecture

`jb_endian` is used throughout Jonathan Beaudoin's and later OMG libraries (`jb_utils`, `omg_buffer`, `j_EM_watercol`, `kongsberg`, `s7k`, and `gsf` utilities) whenever binary files or network datagrams require explicit Big-Endian or Little-Endian serialization.
