---
layout: default
title: heli2caris
parent: CARIS HIPS Integration Utilities (hips_goodies)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 1
tool_name: heli2caris
source_path: code/hips_goodies/heli2caris.c
category: Caris HIPS Conversion Utilities
input_formats:
- OEM4 ASCII GPS
- PRTKA ASCII GPS
- NMEA GGA (.txt, .log)
output_formats:
- CARIS FOF/NTX command script
related_tools:
- mvp2hips
- stripNav
- iNav2SHP
---

# heli2caris (and `helo2caris.cpp`)

## Overview

`heli2caris` (`code/hips_goodies/heli2caris.c`) and its companion C++ source file `helo2caris.cpp` (`code/hips_goodies/helo2caris.cpp`) are interactive command-line utilities developed by Jason Bartlett (CHS Burlington, March 2005) for converting raw helicopter-logged GPS data strings into CARIS (Computer Aided Resource Information System) feature-coded line input files.

In Canadian Hydrographic Service (CHS) shoreline and intertidal surveys, a helicopter flies along coastal features while logging GPS positions. `heli2caris` reads the resulting ASCII GPS log—supporting **NovAtel OEM4**, **NovAtel PRTKA**, and standard **NMEA `$GPGGA`** sentence formats—and generates a CARIS batch command stream that opens a feature file (`opvfof`), assigns the vessel/survey ID (`opid`), projection/unit header (`opun94...`), elevation (`lico`), and CHS feature code (`clsl`, `cllwrlltsm`, `cllw`, or user-specified), emits `/ge=<Lat>,<Long>` geographic vertex directives, and closes the line feature (`q`, `opvfon`, `oppmcr`).

---

## Differences Between `heli2caris.c` and `helo2caris.cpp`

Both files implement the exact same CARIS formatting state machine and GPS string tokenizers, differing only in how input/output filenames and file streams are handled:

| Aspect | `heli2caris.c` (Compiled by `makefile`) | `helo2caris.cpp` (Legacy C++ Variant) |
| :--- | :--- | :--- |
| **Language & I/O** | Standard C (`stdio.h`, `FILE *fin`, `FILE *fout`, `fgets`) | Legacy C++ (`fstream.h`, `iostream.h`, `fstream infile`, `infile.getline`) |
| **File Arguments** | Passed on the command line: `heli2caris <infile> <outfile>` (`argv[1]`, `argv[2]`) | Prompted interactively via `scanf("%s", input)` and `scanf("%s", outputfile)` |
| **Build Status** | Built automatically by `code/hips_goodies/makefile` (`$(wildcard *.c)`) | Kept in `code/hips_goodies/` as original C++ reference source |

---

## Usage & Interactive Prompts

### Command-Line Invocation (`heli2caris`)

```bash
heli2caris <input_gps_file> <output_caris_file>
```

### Interactive Session Flow

Once launched, `heli2caris` prompts the operator on `stdin` for survey metadata and GPS sentence format:

1. **Julian Day (`1`–`366`)**:
   - Prompt: `Enter the Julian day!`
   - Validated in a `while (day > 366 || day < 1)` loop.
2. **Survey Year (4-digit year)**:
   - Prompt: `Enter the year!`
   - Subtracted by `2000` (`year = year - 2000`) and zero-padded if `year < 10` when writing `opid` and `opun94` headers.
3. **Vessel / Platform ID (exact 4-character code)**:
   - Prompt: `Enter the vessel ID(4 characters)!`
   - Validated via `while (strlen(userID) != 4)`.
4. **CARIS Feature Code Selection (`1`–`4`)**:
   - `1`: `clsl` (Coastline / Shoreline)
   - `2`: `cllwrlltsm` (Coastline Low Water Rock Ledge / Foreshore)
   - `3`: `cllw` (Coastline Low Water Line)
   - `4`: `OTHER` — prompts the user to enter a custom feature code string (`char code[15]`).
5. **Feature Elevation (`float Elev`)**:
   - Prompt: `Enter the Elevation!`
   - Written with `%0.1f` precision immediately following the `lico` directive.
6. **GPS Format String Type (`1`–`3`)**:
   - `1`: **OEM4** (NovAtel OEM4 comma/semicolon-delimited log; skips header line, extracts token 11 as decimal degrees `Lat` and token 12 as `Long`, negating `Long = Long * -1` for Western Hemisphere convention).
   - `2`: **PRTKA** (Comma-delimited kinematic log; skips header line, extracts token 1 as `Lat` and token 2 as `Long`, negating `Long = Long * -1`).
   - `3`: **GGA** (NMEA `$GPGGA` comma-delimited sentence; skips first line, extracts token 1 as `DDMM.MMMM` latitude and token 3 as `DDDMM.MMMM` longitude, converts degrees-minutes `Lat / 100` and `Long / 100` into decimal degrees via `(temp2 * 100) / 60`).

---

## Output Format Structure

```text
opvfof
opidHELI05063
opun9405063
oppmba
lico
0.0
clsl
/ge=44.62518420,-63.57192840
/ge=44.62521050,-63.57195110
q
q

opvfon
oppmcr
```

---

## Architectural Fit

Within the OMG software ecosystem, `heli2caris` is part of the `hips_goodies/` auxiliary toolkit used when exchanging field data between UNB OMG tools and CARIS HIPS/SIPS or GIS packages.
