---
layout: default
title: GrafNav_2_OMG
parent: Tidal Reduction & Constituents (tide)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
tool_name: GrafNav_2_OMG
source_path: code/tide/GrafNav_2_OMG.c
category: tide
input_formats:
- GrafNav PPK ASCII (.txt / .pos)
output_formats:
- .nav (binary jcu_nav_rec tide)
- ASCII tide (time lat lon height)
related_tools:
- posProc_2_OMG
- binTide
- mergeTide
- diffTide
---

# GrafNav_2_OMG

## Overview

`GrafNav_2_OMG` converts post-processed kinematic (PPK) GNSS output files from Waypoint **GrafNav** into an OMG binary `jcu_nav_rec` tide/navigation file (or an optional 4-column ASCII file). Ellipsoidal or orthometric height from the PPK solution is stored in the `bin_nav.azi` field, while timestamps are converted to UTC epoch seconds (`time` and `centisecs`) and horizontal positions are stored in `bin_nav.lat` and `bin_nav.lon`.

The resulting binary file can be merged directly into OMG-HDCS `.merged` multibeam files using [`mergeTide`](mergeTide.html) (for example with `-RTK` or standard tide application).

---

## Syntax & CLI Options

```bash
GrafNav_2_OMG [OPTIONS] -in <posprocfilename> -out <mytideformatname>
```

| Option | Description | Default |
|---|---|---|
| `-in <filename>` | **Required.** Input ASCII post-processed GNSS file exported from GrafNav. | None |
| `-out <filename>` | **Required.** Output OMG binary `jcu_nav_rec` tide file (or ASCII file if `-ascii` is set). | None |
| `-lines_to_skip <N>` | Number of header lines to skip at the beginning of the input file before parsing data records. | `18` |
| `-mdy_dms` | Parse alternate GrafNav format with `MM/DD/YYYY HH:MM:SS.S`, GPS week, GPS seconds, DMS latitude (`deg min sec`), DMS longitude (`deg min sec`), and height. | Disabled (default YMD decimal degrees) |
| `-yj_gpst` | Parse 6-column pre-formatted `year jday fsec lat lon height` records. | Disabled |
| `-ascii` | Write output as 4-column ASCII (`epoch_sec lat lon height`) instead of binary `jcu_nav_rec` records. | Disabled (writes binary `jcu_nav_rec`) |
| `-v` | Enable verbose diagnostic output for each parsed navigation/tide record. | Disabled |

---

## How It Works

1. **Header Skipping:** Reads and discards the first `lines_to_skip` lines (default `18`) from the input GrafNav file.
2. **Delimiter Normalization:** Replaces `/` and `:` characters in each line with spaces so date (`YYYY/MM/DD` or `MM/DD/YYYY`) and time (`HH:MM:SS.SS`) fields can be tokenized with `sscanf`.
3. **Format Parsing:**
   - **Default mode:** Parses `year month day hour min fsec fdum lat lon height` (`%d %d %d %d %d %lf %lf %lf %lf %f`) and computes Julian day via `stdtime_dmy_to_jul_day`.
   - **`-mdy_dms` mode:** Parses `month day year hour min fsec iweek fdum latdeg latmin latsec londeg lonmin lonsec height` and converts DMS coordinates to decimal degrees (`deg + min/60.0 + sec/3600.0`).
   - **`-yj_gpst` mode:** Parses `year jday fsec lat lon height` directly.
4. **Epoch Conversion & Output:** Converts `(year, jday, hour, min, fsec)` to 1970 UTC epoch seconds (`stdtime_from_jul_day`), populates `jcu_nav_rec` (`time`, `centisecs`, `lat`, `lon`, `azi = height`, `velocity = 0`, `depth = 0`), and writes each record via `nav_write` (or `fprintf` when `-ascii` is specified).

---

## Examples

**1. Convert standard GrafNav PPK export to binary OMG tide format:**

```bash
GrafNav_2_OMG -in grafnav_export.txt -out rtk_tide.bin
```

**2. Convert a GrafNav export with 22 header lines and DMS coordinates:**

```bash
GrafNav_2_OMG -lines_to_skip 22 -mdy_dms -in grafnav_dms.pos -out rtk_tide.bin
```

**3. Export to 4-column ASCII for inspection:**

```bash
GrafNav_2_OMG -ascii -in grafnav_export.txt -out rtk_tide.txt
```

---

## Workflow Context

- **Upstream:** Waypoint GrafNav GNSS post-processing software.
- **Downstream:** [`mergeTide`](mergeTide.html) (to apply PPK/RTK heights to `.merged` multibeam lines) or [`diffTide`](diffTide.html) (to compare PPK heights against gauge tides or another navigation source).
- **Related Alternative:** [`posProc_2_OMG`](posProc_2_OMG.html) performs the equivalent conversion for Applanix POSPac / PosProc outputs.
