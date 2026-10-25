---
layout: default
title: noaaTide
parent: Tide Tools
tool_name: noaaTide
source_path: code/tide/noaaTide.c
category: tide
input_formats: ["Legacy NOAA 8-column DCP ASCII tide"]
output_formats: ["JHC ASCII tide (jday hour min tide)"]
related_tools: ["noaaTC_Tide", "binTide", "mergeTide"]
---

# noaaTide

## Overview

`noaaTide` converts legacy 8-column NOAA Data Collection Platform (DCP) ASCII water-level files (`sid dcp YY/MM/DD HH:MM:SS tide flat rofc t_flag`) into the 4-column JHC ASCII tide format (`jday hour min tide`).

---

## Syntax & CLI Options

```bash
noaaTide [OPTIONS] <infilename> <outfilename>
```

| Option | Description | Default |
|---|---|---|
| `<infilename>` | **Required.** Input legacy 8-column NOAA ASCII tide file. | None |
| `<outfilename>` | **Required.** Output 4-column JHC ASCII tide file. | None |
| `-shift <days> <hours> <mins>` | Apply an integer time shift (`shift_day`, `shift_hour`, `shift_min`) to each timestamp before computing day-of-year. | `0 0 0` |
| `-v` | Print converted `jday hour min tide` records to stdout. | Disabled |

---

## How It Works

1. Reads 8 whitespace-separated tokens per record:
   ```c
   fscanf(floatfile, "%d%d%s%s%f%d%d%d", &sid, &dcp, &str1, &str2, &rtide, &flat, &rofc, &t_flag)
   ```
2. Extracts 2-digit `year`, `month`, and `day` from `str1` (`YY/MM/DD`) and `hour`, `min`, `sec` from `str2` (`HH:MM:SS`).
3. Applies any time offset specified via `-shift <days> <hours> <mins>`, converts `(month, day)` to day-of-year (`1..365`), and writes `day hour min rtide` to `<outfilename>`.

---

## Examples

**Convert a legacy NOAA DCP tide file with a +5 hour timezone shift to UTC:**
```bash
noaaTide -shift 0 5 0 noaa_dcp.raw noaa_utc.asc
binTide -year 1994 noaa_utc.asc noaa_utc.bin
```

---

## Workflow Context

- **Upstream:** Legacy NOAA NOS/DCP water level logs.
- **Modern Alternative:** Use [`noaaTC_Tide`](noaaTC_Tide.md) for modern NOAA CO-OPS Tides & Currents web exports.
- **Downstream:** [`binTide`](binTide.md) $\rightarrow$ [`mergeTide`](mergeTide.md).
