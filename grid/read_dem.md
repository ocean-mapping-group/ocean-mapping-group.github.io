---
layout: default
title: read_dem
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: read_dem
source_path: code/grid/read_dem.c
category: gridding
input_formats:
- USGS ASCII DEM (7.5-minute / 1-degree)
- USGS SDTS ISO-8211 (.tar)
output_formats:
- 16-bit Binary Band-Sequential Array (.bsq)
- ASCII Header Report
related_tools:
- readUSGS_DEM
- USGS_30sec_to_JHC
- r4to16bit
---

# read_dem

## Overview

`read_dem` converts a US Geological Survey (USGS) Digital Elevation Model (DEM)—stored either in classic ASCII Type A/B/C record format or as an uncompressed Spatial Data Transfer Standard (SDTS / ISO-8211) `.tar` archive—into a 16-bit signed integer binary band-sequential raster (`<outbsq>`) and a human-readable metadata report (`[outhdr]`).

---

## Syntax & CLI Options

```
read_dem <indem> <outbsq> [outhdr] [nodataval]
```

| Argument | Description |
|----------|-------------|
| `<indem>` | Input USGS ASCII DEM file or uncompressed SDTS `.tar` archive. |
| `<outbsq>` | Output 16-bit binary band-sequential raster file (`nrows * ncols * 2` bytes). |
| `[outhdr]` | Optional output text file for the formatted DEM header report (defaults to `stdout`). |
| `[nodataval]` | Optional integer value assigned to nodata cells outside the quadrangle polygon (default: `-32767`). |

---

## How It Works

1. **Auto-Detection (ASCII DEM vs. SDTS `.tar`)**:
   - Checks whether `<indem>` is a POSIX tar archive containing ISO-8211 `.DDF` modules (`CATD.DDF`, `IREF.DDF`, `XREF.DDF`, `SPDM.DDF`, `LDEF.DDF`, `RSDF.DDF`, `DDSH.DDF`, `CELL.DDF`) or a fixed/variable-record ASCII DEM.
2. **Profile & Cell Assembly**:
   - For ASCII DEMs, reads the Type A header, determines the bounding northing/easting limits across the 4 quadrangle corners, allocates a rectangular `nrows x ncols` 16-bit grid initialized to `nodataval`, and populates each south-to-north Type B elevation profile into the north-up raster.
   - For SDTS `.tar` archives, extracts the binary cell module (`CELL.DDF`) and maps void/fill values (`-32766`, `-32767`, `32767`) to `nodataval`.
3. **Output**:
   - Writes the binary 16-bit array to `<outbsq>` and prints the full quadrangle metadata summary (origin, corner coordinates, projection/UTM zone, units, min/max elevation, and RMSE statistics) to `[outhdr]` or `stdout`.

---

## Examples

### Convert an SDTS `.tar` DEM archive to a 16-bit binary raster and header file

```bash
read_dem 1601234.dem.sdts.tar quad.bsq quad.hdr -9999
```

---

## Workflow Context

- **Sibling Tool**: [`readUSGS_DEM`](readUSGS_DEM.html) (extends `read_dem` to also dump positive elevations as `pos1 pos2 -z` into `thedata`).
- **Related Tools**: [`USGS_30sec_to_JHC`](USGS_30sec_to_JHC.html).
