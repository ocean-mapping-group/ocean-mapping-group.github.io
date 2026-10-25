---
layout: default
title: omg_buffer
parent: Core Shared Libraries (subr)
module_name: omg_buffer
source_path: code/subr/omg_buffer.c
header_path: code/subr/omg_buffer.h
category: Memory Management & Dynamic Buffers
related_tools:
  - normalization
  - newGetBP
  - s7k / kmall / gsf packet readers
---

# `omg_buffer` — Dynamic Resizable Byte & Double Buffer Management Library

## Overview & Purpose in the OMG Architecture

`omg_buffer` (`code/subr/omg_buffer.c`, `code/subr/omg_buffer.h`), written by Jonathan Beaudoin and extended by Anand Hiroji (July 2015), provides lightweight, dynamically resizable heap buffers for raw binary packet I/O (`OMG_Buffer`) and double-precision statistical sample accumulation (`OMG_Buffer_double`).

When parsing variable-length sonar datagrams (such as Reson 7k, Kongsberg EM/KMALL, or GSF records) from disk, allocating a fixed buffer on the stack risks buffer overflow on unusually large water-column or snippet packets, while calling `malloc()`/`free()` on every single ping incurs heavy heap fragmentation overhead. `omg_buffer` solves this by maintaining a persistent heap allocation (`size_buffer`) that only calls `realloc()` when a newly encountered record (`new_size`) exceeds the current high-water mark, while tracking the active payload length in `size_record`.

In July 2015, `OMG_Buffer_double` was added to apply the same grow-on-demand pattern to double-precision floating-point arrays in `normalization.c` (storing individual linear backscatter intensities inside each 4D `[Sector][ATBSA][GRA][SRA]` bin for Rayleigh/outlier statistical filtering).

---

## Key Data Structures (`code/subr/omg_buffer.h`)

### `OMG_Buffer`
Dynamic byte buffer for raw binary I/O:
```c
typedef struct {
    unsigned char *buffer;      /* Pointer to heap-allocated byte array             */
    unsigned int   size_buffer; /* Total allocated capacity in bytes                */
    unsigned int   size_record; /* Size of active data currently stored (<= size_buffer) */
} OMG_Buffer;
```

### `OMG_Buffer_double`
Dynamic double-precision floating-point array buffer:
```c
typedef struct {
    double       *buffer;      /* Pointer to heap-allocated double array            */
    unsigned int  size_buffer; /* Total allocated capacity (number of doubles)      */
    unsigned int  size_record; /* Number of active doubles currently stored         */
} OMG_Buffer_double;
```

---

## Public Functions & Signatures

### Raw Byte Buffer API (`OMG_Buffer`)
- `int init_OMG_Buffer(OMG_Buffer *buffer)`
  Zero-initializes the `OMG_Buffer` struct (`buffer = NULL`, `size_buffer = 0`, `size_record = 0`) using `memset()`. Returns `0`.
- `int grow_OMG_Buffer(OMG_Buffer *buffer, unsigned int new_size)`
  Ensures that `buffer->buffer` has at least `new_size` bytes of allocated capacity:
  - If `new_size <= buffer->size_buffer`, returns `0` immediately without reallocating.
  - Otherwise, resizes `buffer->buffer` via `realloc(buffer->buffer, new_size)`, aborts via `error("Puked on buffer resize!")` (`support.h`) on out-of-memory failure, updates `buffer->size_buffer = new_size`, and returns `0`.
- `int wipe_OMG_Buffer(OMG_Buffer *buffer)`
  Zeroes out all `buffer->size_buffer` allocated bytes via `memset(buffer->buffer, 0, buffer->size_buffer)` without freeing the underlying allocation. Returns `0`.
- `int free_OMG_Buffer(OMG_Buffer *buffer)`
  Frees `buffer->buffer` if non-null and resets all struct fields to zero via `init_OMG_Buffer()`. Returns `0`.

### Double-Precision Array Buffer API (`OMG_Buffer_double`)
- `int init_OMG_Buffer_double(OMG_Buffer_double *buffer)`
  Zero-initializes the `OMG_Buffer_double` struct via `memset()`. Returns `0`.
- `int grow_OMG_Buffer_double(OMG_Buffer_double *buffer, unsigned int new_size)`
  If `new_size > buffer->size_buffer`, resizes `buffer->buffer` to `sizeof(double) * new_size` bytes via `realloc()`, updates `buffer->size_buffer = new_size`, and returns `0`.
- `int wipe_OMG_Buffer_double(OMG_Buffer_double *buffer)`
  Zeroes the buffer contents via `memset()`. Returns `0`.
- `int free_OMG_Buffer_double(OMG_Buffer_double *buffer)`
  Frees `buffer->buffer` if non-null and re-initializes the struct to zero. Returns `0`.

---

## How It Fits Into the OMG Architecture

`omg_buffer` is a foundational memory-management helper used across OMG binary format readers and the 4D backscatter normalization engine (`normalization.h` / `normalization.c`).
