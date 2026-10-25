---
layout: default
title: mvp2hips
parent: HIPS Goodies (hips_goodies)
nav_order: 2
tool_name: mvp2hips
source_path: code/hips_goodies/mvp2hips.c
category: Caris HIPS Conversion Utilities
input_formats: [".001c (MVP calculated sound speed file)", ".svp"]
output_formats: [".svp (CARIS HIPS SVP_VERSION_2)"]
related_tools: ["heli2caris", "read_kmall", "mergeAtt", "newMergeAtt"]
---

# mvp2hips

## Overview

`mvp2hips` (`code/hips_goodies/mvp2hips.c`) is a command-line sound velocity profile conversion utility authored by Jason Bartlett (Canadian Hydrographic Service, Burlington, March 2005). It reads a calculated **Moving Vessel Profiler (MVP)** ASCII cast file (conventionally named with a `c` suffix, such as `jul08.001c`) and converts it into a **CARIS HIPS `.svp` Version 2** sound velocity profile file.

During underway multibeam hydrographic surveys, an MVP free-fall fish measures pressure/depth, sound velocity, and temperature while the survey vessel is steaming. The MVP controller software outputs a calculated profile header containing the cast date (`CALC`, `DATE`, `TIME`), a tabular block of depth, sound speed, and temperature observations, and a trailing NMEA `$GPGGA` sentence recording the geographic coordinates of the cast. `mvp2hips` extracts these metadata fields and sound speed samples and formats them into a CARIS HIPS `Section` record.

---

## Usage

```bash
mvp2hips <input.001c> <output.svp>
```

> [!WARNING]
> **Command-Line Argument Check Quirk (`argc != 2`)**:
> In `code/hips_goodies/mvp2hips.c` (line 23), the argument count check is written as `if (argc != 2)` before opening both `argv[1]` (input file) and `argv[2]` (output file). Because `argc` includes the program name (`argv[0]`), passing two filename arguments results in `argc == 3`, which triggers the usage message and exits unless `mvp2hips.c` is patched to `if (argc != 3)`.

---

## Internal Parsing Pipeline & Data Structures

`mvp2hips` allocates three static 2,000-element floating-point arrays on the stack to buffer the cast:

| Buffer / Variable | Type | Description |
| :--- | :--- | :--- |
| `depth[2000]` | `float[2000]` | Sample depth in meters parsed via `atof(&string[0])` from column 1 of each cast row. |
| `speed[2000]` | `float[2000]` | Calculated sound velocity in m/s parsed from token 1 (`strtok(string, "  ")`). |
| `temp[2000]` | `float[2000]` | Water temperature in °C parsed from token 2 (`strtok(0, "  ")`). |
| `year`, `JD`, `time` | `int` | Cast year (offset `+16` after `"CALC"` on line 1), Julian Day (offset `+7` after `"DATE"` on line 3), and `HHMM` timestamp (offset `+5` after `"TIME"` on line 3). |
| `Lat`, `Long` | `double` | Raw NMEA `$GPGGA` latitude (`DDMM.MMMM`, token 1) and longitude (`DDDMM.MMMM`, token 3) from the `$`-prefixed trailer line. |

### Step-by-Step Conversion Logic

1. **Header Date & Time Extraction**:
   - Reads line 1 (`fgets`), locates `"CALC"` via `strstr()`, advances 16 bytes, and parses `year = atoi(tester)`.
   - Skips line 2, reads line 3, locates `"DATE"` (+7 bytes) for `JD` (Julian Day) and `"TIME"` (+5 bytes) for `time` (`HHMM`), splitting `time` into hours (`a = time / 100`) and minutes (`c = (int)b + 1`).
2. **Depth / Sound Speed Table Scan**:
   - Skips 2 additional header lines and loops until a line starting with `'$'` (the NMEA `$GPGGA` trailer) is encountered.
   - Populates `depth[j]`, `speed[j]`, and `temp[j]` for up to 2,000 depth levels.
3. **NMEA `$GPGGA` Coordinate Conversion**:
   - Tokenizes the `$`-prefixed line on commas (`,`) to extract `Lat` and `Long` in NMEA `DDMM.MMMM` format, then decomposes them into integer degrees, minutes, and seconds (`e:g:l` for Latitude, `f:h:k` for Longitude, with `f = -(int)Long / 100` for West longitude).
4. **CARIS `.svp` Output Generation**:
   - Writes the header `SVP_VERISON_2` (note the historic spelling in source line 99), `F:`, and `Section <year>-<JD> <HH>:<MM>:00 <LatD>:<LatM>:<LatS> <LonD>:<LonM>:<LonS>`, followed by `%0.2f %0.2f` depth and sound speed pairs for all non-zero sound speed samples.

---

## Architectural Fit

Alongside [`heli2caris`](heli2caris.md), `mvp2hips` supports multi-software hydrographic processing environments where MVP casts collected during OMG/UNB multibeam operations must also be imported into CARIS HIPS project vessel configurations.
