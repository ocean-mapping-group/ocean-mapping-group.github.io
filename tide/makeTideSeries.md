---
layout: default
title: makeTideSeries
parent: Tidal Reduction & Constituents (tide)
grand_parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
tool_name: makeTideSeries
source_path: code/tide/makeTideSeries.c
category: tide
input_formats:
- CLI parameters (location and time range)
output_formats:
- .nav / .bin (binary jcu_nav_rec time series template)
related_tools:
- mergeTide
- binTide
- diffTide
---

# makeTideSeries

## Overview

`makeTideSeries` generates a synthetic OMG binary `jcu_nav_rec` file at a fixed geographic coordinate (`-lalo <lat> <lon>`) over a specified UTC start/end time range (`-start` to `-end`) at a uniform time step (`-timestep_min`).

It is designed to create a regular fixed-station time series template that can then be populated by a tidal prediction engine (such as `tidecor` or WebTide) and subsequently merged into survey lines with [`mergeTide`](mergeTide.html).

---

## Syntax & CLI Options

```bash
makeTideSeries -lalo <lat> <lon> -start <yr> <jday> <hr> <min> -end <yr> <jday> <hr> <min> [-timestep_min <min>] -out <tide.bin>
```

| Option | Description | Default |
|---|---|---|
| `-lalo <lat> <lon>` | Fixed station decimal latitude and longitude (`N` positive, `E` positive). | `45.0 -65.0` |
| `-start <yr> <jday> <hr> <min>` | **Required.** Start UTC timestamp: 4-digit year, Julian day (`1..366`), hour (`0..23`), and minute (`0..59`). | None |
| `-end <yr> <jday> <hr> <min>` | **Required.** End UTC timestamp: 4-digit year, Julian day (`1..366`), hour (`0..23`), and minute (`0..59`). | None |
| `-timestep_min <minutes>` | Time interval in minutes between consecutive output records. | `5.0` |
| `-out <filename>` | **Required.** Output binary `jcu_nav_rec` filename. | None |
| `-v` | Enable verbose flag. | Disabled |

---

## How It Works

1. Converts `-start` and `-end` `(year, jday, hour, min, 0)` into 1970 UTC epoch seconds (`starttime` and `endtime`) using `stdtime_from_jul_day`.
2. Sets `tide_rec.lat = lat` and `tide_rec.lon = lon`.
3. Loops from `the_time = starttime` while `the_time < endtime`, incrementing by `timestep_min * 60.0` seconds on each step, and writes binary `jcu_nav_rec` records via `nav_write`.

---

## Examples

**Create a 5-minute station template in the Bay of Fundy for Julian Day 180:**

```bash
makeTideSeries \
    -lalo 45.15 -66.05 \
    -start 2007 180 00 00 \
    -end 2007 181 00 00 \
    -timestep_min 5 \
    -out fundy_station_template.bin
```

---

## Workflow Context

- **Downstream:** Used as input to tidal constituent predictors (`tidecor`) to evaluate predicted tides at a fixed virtual gauge, followed by [`mergeTide`](mergeTide.html).
