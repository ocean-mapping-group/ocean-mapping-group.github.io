---
layout: default
title: make_bases
parent: Grid Tools
tool_name: make_bases
source_path: code/grid/make_bases.c
category: gridding
input_formats: [".r4 (optional reference DTM for depth-range filtering)"]
output_formats: ["Box.header<N> or Box.<lat>_<lon> or Box.<mpp>m_<N> (1024-byte JHC_header files)", "box.coords (ASCII bounding polygons in -gsi mode)"]
related_tools: ["make_blank", "weigh_grid", "project", "edhead"]
---

# make_bases

## Overview

`make_bases` generates a regular 2D matrix (`nocols x norows`) of `JHC_header` basemap header files (`Box.header0`, `Box.header1`, ... or `Box.<lat>_<lon>`) covering a survey region. When an existing regional bathymetric DTM is supplied via `-dtm <file.r4>`, `make_bases` automatically inspects the depth span inside each candidate tile and only outputs map sheets that contain valid bathymetry deeper than `50 m` and shallower than `-mdepth` (default `6000 m`).

It supports orthogonal and rotated Mercator, UTM (with automatic 6° UTM zone central meridian calculation), and New Brunswick Double Stereographic (`NBSDP`) projections.

---

## Syntax & CLI Options

```bash
make_bases [-v] [-gsi] [-binhead] [-latlon_name] [-dtm <file.r4>] [-mdepth <max_m>] [-pixel <mpp>]
```

| Option | Description | Default |
|---|---|---|
| `-dtm <file.r4>` | Reference `.r4` bathymetric DTM used to test whether each candidate tile contains valid depths between `50 m` and `<mdepth>`. | None (all tiles pass if omitted in standard mode; required in `-gsi` mode) |
| `-mdepth <meters>` | Maximum minimum-depth threshold: tiles whose shallowest depth is deeper than `<mdepth>` (or whose deepest depth is shallower than `50 m`) are skipped. | `6000.0` |
| `-pixel <mpp>` | Pixel resolution in meters per pixel (`the_mpp`) used when computing tile dimensions in `-gsi` mode. | `1.0` |
| `-gsi` | Enable GSI (Geological Survey of Ireland / regional charting) mode: prompts for bottom-left corner, minute shifts, and grid counts, writes tile bounding-box polygons to `box.coords`, and (if `-binhead` is set) writes `Box.<mpp>m_<sheetno>` headers. Requires `-dtm`. | Disabled |
| `-binhead` | Used with `-gsi`: write 1024-byte binary `JHC_header` files (`Box.<mpp>m_<sheetno>`) in addition to `box.coords`. | Disabled |
| `-latlon_name` | In standard interactive mode, name output header files by their center coordinates (`Box.<lat>_<lon>`) instead of sequential numbers (`Box.header<N>`). | Disabled (`Box.header<N>`) |
| `-v` | Enable verbose output of projected bounds and depth ranges. | Disabled |

---

## How It Works

1. **Interactive Grid Array Definition:**
   - Prompts `stdin` for:
     - Starting sheet number (unless `-latlon_name` or `-gsi` is set)
     - Latitude and longitude (`latdeg latmin londeg lonmin`) of the first (bottom-left) mapsheet
     - Latitude and longitude step (`dlatmin dlonmin`) in arc-minutes between adjacent mapsheets
     - Number of columns (`nocols`) across and rows (`norows`) up
   - In standard mode, also prompts for:
     - Box dimensions in meters (`0`) or arc-minutes (`1`)
     - Ellipsoid (`1=WGS84, 2=NAD27, 3=CLK66, 4=AGD85`)
     - Orthogonal (`1`: `1=Merc, 2=UTM, 6=NBSDP`) or Rotated (`0`: `5=rotMerc, 4=rotUTM, 8=rotNBStereo`) projection
     - Hemisphere (`0=North, 1=South`)
2. **Projection & Automatic UTM Zone Calculation:**
   - For UTM tiles (`Proj_Type == 2` or `4`), automatically computes the standard $6^\circ$ UTM zone central meridian from each tile's center longitude (`Auto_cen_merid`).
   - Projects all four corners of each tile to determine `xmin`, `xmax`, `ymin`, `ymax`, `dx`, and `dy`.
3. **DTM Depth Filtering (`get_depth_span`):**
   - If `-dtm` is supplied, inverse-projects the tile corners into the reference DTM's pixel space and scans the DTM for `mindepth` and `maxdepth` (`depth = -fdata`).
   - Only creates the output `JHC_header` file if `valid > 0 && maxdepth > 50 && mindepth < mdepth`.

---

## Examples

**1. Generate a tiled series of mapsheet headers named by center Lat/Lon:**
```bash
make_bases -latlon_name -dtm regional_bathy.r4 -mdepth 2500
```

**2. Run GSI charting tile layout with 5 m pixel size and output `box.coords` + binary headers:**
```bash
make_bases -gsi -binhead -dtm ireland_eeza.r4 -pixel 5.0 -mdepth 4000
```

---

## Workflow Context

- **See Also:** [`make_blank`](make_blank.md) (creates a single `.blank` mapsheet) and [`weigh_grid`](weigh_grid.md).
- After generating header-only `Box.header*` files with `make_bases`, use `tor4` or `edhead` to initialize full `.r4` grids for [`weigh_grid`](weigh_grid.md).
