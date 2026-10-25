---
layout: default
title: jb_utils
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/jb_utils.c
category: General Utilities, Sorting & Image Header I/O
related_tools:
- j_SUB2K
- jb_watercolumn
- soundscape
- image export utilities
module_name: jb_utils
header_path: code/subr/jb_utils.h
---

# `jb_utils` — General Purpose String, `qsort` Comparator, Color Space & Raster Header Utilities

## Overview & Purpose in the OMG Architecture

`jb_utils` (`code/subr/jb_utils.c`, `code/subr/jb_utils.h`), written by Jonathan Beaudoin, is a lightweight utility module providing common helper functions needed across OMG processing tools: dynamic string concatenation (`strAppend`), minimal 1024-byte `OMG1` (`JHC_header`) and Netpbm `.pgm` raster header writers (`writeJHC`, `writePGM`), standard C library `qsort()` comparator callbacks (`float_compare`, `int_compare`, `byte_compare`), HSV-to-RGB color conversion (`jb_hsv_to_rgb`), and file existence verification (`check_safe_filename`).

---

## Key Constants & Macros (`code/subr/jb_utils.h`)

### `writeJHC` Data Type Identifiers
- `JB_8BIT` (`1`): 8-bit unsigned char raster (`unsigned char`, `.u1` / `.bw`).
- `JB_16BIT` (`2`): 16-bit integer raster (`short`, `.i2`).
- `JB_FLOAT` (`3`): 32-bit floating-point raster (`float`, `.r4`).

---

## Public Functions & Signatures

### String & File Safety Helpers
- `char *strAppend(char *str1, char *str2)`
  Allocates a new heap string of length `strlen(str1) + strlen(str2) + 1` via `malloc()`, copies `str1`, appends `str2`, and returns the newly allocated pointer.
- `int check_safe_filename(char *inname)`
  Tests whether a file named `inname` already exists and is readable by attempting `fopen(inname, "r")`. If opened, closes the stream and returns `1` (file exists); otherwise returns `0`.

### Raster Image Header Writers
- `void writeJHC(FILE *outfile, int width, int height, unsigned char dataType)`
  Constructs and writes a minimal 1024-byte OMG raster header (`"OMG1"` magic bytes at offset `0..3`, Big-Endian 32-bit `width` at offset `4` and `height` at offset `8` via `put_BE_int()`, and `dataType` at byte offset `64`) to `outfile`. This allows quick generation of unprojected 2D diagnostic rasters (such as acoustic water-column fans or SVP error wedges) that can be immediately opened in `jview`.
- `void writePGM(FILE *outfile, int width, int height, char *comments)`
  Writes a standard Portable GrayMap (`P5` binary 8-bit grayscale, max value `255`) header with an embedded `#comments` line and `width height` dimensions to `outfile`.

### `qsort()` Comparison Callbacks
Designed to be passed directly as the comparator function pointer to `stdlib.h`'s `qsort()`:
- `int float_compare(const void *val1, const void *val2)`
  Compares two `float` values pointed to by `val1` and `val2`, returning `-1` if `*val1 < *val2`, `1` if `*val1 > *val2`, or `0` if equal. Used in median filtering (e.g., `j_SUB2K.c` and `jb_watercolumn.c`).
- `int int_compare(const void *val1, const void *val2)`
  Compares two `int` values, returning `-1`, `1`, or `0`.
- `int byte_compare(const void *val1, const void *val2)`
  Compares two `unsigned char` values, returning `-1`, `1`, or `0`.

### Color Space Conversion
- `void jb_hsv_to_rgb(int *r, int *g, int *b, double h, double s, double v)`
  Converts a color specified in Hue-Saturation-Value space (`h` in $[0, 360^\circ)$, `s` in $[0, 1]$, `v` in $[0, 1]$) into 8-bit Red, Green, and Blue integer components `(*r, *g, *b)` in the range `[0..255]`.

---

## How It Fits Into the OMG Architecture

`jb_utils` is included directly by `jb_watercolumn.h`, `j_SUB2K.c`, and various water-column and backscatter visualization utilities. It relies on `jb_endian.h` (`put_BE_int`) to ensure that `writeJHC()` produces portable Big-Endian `OMG1` headers on all platforms.
