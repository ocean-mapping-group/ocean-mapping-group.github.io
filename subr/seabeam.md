---
layout: default
title: seabeam
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/seabeam.c
category: Multibeam Vendor Parsers
related_tools:
- refoSB_Classic
- selectcb
- iosedit
- gledit
- glgain
- glmerge
- azimerge
- addheader
module_name: seabeam
header_path: code/subr/seabeam.h
---

# `seabeam` — URI-Format Classic General Instruments SeaBeam I/O Library

## Overview & Purpose

The `seabeam` module (`code/subr/seabeam.c` and `code/subr/seabeam.h`), written by G. Carpenter and John Hughes Clarke (November 1989, updated August 1991 and August 2014), provides a modular read, write, binary time-search, and geographic projection package for classic 19-beam General Instruments **SeaBeam** multibeam data stored in the **University of Rhode Island (URI)** tape block format.

In the URI SeaBeam format, each ping record (`sb_urirec`) is 102 bytes (51 `short` integers), and 5 records are packed into each 512-byte VAX tape block (with 2 trailing pad bytes per block, or 514-byte alignment when `Align_514` is enabled). The module handles block-aligned byte offset calculation, random-access record reading/writing, binary search by Unix timestamp, VAX 512-byte block padding, and geographic positioning of the 19 beams (`get_xyz_beams`).

---

## Key Constants & Data Structures

### Constants & Globals (`seabeam.h`)

- **`#define sb_beams 19`**: Number of beams in a classic SeaBeam swath.
- **`int Align_514`**: Global flag controlling block stride in `sb_recoffset()` (`514` bytes per 5-record block if non-zero, otherwise standard `512`-byte VAX block alignment).

### `sb_urirec` Structure (102 bytes)

```c
typedef struct sb_urirec {
    short depth[sb_beams];   /* 19 beam depths in meters */
    short disp[sb_beams];    /* 19 cross-track displacements in meters */
    short speed;             /* Vessel speed in hundredths of a knot */
    short course;            /* Vessel course made good in tenths of a degree */
    short centre;            /* Center beam index / reference */
    short sb_heading;        /* SeaBeam gyro heading in tenths of a degree */
    short lat_min_frac;      /* Fractional minutes of latitude (1/10,000th min) */
    short lat_min;           /* Integer minutes of latitude from South Pole (+90 deg offset) */
    short lon_min_frac;      /* Fractional minutes of longitude (1/10,000th min) */
    short lon_min;           /* Integer minutes of longitude (0 to 360 deg E) */
    short time_sec;          /* Seconds (0-59) */
    short time_min;          /* Minutes of day (hour * 60 + minute) */
    short jday;              /* Julian day of year (1-366) */
    short year;              /* 4-digit calendar year */
    short sb_time;           /* Internal SeaBeam clock word */
} sb_urirec;
```

---

## Public Functions & Signatures

### 1. Block Offset & File I/O

- **`int sb_recoffset(unsigned int r)`**
  Converts a 0-based record index `r` to a file byte offset, accounting for 5 records (102 bytes each = 510 bytes) packed per 512-byte (or 514-byte if `Align_514` is set) block: `(r / 5) * 512 + (r % 5) * 102`.
- **`int sb_readuri(FILE *file, unsigned int recordnum, sb_urirec *data)`**
  Seeks to `sb_recoffset(recordnum)` and reads a 102-byte `sb_urirec` structure, unpacking the 51 `short` fields into `data`. Returns `1` on success or `0` on error.
- **`int sb_writeuri(FILE *file, unsigned int recordnum, sb_urirec *data)`**
  Seeks to `sb_recoffset(recordnum)` and writes `data` to `file`.
- **`void sb_padfile(FILE *file)`**
  Pads the end of `file` with zero bytes to an exact multiple of 512 bytes for compatibility with legacy VAX tape block readers.
- **`int sb_record_count(FILE *file)`**
  Determines the total number of `sb_urirec` records in `file` from its byte length: `(len / 512) * 5 + ((len % 512) / 102)`.
- **`void dump_cb_size(FILE *file)`**
  Prints a summary of a URI SeaBeam file's byte length, total record count, start timestamp (record 0), and last valid non-zero record timestamp.

### 2. Time Conversion & Binary Search

- **`int sb_jultostdtime(short year, short day, short hour, short min, short sec)`**
  Converts a Julian day timestamp into Unix epoch seconds since 1970-01-01 00:00:00 UTC.
- **`int sb_stdtime(sb_urirec *data)`**
  Returns the Unix epoch timestamp of `data` by calling `sb_jultostdtime()`.
- **`int sb_time_search(FILE *file, int wanttime, int *rec)`**
  Performs an $O(\log N)$ binary search across all records in `file` to find the record index `*rec` matching or immediately following Unix timestamp `wanttime`.
- **`char *sb_datestring(sb_urirec *data)` / `sb_datestring2(sb_urirec *data)` / `sb_datestring3(sb_urirec *data)`**
  Format the record timestamp as `"year YYYY day DDD time HH:MM:SS"`, `asctime(gmtime())`, or `"YYYY-DDD-HH:MM:SS"`.

### 3. Coordinate Conversion, Beam Projection & Display

- **`double sb_declat(short min, short frac)` / `double sb_declon(short min, short frac)`**
  Convert URI SeaBeam encoded latitude (minutes north of South Pole `-90°`) and longitude (`[-180°, +180°]`) into decimal degrees.
- **`void sb_dms(double dd, short *d, short *m, short *s)`**
  Decomposes decimal degrees `dd` into degrees, minutes, and seconds.
- **`int get_xyz_beams(sb_urirec *rec, double xyz[19][3])`**
  Projects all valid beams (`rec->depth[k] > 0`) into geographic coordinates `xyz[k][0]` (longitude in degrees), `xyz[k][1]` (latitude in degrees), and `xyz[k][2]` (`-depth` in meters) by rotating the cross-track displacement `rec->disp[k]` perpendicular to `rec->course / 10.0`. Returns the number of valid beams.
- **`int sb_showuri(FILE *file, sb_urirec *data)` / `int sb_showuri_raw(FILE *file, sb_urirec *data)`**
  Print formatted human-readable or raw integer dumps of an `sb_urirec` record to `file`.

---

## How It Fits Into the OMG Architecture

- **SeaBeam Reformatting & Gridding (`sb2k/refoSB_Classic.c`, `grid/selectcb.c`)**: Read URI SeaBeam files and project beam soundings into OMG HDCS or gridded bathymetry datasets.
- **GLORIA / Sidescan Merging & Editing (`sidescan/edit/iosedit.c`, `sidescan/edit/gledit.c`, `sidescan/gain/glgain.c`, `sidescan/merge/glmerge.c`, `sidescan/merge/azimerge.c`, `sidescan/merge/addheader.c`, `sidescan/mock/offtrack.c`, `sidescan/mock/showgains.c`)**: Use `sb_time_search()`, `sb_readuri()`, and `get_xyz_beams()` to look up coincident SeaBeam bathymetry and navigation when processing and terrain-correcting GLORIA long-range sidescan sonar imagery.
