---
layout: default
title: AuketoNav
parent: Navigation Tools
nav_order: 5
tool_name: AuketoNav
source_path: code/nav/AuketoNav.c
category: Navigation & Georeferencing
input_formats: ["ASCII text (Auke TGO / Peter Stewart custom heave & nav)"]
output_formats: [".nav (jcu_nav_rec binary)"]
related_tools: ["AGCtoNav", "Generic_to_Nav", "NJWtoNav", "mergeNav", "avNav"]
---

# AuketoNav

## Description
`AuketoNav` converts custom ASCII GPS/RTK navigation and height logs (originally developed for Auke TGO post-processed GPS outputs in April 2008, and extended in April 2012 with `-peter_stewart` for modified heave/height time-series files) into the standard 48-byte OMG binary navigation format (`jcu_nav_rec`, `.nav`).

In both modes, `AuketoNav` stores the parsed vertical height or heave column in the `tide_rec.azi` field of the output `.nav` record so that it can be smoothed with [`avNav`](avNav.md), inspected with [`dumpnav`](dumpnav.md), or merged as a vertical correction.

---

## Usage

```bash
AuketoNav [OPTIONS] -comp <output.nav> <input_ascii_file(s)>
```

### Common Workflow Examples

**1. Convert standard 9-column Auke TGO ASCII navigation & height files:**
```bash
AuketoNav -comp tgo_rtk.nav line01_tgo.txt line02_tgo.txt
```

**2. Convert Peter Stewart 6-column Julian Day + seconds-since-midnight heave/height files:**
```bash
AuketoNav -peter_stewart -year 2012 -comp stewart_heave.nav heave_dump.txt
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-comp <filename>` | **Required.** Output binary `.nav` filename (`jcu_nav_rec` format). | None |
| `<tgo_ssp_infile(s)>` | **Required.** One or more input ASCII navigation/height files (up to 300 files). | None |
| `-peter_stewart` | Parse the 6-column Peter Stewart custom format (`jday secs_since_midnight lat lon height fdum`) instead of the default 9-column Auke TGO format. Requires `-year`. | Disabled (Auke TGO format) |
| `-year <YYYY>` | 4-digit survey year. **Required** when using `-peter_stewart` (since the file only contains Julian day and seconds of day). | `-1` |
| `-jday <DDD>` | Julian day parameter parsed from the command line (`day = strtoint(*argv)`). | `-1` |
| `-skip <N>` | Decimation value parsed from the command line (`skip = strtoint(*argv)`). | `1` |
| `-v` | Enable verbose flag (`verbose_flag`). | Disabled |

---

## Input & Output Record Formats

### 1. Default Auke TGO Format (9 columns)
Each whitespace-delimited line in the input file contains:
```text
<hour> <min> <sec> <day> <month> <year> <lat_deg> <lon_deg> <height_m>
```
* `hour`, `min`, `sec`: Integer UTC time of day (`%hd`).
* `day`, `month`, `year`: Integer calendar date (`%hd`). Converted to Julian day via `stdtime_dmy_to_jul_day(day, month, year)` and then to Unix epoch seconds via `stdtime_from_jul_day(year, jday, hour, min, sec)`.
* `lat_deg`, `lon_deg`: Geographic coordinates in decimal degrees (`%lf`).
* `height_m`: Ellipsoidal/antenna height or vertical offset (`%f`), stored in `tide_rec.azi`.

### 2. Peter Stewart Format (`-peter_stewart`, 6 columns)
Each whitespace-delimited line in the input file contains:
```text
<jday> <secs_since_midnight> <lat_deg> <lon_deg> <height_m> <fdum>
```
* `jday`: Day of year (`1..366`, `%hd`).
* `secs_since_midnight`: Floating-point seconds since `00:00:00` UTC (`%lf`). Added to `stdtime_from_jul_day(year, jday, 0, 0, 0)`. (Note: `dtime` is declared as `int`, so timestamps are truncated to integer seconds with `centisecs = 0.0`).
* `lat_deg`, `lon_deg`: Geographic latitude and longitude in decimal degrees (`%lf`).
* `height_m`: Height/heave value (`%f`), stored in `tide_rec.azi`.
* `fdum`: Sixth floating-point column read and discarded.

### Output Binary Structure (`jcu_nav_rec`)
For every parsed line, `AuketoNav` writes a 48-byte `jcu_nav_rec` record:
* `lat`, `lon`: Decimal degrees.
* `time`: Unix epoch seconds (`int`).
* `centisecs`: `0.0`.
* `azi`: `height` (float).
* `velocity`: `0.0`.
* `flag[0..3]`: `0`.

---

## How It Works

1. Parses command-line arguments and opens the output binary `.nav` file (`-comp`).
2. Loops over all input files (`name[0 .. no_files-1]`).
3. If `-peter_stewart` is enabled, reads 6-column records using `fscanf(file, "%hd%lf%lf%lf%f%f", ...)` until EOF or format mismatch, computing Unix epoch time from the CLI `-year` and the record's `jday` + `secs_since_midnight`.
4. Otherwise (or after the `-peter_stewart` loop), scans 9-column Auke TGO records using `fscanf(file, "%hd%hd%hd%hd%hd%hd%lf%lf%f", ...)`, converting `day/month/year` to Julian day and Unix epoch time.
5. Writes each populated `jcu_nav_rec` sequentially to the output `.nav` file via `nav_write()`.
