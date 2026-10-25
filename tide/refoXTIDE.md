---
layout: default
title: refoXTIDE
parent: Tide Tools
tool_name: refoXTIDE
source_path: code/tide/refoXTIDE.c
category: tide
input_formats: ["XTide UNIX epoch ASCII (-m r)", "XTide V2 ASCII"]
output_formats: ["JHC ASCII tide (jday hour min tide_m)"]
related_tools: ["medsTide", "wlvTide", "binTide", "mergeTide"]
---

# refoXTIDE

## Overview

`refoXTIDE` converts **XTide** output files into the 4-column JHC ASCII tide format (`jday hour min tide_m`). It supports both XTide raw epoch timestamp mode (`unix_epoch_sec tide_feet`, which it converts from feet to meters) and an alternate 7-token format (`-v2`, where tide values are already in meters).

---

## Syntax & CLI Options

```bash
refoXTIDE [OPTIONS] -in <xtidefilename> -out <asciijhctide>
```

| Option | Description | Default |
|---|---|---|
| `-in <filename>` | **Required.** Input XTide file. | None |
| `-out <filename>` | **Required.** Output 4-column JHC ASCII tide file (`jday hour min tide_m`). | None |
| `-v2` | Parse 7-token lines (`rtide hour min tz_str year month day`) where `rtide` is already in meters (no feet-to-meters scaling applied). | Disabled (default raw epoch + feet) |
| `-v` | Enable verbose output of parsed `tm_year`, `tm_mon`, `jday`, and `hour`. | Disabled |

---

## How It Works

1. **Default Mode (XTide raw `-m r` output in feet):**
   - Prints a warning: `BE WARNED---- this assumes the xtide z values are FEET!`.
   - Reads pairs of `thetime rtide` (`%lf %f`), where `thetime` is UNIX epoch seconds.
   - Calls `gmtime_r` to extract UTC day of year (`tm_yday + 1`), `tm_hour`, and `tm_min`.
   - Multiplies `rtide` by `0.307` (`rtide * 0.307`) and writes `jday hour min tide_m` to `-out`.
2. **`-v2` Mode:**
   - Reads lines formatted as `rtide hour min string year month day` (`%f %d %d %s %d %d %d`).
   - Computes `jday` via `stdtime_dmy_to_jul_day(day, month, year)` and writes `jday hour min rtide` without scaling.

---

## Examples

**1. Convert raw XTide epoch output (in feet) to JHC ASCII (in meters):**
```bash
refoXTIDE -in xtide_raw_feet.txt -out tide_meters.asc
binTide -year 1996 tide_meters.asc tide_meters.bin
```

**2. Convert pre-formatted V2 XTide output (already in meters):**
```bash
refoXTIDE -v2 -in xtide_v2.txt -out tide_v2.asc
```

---

## Workflow Context

- **See Also:** [`medsTide`](medsTide.md) (`-xtide` flag) and [`wlvTide`](wlvTide.md) (`-UTC` flag) for other XTide text output formats.
- **Downstream:** [`binTide`](binTide.md) $\rightarrow$ [`mergeTide`](mergeTide.md).
