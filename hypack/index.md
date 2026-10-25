---
layout: default
title: HYPACK HSX / RAW Converters (hypack)
parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 14
has_children: true
source_path: code/hypack/
category: Raw Data Unraveling & Format Conversion
related_tools:
- dehypack
- hypack2omg
- mergeNav
- mergeAtt
- mergeTide
---

# Hypack Tools (`hypack/`)

## Overview

The `hypack/` (`code/hypack/`) directory contains command-line utilities for unpacking and converting **HYPACK / HYSWEEP** hydrographic survey files (specifically binary-wrapped raw files and ASCII `.HSX` HYSWEEP multibeam text files) into the **OMG-HDCS (Ocean Mapping Group - Hydrographic Data Conversion System)** suite of files (`.merged`, `.nav`, `.tide`, `.orientation`, `.heading`, and `.param`).

Authored primarily by Jonathan Beaudoin (`jonnyb`) with enhancements by John Hughes Clarke (February 2014 for Kongsberg Mesotech M3 and Reson SeaBat 7125/8101 testing), these tools allow multibeam surveys logged in HYPACK HYSWEEP to be processed through the standard OMG ray-tracing, swath-editing (`swathed`), bathymetric gridding (`weigh_grid`), and sidescan mosaicking (`mos2`) workflows.

---

## Tools in `hypack/`

| Tool | Source File | Primary Role | Input Formats | Output Formats |
| :--- | :--- | :--- | :--- | :--- |
| **[`dehypack`](dehypack.html)** | `code/hypack/dehypack.c` | Strips 4-byte little-endian record-length framing headers from HYPACK binary-wrapped sonar logs to recover the native underlying sonar byte stream. | HYPACK framed binary log | Native unframed sonar binary stream |
| **[`hypack2omg`](hypack2omg.html)** | `code/hypack/hypack2omg.c` | Unpacks ASCII HYSWEEP `.HSX` multibeam survey files (`POS`, `TID`, `HCP`, `GYR`, `RMB` records and header tables) into OMG-HDCS v2/v4 `.merged`, `.nav`, `.tide`, `.orientation`, `.heading`, and `.param` files. | `.hsx` (HYPACK HYSWEEP ASCII) | `.merged`, `.nav`, `.tide`, `.orientation`, `.heading`, `.param` |

---

## Key Header & Data Structures (`omg_hypack.h`)

Both tools link against `liblocal.a`, which provides the HYSWEEP parser declarations in `/home/iwc/local/include/omg_hypack.h`:

- **`Hypack_HSX_Header`**: Stores file-wide metadata parsed from the `.HSX` header block:
  - `TND` record: Survey date (`year`, `month`, `day`), time (`hour`, `minute`, `second`), and `basetime` (Unix epoch seconds at start of day).
  - `INF` record: `initial_tide_correction`, `initial_draft_correction`, `sound_velocity`.
  - `HSP` record: Depth/offset/angle gating limits, beam quality thresholds, `sonar_range`, `towfish_layback`, and `work_units`.
  - `DEV`, `DV2`, `OF2`, `SSI`, `MBI` records: Array of up to `HSX_MAX_NUM_DEVICES` (100) `Hypack_HSX_Device` structures containing sensor capability bitmasks and lever-arm/angular mounting offsets (`OMG_HDCS_motion_sensor offsets`).
  - `SVC` records: Array of up to `HSX_MAX_NUM_SVP_LAYERS` (1000) `Hypack_HSX_Sound_Velocity_Layer` entries.
- **`Hypack_HSX_Record`**: Holds the 3-character record identifier (`char id[4]`, e.g., `"POS"`, `"HCP"`, `"GYR"`, `"RMB"`) and a dynamically resized `OMG_Buffer buffer` containing the raw line.

---

## Typical HYPACK-to-OMG Processing Workflow

```bash
# 1. Unpack HYSWEEP .hsx file (with bathy, UTM zone 20N, and gyro device 1)
hypack2omg -v -do_bathy -zone 20 n -gyro 1 \
    -hsx raw/0001_line.HSX \
    -omg merged/0001_line

# 2. Interpolate navigation into the .merged ping headers
mergeNav -in merged/0001_line.merged -nav merged/0001_line.nav

# 3. Merge high-rate attitude (.orientation and .heading) and ray-trace
mergeAtt -in merged/0001_line.merged \
    -att merged/0001_line.orientation \
    -head merged/0001_line.heading \
    -param merged/0001_line.param
```
