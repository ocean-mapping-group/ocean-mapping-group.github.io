---
layout: default
title: posProc_2_OMG
parent: Tidal Reduction & Constituents (tide)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
tool_name: posProc_2_OMG
source_path: code/tide/posProc_2_OMG.c
category: tide
input_formats:
- Applanix PosProc / POSPac PPK ASCII
output_formats:
- .nav (binary jcu_nav_rec tide)
- ASCII tide (time lat lon height)
related_tools:
- GrafNav_2_OMG
- binTide
- mergeTide
- diffTide
---

# posProc_2_OMG

## Overview

`posProc_2_OMG` converts post-processed kinematic (PPK) GNSS/inertial solution text files exported from Applanix **PosProc / POSPac** into an OMG binary `jcu_nav_rec` tide/navigation file (or 4-column ASCII file with `-ascii`). It converts GPS seconds-of-day/week (`weeksecs`) relative to a specified year and Julian day (`-year`, `-jday`) into 1970 UTC epoch timestamps, storing the PPK ellipsoidal/orthometric height in `bin_nav.azi` and position in `bin_nav.lat` and `bin_nav.lon`.

---

## Syntax & CLI Options

```bash
posProc_2_OMG [OPTIONS] -year <YYYY> -jday <DDD> -in <posprocfilename> -out <mytideformatname>
```

| Option | Description | Default |
|---|---|---|
| `-in <filename>` | **Required.** Input ASCII PosProc / POSPac solution file. | None |
| `-out <filename>` | **Required.** Output binary `jcu_nav_rec` file (or ASCII file if `-ascii` is set). | None |
| `-year <YYYY>` | Reference 4-digit year for timestamp conversion. | `1970` |
| `-jday <DDD>` | Reference Julian day (`1..366`) to which `weeksecs` is added (`stdtime_from_jul_day(year, jday, 0, 0, 0) + weeksecs`). | `0` |
| `-lines_to_skip <N>` | Number of header lines to skip at the beginning of the input file. | `23` |
| `-ascii` | Write 4-column ASCII (`dtime lat lon height`) instead of binary `jcu_nav_rec` records. | Disabled (binary) |
| `-v` | Print verbose `lat`, `lon`, `time`, and `centisecs` for every record. | Disabled |

---

## How It Works

1. **Header Skipping:** Reads and skips the first `lines_to_skip` lines (default `23`).
2. **Column Parsing:** Parses 7 columns from each line:

   ```c
   sscanf(linestring, "%lf %f %f %f %f %lf %lf",
          &weeksecs, &fdum, &fdum, &fdum, &bin_nav.azi, &bin_nav.lat, &bin_nav.lon);
   ```
   where column 1 is seconds (`weeksecs`), columns 2–4 are skipped, column 5 is height (`bin_nav.azi`), column 6 is latitude (`bin_nav.lat`), and column 7 is longitude (`bin_nav.lon`).
3. **Epoch Calculation & Output:** Computes UTC epoch seconds as `stdtime_from_jul_day(year, jday, 0, 0, 0) + weeksecs`, populates `bin_nav.time` and `bin_nav.centisecs`, and writes binary `jcu_nav_rec` records via `nav_write` (or ASCII lines with `-ascii`).

---

## Examples

**1. Convert a PosProc export for Julian Day 173, 2008 to binary OMG tide format:**

```bash
posProc_2_OMG -year 2008 -jday 173 -in posproc_jd173.txt -out posproc_jd173.bin
mergeTide -RTK -tide posproc_jd173.bin merged/JD173/*.merged
```

**2. Convert with custom header length to ASCII for inspection:**

```bash
posProc_2_OMG -lines_to_skip 25 -year 2008 -jday 173 -ascii -in posproc.txt -out posproc.asc
```

---

## Workflow Context

- **Upstream:** Applanix PosProc / POSPac post-processed GNSS/INS text exports.
- **Downstream:** [`mergeTide`](mergeTide.html) or [`diffTide`](diffTide.html).
- **See Also:** [`GrafNav_2_OMG`](GrafNav_2_OMG.html) for Waypoint GrafNav exports.
