---
layout: default
title: readUSGS_DEM
parent: Grid Tools
tool_name: readUSGS_DEM
source_path: code/grid/readUSGS_DEM.c
category: gridding
input_formats: ["USGS ASCII DEM (7.5-minute / 1-degree)", "USGS SDTS ISO-8211 (.tar)"]
output_formats: ["16-bit Binary Band-Sequential Array (.bsq)", "ASCII Header Report", "ASCII XYZ Soundings (thedata)"]
related_tools: ["read_dem", "USGS_30sec_to_JHC", "weigh_grid"]
---

# readUSGS_DEM

## Overview

`readUSGS_DEM` reads a US Geological Survey (USGS) Digital Elevation Model (DEM)—either in classic ASCII format (1024-byte fixed records or linefeed-delimited) or as an uncompressed Spatial Data Transfer Standard (SDTS / ISO-8211) `.tar` archive—and writes a 16-bit signed integer binary raster (`<outbsq>`), an optional formatted header summary (`[outhdr]`), and an OMG 3-column ASCII point file named `thedata` containing all positive land elevations converted to negative-down meters (`pos1 pos2 -elevation_m`) ready for gridding with `weigh_grid`.

---

## Syntax & CLI Options

```
readUSGS_DEM <indem> <outbsq> [outhdr] [nodataval]
```

| Argument | Description |
|----------|-------------|
| `<indem>` | Input USGS ASCII DEM file or uncompressed SDTS `.tar` archive. |
| `<outbsq>` | Output 16-bit binary band-sequential raster file. |
| `[outhdr]` | Optional output text file for the formatted Type A / Type C DEM metadata report (defaults to `stdout`). |
| `[nodataval]` | Optional integer value for nodata cells in `<outbsq>` (default: `-32767`). |

---

## How It Works

1. **Format Detection & Parsing**:
   - Inspects `<indem>` to determine whether it is an uncompressed SDTS `.tar` archive (containing `CATD.DDF`, `LDEF.DDF`, `RSDF.DDF`, `DDSH.DDF`, `CELL.DDF`, etc.) or a traditional USGS ASCII DEM (Type A header record, Type B elevation profiles, and optional Type C accuracy record).
   - Assembles the full 2D elevation array (`short *data`) oriented north-to-south, west-to-east, filling missing profile pads with `nodata` (default `-32767`).
2. **Binary & Header Output**:
   - Writes the 16-bit binary raster to `<outbsq>` and formats the quadrangle corners, UTM zone, ground planimetric/elevation units, and resolution into `[outhdr]`.
3. **OMG `thedata` Point Extraction**:
   - Opens `thedata` in the current working directory and iterates over every grid cell `(r, c)`.
   - Converts raw elevation values to meters (`* 0.3048` if `hdr.euni == 1` [feet]).
   - Converts coordinates (`pos1`, `pos2`) to kilometers (`* 0.001`) if `hdr.puni == 2` (meters in UTM) or decimal degrees (`/ 3600.0`) if `hdr.puni == 3` (arc-seconds in geographic).
   - Writes all non-zero, positive land elevations as `pos1 pos2 -elev_m` (following the OMG positive-down depth convention) to `thedata`.

---

## Examples

### Extract a 7.5-minute USGS DEM into a binary raster and `thedata` XYZ points
```bash
readUSGS_DEM portland_oe_e.dem portland.bsq portland.hdr
```

---

## Workflow Context

- **Sibling Tool**: [`read_dem`](read_dem.html) (identical converter without writing the `thedata` ASCII XYZ file).
- **Downstream**: [`weigh_grid`](weigh_grid.html) (grids the generated `thedata` point file onto an `.r4` mapsheet).
