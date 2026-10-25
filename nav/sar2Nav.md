---
layout: default
title: sar2Nav
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 30
tool_name: sar2Nav
source_path: code/nav/sar2Nav.c
category: Navigation & Georeferencing
input_formats:
- JPL AIRSAR ASCII navigation
output_formats:
- .nav
related_tools:
- toNav
- video2Nav
- xsonar2Nav
- appendNav
---

# sar2Nav

## Description
`sar2Nav` (authored by John Hughes Clarke, February 1995) converts NASA/JPL **AIRSAR** (Airborne Synthetic Aperture Radar) ASCII flight navigation logs into the binary OMG navigation format (`.nav`, `jcu_nav_rec`).

Each input AIRSAR file begins with a 224-byte ASCII header block followed by whitespace-delimited records containing UTC time (`hour min sec`), `PDOP`, latitude in degrees/minutes/seconds (`latdeg latmin latsec`), longitude in degrees/minutes/seconds (`londeg lonmin lonsec`), and aircraft `altitude`.

---

## Usage

```bash
sar2Nav [-v] [-new] [-skip <N>] -comp <out_navfile> <airsar_file(s)>
```

### Common Workflow Examples

**1. Convert JPL AIRSAR flight track files into a binary `.nav` file:**

```bash
sar2Nav -comp airsar_track.nav flight_01.sar flight_02.sar
```

**2. Convert with verbose record printout:**

```bash
sar2Nav -v -comp airsar_track.nav flight_01.sar
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-comp <filename>` | **Required.** Output binary `.nav` filename (`tidename`). | None |
| `<airsar_file(s)>` | **Required.** One or more JPL AIRSAR navigation files (up to 300 files). | None |
| `-v` | Verbose mode: prints `hour min sec PDOP lat lon alt` for every parsed record. | Disabled |
| `-new` | Parsed on the command line (`new_flag++`); both branches read the 224-byte header block. | Disabled |
| `-skip <N>` | Parsed on the command line (`skip`), legacy option from `toNav`. | `1` |

---

## Input & Output Record Formats

### Input JPL AIRSAR Format
1. **Header Block (224 bytes):**
   The first 224 bytes of each input file are read via `fread(&headerstring, 224, 1, file)` and echoed to `stdout`.
2. **Data Records (11 ASCII fields per record):**
   Parsed via `fscanf(file, "%hd%hd%hd%f%d%d%f%d%d%f%f", ...)`:

   ```text
   hour  min  sec  PDOP  latdeg  latmin  latsec  londeg  lonmin  lonsec  altitude
   ```
   * If `latdeg < 0`, `latmin` and `latsec` are negated so that:
     $$\text{latitude} = \text{latdeg} + \frac{\text{latmin}}{60.0} + \frac{\text{latsec}}{3600.0}$$
   * If `londeg < 0`, `lonmin` and `lonsec` are similarly negated to compute decimal `longitude`.

### Output Binary `.nav` (`jcu_nav_rec`)
For every 11-field record read, `sar2Nav` populates a 48-byte `jcu_nav_rec`:
* `lat`, `lon`: Decimal degrees.
* `time`: Computed via `stdtime_from_jul_day(1994, 272, hour, min, sec)` *(hardcoded to the 1994 JPL AIRSAR survey campaign epoch: Year `1994`, Julian Day `272` / Sept 29, 1994)*.
* `centisecs`: `0`.
* `azi`: `0.0`.
* `velocity`: `0.0` *(Note: `tide_rec.velocity = altitude` is assigned on line 162 and then overwritten with `0.0` on line 165)*.
* `depth`: `0`.
* `flag[0]`: `0`, `flag[1]`: `0`, `flag[2]`: `(short)(PDOP * 10.0)`, `flag[3]`: `0`.
