---
layout: default
title: r4toESRI
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: r4toESRI
source_path: code/grid/r4toESRI.c
category: gridding
input_formats:
- JHC_header (.r4 / .8bit)
output_formats:
- ESRI Binary Grid (.flt + .hdr + _prj.adf)
- ESRI ASCII Grid (.asc)
related_tools:
- r4toASCII
- r4toGRASS
- r4to16bit
- tifftor4
---

# r4toESRI

## Overview

`r4toESRI` converts an OMG 32-bit floating-point (`.r4`) or 8-bit unsigned (`.8bit` / `.sun`) grid into an ESRI ArcInfo / ArcGIS raster format: either a binary floating-point grid pair (`<outname>.flt` + `<outname>.hdr`, with optional `<outname>_prj.adf` projection metadata) or a single ESRI ASCII grid (`<outname>.asc`).

---

## Syntax & CLI Options

```
r4toESRI [OPTIONS] -in <infile.r4_or_8bit> -out <outfile_prefix>
```

| Flag | Description |
|------|-------------|
| `-in <file>` | Input `.r4` or `.8bit` grid file. |
| `-out <prefix>` | Output filename prefix. Produces `<prefix>.flt` and `<prefix>.hdr` (or `<prefix>.asc` with `-ascii`). |
| `-no_data <val>` | Value written for nodata grid cells (default: `-99999.0` for float input, `255` for 8-bit input, or `1.0` with `-dB`). |
| `-float_no_data <val>` | Deprecated alias for `-no_data` on floating-point grids. |
| `-8bit_no_data <val>` | Deprecated alias for `-no_data` on 8-bit grids. |
| `-center` | Report the center of the lower-left pixel in `xllcorner` / `yllcorner` instead of nudging by `-0.5 * xstep` and `+0.5 * ystep` to the outer corner. |
| `-dB` | For 8-bit backscatter grids (`data_type == 1`): convert 8-bit digital numbers (`0..254`) to decibels via `dB = (DN - 255) / 2.0`. |
| `-real_8bit_range <min> <max>` | For 8-bit grids (`data_type == 1`): linearly rescale `0..254` to the real-valued interval `[min, max]`. |
| `-proj_long <lon>` | Reference longitude (`-180.0` default) used when calculating Mercator meter coordinates (`projection == 1`). |
| `-ascii` | Output a single ESRI ASCII Grid (`<prefix>.asc`) instead of a binary `.flt` + `.hdr` pair. |
| `-CHS` | Append Canadian Hydrographic Service header tags (`PIXELTYPE F` and `NBITS 32`) to `<prefix>.hdr`. |
| `-PRJ` | Write an ESRI `<prefix>_prj.adf` projection definition file for Mercator WGS84 mapsheets. |

---

## How It Works

1. **Header & Coordinate Conversion**:
   - Reads the 1024-byte `JHC_header` from `-in`.
   - Computes cell size and lower-left corner coordinates (`xllcorner`, `yllcorner`) based on `head.projection`:
     - **Geographic (`projection == 3`)**: Multiplies `xmin`, `ymin`, `xstep`, and `ystep` by `60.0` (if stored in degrees) and enforces square cell spacing (`xstep == ystep`).
     - **Mercator (`projection == 1`)**: Projects the lower-left corner (`xmin`, `ymin`) to Mercator meters relative to `-proj_long` (default `-180.0°`) and computes metric grid spacing at the reference latitude `zmin`.
     - **UTM (`projection == 2`)**: Uses `xmin * 1000.0`, `ymin * 1000.0`, and `xstep * 1000.0` in meters.
   - Unless `-center` is specified, shifts the origin by `-0.5 * xstep` in X and `+0.5 * ystep` in Y to match ESRI's lower-left pixel corner convention.
2. **Data Conversion & Export**:
   - **32-bit float (`data_type == 2`)**: Replaces OMG nodata cells (`10000.0` or `-99999.0`) with `no_data` (default `-99999.0`).
   - **8-bit unsigned (`data_type == 1`)**: Replaces `255` with `no_data`, or converts valid pixels (`0..254`) to decibels (`-dB`) or a custom floating-point range (`-real_8bit_range`).
   - In default binary mode, writes `<prefix>.hdr` with `BYTEORDER LSBFIRST` and streams IEEE little-endian 32-bit floats (`fwrite_LE_float`) to `<prefix>.flt`.
   - In `-ascii` mode, writes both the 6-line ESRI ASCII header and space-delimited grid rows directly to `<prefix>.asc`.

---

## Examples

### Export a bathymetric `.r4` grid to ESRI binary `.flt` + `.hdr`

```bash
r4toESRI -in harbor_bathy.r4 -out harbor_esri -CHS
```

### Convert an 8-bit backscatter mosaic to an ESRI ASCII grid in dB

```bash
r4toESRI -in mosaic.8bit -out mosaic_db -dB -ascii
```

---

## Workflow Context

- **Upstream**: [`weigh_grid`](weigh_grid.html), [`combine`](weigh_grid.html), [`mosaic`](../newmos/mos2.html), [`medfilt`](../image/index.html).
- **Related Export Tools**: [`r4toASCII`](r4toASCII.html), [`r4toGRASS`](r4toGRASS.html), [`r4to16bit`](r4to16bit.html).
