---
layout: default
title: noaaTC_Tide
parent: Tide Tools
tool_name: noaaTC_Tide
source_path: code/tide/noaaTC_Tide.c
category: tide
input_formats: ["NOAA Tides & Currents ASCII"]
output_formats: ["JHC ASCII tide (jday hour min tide)"]
related_tools: ["noaaTide", "binTide", "mergeTide"]
---

# noaaTC_Tide

## Overview

`noaaTC_Tide` converts water level files downloaded from the **NOAA Tides & Currents** web portal (`station_id YYYYMMDD HH:MM predicted_tide verified_tide`) into the 4-column JHC ASCII tide format (`jday hour min tide`).

---

## Syntax & CLI Options

```bash
noaaTC_Tide [OPTIONS] -in <tidefilename> -out <mytideformatname>
```

| Option | Description | Default |
|---|---|---|
| `-in <filename>` | **Required.** Input NOAA Tides & Currents ASCII file. | None |
| `-out <filename>` | **Required.** Output JHC ASCII tide file (`jday hour min tide`). | None |
| `-skip <N>` | Number of header lines to skip at the beginning of the input file. | `14` |
| `-v` | Print parsed year, month, day, hour, minute, predicted tide, and observed tide for each line. | Disabled |

---

## How It Works

1. **Header Skipping:** Reads and discards the first `skip` lines (default `14`).
2. **Column Parsing:** Parses 5 whitespace-separated fields per line:
   ```c
   sscanf(linestring, "%s %s %s %f %f", am_pm, datestring, timestring, &ptide, &tide);
   ```
   where `datestring` is `YYYYMMDD`, `timestring` is `HH:MM`, `ptide` is column 4 (predicted), and `tide` is column 5 (verified/observed).
3. **Julian Day Conversion:** Converts `(day, month, year)` to Julian day (`jday`) via `stdtime_dmy_to_jul_day` and outputs `jday hour min tide` (using the 5th column `tide`).

---

## Examples

**Convert a NOAA Tides & Currents verified 6-minute water level file:**
```bash
noaaTC_Tide -skip 14 -in noaa_8410140_eastport.txt -out eastport.asc
binTide -year 2007 eastport.asc eastport.bin
```

---

## Workflow Context

- **Upstream:** NOAA Tides & Currents CO-OPS station data exports.
- **Downstream:** [`binTide`](binTide.md) $\rightarrow$ [`mergeTide`](mergeTide.md).
- **See Also:** [`noaaTide`](noaaTide.md) for legacy 8-column NOAA DCP tide files.
