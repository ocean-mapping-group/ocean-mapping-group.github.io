---
layout: default
title: transTide
parent: Tidal Reduction & Constituents (tide)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
tool_name: transTide
source_path: code/tide/transTide.c
category: tide
input_formats:
- 81-byte fixed-record Australian (Oz) / CHS tide format
output_formats:
- JHC ASCII tide (jday hour min tide_m)
related_tools:
- quebecTide
- binTide
- mergeTide
---

# transTide

## Overview

`transTide` translates Australian ("Oz") and CHS 81-byte fixed-record tide gauge files (each containing 12 fifteen-minute tide heights in centimeters across a 3-hour block) into the 4-column JHC ASCII tide format (`jday hour min tide_m`).

---

## Syntax & CLI Options

```bash
transTide [OPTIONS] -tide <tidefilename> <outfilename>
```

| Option | Description | Default |
|---|---|---|
| `-tide <filename>` | **Required.** Input 81-byte fixed-record tide file. | None |
| `<outfilename>` | **Required.** Output 4-column JHC ASCII tide file (`jday hour min tide_m`). | None |
| `-v` | Print parsed 4-character station header, date/hour, and 15-minute values to stdout. | Disabled |

---

## How It Works

1. Reads 81-byte blocks continuously (`fread(line, 81, 1, tidefile)`) until EOF.
2. Extracts 2-digit `year` (bytes `11..12`), `month` (bytes `13..14`), `day` (bytes `15..16`), and `hour` index (bytes `18..19`).
3. Converts `(month, day)` to leap-year day-of-year (`1..366`).
4. Loops over the 12 three-character integer centimeter tide readings (`line[22 + 5 * i]` for `i = 0..11`), divides each by `100.0` to convert to meters, and writes `day (hour + i)/4 15*(i%4) tide_m` to `<outfilename>`.

---

## Examples

**Convert an 81-byte Australian tide file to binary OMG tide format:**

```bash
transTide -tide oz_tide.dat oz_tide.asc
binTide -year 1993 oz_tide.asc oz_tide.bin
mergeTide -tide oz_tide.bin merged/*.merged
```

---

## Workflow Context

- **See Also:** [`quebecTide`](quebecTide.html).
- **Downstream:** [`binTide`](binTide.html) $\rightarrow$ [`mergeTide`](mergeTide.html).
