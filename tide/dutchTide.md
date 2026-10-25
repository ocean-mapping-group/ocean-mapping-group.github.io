---
layout: default
title: dutchTide
parent: Tidal Reduction & Constituents (tide)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
tool_name: dutchTide
source_path: code/tide/dutchTide.c
category: tide
input_formats:
- Dutch RWS / North Sea ASCII tide
output_formats:
- JHC ASCII tide (jday hour min MLLW_m)
related_tools:
- binTide
- mergeTide
---

# dutchTide

## Overview

`dutchTide` converts Dutch hydrographic tide gauge / model ASCII files (containing `YYYYMMDD`, `HHMMSS`, Easting, Northing, astronomical tide, surge, MSL water level, and MLLW water level in centimeters) into the 4-column JHC ASCII tide format (`jday hour min tide_m`).

---

## Syntax & CLI Options

```bash
dutchTide [OPTIONS] -in <tidefilename> -out <mytideformatname>
```

| Option | Description | Default |
|---|---|---|
| `-in <filename>` | **Required.** Input Dutch ASCII tide file (7-line header). | None |
| `-out <filename>` | **Required.** Output JHC ASCII tide filename (`jday hour min elev_m`). | None |
| `-v` | Print verbose date, time, and elevation values to stdout. | Disabled |

---

## How It Works

1. **Header Skipping:** Skips the first `7` header lines of the input file.
2. **Record Parsing:** Reads each data line using:

   ```c
   sscanf(linestring, "%s %s %s %s %d %d %d %d",
          datestring, timestring, eaststring, northstring,
          &tide, &surge, &MSLlevel, &MLLWlevel);
   ```
3. **Date/Time & Unit Conversion:**
   - Extracts `YYYY`, `MM`, `DD` from `datestring` and `HH`, `MM`, `SS` from `timestring`.
   - Computes Julian day (`jday`) via `stdtime_dmy_to_jul_day(day, month, year)`.
   - Converts `MLLWlevel` from centimeters to meters (`(float)MLLWlevel / 100.0`) and writes `jday hour min MLLW_m` to the output file.

---

## Examples

**Convert a Dutch RWS tide file and compile to binary format:**

```bash
dutchTide -in rws_ijmuiden.txt -out ijmuiden.asc
binTide -year 2003 ijmuiden.asc ijmuiden.bin
```

---

## Workflow Context

- **Upstream:** Dutch Rijkswaterstaat (RWS) / Royal Netherlands Navy tide exports.
- **Downstream:** [`binTide`](binTide.html) $\rightarrow$ [`mergeTide`](mergeTide.html).
