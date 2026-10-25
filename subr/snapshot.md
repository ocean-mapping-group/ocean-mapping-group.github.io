---
layout: default
title: snapshot
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/snapshot.c
category: Multibeam Vendor Parsers
related_tools:
- read_snapshot
- snapshot2pgm
module_name: snapshot
header_path: code/subr/snapshot.h
---

# `snapshot` — Reson SeaBat Beamformed Amplitude & Phase Snapshot Parser

## Overview & Purpose

The `snapshot` module (`code/subr/snapshot.c` and `code/subr/snapshot.h`) reads, unpacks, and manages memory for binary **Reson SeaBat "snapshot" files**—single-ping full water-column beamformed amplitude and phase captures recorded by Reson SeaBat 81xx-series multibeam echosounders.

Each snapshot file begins with a 121-byte big-endian extended header (`snapshot_header`) containing UTC time, vessel navigation (`latitude`, `longitude`), attitude (`heave`, `roll`, `pitch`, `heading`), and sonar operating settings (`sound_speed`, `sample_rate`, `pulse_width_microsec`, `ping_rate`, `range_setting`, `power`, `gain`, `tvg_spread`, `tvg_absorp`, `beam_width`, and `beam_count`). Following the header is a sequence of `num_packets` range-slice data packets (`snapshot_data`), each containing a 16-bit unsigned amplitude and a 16-bit signed phase value for every beam in the swath.

---

## Key Constants & Data Structures

### Constants (`snapshot.h`)

- **`#define SIZE_OF_SNAPSHOT_HEADER 121`**: Exact on-disk byte size of the binary snapshot file header.

### `snapshot_header` Structure (121 bytes on disk)

```c
typedef struct {
    unsigned short extended_header;
    unsigned short packet_size;
    unsigned char utc_time[32];

    double latitude;
    double longitude;
    double heave;
    double roll;
    double pitch;
    double heading;

    unsigned char start_character;
    unsigned char packet_id;
    unsigned short packet_size_2;      /* beam count / inner packet size */
    unsigned short header_id;          /* 0xffff */

    unsigned int time_sec;
    unsigned int time_millis;

    unsigned short sound_speed;
    unsigned short sample_rate;
    unsigned char pulse_width_microsec;
    unsigned short ping_rate;
    unsigned short range_setting;
    unsigned short power;
    unsigned short gain;
    unsigned short projector_setting;
    unsigned char tvg_spread;
    unsigned char tvg_absorp;
    unsigned char beam_width;
    unsigned short beam_count;

    unsigned char end_character;
    unsigned short check_sum;
} snapshot_header;
```

### `snapshot_data` & `snapshot` Structures

```c
typedef struct {
    unsigned char start_character;
    unsigned char packet_id;
    unsigned short packet_size;
    unsigned short packet_number;
    unsigned short *amplitude;  /* [beam_count] */
    signed short *phase;        /* [beam_count] */
    unsigned char end_character;
    unsigned short check_sum;
} snapshot_data;

typedef struct {
    snapshot_header header;
    snapshot_data data;
    unsigned short **amplitude; /* [beam_count][num_packets] */
    signed short **phase;       /* [beam_count][num_packets] */
    int num_packets;
} snapshot;
```

---

## Public Functions & Signatures

### 1. Whole-File Snapshot Management

- **`int init_snapshot(snapshot *the_snapshot)`**
  Zeroes `the_snapshot->header`, sets `amplitude` and `phase` 2D pointers to `NULL`, sets `num_packets = 0`, and initializes `the_snapshot->data` via `init_snapshot_data()`.
- **`int read_snapshot(snapshot *the_snapshot, FILE *infile)`**
  Reads an entire snapshot file into `the_snapshot`:
  1. Determines the file length via `fseek(infile, 0, SEEK_END)` and `ftell()`.
  2. Rewinds to offset `0` and calls `read_snapshot_header(&the_snapshot->header, infile)`.
  3. Computes the per-slice packet size (`9 + 4 * beam_count` bytes) and total range slices `num_packets = (file_length - 121) / packet_size`.
  4. Dynamically allocates/reallocates the 2D `[beam_count][num_packets]` arrays `the_snapshot->amplitude` and `the_snapshot->phase`.
  5. Loops through all `num_packets` slices, calling `read_snapshot_data()` and transposing each slice into `[beam][packet]` order.
- **`int print_snapshot(snapshot *the_snapshot)`**
  Prints the snapshot header metadata to `stdout` by calling `print_snapshot_header(&the_snapshot->header)`.
- **`int free_snapshot(snapshot *the_snapshot)`**
  Frees all per-beam rows and top-level pointer arrays in `the_snapshot->amplitude` and `the_snapshot->phase`, then resets the struct via `init_snapshot()`.

### 2. Low-Level Header & Packet Helpers

- **`int read_snapshot_header(snapshot_header *header, FILE *infile)`**
  Reads `SIZE_OF_SNAPSHOT_HEADER` (121) bytes from `infile` and unpacks all fields using big-endian deserialization helpers from `jb_endian.h` (`get_BE_short`, `get_BE_int`, `get_BE_double`, `get_BE_char`).
- **`int print_snapshot_header(snapshot_header *header)`**
  Prints a human-readable dump of all navigation, attitude, and sonar settings in `header` (scaling `ping_rate / 1000.0`, `tvg_spread / 4.0`, and `beam_width / 10.0`).
- **`int init_snapshot_data(snapshot_data *data)`**
  Sets `data->amplitude = NULL` and `data->phase = NULL`.
- **`int read_snapshot_data(snapshot_data *data, int num_beams, FILE *infile)`**
  Reads one range-slice packet (`9 + 4 * num_beams` bytes) from `infile` and unpacks the packet framing plus `num_beams` pairs of big-endian 16-bit `amplitude` and `phase` samples.

---

## How It Fits Into the OMG Architecture

- **Water-Column Snapshot Inspection & Imaging (`jonnyb/gom_stuff/read_snapshot.c`, `jonnyb/gom_stuff/snapshot2pgm.c`)**: Use `init_snapshot()`, `read_snapshot()`, `print_snapshot()`, and `free_snapshot()` to inspect Reson SeaBat water-column snapshot headers and render beam-vs-range amplitude and phase matrices into Portable GrayMap (`.pgm`) images.
