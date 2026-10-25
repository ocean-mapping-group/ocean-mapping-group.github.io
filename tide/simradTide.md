---
layout: default
title: simradTide
parent: Tidal Reduction & Constituents (tide)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
tool_name: simradTide
source_path: code/tide/simradTide.c
category: tide
input_formats:
- Simrad ASCII tide file
output_formats:
- JHC ASCII tide (jday hour min -MLLWlevel)
related_tools:
- binTide
- mergeTide
---

# simradTide

## Overview

`simradTide` converts Simrad multibeam ASCII tide files (fixed-column `YYYYMMDDHHMM` followed by water level) into the 4-column JHC ASCII tide format (`jday hour min tide`), inverting the sign of the water level (`-MLLWlevel`) to match OMG's tide sign convention.

---

## Syntax & CLI Options

```bash
simradTide [OPTIONS] -in <tidefilename> -out <mytideformatname>
```

| Option | Description | Default |
|---|---|---|
| `-in <filename>` | **Required.** Input Simrad ASCII tide file (1 header line). | None |
| `-out <filename>` | **Required.** Output 4-column JHC ASCII tide file (`jday hour min tide`). | None |
| `-v` | Print parsed year, month, day, hour, minute, and water level to stdout. | Disabled |

---

## How It Works

1. **Header Skipping:** Reads and discards `1` header line at the top of the input file.
2. **Fixed-Column Slicing:** For each subsequent line:
   - Bytes `[0..3]`: 4-digit `year` (`YYYY`)
   - Bytes `[4..5]`: 2-digit `month` (`MM`)
   - Bytes `[6..7]`: 2-digit `day` (`DD`)
   - Bytes `[8..9]`: 2-digit `hour` (`HH`)
   - Bytes `[10..11]`: 2-digit `min` (`mm`)
   - Bytes `[12..17]`: floating-point water level (`MLLWlevel`)
3. **Julian Day & Sign Inversion:** Computes `jday` via `stdtime_dmy_to_jul_day(day, month, year)` and writes `jday hour min -MLLWlevel` to `-out`.

---

## Examples

**Convert a Simrad tide file to OMG binary tide format:**

```bash
simradTide -in simrad_tide.txt -out omg_tide.asc
binTide -year 2004 omg_tide.asc omg_tide.bin
mergeTide -tide omg_tide.bin merged/JD120/*.merged
```

---

## Workflow Context

- **Upstream:** Kongsberg / Simrad SIS or Neptune ASCII tide files.
- **Downstream:** [`binTide`](binTide.html) $\rightarrow$ [`mergeTide`](mergeTide.html).
