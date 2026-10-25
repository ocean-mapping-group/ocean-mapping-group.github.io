---
layout: default
title: switchTide
parent: Tidal Reduction & Constituents (tide)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
tool_name: switchTide
source_path: code/tide/switchTide.c
category: tide
input_formats:
- 7-column Predicted Tide ASCII
output_formats:
- JHC ASCII tide (jday hour min tide)
- COWLIS ASCII tide (-cowlis)
related_tools:
- convTide
- binTide
- mergeTide
---

# switchTide

## Overview

`switchTide` converts 7-column predicted tide ASCII files (`dum1 hour min dum2 day month rtide`) into either the standard 4-column JHC ASCII tide format (`jday hour min rtide`) or COWLIS-formatted ASCII strings (`94/month/day hour:min:00 rtide 0.030` when `-cowlis` is specified).

---

## Syntax & CLI Options

```bash
switchTide [OPTIONS] <infilename> <outfilename>
```

| Option | Description | Default |
|---|---|---|
| `<infilename>` | **Required.** Input 7-column predicted tide ASCII file. | None |
| `<outfilename>` | **Required.** Output JHC ASCII (or COWLIS ASCII) tide file. | None |
| `-cowlis` | Write output in COWLIS format (`94/MM/DD HH:MM:00 tide 0.030`) instead of `jday hour min tide`. | Disabled (JHC ASCII) |
| `-verbose` | Print converted `jday hour min rtide` records to stdout. | Disabled |

---

## How It Works

1. Reads 7 whitespace-separated fields from `<infilename>`:

   ```c
   fscanf(floatfile, "%d%d%d%d%d%d%f", &dum1, &hour, &min, &dum2, &day, &month, &rtide)
   ```
2. **Default Mode:** Converts `(month, day)` into cumulative day of year (`1..365`) and writes `day hour min rtide` to `<outfilename>`.
3. **`-cowlis` Mode:** Preserves `month` and `day` and writes `94/<month>/<day> <hour>:<min>:00 <rtide> 0.030` so the file can be processed by tools expecting COWLIS input (such as [`convTide`](convTide.html)).

---

## Examples

**1. Convert a 7-column predicted tide file to JHC ASCII:**

```bash
switchTide pred_tide.txt jhc_tide.asc
binTide -year 1994 jhc_tide.asc jhc_tide.bin
```

**2. Convert to COWLIS format:**

```bash
switchTide -cowlis pred_tide.txt cowlis_tide.txt
```

---

## Workflow Context

- **Downstream:** [`binTide`](binTide.html) $\rightarrow$ [`mergeTide`](mergeTide.html) (or [`convTide`](convTide.html) if `-cowlis` is used).
