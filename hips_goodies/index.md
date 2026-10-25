---
layout: default
title: CARIS HIPS Integration Utilities (hips_goodies)
parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 15
has_children: true
source_path: code/hips_goodies/
category: Caris HIPS Conversion Utilities
related_tools:
- heli2caris
- mvp2hips
- read_kmall
- mergeAtt
---

# HIPS Goodies (`hips_goodies/`)

## Overview

The `hips_goodies/` (`code/hips_goodies/`) directory contains standalone command-line utilities originally written by Jason Bartlett (Canadian Hydrographic Service, Burlington) in March 2005 for converting auxiliary field survey logs—specifically helicopter shoreline GPS tracks and Moving Vessel Profiler (MVP) sound velocity profiles—into formats directly ingestible by **CARIS HIPS and SIPS** and the OMG processing pipeline.

During joint CHS/UNB hydrographic and Arctic coastal mapping surveys, shoreline verification is frequently conducted using helicopter-mounted GPS receivers (logging NovAtel OEM4, PRTKA, or NMEA `$GPGGA` strings), while underway sound speed profiling is performed with Brooke Ocean Technology / AML Moving Vessel Profilers (`.001c` calculated profile files). The tools in `hips_goodies/` bridge these raw field acquisition logs into CARIS NTX/FOF batch command scripts and CARIS `.svp` Version 2 sound velocity files.

---

## Tools in `hips_goodies/`

| Tool / Source File | Primary Role | Input Formats | Output Formats |
| :--- | :--- | :--- | :--- |
| **[`heli2caris`](heli2caris.html)** (`heli2caris.c` / `helo2caris.cpp`) | Interactive converter that parses raw helicopter GPS logs (OEM4, PRTKA, or NMEA GGA) and writes CARIS FOF/NTX shoreline feature batch scripts with feature codes (`clsl`, `cllwrlltsm`, `cllw`, or custom). | Raw ASCII GPS logs (`.gps`, `.txt`, `.log`) | CARIS batch command / feature input file |
| **[`mvp2hips`](mvp2hips.html)** (`mvp2hips.c`) | Converts Moving Vessel Profiler (`xxxc` calculated ASCII files, e.g., `jul08.001c`) into CARIS HIPS `SVP_VERSION_2` `.svp` sound velocity profile files. | Calculated MVP ASCII file (`.001c`, `.svp`) | CARIS HIPS `.svp` (`SVP_VERISON_2`) |

---

## Architectural Fit in the OMG & CHS Workflow

1. **Shoreline & Coastline Digitization (`heli2caris` / `helo2caris.cpp`)**:
   - Helicopter shoreline surveys log continuous GPS positions along the high-water line, low-water line, or intertidal rock ledges.
   - `heli2caris` (ANSI C CLI argument version) and `helo2caris.cpp` (legacy C++ `fstream` interactive prompt version) convert those trajectories into `/ge=lat,lon` coordinate streams wrapped in CARIS `opvfof` / `lico` header and `opvfon` / `oppmcr` trailer commands.
2. **Underway Sound Velocity Profile Conversion (`mvp2hips`)**:
   - Parses `CALC`, `DATE`, and `TIME` headers plus NMEA GGA position footers (`$GPGGA`) from Brooke Ocean MVP `xxxc` files and formats depth/sound-speed pairs (`depth[i]`, `speed[i]`) under a `Section YYYY-DDD HH:MM:00 DD:MM:SS DD:MM:SS` header for HIPS ray-tracing.
3. **Build Configuration**:
   - Built via `code/hips_goodies/makefile` (authored by J. Beaudoin, March 2008), which compiles all `.c` targets (`heli2caris`, `mvp2hips`) and links them against `liblocal.a` and `libsimrad.a` into `$LOCALBIN`.

---

## Quick-Start Examples

```bash
# Convert a helicopter GPS shoreline log (OEM4, PRTKA, or NMEA GGA) into a CARIS FOF batch script:
heli2caris raw_heli_gga.txt shoreline_fof.cmd

# Convert a Brooke Ocean Moving Vessel Profiler (.001c) cast into a CARIS HIPS v2 .svp file:
mvp2hips jul08.001c jul08_hips.svp
```
