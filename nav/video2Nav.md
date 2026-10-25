---
layout: default
title: video2Nav
parent: Navigation Processing (nav)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 34
tool_name: video2Nav
source_path: code/nav/video2Nav.c
category: Navigation & Georeferencing
input_formats:
- USGS VISOE ASCII camera drift navigation
output_formats:
- .nav (<comp><drift_id>)
related_tools:
- xsonar2Nav
- sar2Nav
- appendNav
- iNav2SHP
---

# video2Nav

## Description
`video2Nav` (authored by John Hughes Clarke, March 1997) converts USGS **VISOE** (Video and Still Camera Observation Equipment, Page Valentine format) ASCII seabed camera drift navigation files into separate binary OMG navigation files (`.nav`, `jcu_nav_rec`)—one output file per camera drift station.

Because VISOE drift files group multiple camera drift tracks into a single ASCII file separated by `END <drift_id>` markers and contain only `(lon, lat)` coordinates without timestamps, `video2Nav` automatically splits each drift into its own output file named `<comp><drift_id>`, stores the numeric drift ID in `tide_rec.azi`, and assigns synthetic timestamps incrementing by `10` seconds per fix (`0, 10, 20, ...`).

---

## Usage

```bash
video2Nav [-v] [-new] [-skip <N>] -comp <out_prefix> <visoe_drift_file(s)>
```

### Common Workflow Examples

**1. Split a VISOE ASCII camera drift log into individual binary `.nav` files:**

```bash
video2Nav -comp drifts/station_ stellwagen_visoe.txt
# If stellwagen_visoe.txt contains drifts 101, 102, 103, produces:
# drifts/station_101, drifts/station_102, drifts/station_103
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-comp <prefix>` | **Required.** Output filename prefix (`tidename`). Each drift's identifier string (`string2`) is appended directly to `<prefix>` via `mem_strappend(tidename, string2)`. | None |
| `<visoe_drift_file(s)>` | **Required.** One or more ASCII VISOE drift navigation files (up to 300 files). | None |
| `-v` | Increment verbose flag (`verbose_flag++`). | Disabled |
| `-new` | Parsed on the command line (`new_flag++`), unused. | Disabled |
| `-skip <N>` | Parsed on the command line (`skip`), unused. | `1` |

---

## Input & Output Formats

### Input VISOE ASCII Drift Format
The input file begins with the first drift's identifier token (`string2`), followed by pairs of whitespace-delimited tokens (`string1 string2`):
* **Coordinate Pair:** `<longitude> <latitude>` in decimal degrees (note that longitude comes first, followed by latitude).
* **Segment Delimiter:** `END <next_drift_id>` closes the current output `.nav` file, resets the synthetic timestamp counter (`timeindrift = 0`) and record counter (`tide_rec_no = 0`), parses `driftno` as a `float` from `<next_drift_id>`, and opens a new output file `<comp><next_drift_id>`.

Example input structure:

```text
01
-70.25120 42.15430
-70.25135 42.15442
-70.25150 42.15455
END 02
-70.26010 42.16005
-70.26025 42.16020
```

### Output Binary `.nav` (`jcu_nav_rec`)
For each coordinate pair in a drift:
* `lat`: Parsed from `string2` (decimal degrees).
* `lon`: Parsed from `string1` (decimal degrees).
* `azi`: `driftno` (numeric drift ID parsed after `END`, or `0.0` for the initial drift before the first `END`).
* `time`: `timeindrift` (starts at `0` for each drift and increments by `+10` seconds per fix).
* `centisecs`, `velocity`, `depth`, `flag[0..3]`: `0`.
