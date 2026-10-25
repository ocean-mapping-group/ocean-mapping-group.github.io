---
layout: default
title: xsonar2Nav
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 35
tool_name: xsonar2Nav
source_path: code/nav/xsonar2Nav.c
category: Navigation & Georeferencing
input_formats:
- USGS XSONAR ASCII navigation
output_formats:
- .nav
related_tools:
- video2Nav
- mergeNav
- appendNav
- stripNav
---

# xsonar2Nav

## Description
`xsonar2Nav` (authored by John Hughes Clarke, March 1997; header comment `xsonarNav.c`) converts USGS **XSONAR** (Bill Danforth's sidescan sonar processing package) ASCII navigation files into the binary OMG navigation format (`.nav`, `jcu_nav_rec`).

Because XSONAR ASCII navigation files record time using only the Julian day (`day`), `hour`, `min`, and `sec` without a calendar year column, the survey year **must** be supplied on the command line via `-year <YYYY>`.

---

## Usage

```bash
xsonar2Nav [-v] -year <YYYY> [-skip <N>] -comp <out_navfile> <xsonar_navfile(s)>
```

### Common Workflow Examples

**1. Convert an XSONAR ASCII navigation file from a 1997 sidescan survey into `.nav` format:**

```bash
xsonar2Nav -year 1997 -comp line01.nav xsonar_line01.txt
```

**2. Batch-convert multiple XSONAR navigation files into a single composite `.nav` file:**

```bash
xsonar2Nav -year 1998 -comp survey_all.nav raw_xsonar/*.nav_asc
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-year <YYYY>` | **Required.** Four-digit survey calendar year (e.g., `1997`). If omitted (`year == -1`), `xsonar2Nav` aborts with `"gotta spec. year!"`. | `-1` (Required) |
| `-comp <filename>` | **Required.** Output binary `.nav` filename (`tidename`). | None |
| `<xsonar_navfile(s)>` | **Required.** One or more ASCII XSONAR navigation files (up to 300 files). | None |
| `-skip <N>` | Parsed on the command line (`skip`), legacy option from `toNav`. | `1` |
| `-new` | Parsed on the command line (`new_flag++`), unused. | Disabled |
| `-v` | Increment verbose flag (`verbose_flag++`). | Disabled |

---

## Input & Output Formats

### Input XSONAR ASCII Format
Each line in the input file contains 8 whitespace-delimited fields parsed via `fscanf(file, "%hd%hd%hd%hd%d%lf%d%lf", ...)`:

```text
day  hour  min  sec  latdeg  latmin  londeg  lonmin
```
* `day`: UTC Julian day of year (`1..366`).
* `hour`, `min`, `sec`: UTC time of day.
* `latdeg`, `latmin`: Northern Hemisphere latitude degrees and decimal minutes:
  $$\text{lat} = \text{latdeg} + \frac{\text{latmin}}{60.0}$$
* `londeg`, `lonmin`: Signed Western Hemisphere longitude degrees (negative in North America, e.g., `-70`) and positive decimal minutes:
  $$\text{lon} = \text{londeg} - \frac{\text{lonmin}}{60.0}$$

> [!NOTE]
> **Longitude Sign Convention:**
> Because `tide_rec.lon` is computed as `(double)londeg - lonmin / 60.0`, `londeg` is expected to be **negative** (Western Hemisphere, e.g. `-70 30.0` $\rightarrow -70.5^\circ$) while `latdeg` is **positive** (Northern Hemisphere, e.g. `42 15.0` $\rightarrow +42.25^\circ$).

### Output Binary `.nav` (`jcu_nav_rec`)
For every 8-field record read, `xsonar2Nav` writes a 48-byte `jcu_nav_rec`:
* `lat`, `lon`: Decimal degrees.
* `time`: UTC epoch seconds since Jan 1, 1970, computed via `stdtime_from_jul_day(year, day, hour, min, sec)`.
* `centisecs`, `azi`, `velocity`, `flag[0..3]`: `0`.
