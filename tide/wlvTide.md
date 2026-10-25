---
layout: default
title: wlvTide
parent: Tidal Reduction & Constituents (tide)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
tool_name: wlvTide
source_path: code/tide/wlvTide.c
category: tide
input_formats:
- .wlv ASCII water level file
- XTide UTC ASCII tide
output_formats:
- JHC ASCII tide (jday hour min tide)
related_tools:
- medsTide
- refoXTIDE
- binTide
- mergeTide
---

# wlvTide

## Overview

`wlvTide` converts `.wlv` water level ASCII files (such as Caris / CHS `.wlv` files with a 24-line header) and UTC XTide text outputs (`-UTC`) into the 4-column JHC ASCII tide format (`jday hour min tide`).

---

## Syntax & CLI Options

```bash
wlvTide [OPTIONS] -in <tidefilename> -out <mytideformatname>
```

| Option | Description | Default |
|---|---|---|
| `-in <filename>` | **Required.** Input `.wlv` or XTide UTC ASCII file. | None |
| `-out <filename>` | **Required.** Output 4-column JHC ASCII tide file (`jday hour min tide`). | None |
| `-skip <N>` | Number of header lines to skip at the beginning of the input file. | `24` |
| `-MDY` | Parse date strings as `MM/DD/YYYY` instead of the default `YYYY/MM/DD`. | `YMD` (`YYYY/MM/DD`) |
| `-UTC` | Expect an extra timezone token (`UTC`) between the time string and the tide value (`date time TZ tide`, as produced by XTide in 24-hour UTC mode). | Disabled (`date time tide`) |
| `-v` | Print parsed year, month, day, hour, minute, and tide height for each line. | Disabled |

---

## How It Works

1. **Header Skipping:** Reads and skips the first `skip` lines (default `24`).
2. **Line Parsing:**
   - Default mode: `sscanf(linestring, "%s %s %f", datestring, timestring, &tide)`
   - `-UTC` mode: `sscanf(linestring, "%s %s %s %f", datestring, timestring, am_pm, &tide)`
3. **Date & Time Extraction:**
   - In default `YMD` mode, extracts `year` from `datestring[0..3]`, `month` from `datestring[5..6]`, and `day` from `datestring[8..9]`.
   - In `-MDY` mode, extracts `month` from `datestring[0..1]`, `day` from `datestring[3..4]`, and `year` from `datestring[6..9]`.
   - Extracts `hour` (`timestring[0..1]`) and `min` (`timestring[3..4]`).
4. **Julian Day Calculation:** Computes `jday` via `stdtime_dmy_to_jul_day(day, month, year)` and writes `jday hour min tide` to `-out`.

---

## Examples

**1. Convert a standard `.wlv` file (24-line header, `YYYY/MM/DD`):**

```bash
wlvTide -in station_001.wlv -out station_001.asc
binTide -year 2007 station_001.asc station_001.bin
```

**2. Convert a 24-hour UTC XTide listing with `MM/DD/YYYY` dates and 4 header lines:**

```bash
wlvTide -skip 4 -UTC -MDY -in xtide_utc.txt -out xtide_utc.asc
```

---

## Workflow Context

- **Upstream:** `.wlv` water level gauge files or XTide UTC text files.
- **Downstream:** [`binTide`](binTide.html) $\rightarrow$ [`mergeTide`](mergeTide.html).
