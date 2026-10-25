---
layout: default
title: jcu_nav
parent: Core Shared Libraries (subr)
module_name: jcu_nav
source_path: code/subr/jcu_nav.c
header_path: code/subr/jcu_nav.h
category: Navigation Format I/O & Time Indexing
related_tools:
  - j_SUB2K
  - appendNav_asciiSecs
  - mergeNav
  - jview
---

# `jcu_nav` — OMG / JCU Binary & ASCII Navigation Record Format Library

## Overview & Purpose in the OMG Architecture

`jcu_nav` (`code/subr/jcu_nav.c`, `code/subr/jcu_nav.h`), authored by John E. Hughes Clarke (November 1989 / February 1990), defines the standard 48-byte binary and 80-byte ASCII **OMG/JCU Navigation Record (`jcu_nav_rec`)** format, along with random-access record I/O, $O(\log N)$ binary time-search routines, and `qsort` chronological comparators.

Throughout the OMG processing pipeline, vessel navigation (`lat`, `lon`, `time`, `centisecs`, `azi`, `velocity`, `depth`, and quality flags) is stored in `.nav` files using the fixed 48-byte `JCU_BINNAV_RECLEN` layout. Because `.nav` records are fixed-width and sorted chronologically, any tool merging navigation with sonar pings or attitude streams can use `nav_time_search_double()` to jump directly to the exact navigation fix in $O(\log N)$ disk seeks regardless of file size.

---

## Key Data Structures & Constants (`code/subr/jcu_nav.h`)

### Constants
- `NAV_RECLEN` (`80`): Byte length of a single fixed-width JCU ASCII navigation line.
- `JCU_BINNAV_RECLEN` (`48`): Byte length of a serialized binary `jcu_nav_rec` on disk (including 2 bytes of 32-bit alignment padding after `centisecs`).

### Core Struct: `jcu_nav_rec`
```c
typedef struct {
    double lat;       /* Latitude in decimal degrees (+N, -S)          [offset 0,  8 bytes] */
    double lon;       /* Longitude in decimal degrees (+E, -W)         [offset 8,  8 bytes] */
    int    time;      /* UTC time in seconds since Jan 1, 1970         [offset 16, 4 bytes] */
    short  centisecs; /* Hundredths of seconds (0..99)                 [offset 20, 2 bytes] */
                      /* (2 bytes padding on disk at offset 22..23)                         */
    float  azi;       /* Vessel heading / course made good in degrees  [offset 24, 4 bytes] */
    float  velocity;  /* Vessel speed (m/s or knots)                   [offset 28, 4 bytes] */
    short  depth;     /* Centerbeam / echosounder water depth (m)      [offset 32, 2 bytes] */
    short  flag[4];   /* 4 status/quality flags                        [offset 34..41, 8 B] */
                      /* (6 bytes trailing padding in 48-byte record)                       */
} jcu_nav_rec;
```

---

## Public Functions & Signatures

### Random-Access Binary & ASCII Record I/O
- `int nav_read(FILE *file, unsigned int recordnum, jcu_nav_rec *data)`
  Seeks to `recordnum * JCU_BINNAV_RECLEN` (`48 * recordnum`), reads 48 bytes, and unpacks all fields into `data` using Big-Endian `get_swapped_*()` (`swapio.h`). Returns `1` on success or `0` on EOF/seek error.
- `int nav_write(FILE *file, unsigned int recordnum, jcu_nav_rec *data)`
  Packs `data` into a 48-byte buffer using `put_swapped_*()`, seeks to `recordnum * 48`, and writes the record to `file`. Returns `1` on success.
- `int nav_readjcu_ascii(FILE *file, unsigned int recordnum, jcu_nav_rec *data)`
  Seeks to `recordnum * NAV_RECLEN` (`80 * recordnum`), reads an 80-character ASCII navigation record, and parses `lat`, `lon`, `depth`, `velocity`, `azi`, `year`, `day`, `hour`, `min`, `secs`, and `flag[0..3]`.
- `int nav_show(FILE *file, jcu_nav_rec *data)`
  Formats and prints a `jcu_nav_rec` as a human-readable ASCII line to `file`, converting `data->time` via `gmtime()` into `YYYY JJJ (MM DD) HH MM SS.CC`.

### Chronological Binary Search & Sorting
- `int nav_time_search_double(FILE *file, double wanttime, int *recnum)`
  Performs an $O(\log N)$ binary search over a binary `.nav` file using full sub-second precision (`(double)rec.time + (double)rec.centisecs / 100.0`), followed by a local linear fine-tuning step (`rn -= 3` and advancing) to guarantee that `*recnum` points to the record immediately preceding `wanttime`. Returns `1` on success or `0` if the file is empty.
- `int nav_time_search(FILE *file, int wanttime, int *recnum)`
  Performs an integer-second (`rec.time`) binary search over a binary `.nav` file.
- `int nav_time_search_ascii(FILE *file, int wanttime, int *recnum)`
  Performs an integer-second binary search over a fixed-80-byte-line ASCII navigation file.
- `int nav_compare(const void *val1, const void *val2)`
  Standard `qsort()` comparator function that compares two `jcu_nav_rec` structs by their full sub-second timestamp (`time + centisecs / 100.0`), returning `-1`, `1`, or `0`.

---

## How It Fits Into the OMG Architecture

`jcu_nav` is the primary navigation file library across `code/nav/`, `code/omg/`, `code/submetrix/` (`j_SUB2K`), and `code/JV/` (`jview`), providing fast random-access navigation lookup and interpolation for swath sonar and sidescan processing.
