---
layout: default
title: quebecTide
parent: Tide Tools
tool_name: quebecTide
source_path: code/tide/quebecTide.c
category: tide
input_formats: ["81-byte fixed-record CHS Quebec / Australian tide format"]
output_formats: ["JHC ASCII tide (jday hour min tide_m)"]
related_tools: ["transTide", "convCHSpredTide", "binTide", "mergeTide"]
---

# quebecTide

## Overview

`quebecTide` converts 81-byte fixed-width tide gauge records (containing 12 fifteen-minute centimeter tide readings per 3-hour record) into the 4-column JHC ASCII tide format (`jday hour min tide_m`). It is a variant of [`transTide`](transTide.md).

---

## Syntax & CLI Options

```bash
quebecTide [OPTIONS] -tide <tidefilename> <outfilename>
```

| Option | Description | Default |
|---|---|---|
| `-tide <filename>` | **Required.** Input fixed-record (81-byte) tide file. | None |
| `<outfilename>` | **Required.** Output 4-column JHC ASCII tide file (`jday hour min tide_m`). | None |
| `-v` | Enable verbose output of parsed record headers and 15-minute values. | Disabled |

---

## How It Works

1. Reads 81-byte fixed-length records from `-tide`.
2. Extracts 2-digit `year` (bytes `11..12`), `month` (bytes `13..14`), `day` (bytes `15..16`), and `hour` index (bytes `18..19`).
3. Converts `(month, day)` to leap-year Julian day (`1..366`).
4. Loops over 12 three-character integer fields starting at byte offset `22` (`22 + 5 * i` for `i = 0..11`), divides each integer centimeter reading by `100.0`, and writes `day (hour + i)/4 15*(i%4) tide_m` to `<outfilename>`.

---

## Examples

**Convert an 81-byte fixed-record tide file to JHC ASCII:**
```bash
quebecTide -tide quebec_raw.dat quebec_tide.asc
binTide -year 1992 quebec_tide.asc quebec_tide.bin
```

---

## Workflow Context

- **See Also:** [`transTide`](transTide.md) (which parses the same 81-byte record structure without the initial `getchar` loop) and [`convCHSpredTide`](convCHSpredTide.md).
- **Downstream:** [`binTide`](binTide.md) $\rightarrow$ [`mergeTide`](mergeTide.md).
