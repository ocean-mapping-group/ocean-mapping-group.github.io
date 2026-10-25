---
layout: default
title: medsTide
parent: Tidal Reduction & Constituents (tide)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
tool_name: medsTide
source_path: code/tide/medsTide.c
category: tide
input_formats:
- DFO MEDS ASCII tide
- XTide AM/PM ASCII tide
output_formats:
- JHC ASCII tide (jday hour min tide)
related_tools:
- binTide
- mergeTide
- convCHSpredTide
- refoXTIDE
- wlvTide
---

# medsTide

## Overview

`medsTide` converts Canadian Marine Environmental Data Section (MEDS / DFO) ASCII water level files—as well as 12-hour AM/PM XTide text predictions (`-xtide`)—into the 4-column JHC ASCII tide format (`jday hour min tide_m`).

---

## Syntax & CLI Options

```bash
medsTide [OPTIONS] -in <tidefilename> -out <mytideformatname>
```

| Option | Description | Default |
|---|---|---|
| `-in <filename>` | **Required.** Input MEDS (or XTide) ASCII tide file. | None |
| `-out <filename>` | **Required.** Output JHC ASCII tide file (`jday hour min tide`). | None |
| `-skip <N>` | Number of header lines to skip at the start of the input file. | `8` (or `0` if `-xtide` is set before `-skip`) |
| `-xtide` | Parse XTide 12-hour format (`YYYY-MM-DD HH:MM AM/PM TZ tide`) and set `skip = 0` (unless overridden by a subsequent `-skip`). | Disabled (default MEDS `DD/MM/YYYY HH:MM:SS AM/PM, tide`) |
| `-v` | Print parsed year, month, day, 24-hour time, and tide value for each record. | Disabled |

---

## How It Works

1. **Header Skipping:** Skips `skip` header lines (default `8` for MEDS files; `0` when `-xtide` is specified).
2. **Delimiter Normalization:** Replaces `/`, `:`, `,`, and date hyphens (`-` within the first 11 characters) with spaces.
3. **Record Parsing & 12-to-24 Hour Conversion:**
   - **Default MEDS mode:** Parses `day month year hour min sec am_pm tide`.
   - **`-xtide` mode:** Parses `year month day hour min am_pm timezone tide`.
   - Converts 12-hour `AM`/`PM` timestamps to 24-hour time (handling `12 PM` $\rightarrow$ `12` and `12 AM` $\rightarrow$ `0` in `-xtide` mode).
4. **Julian Day Calculation:** Converts `(day, month, year)` to Julian day (`jday`) via `stdtime_dmy_to_jul_day` and writes `jday hour min tide` to `-out`.

---

## Examples

**1. Convert a standard DFO MEDS tide gauge file (skipping 8 header lines):**

```bash
medsTide -in meds_saint_john.csv -out saint_john.asc
binTide -year 2007 saint_john.asc saint_john.bin
```

**2. Convert an XTide AM/PM prediction listing:**

```bash
medsTide -xtide -in xtide_pred.txt -out xtide_pred.asc
```

---

## Workflow Context

- **Upstream:** DFO MEDS CSV/ASCII water level downloads or XTide text predictions.
- **Downstream:** [`binTide`](binTide.html) $\rightarrow$ [`mergeTide`](mergeTide.html).
