---
layout: default
title: combineMW
parent: HAWAII MR1 Towed Sidescan (mr1)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 1
tool_name: combineMW
source_path: mr1/combineMW.c
category: navigation_processing
input_formats:
- MOANA_WAVE_ASCII
output_formats:
- ASCII_XYZ
related_tools:
- mergeMWascii
- subsetAscii
- swapascii
---

# combineMW

## Overview

`combineMW` merges R/V *Moana Wave* fixed-width ASCII navigation records (48 bytes per record) and bathymetry records (33 bytes per record) by timestamp using binary search and linear interpolation, producing a combined 3-column ASCII `lat lon depth` file at the navigation sample interval (typically 1 minute).

## Usage

```
combineMW (-v) -nav navfile -dep bathyfile -out outfile
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-nav` | `<navfile>` | *required* | Input 48-byte fixed-width R/V *Moana Wave* ASCII navigation file (`year jday hh:mm:ss ... lat lon`). |
| `-dep` | `<bathyfile>` | *required* | Input 33-byte fixed-width R/V *Moana Wave* ASCII depth file (`year jday hh:mm:ss ... depth`). |
| `-out` | `<outfile>` | *required* | Output ASCII `lat lon depth` file. |
| `-v` | none | `0` | Enable verbose output (prints parsed timestamps, lat/lon, and depths). |

## How It Works

1. **Fixed-Width Record Parsing**: Reads each 48-byte record from `-nav` via `read_mw_nav()`, decoding `year`, `jday`, `hour`, `min`, `sec` into Unix epoch seconds (`stdtime_from_jul_day`) and extracting `lat` and `lon`.
2. **Binary Search & Linear Interpolation**: For each navigation timestamp `need_time`, performs a binary search on the 33-byte records of `-dep` (`get_mw_depth(need_time)`), reads the bracketing depth records (`prev_time`, `next_time`), linearly interpolates `depth`, and writes `lat lon (int)depth` to `-out`.

## Practical Examples

### Combine Moana Wave navigation and centerbeam depth logs

```bash
combineMW -v -nav mw9204.nav -dep mw9204.dep -out mw9204_track.xyz
```
