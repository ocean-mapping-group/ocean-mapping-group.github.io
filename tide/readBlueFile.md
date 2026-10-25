---
layout: default
title: readBlueFile
parent: Tide Tools
tool_name: readBlueFile
source_path: code/tide/readBlueFile.c
category: tide
input_formats: ["CHS Harmonic Constituent BlueFile"]
output_formats: ["outlist (lat lon station_name)", "stdout harmonic constituents"]
related_tools: ["makeTideSeries", "convCHSpredTide", "medsTide"]
---

# readBlueFile

## Overview

`readBlueFile` parses a Canadian Hydrographic Service (CHS) harmonic constituent **BlueFile** (carriage-return `\r` delimited), extracts tide station coordinates (`lat -lon station_name`) to a file named `outlist`, and prints harmonic constituent amplitudes (in meters) and phases (in degrees) for 41 standard tidal constituents (`Z0`, `O1`, `K1`, `M2`, `S2`, `N2`, `M4`, `MS4`, etc.) to `stdout`.

---

## Syntax & CLI Options

```bash
readBlueFile [OPTIONS] -in <bluefile>
```

| Option | Description | Default |
|---|---|---|
| `-in <filename>` | **Required.** Input CHS harmonic constituent BlueFile. | None |
| `-v` | Enable verbose flag. | Disabled |

---

## How It Works

1. **Line Reading (`getc_line_slashR`):** Reads `\r`-delimited lines from `-in`.
2. **Station Header Records (`S4`):**
   - When a line begins with `"S4"`, extracts the 16-character station name from bytes `[10..25]` (replacing spaces with `_`) and parses `latdeg latmin londeg lonmin` starting at byte `38`.
   - Converts DMS to decimal degrees (`lat = latdeg + latmin/60.0`, `lon = londeg + lonmin/60.0`) and writes `lat -lon station_name` to `outlist` in the current working directory.
3. **Constituent Records:**
   - Parses constituent lines (`J station_no mag_mm phase_decideg timezone num2 num3 X num4 which const_num`).
   - Filters for 41 recognized tidal constituents (`Z0`, `O1`, `K1`, `M2`, `S2`, `M4`, `MS4`, `N2`, `MM`, `Q1`, `J1`, `OO1`, `MU2`, `L2`, `NO1`, `MN4`, `M8`, `2Q1`, `P1`, `2N2`, `NU2`, `K2`, `M3`, `MO3`, `MK3`, `SK3`, `SN4`, `S4`, `2MN6`, `M6`, `2MS6`, `2SM6`, `MSF`, `ALP1`, `UPS1`, `EPS2`, `ETA2`, `2MK5`, `2SK5`, `3MK7`, `M10`).
   - Converts `mag_mm` to meters (`mag_mm / 1000.0`) and `phase_decideg` to degrees (`phase_decideg / 100.0`) and prints them to `stdout`.

---

## Examples

**Extract station coordinates (`outlist`) and harmonic constituents from a CHS BlueFile:**
```bash
readBlueFile -in chs_atlantic.blu > constituents_dump.txt
head outlist
```

---

## Workflow Context

- Used to extract CHS tide station locations and harmonic constituent tables for harmonic tide prediction utilities (`tidecor`).
