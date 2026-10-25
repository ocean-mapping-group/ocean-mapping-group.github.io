---
layout: default
title: USGS_30sec_to_JHC
parent: Grid Tools
tool_name: USGS_30sec_to_JHC
source_path: code/grid/USGS_30sec_to_JHC.c
category: gridding
input_formats: ["USGS 30-arc-second 16-bit DEM", "NASA SRTM 1-arc-second (.hgt) 16-bit DEM"]
output_formats: [".r4 (JHC 32-bit float grid)", ".llz (ASCII lat lon depth)"]
related_tools: ["SatAlt_to_JHC", "gtopo2ascii", "readUSGS_DEM", "project"]
---

# USGS_30sec_to_JHC

## Overview

`USGS_30sec_to_JHC` converts big-endian 16-bit signed integer digital elevation models—either **USGS 30-arc-second CONUS grids (`-usgs_30sec`)** or **1-arc-second SRTM `.hgt` tiles (`-srtm_1sec`, $3601 \times 3601$)**—simultaneously into an OMG unprojected geographic `.r4` floating-point grid (`<outprefix>.r4`) and a 3-column ASCII point file (`<outprefix>.llz`).

---

## Syntax & CLI Options

```bash
USGS_30sec_to_JHC [OPTIONS] (-usgs_30sec | -srtm_1sec) <USGS_or_SRTM_file> <JHC_out_prefix>
```

| Option | Description | Default |
|---|---|---|
| `<USGS_or_SRTM_file>` | **Required.** Input 16-bit big-endian binary DEM or SRTM `.hgt` tile. | None |
| `<JHC_out_prefix>` | **Required.** Output filename prefix; produces `<prefix>.r4` and `<prefix>.llz`. | None |
| `-usgs_30sec` | Configure for 30-arc-second USGS grid (`dx = 7200`, `dy = 3120`, `24°N–50°N`, `126°W–66°W`, `step = 30/3600°`, `invalid = -9999`). | None (must specify `-usgs_30sec` or `-srtm_1sec`) |
| `-srtm_1sec` | Configure for $1^\circ \times 1^\circ$ 1-arc-second SRTM `.hgt` tile (`dx = 3601`, `dy = 3601`, `step = 1/3600°`, `invalid = 0`). Requires `-minlat <blat>` and `-minlon <tlon>` to set the SW tile corner! | None |
| `-minlat <deg>` | Southern latitude bound (`blat`). For `-srtm_1sec`, `tlat` is automatically set to `blat + 1.0`. | `24.0` (in `-usgs_30sec`) |
| `-minlon <deg>` | Western longitude bound (`tlon`). For `-srtm_1sec`, `blon` is automatically set to `tlon + 1.0`. | `-126.0` (in `-usgs_30sec`) |
| `-maxlat <deg>` | Northern latitude bound (`tlat`). | `50.0` (or `blat + 1.0`) |
| `-maxlon <deg>` | Eastern longitude bound (`blon`). | `-66.0` (or `tlon + 1.0`) |
| `-dx <cols>` / `-dy <rows>` | Override grid dimensions (note: overridden by `-usgs_30sec` or `-srtm_1sec` preset block). | `7200 x 3120` or `3601 x 3601` |
| `-xstep <deg>` / `-ystep <deg>` | Override angular cell size. | `30/3600` or `1/3600` |
| `-merid <deg>` | Central meridian parameter. | `0.0` |
| `-low <val>` / `-high <val>` | Parsed on CLI. | `0.0` |

---

## How It Works

1. **Preset Initialization:**
   - If `-usgs_30sec` is selected, sets `dx = 7200`, `dy = 3120`, bounds `24°N–50°N` and `126°W–66°W`, `secstep = 30`, and `invalid = -9999`.
   - If `-srtm_1sec` is selected, sets `dx = 3601`, `dy = 3601`, `tlat = blat + 1.0`, `blon = tlon + 1.0`, `secstep = 1`, and `invalid = 0`.
2. **Header Creation:** Writes an `OMG1` `JHC_header` to `<JHC_out_prefix>.r4` with `projection = 3` (Geographic lat/lon), `ellipsoid = 1` (WGS84), and `data_type = 3` (float).
3. **Byte-Swapping & Dual Output:**
   - Reads each scanline of `dx` 16-bit shorts, byte-swaps each value via `swap_short`, converts to `float`, and writes the row to `<JHC_out_prefix>.r4` via `jswapfloat_fwrite`.
   - Simultaneously writes `lat lon depth` to `<JHC_out_prefix>.llz` for every valid cell (`depth != invalid`).

---

## Examples

**1. Convert a 1-arc-second SRTM tile (`N45W067.hgt`) to `.r4` and `.llz`:**
```bash
USGS_30sec_to_JHC -srtm_1sec -minlat 45.0 -minlon -67.0 N45W067.hgt N45W067
# Produces N45W067.r4 (geographic projection=3) and N45W067.llz
```

**2. Reproject the resulting geographic `.r4` grid onto a UTM mapsheet:**
```bash
project -in N45W067.r4 -Area fundy_utm.blank -out N45W067_utm.r4
```

---

## Workflow Context

- **Downstream:** Use [`project`](project.md) to reproject the geographic `.r4` grid (`projection = 3`) onto a Mercator or UTM mapsheet, or grid the `.llz` points directly with [`weigh_grid`](weigh_grid.md).
