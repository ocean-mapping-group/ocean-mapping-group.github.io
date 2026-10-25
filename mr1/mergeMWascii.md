---
layout: default
title: mergeMWascii
parent: MR1 Tools
nav_order: 5
tool_name: mergeMWascii
source_path: mr1/mergeMWascii.c
category: navigation_processing
input_formats: [OMG_MR1_SS, MOANA_WAVE_ASCII]
output_formats: [OMG_MR1_SS]
related_tools: [combineMW, plotmr1, edbathy]
---

# mergeMWascii

## Overview

`mergeMWascii` merges R/V *Moana Wave* fixed-width ASCII navigation (`-nav`), speed/azimuth (`-spa`), and centerbeam depth (`-dep`) logs onto unpacked OMG HAWAII MR1 sidescan records (`OMG_MR1_ss_rec`, e.g., `.slr_ss`), applying an optional time lag (`-lag`) and computing towfish altitude from interpolated water depth minus towfish depth.

## Usage

```
mergeMWascii (-v) (-lag 120) -nav navfile -spa speedazifile -dep bathyfile \
             -in infile -out outfile
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-nav` | `<navfile>` | *required* | Input 48-byte fixed-width R/V *Moana Wave* ASCII navigation file. |
| `-spa` | `<speedazifile>` | *required* | Input 46-byte fixed-width R/V *Moana Wave* ASCII speed and gyro azimuth file. |
| `-dep` | `<bathyfile>` | *required* | Input 33-byte fixed-width R/V *Moana Wave* ASCII water depth file. |
| `-in` | `<infile>` | *required* | Input OMG MR1 sidescan file (`.slr_ss` or `.raw_ss`). |
| `-out` | `<outfile>` | *required* | Output merged OMG MR1 sidescan file (e.g., `.slr_mer`). |
| `-lag` | `<seconds>` | `0` | Time lag in seconds subtracted from the MR1 ping timestamp (`need_time = slr_rec.header.time - lag`) to account for towfish layback or clock offsets. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **Binary Search Lookup**: For each `OMG_MR1_ss_rec` in `-in`, computes `need_time = slr_rec.header.time - lag` and performs binary searches across the fixed-width ASCII files (`get_mw_nav`, `get_mw_spazi`, `get_mw_depth`).
2. **Linear Interpolation & Altitude Update**:
   - Linearly interpolates `lat` and `lon` between bracketing 48-byte nav records.
   - Reads the nearest ADCP/gyro heading from `-spa` and converts it to radians (`azi *= M_PI / 180.0`).
   - Linearly interpolates water `depth` between bracketing 33-byte depth records and sets `slr_rec.header.altitude = depth - slr_rec.header.fishdepth`.
3. **Output**: Writes the updated `OMG_MR1_ss_rec` to `-out`.

## Practical Examples

### Merge Moana Wave navigation, gyro, and depth onto MR1 slant-range sidescan

```bash
mergeMWascii -v -lag 120 -nav mw9204.nav -spa mw9204.spa -dep mw9204.dep \
             -in MR19208512.00.slr_ss -out MR19208512.00.slr_mer
```
