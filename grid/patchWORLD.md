---
layout: default
title: patchWORLD
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: patchWORLD
source_path: code/grid/patchWORLD.c
category: gridding
input_formats:
- '.r4 (global/regional source grid: ETOPO5, Smith & Sandwell, EGM96, EGM08, CGG2010, GPSH, WOA01)'
- .r4 (target mapsheet via -into)
- .nav (target binary navigation via -tonav)
output_formats:
- .r4 (modified in-place with interpolated values)
- .nav (modified in-place with interpolated value in azi)
related_tools:
- make_blank
- project
- addDTM
- mergeTide
- diffTide
---

# patchWORLD

## Overview

`patchWORLD` bilinearly interpolates a global or regional reference grid (`-source <grid.r4>`)—such as **ETOPO5 (`-etopo`)**, **Smith & Sandwell predicted bathymetry (`-predict`)**, **EGM96 (`-egm96`)**, **EGM08 (`-egm08`)**, **CGG2010 (`-cgg2010`)**, **Canadian GPS-H (`-gpsh`)**, **World Ocean Atlas 2001 (`-woa01`)**, or a **custom geographic grid (`-custom`)**—into one of three targets:
1. Every pixel of an existing OMG `.r4` mapsheet (`-into <target.r4>`), regardless of the target mapsheet's projection,
2. The `azi` (tide/height) field of every record in an OMG binary `jcu_nav_rec` navigation file (`-tonav <navfile.bin>`), or
3. Interactive single-point coordinate queries on `stdin` (`-test`).

---

## Syntax & CLI Options

```bash
patchWORLD (-etopo | -predict | -egm96 | -egm08 | -cgg2010 | -gpsh | -woa01 | -custom) \
    [OPTIONS] -source <source.r4> (-into <target.r4> | -tonav <nav.bin> | -test)
```

### Source Model Selection (Required — choose one)

| Option | Source Grid Geometry | Resolution |
|---|---|---|
| `-etopo` | Global ETOPO5 (`0°..360°E`, `90°N..-90°S`) | $5'$ ($12\text{ pixels/deg}$) |
| `-predict` | Smith & Sandwell Spherical Mercator (`0°..360°E`, `72°S..72°N`, `10800 x 6336`) | $2'$ at Equator |
| `-egm96` | Global EGM96 Geoid (`0°..360°E`, `90°N..-90°S`) | $15'$ ($4\text{ pixels/deg}$) |
| `-egm08` | Global EGM2008 Geoid (`0°..360°E`, `90°N..-90°S`) | $1'$ ($60\text{ pixels/deg}$) |
| `-cgg2010` | Canadian Gravimetric Geoid CGG2010 (`170°W..10°W`, `90°N..10°N`) | $2'$ ($30\text{ pixels/deg}$) |
| `-gpsh` | Canadian NRCan GPS-H Geoid (`141°59'W..48°01'W`, `41°01'N..83°59'N`) | $2'$ ($120''$) |
| `-woa01` | World Ocean Atlas 2001 (`0.125°E..359.875°E`, `89.875°S..89.875°N`) | $0.25^\circ$ ($4\text{ pixels/deg}$) |
| `-custom` | Custom geographic 8-bit grid; prompts `stdin` for top-left `lat lon` and `dlatdeg dlondeg`. | User-prompted |

### Target & Interpolation Options

| Option | Description | Default |
|---|---|---|
| `-source <file.r4>` | **Required.** Path to the source `.r4` model grid file. | None |
| `-into <target.r4>` | Interpolate the source grid into every pixel of the existing `.r4` (or `.8bit` if `-custom`) target mapsheet in-place. | None |
| `-tonav <nav.bin>` | Interpolate the source grid at each `(lat, lon)` fix of the binary `jcu_nav_rec` file and store the result in `nav_rec.azi` in-place. | None |
| `-test` | Interactive test mode: prompt `stdin` for `lat lon` (enter `0 0` to exit) and print the interpolated pixel coordinates and value. | Disabled |
| `-latminshift <min>` | Shift lookup latitude by `<min>` arc-minutes (`lat += latminshift / 60.0`) before sampling the source grid. | `0.0` |
| `-lonminshift <min>` | Shift lookup longitude by `<min>` arc-minutes (`lon += lonminshift / 60.0`) before sampling the source grid. | `0.0` |
| `-switch_horizontal` | Invert horizontal sub-pixel bilinear interpolation weights (`across_weight`). | Disabled |
| `-switch_vertical` | Invert vertical sub-pixel bilinear interpolation weights (`down_weight`). | Disabled |
| `-v` / `-debug` | Print verbose sub-pixel bilinear interpolation weights and corner values. | Disabled |

---

## How It Works

1. **Coordinate Inverse Projection:**
   - In `-into <target.r4>` mode, iterates over every pixel `(j, i)` of `<target.r4>` and calls `inv_proj` using `into_head` to obtain geographic `(lat, lon)`.
   - In `-tonav <nav.bin>` mode, reads each `jcu_nav_rec` record's `(lat, lon)`.
2. **Source Pixel Mapping (`get_specific_loc`):**
   - Applies any `-latminshift` and `-lonminshift` offsets and converts `(lat, lon)` into continuous floating-point pixel coordinates `(xpixel, ypixel)` inside the selected global/regional source grid.
3. **Sub-Pixel Bilinear Interpolation (`get_Value_at_pixel`):**
   - Seeks to the $2 \times 2$ neighborhood (`tl`, `tr`, `bl`, `br`) surrounding `(xpixel, ypixel)` in `-source` and performs bilinear interpolation using the fractional pixel weights `across_weight` and `down_weight`.
   - Writes the interpolated float row back to `<target.r4>` (`jswapfloat_fwrite`) or into `nav_rec.azi` (`nav_write`).

---

## Examples

**1. Populate a blank UTM mapsheet with EGM2008 geoid undulation heights:**

```bash
make_blank -float -utm -merid -66.0 fundy_geoid -boundsof merged/*.merged
cp fundy_geoid.blank fundy_egm08.r4
patchWORLD -egm08 -source /data/geoid/EGM08_global.r4 -into fundy_egm08.r4
```

**2. Extract CGG2010 geoid heights along a binary vessel navigation track (to subtract geoid from ellipsoidal PPK heights with `diffTide`):**

```bash
cp ppk_ellipsoid.bin geoid_along_track.bin
patchWORLD -cgg2010 -source /data/geoid/CGG2010.r4 -tonav geoid_along_track.bin
diffTide -tide1 ppk_ellipsoid.bin -tide2 geoid_along_track.bin -out orthometric_tide.bin
```

**3. Interactively query Smith & Sandwell predicted bathymetry at specific coordinates:**

```bash
patchWORLD -predict -source /data/world/topo_8.2.r4 -test
```

---

## Workflow Context

- **Geoid & Vertical Datum Workflows:** `patchWORLD -tonav` + [`diffTide`](../tide/diffTide.html) + [`mergeTide`](../tide/mergeTide.html) allows converting ellipsoidal GNSS PPK trajectories (`GrafNav_2_OMG` / `posProc_2_OMG`) to orthometric (MSL/geoid) water levels along the vessel track.
- **Regional Bathymetry Compilation:** `patchWORLD -into` + [`addDTM`](addDTM.html) allows filling unmapped offshore background areas of a survey mapsheet with Smith & Sandwell (`-predict`) or ETOPO (`-etopo`) bathymetry.
