---
layout: default
title: swapio
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/swapio.c
category: Core System, I/O & Time Utilities
related_tools:
- jb_endian
- OMG_HDCS_jversion
- array
- j_farray
module_name: swapio
header_path: code/subr/swapio.h
---

# swapio

## Overview
`swapio` (`swapio.c` / `swapio.h`), written by John Hughes Clarke (March 1996, updated 2006–2016 for 64-bit x86/AMD64 architectures), is the foundational **cross-platform endianness and byte-swapping I/O library** for the Ocean Mapping Group software suite.

Historically, OMG binary formats (`.merged`, `.orientation`, `.nav`, `.r4`, `.mos`, `.ss`) were designed on big-endian Motorola (`mc68000`), Sun SPARC (`sun`), and Silicon Graphics MIPS (`sgi`) workstations (`MOTOROLA == 1`). When running on little-endian architectures (`INTEL == 1`: `i386`, `__x86_64`, `__amd64`, `__alpha`, `ultrix`), `swapio` transparently swaps 16-bit (`short`), 32-bit (`int`, `float`), and 64-bit (`double`) values when reading from or writing to disk buffers and `FILE *` streams.

---

## Architecture Detection Macros

Defined in `swapio.h` via compiler preprocessor symbols:

| Macro | Condition | Meaning |
|---|---|---|
| `INTEL` | `__alpha`, `ultrix`, `i386`, `__x86_64`, `__amd64` | Host CPU is **Little-Endian** (`1`). `swapio` performs byte-reversal on all big-endian OMG file I/O. |
| `MOTOROLA` | `mc68000`, `sony`, `sgi`, `sun` | Host CPU is **Big-Endian** (`1`). `swapio` performs direct `memcpy` / `fread` / `fwrite` without swapping. |

---

## Public Functions

### 1. In-Memory Value Byte Swapping
Unconditionally reverses byte order of a scalar value (using byte-array unions or in-place pointer swaps):

| Function | Signature | Description |
|---|---|---|
| `swap_short` | `short swap_short(short value)` | Reverses 2 bytes (`[0] <-> [1]`) of a 16-bit `short`. |
| `swap_int` | `int swap_int(int value)` | Reverses 4 bytes (`[0]<->[3]`, `[1]<->[2]`) of a 32-bit `int`. |
| `swap_float` | `float swap_float(float value)` | Reverses 4 bytes of a 32-bit IEEE 754 `float` via a union. |
| `new_swap_float` | `void new_swap_float(void *value)` | Swaps 4 bytes of a `float` in-place via `unsigned char *` pointers without loading a signaling NaN into a floating-point register on x86/x86_64. |
| `swap_double` | `double swap_double(double value)` | Reverses 8 bytes (`[0]<->[7]` ... `[3]<->[4]`) of a 64-bit `double`. |
| `print_byte_bits` | `void print_byte_bits(char *the_byte)` | Prints the 8 binary bits (`1`/`0`, MSB to LSB) of `*the_byte` to `stdout` for bit-level debugging. |

### 2. Buffer Unpacking & Packing (`get_swapped_*` / `put_swapped_*`)
Copies values between raw unaligned byte buffers (`char *data`) and typed variables, swapping automatically if `INTEL && !MOTOROLA`:

| Function Pair | Signature | Bytes |
|---|---|---|
| `get_swapped_char` / `put_swapped_char` | `void get_swapped_char(char *data, char *achar, int count)` | `count` bytes (direct `memcpy` for API symmetry) |
| `get_swapped_short` / `put_swapped_short` | `void get_swapped_short(char *data, short *sht)` | 2 bytes (`short`) |
| `get_swapped_int` / `put_swapped_int` | `void get_swapped_int(char *data, int *anint)` | 4 bytes (`int`) |
| `get_swapped_float` / `put_swapped_float` | `void get_swapped_float(char *data, float *afloat)` | 4 bytes (`float`, uses `new_swap_float`) |
| `get_swapped_double` / `put_swapped_double` | `void get_swapped_double(char *data, double *adouble)` | 8 bytes (`double`) |

### 3. Stream Block I/O (`jswap*_fread` / `jswap*_fwrite`)
Drop-in replacements for standard C `fread()` and `fwrite()` that automatically byte-swap arrays on little-endian hosts. Notably, the `fwrite` wrappers swap the array in-place before calling `fwrite()`, and then **swap the buffer back** immediately afterward so the caller's in-memory array remains valid in native host byte order:

| Function | Signature | Description |
|---|---|---|
| `jswapshort_fread` / `jswapshort_fwrite` | `size_t jswapshort_fread(short *ptr, size_t size, size_t n, FILE *stream)` | Reads/writes `n` items of 16-bit `short` integers in big-endian file order. |
| `jswapint_fread` / `jswapint_fwrite` | `size_t jswapint_fread(int *ptr, size_t size, size_t n, FILE *stream)` | Reads/writes `n` items of 32-bit `int` integers in big-endian file order. |
| `jswapfloat_fread` / `jswapfloat_fwrite` | `size_t jswapfloat_fread(float *ptr, size_t size, size_t n, FILE *stream)` | Reads/writes `n` items of 32-bit `float` values in big-endian file order. |

---

## Architectural Role
`swapio` underpins [`OMG_HDCS_jversion`](OMG_HDCS_jversion.html), [`array`](array.html), [`j_farray`](j_farray.html), and legacy big-endian sonar parsers. While newer modules also use [`jb_endian`](jb_endian.html) for explicit `_LE_` / `_BE_` stream reads, `swapio` ensures all classic OMG binary files remain portable across SPARC/MIPS and modern x86_64 Linux systems.
