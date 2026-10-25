---
layout: default
title: usgsTide
parent: Tidal Reduction & Constituents (tide)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
tool_name: usgsTide
source_path: code/tide/usgsTide.c
category: tide
input_formats:
- USGS / Rich Signell 7-column ASCII tide
output_formats:
- JHC ASCII tide (jday hour min tide)
related_tools:
- cncTide
- binTide
- mergeTide
---

# usgsTide

## Overview

`usgsTide` converts 7-column USGS / Rich Signell ASCII tide model or gauge files (`year month day hour min sec rtide`) into the 4-column JHC ASCII tide format (`jday hour min rtide`).

---

## Syntax & CLI Options

```bash
usgsTide [OPTIONS] -tide <tidefilename> <outfilename>
```

| Option | Description | Default |
|---|---|---|
| `-tide <filename>` | **Required.** Input 7-column USGS ASCII tide file (`year month day hour min sec rtide`). | None |
| `<outfilename>` | **Required.** Output 4-column JHC ASCII tide file (`jday hour min rtide`). | None |
| `-v` | Print `year month day hour` diagnostics for each record. | Disabled |

---

## How It Works

1. Reads 7 whitespace-delimited fields per line (`fscanf(tidefile, "%d%d%d%d%d%d%f", &year, &month, &day, &hour, &min, &sec, &rtide)`).
2. Converts `(month, day)` to standard 365-day Julian day (`day += month_offset`).
3. Writes `day hour min rtide` (with two decimal places `%.2f`) to both `stdout` and `<outfilename>`.

---

## Examples

**Convert a 7-column USGS tide file to OMG binary format:**

```bash
usgsTide -tide signell_stellwagen.txt stellwagen.asc
binTide -year 1994 stellwagen.asc stellwagen.bin
mergeTide -tide stellwagen.bin merged/*.merged
```

---

## Workflow Context

- **See Also:** [`cncTide`](cncTide.html) (which adds `-fmt 2` and `-y2k` support for Rich Signell's tide format).
- **Downstream:** [`binTide`](binTide.html) $\rightarrow$ [`mergeTide`](mergeTide.html).
