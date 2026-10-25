---
layout: default
title: SWtoJHC
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: SWtoJHC
source_path: code/grid/SWtoJHC.c
category: gridding
input_formats:
- Smith & Weissel (.sw)
- ESRI Binary Float (.flt + .hdr)
- Raw 32-bit float binary
- ncdump ASCII text
output_formats:
- .r4 (JHC 32-bit float grid)
- ASCII XYZ / LatLonZ (with -netCDF)
related_tools:
- ASCIItoJHC
- r4toESRI
- r4to8bit
- edhead
---

# SWtoJHC

## Overview

`SWtoJHC` imports external floating-point raster grids into the OMG `JHC_header` 32-bit float (`.r4`) format. Originally written to transpose and convert Smith & Weissel (`SW_header`) binary grids, it also supports importing **ESRI binary float grids (`.flt` + `.hdr`)** via `-esri_flt`, **headerless raw 32-bit float arrays** via `-rawfloat -rawxdim <nx>`, and **`ncdump` ASCII text dumps of netCDF grids** via `-netCDF`.

---

## Syntax & CLI Options

```bash
SWtoJHC [OPTIONS] <SW_or_input_file> <JHC_output_file>
```

| Option | Description | Default |
|---|---|---|
| `<SW_or_input_file>` | **Required.** Input filename (or file prefix without `.flt`/`.hdr` when `-esri_flt` is set). | None |
| `<JHC_output_file>` | **Required.** Output OMG `.r4` grid filename (or ASCII XYZ/LLZ file when `-netCDF` is set). | None |
| `-esri_flt` | Read an ESRI binary float grid pair (`<prefix>.flt` and `<prefix>.hdr`), setting unprojected geographic coordinates (`projection = 3`, `ellipsoid = 1`) and mapping `NODATA_value` to `0.0`. | Disabled |
| `-rawfloat` | Read a headerless raw 32-bit floating-point binary file. Requires `-rawxdim <nx>`. | Disabled |
| `-rawxdim <nx>` | Number of columns (`dx`) for `-rawfloat`; `dy` is computed automatically from file size (`filesize / (dx * 4)`). | `0` |
| `-strange` | Read `dx` and `dy` as 32-bit integers at byte offset `1460` and copy the float array directly. | Disabled |
| `-netCDF` | Parse an ASCII `ncdump` file (searching for `x = `, `y = `, and `z =` blocks) and write 3-column ASCII (`X Y Z` or `lat lon Z`) to `<JHC_output_file>`. | Disabled |
| `-want_lalo` | Used with `-netCDF`: output `Y X Z` (`lat lon Z`) instead of `X Y Z`. | Disabled (`X Y Z`) |
| `-nudge_zero` | Used with `-netCDF`: replace valid `0.0` elevations with `0.00000000002` so they are not treated as nodata (`0.0`) by OMG tools. | Disabled |
| `-flip` | Flip vertical row orientation when transposing a Smith & Weissel array. | Disabled |
| `-pixel <size>` | Override `xstep` and `ystep` in the output `JHC_header`. | From input header |
| `-tlon <lon>` | Override `xmin` (western/left longitude or X coordinate) in `JHC_header`. | From input header |
| `-blon <lon>` | Override `xmax` (eastern/right longitude or X coordinate) in `JHC_header`. | From input header |
| `-blat <lat>` | Override `ymin` (southern/bottom latitude or Y coordinate) in `JHC_header`. | From input header |
| `-tlat <lat>` | Override `ymax` (northern/top latitude or Y coordinate) in `JHC_header`. | From input header |
| `-low <val>` / `-high <val>` | Parsed on command line (reserved for depth clipping). | `0.0` |

---

## How It Works

1. **Header & Metadata Ingestion:**
   - **Standard SW mode:** Reads `SW_header` (`dx`, `dy`, `xinc`, `yinc`, `xmin`, `xmax`, `ymin`, `ymax`).
   - **ESRI Float mode (`-esri_flt`):** Opens `<prefix>.hdr` and parses `ncols`, `nrows`, `xllcorner`, `yllcorner`, `cellsize` (or `xdim`/`ydim`), and `NODATA_value`. Computes `blon = tlon + pixel * dx` and `tlat = blat + pixel * dy`, and sets `JHChead.projection = 3` (Geographic) and `JHChead.ellipsoid = 1` (WGS84).
   - **Raw Float mode (`-rawfloat`):** Uses `-rawxdim` for `dx` and computes `dy` from the byte length of the file.
   - **netCDF `ncdump` mode (`-netCDF`):** Scans the ASCII `ncdump` text for dimension declarations `x = <dx>` and `y = <dy>`, reads coordinate vectors `x = ...` and `y = ...`, and streams non-missing (`!= '_'`) `z =` values to an ASCII XYZ/LLZ file.
2. **Array Conversion & Nodata Mapping:**
   - Allocates memory for the float grid (reading row-by-row if total size exceeds $2^{31}$ bytes).
   - In `-esri_flt` mode, replaces valid `0.0` values with `0.0000001` and maps `nodata` pixels to `0.0` (OMG's background/empty pixel value).
   - Writes the 1024-byte `OMG1` `JHC_header` (`data_type = 3`) followed by big-endian IEEE 754 floats via `jswapfloat_fwrite`.

---

## Examples

**1. Import an ESRI binary float grid (`bathy.flt` and `bathy.hdr`) into OMG `.r4` format:**

```bash
SWtoJHC -esri_flt bathy bathy.r4
```

**2. Import a headerless 4096-column raw float grid with known bounds:**

```bash
SWtoJHC -rawfloat -rawxdim 4096 -pixel 10.0 -tlon -67.0 -blon -66.0 -blat 44.0 -tlat 45.0 raw_dem.bin dem.r4
```

**3. Extract `lat lon z` points from an `ncdump` text file of a GMT/GEBCO netCDF grid:**

```bash
ncdump gebco_sub.nc > gebco_sub.cdl
SWtoJHC -netCDF -want_lalo -nudge_zero gebco_sub.cdl gebco_sub.llz
```

---

## Workflow Context

- **Counterpart:** [`r4toESRI`](r4toESRI.html) exports OMG `.r4` grids to ESRI `.flt`/`.hdr` or `.bil` format.
- **Downstream:** [`edhead`](edhead.html), [`r4to8bit`](r4to8bit.html), [`addSUN`](addSUN.html), [`project`](project.html).
