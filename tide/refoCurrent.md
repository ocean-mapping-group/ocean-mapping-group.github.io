---
layout: default
title: refoCurrent
parent: Tidal Reduction & Constituents (tide)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
tool_name: refoCurrent
source_path: code/tide/refoCurrent.c
category: tide
input_formats:
- ASCII vessel/current log (short / medium / long)
output_formats:
- .nav (binary jcu_nav_rec)
- asciiplot format
related_tools:
- binTide
- mergeTide
- diffTide
---

# refoCurrent

## Overview

`refoCurrent` reformats ASCII shipboard current/navigation log files (containing date, time, latitude, longitude, vessel heading/speed, GPS course/speed, and current azimuth/speed) into either an `asciiplot`-compatible multi-channel plot file (default) or an OMG binary `jcu_nav_rec` navigation/current file (`-navfmt`).

---

## Syntax & CLI Options

```bash
refoCurrent [OPTIONS] <infilename> <outfilename>
```

| Option | Description | Default |
|---|---|---|
| `<infilename>` | **Required.** Input ASCII current/navigation log file. | None |
| `<outfilename>` | **Required.** Output `asciiplot` file (default) or binary `jcu_nav_rec` file (if `-navfmt` is set). | None |
| `-navfmt` | Output binary `jcu_nav_rec` records (`lat`, `lon`, `azi = cur_azi`, `velocity = cur_speed`, `depth = speed * 10`) instead of `asciiplot` text. | Disabled (`asciiplot` text) |
| `-bounds <start> <end>` | Record index range (`start < count < end`) to include when writing `asciiplot` output. | Uninitialized unless specified |
| `-long` | Expect 18-column input lines (including `gain`, `port`, `centre`, `stbd`). | Default (`F_LONG`) |
| `-medium` | Expect 15-column input lines (including `gain`). | Disabled |
| `-short` | Expect 14-column input lines (ending at `cur_azi cur_speed`). | Disabled |
| `-verbose` | Print parsed month and `hour min sec` / binary fix details. | Disabled |

---

## How It Works

1. **Line Parsing (`get_line`):**
   - Reads date (`str1 str2 day year`), time (`HH:MM:SS`), `type`, `lat`, `lon`, `azi`, `speed`, `gps_azi`, `gps_speed`, `cur_azi`, `cur_speed`, plus optional `gain` (`-medium`/`-long`) and `port centre stbd` (`-long`).
2. **Output Modes:**
   - **Plot Mode (default):** Writes an `asciiplot` header specifying 5 variables and axis bounds, followed by `(count - start) gps_speed cur_speed speed cur_azi azi` for records within `-bounds <start> <end>`.
   - **Binary Nav Mode (`-navfmt`):** Converts timestamp to 1970 epoch seconds (`stdtime_from_jul_day`) and writes `jcu_nav_rec` records where `azi` stores current direction (`cur_azi`), `velocity` stores current speed (`cur_speed`), and `depth` stores `speed * 10.0`.

---

## Examples

**1. Convert a 14-column current log into binary `jcu_nav_rec` format:**

```bash
refoCurrent -short -navfmt ship_current.log ship_current.nav
```

**2. Extract records 100 to 500 into an `asciiplot` file:**

```bash
refoCurrent -bounds 100 500 ship_current.log current_plot.asc
```

---

## Workflow Context

- Converts underway shipboard acoustic/GPS current logs into OMG binary `.nav` files or `asciiplot` time series.
