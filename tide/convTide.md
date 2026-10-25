---
layout: default
title: convTide
parent: Tide Tools
tool_name: convTide
source_path: code/tide/convTide.c
category: tide
input_formats: ["COWLIS ASCII tide"]
output_formats: ["JHC ASCII tide (jday hour min tide)"]
related_tools: ["binTide", "mergeTide", "medsTide", "switchTide"]
---

# convTide

## Overview

`convTide` converts Coastal Ocean Water Level Information System (COWLIS) ASCII tide gauge files into the JHC ASCII tide format (`jday hour min tide` or `year jday hour min tide` with `-V2_outyear`) for subsequent binary conversion via [`binTide`](binTide.md).

---

## Syntax & CLI Options

```bash
convTide [OPTIONS] <infilename> <outfilename>
```

| Option | Description | Default |
|---|---|---|
| `<infilename>` | **Required.** Input COWLIS ASCII tide file. | None |
| `<outfilename>` | **Required.** Output JHC ASCII tide file. | None |
| `-y2k` | Parse 4-digit year date strings (`YYYY/MM/DD`) instead of 2-digit year strings (`YY/MM/DD`). | Disabled (2-digit year) |
| `-DMY` | Interpret 2-digit date fields as `DD/MM/YY` instead of `YY/MM/DD`. | `YMD` |
| `-MDY` | Interpret date fields as `MM/DD/YY` (or rearrange `YYYY/MM/DD` in `-type_3`). | `YMD` |
| `-type_2` | Parse 3-column input lines (`date_str time_str tide` without trailing fourth column or seconds field). | `TYPE_1` (4 tokens) |
| `-type_3` | Parse fixed-width 43+ character lines where date is at `[0..9]`, time is at `[11..18]`, and tide is at `[35+]`, outputting `date_str time_str tide`. | `TYPE_1` |
| `-V2_outyear` | Include the year column in the output (`year jday hour min tide`), matching `binTide -V2`. | Disabled (`jday hour min tide`) |
| `-leapyear` | Add 1 day to the cumulative day-of-year calculation for dates after February in leap years. | Disabled |
| `-shift <days> <hours> <mins>` | Apply an integer time offset (`shift_day`, `shift_hour`, `shift_min`) to every timestamp before computing day-of-year. | `0 0 0` |
| `-v` | Print converted records to stdout. | Disabled |

---

## How It Works

1. **Line Parsing (`get_line`):**
   - `TYPE_1` (default): Reads 4 whitespace-separated tokens (`date_str`, `time_str`, `rtide`, `zero`).
   - `TYPE_2` (`-type_2`): Reads 3 whitespace-separated tokens (`date_str`, `time_str`, `rtide`) and sets `sec = 0`.
   - `TYPE_3` (`-type_3`): Reads fixed-column lines (`>= 43` chars), extracting date, time, and tide from character offsets.
2. **Date & Time Extraction:** Extracts `year`, `month`, `day` (reordering if `-DMY` or `-MDY` is set, or parsing 4-digit year if `-y2k` is set) and `hour`, `min`, `sec`.
3. **Time Shifting & Julian Day Conversion:** Applies optional `-shift <day> <hour> <min>` rollovers, converts `(month, day)` into cumulative day of year (adding `+1` if `-leapyear` is specified), and writes the resulting ASCII record.

---

## Examples

**1. Convert a 4-digit-year COWLIS file with year output for `binTide -V2`:**
```bash
convTide -y2k -V2_outyear -type_2 cowlis_2004.txt tide_2004.asc
binTide -V2 tide_2004.asc tide_2004.bin
```

**2. Convert a legacy 2-digit-year DMY file in a leap year:**
```bash
convTide -DMY -leapyear cowlis_96.dat tide_96.asc
```

---

## Workflow Context

- **Upstream:** Raw COWLIS water level text files.
- **Downstream:** [`binTide`](binTide.md) $\rightarrow$ [`mergeTide`](mergeTide.md).
