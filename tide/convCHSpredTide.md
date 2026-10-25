---
layout: default
title: convCHSpredTide
parent: Tide Tools
tool_name: convCHSpredTide
source_path: code/tide/convCHSpredTide.c
category: tide
input_formats: ["CHS Predicted Tide ASCII", "Cape Enrage Measured Tide ASCII"]
output_formats: ["JHC ASCII tide (jday hour min elev)"]
related_tools: ["binTide", "mergeTide", "medsTide", "cncTide"]
---

# convCHSpredTide

## Overview

`convCHSpredTide` converts Canadian Hydrographic Service (CHS) predicted hourly tide tables—or Cape Enrage 5-minute/custom-interval measured tide tables (`-enrage_meas`)—into the standard 4-column JHC ASCII tide format (`jday hour min elevation_m`).

---

## Syntax & CLI Options

```bash
convCHSpredTide [OPTIONS] -tide <tidefilename> <outfilename>
```

| Option | Description | Default |
|---|---|---|
| `-tide <filename>` | **Required.** Input CHS predicted tide file (or Cape Enrage measured tide file). | None |
| `<outfilename>` | **Required.** Positional output filename for the converted JHC ASCII tide records. | None |
| `-jday_start <N>` | Starting Julian day offset (`jday_start + day_of_month`) added to the day number read from the CHS predicted table (use `jday_of_first_of_month - 1`). | `0` |
| `-enrage_meas` | Parse Cape Enrage measured tide format (`year jday hour min dmin` followed by 12 centimeter elevation values per record) instead of standard 24-hour CHS tables. | Disabled |
| `-v` | Enable verbose flag. | Disabled |

---

## How It Works

1. **Standard CHS Predicted Mode (Default):**
   - Skips the first `18` header lines of the CHS predicted tide file.
   - Reads each daily block starting with the day number (`day`), followed by `24` hourly floating-point tide elevations (`elev`, in meters).
   - Writes 24 lines per day to `<outfilename>` (and `stdout`) formatted as:
     ```text
     <jday_start + day> <hour (1..24)> 0 <elev>
     ```
2. **Cape Enrage Measured Mode (`-enrage_meas`):**
   - Reads records containing `year jday hour min dmin` followed by `12` consecutive elevation readings in centimeters.
   - Divides each elevation by `100.0` to convert centimeters to meters and increments the minute field by `i * dmin` (`i = 0..11`), writing `jday hour min elev_m`.

---

## Examples

**1. Convert a CHS predicted monthly tide table starting on May 1 (Julian Day 121, so `-jday_start 120`):**
```bash
convCHSpredTide -jday_start 120 -tide chs_may_pred.txt may_tide.asc
binTide -year 2002 may_tide.asc may_tide.bin
```

**2. Convert Cape Enrage measured centimeter tide blocks:**
```bash
convCHSpredTide -enrage_meas -tide enrage_raw.txt enrage_tide.asc
```

---

## Workflow Context

- **Next Step:** Pass the output JHC ASCII tide file into [`binTide`](binTide.md) to create a binary `jcu_nav_rec` tide file, then apply it to `.merged` survey lines with [`mergeTide`](mergeTide.md).
