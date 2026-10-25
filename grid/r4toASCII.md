---
layout: default
title: r4toASCII
parent: Grid Tools
tool_name: r4toASCII
source_path: code/grid/r4toASCII.c
category: gridding
input_formats: [".r4 (JHC 32-bit float grid)", ".8bit (JHC 8-bit unsigned char grid)", ".lat / .lon (optional exact shoal position grids)"]
output_formats: ["ASCII (lat lon z, lon lat z, east north z, pixel x y z, ESRI grid, or GUI DMS)", "Binary 64-bit double triples (-ddd)"]
related_tools: ["ASCIItoJHC", "r4toESRI", "r4toGRASS", "findShoals", "surface"]
---

# r4toASCII

## Overview

`r4toASCII` exports an OMG `JHC_header` 32-bit floating-point (`.r4`) or 8-bit unsigned char (`.8bit`) grid into ASCII (or binary double `-ddd`) XYZ point listings. By default, it inverse-projects the center of every valid pixel `(x + 0.5, y + 0.5)` into geographic coordinates and outputs `lat lon positive_depth` (`%.10lf %.10lf %.3f`).

It also supports outputting `lon lat depth` (`-lola`), projected UTM `east north depth` (`-utm`), sub-pixel shoal coordinates from companion `.lat`/`.lon` grids (`-shoal_locations`), pixel coordinates for GMT `surface` (`-for_surface`), metric cross-section coordinates (`-for_profile`), distorted grid format (`-dg`), or 64-bit binary double triples (`-ddd`).

---

## Syntax & CLI Options

```bash
r4toASCII [OPTIONS] <infile.r4_or_8bit> <outfile.xyz>
```

### Coordinate System & Format Options

| Option | Output Columns & Format | Default |
|---|---|---|
| `<infile>` | **Required.** Input `JHC_header` `.r4` (`data_type == 3`) or `.8bit` (`data_type == 1`) grid file. | None |
| `<outfile>` | **Required.** Output ASCII (or `-ddd` binary) filename. | None |
| *(default)* | Geographic `lat lon (-val + zshift)` (`%.10lf %.10lf %.3f` for `.r4`, or `lat lon DN` for `.8bit`). Note: negates `.r4` values so negative OMG elevations become positive depths! | Default |
| `-lola` | Swap geographic column order to `lon lat (-val + zshift)` (`X Y Z`). | Disabled (`lat lon Z`) |
| `-utm` | Output projected UTM meters `east north (-val + zshift)` (`%.3f %.3f %.3f`). If the input grid is Mercator (`projection == 1` or `5`), requires `-merid <central_meridian>`. | Disabled |
| `-merid <deg>` | Central meridian (decimal degrees, e.g., `-66.0`) required when exporting a Mercator grid with `-utm`. | `-999.0` |
| `-shoal_locations` | Read companion `<infile>.lat` and `<infile>.lon` sub-pixel offset grids (created by `weigh_grid -retain_pos` or [`findShoals`](findShoals.md)) so exported coordinates reflect exact sounding locations (`ymin + lat_off`, `xmin + lon_off`) rather than pixel centers. | Disabled |
| `-for_surface` | Output unprojected pixel center coordinates `(x + 0.5) (dy - y - 0.5) (val + zshift)` for feeding into [`surface`](surface.md). | Disabled |
| `-for_profile` | Output scaled metric coordinates `(x + 0.5)*xstep -(y + 0.5)*ystep (val + zshift)`. | Disabled |
| `-linear` | Output pixel coordinates `(x + 0.5) (dy - y + 0.5) (val + zshift)` without map projection. | Disabled |
| `-woa` | Output World Ocean Atlas $0.25^\circ$ grid centers `(x*0.25 + 0.125) ((dy - y - 1)*0.25 - 89.875) (val + zshift)`. | Disabled |
| `-dg` | Output Distorted Grid format: writes `dx dy` on line 1, enables `-withzeros`, and outputs `(x+0.5)*xstep (dy-y-0.5)*ystep -val+zshift -val+zshift` (`0 0 0 0` for nodata). | Disabled |
| `-esri` | Write space-separated matrix rows of `-(val + zshift)` with `-99999.99` for `0.0` nodata (note: use [`r4toESRI`](r4toESRI.md) for complete ESRI `.asc`/`.bil` exports with headers). | Disabled |
| `-gui` | Output CARIS/CHS GUI format (`depth/ge=DD-MM-SS.SSSN,DD-MM-SS.SSSW`). | Disabled |
| `-ddd` | Write binary 64-bit IEEE `double[3]` triples (`lon, lat, val`, or `east, north, val` with `-utm`) instead of ASCII text. | Disabled |

### Value Filtering & Offset Options

| Option | Description | Default |
|---|---|---|
| `-withzeros` | Include nodata pixels (`0.0` in `.r4` or `255` in `.8bit`) in the output. By default, nodata pixels are skipped. | Disabled (skip nodata) |
| `-zshift <offset>` | Vertical offset added to every exported Z value (`-(val) + zshift` in geographic/UTM modes, or `val + zshift` in `-for_surface`/`-linear` modes). | `0.0` |
| `-low <val>` / `-high <val>` | Parsed on CLI. | `0.0` |
| `-v` / `-debug` | Print verbose header and coordinate conversion diagnostics. | Disabled |

---

## How It Works

1. Opens `<infile>`, reads `JHChead` (`dx`, `dy`, `xstep`, `ystep`, `projection`, `ellipsoid`, `data_type`), and if `-shoal_locations` is set, opens `<infile>.lat` and `<infile>.lon`.
2. Loops over every row `y = 0 .. dy - 1` and column `x = 0 .. dx - 1`:
   - Skips empty pixels (`*p == 0.0` for `.r4` or `*cp == 255` for `.8bit`) unless `-withzeros` (or `-dg`) is specified.
   - Computes `(lon, lat, east, north)` for pixel center `(x + 0.5, y + 0.5)` via `inv_proj()`, or adds sub-pixel offsets from `.lat`/`.lon` when `-shoal_locations` is active.
   - Formats and writes the requested coordinate triple to `<outfile>`.

---

## Examples

**1. Export valid soundings from a `.r4` grid to `lon lat depth` ASCII:**
```bash
r4toASCII -lola survey.r4 survey_lonlatz.xyz
```

**2. Export UTM `easting northing depth` triples:**
```bash
r4toASCII -utm survey_utm.r4 survey_enu.xyz
```

**3. Export exact shoal sounding coordinates (using `.lat` and `.lon` grids from `weigh_grid`):**
```bash
r4toASCII -shoal_locations -lola survey.r4 survey_shoals.xyz
```

---

## Workflow Context

- **Inverse Tool:** [`ASCIItoJHC`](ASCIItoJHC.md) and [`weigh_grid`](weigh_grid.md) (`-xyz`) convert ASCII XYZ files back into `.r4` grids.
- **GIS Export Alternatives:** Use [`r4toESRI`](r4toESRI.md) for ESRI `.asc`/`.bil`/`.flt` grids and [`r4toGRASS`](r4toGRASS.md) for GRASS GIS ASCII grids.
