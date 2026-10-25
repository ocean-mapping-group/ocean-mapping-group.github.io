---
layout: default
title: toNav
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 33
tool_name: toNav
source_path: code/nav/toNav.c
category: Navigation & Georeferencing
input_formats:
- Ashtech PNAV fixed-width ASCII
output_formats:
- .nav
related_tools:
- PNAVtoNav
- flagNav
- leverNav
- mergeNav
- appendNav
---

# toNav

## Description
`toNav` (authored by John Hughes Clarke, July 1994) converts fixed-width ASCII **Ashtech PNAV** (Precision Navigation post-processed differential/kinematic GPS) output files into the binary OMG navigation format (`.nav`, `jcu_nav_rec`).

It supports both the original 1994 PNAV format (271-byte file header + 125-byte fixed-width records) and the updated PNAV format (`-new`, 250-byte file header + 105-byte fixed-width records). It also populates satellite count (`flag[0] = SVs`), solution quality flag (`flag[1] = FLAG`, which can be filtered downstream with [`flagNav`](flagNav.html)), and scaled PDOP (`flag[2] = PDOP * 100.0`).

*(Note: For newer free-form PNAV ASCII exports or NavLab binary trajectories, see [`PNAVtoNav`](PNAVtoNav.html)).*

---

## Usage

```bash
toNav [-v] [-new] [-skip <N>] -comp <out_navfile> <pnav_file(s)>
```

### Common Workflow Examples

**1. Convert legacy 125-byte Ashtech PNAV files into a binary `.nav` file:**

```bash
toNav -comp pnav_line1.nav raw_pnav/line1.out
```

**2. Convert 105-byte (`-new`) PNAV files and filter for quality flag >= 3 using `flagNav`:**

```bash
toNav -new -comp rtk_track.nav raw_pnav/*.pnav
flagNav -accept 3 rtk_track.nav
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-comp <filename>` | **Required.** Output binary `.nav` filename (`tidename`). | None |
| `<pnav_file(s)>` | **Required.** One or more Ashtech PNAV ASCII files (up to 300 files). | None |
| `-new` | Use the newer PNAV fixed-width layout (skips a **250-byte** header instead of 271 bytes, reads **105-byte** records instead of 125 bytes, and stores `Height` in meters directly in `tide_rec.azi` for use with [`leverNav`](leverNav.html)). | Disabled (271-byte header, 125-byte records) |
| `-skip <N>` | Parsed on the command line (`skip`). | `1` |
| `-v` | Verbose mode: prints parsed project code, `SVs`, `lat`, `lon`, date/time components, Julian day, and velocity components (`V_east`, `V_north`). | Disabled |

---

## Input & Output Formats

### Input Ashtech PNAV Fixed-Width Record
After skipping the fixed file header (`271` bytes default, `250` bytes with `-new`), `toNav` reads fixed-length chunks (`125` bytes default, `105` bytes with `-new`) and parses 15 fields via `sscanf`:

```text
PROJECT  MM/DD/YY  HH:MM:SS.ss  SVs  PDOP  N/S  latitude  E/W  longitude  Height  RMS  FLAG  V_east  V_north  V_up
```
* **Date Conversion:** Extracts 2-digit `year` (`+ 1900`), `month`, and `day` from `DMY` (`MM/DD/YY`), converts month/day to day-of-year (Julian day), and computes Unix epoch time via `stdtime_from_jul_day(year, day, hour, min, sec)`.
* **Longitude Sign Convention:** Negates the parsed unsigned Western Hemisphere longitude (`tide_rec.lon = -longitude`).

### Output Binary `.nav` Mapping (`jcu_nav_rec`)

| `jcu_nav_rec` Field | Default Mode (125-byte record) | `-new` Mode (105-byte record) |
|---|---|---|
| `lat` | `latitude` (decimal degrees) | `latitude` (decimal degrees) |
| `lon` | `-longitude` (West negative) | `-longitude` (West negative) |
| `time` | UTC seconds since Jan 1, 1970 | UTC seconds since Jan 1, 1970 |
| `centisecs` | `0` | `0` |
| `azi` | Course over ground (degrees) computed from `atan(V_east / V_north)` | `Height` (ellipsoid height in meters, ready for [`leverNav`](leverNav.html)) |
| `velocity` | Horizontal speed $\sqrt{V_{\text{east}}^2 + V_{\text{north}}^2}$ | Horizontal speed $\sqrt{V_{\text{east}}^2 + V_{\text{north}}^2}$ |
| `depth` | `(short)(Height * 1000.0)` (height in mm) | Unmodified (`0`) |
| `flag[0]` | `SVs` (number of satellites) | `SVs` (number of satellites) |
| `flag[1]` | `FLAG` (PNAV solution quality code) | `FLAG` (PNAV solution quality code) |
| `flag[2]` | `(short)(PDOP * 100.0)` | `(short)(PDOP * 100.0)` |
| `flag[3]` | `0` (valid) | `0` (valid) |
