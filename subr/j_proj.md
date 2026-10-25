---
layout: default
title: j_proj
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/j_proj.c
category: Map Projections & Coordinate Transformations
related_tools:
- weigh_grid
- makess
- jview
- r4toz
- j_SalishSeaCast
module_name: j_proj
header_path: code/subr/j_proj.h
---

# `j_proj` — Unified Map Projection & Raster Grid Coordinate Transformation Dispatcher

## Overview & Purpose in the OMG Architecture

`j_proj` (`code/subr/j_proj.c`, `code/subr/j_proj.h`), authored by John E. Hughes Clarke on November 10, 1995, provides the unified forward (`Project`, `Proj_up`) and inverse (`inv_proj`, `inv_proj_up`) map projection interface used across the entire OMG software suite to convert between geographic coordinates `(longitude, latitude)` in decimal degrees and 2D raster pixel coordinates `(x, y)` defined by an OMG `JHC_header` (`array.h`).

Rather than requiring individual applications to switch on projection codes or manage rotation matrices and pixel scaling manually, `j_proj` inspects `head->projection`, `head->ellipsoid`, `head->hemisphere`, origin bounds (`xmin`, `ymin`), grid step sizes (`xstep`, `ystep`), and rotation angle (`head->ymax`), and automatically dispatches to the underlying projection engines (`mercator.c`, `utm.c`, `lambert.c`, `nbstereo.c`, `polarstereo.c`).

---

## Supported Projection Codes (`head->projection`)

`j_proj` supports 12 projection modes stored in `JHC_header.projection`:

| Code | Projection Name | Underlying Engine | Rotation |
| :--- | :--- | :--- | :--- |
| `0` or `3` | Geographic (Unprojected Degrees/Minutes) | Direct linear scaling by `xmin`, `ymin`, `xstep`, `ystep` | North-up |
| `1` | Mercator | `merc_init()`, `mercator()`, `inv_merc()` | North-up |
| `2` | Universal Transverse Mercator (UTM) | `geoutm()`, `utmgeo()` | North-up |
| `4` | Rotated UTM | `geoutm()`, `utmgeo()` + 2D rotation about grid center | Rotated by `head->ymax` (deg) |
| `5` | Rotated Mercator | `merc_init()`, `mercator()`, `inv_merc()` + 2D rotation | Rotated by `head->ymax` (deg) |
| `6` | New Brunswick Double Stereographic (NB Stereo) | `nbstereo_init()`, `nbstereo()`, `nbstereo_inv()` | North-up |
| `7` | Universal Polar Stereographic (UPS) | `polarstereo_init()`, `polarstereo()`, `polarstereo_inv()` | North-up |
| `8` | Rotated NB Double Stereographic | `nbstereo` + 2D rotation about grid center | Rotated by `head->ymax` (deg) |
| `9` | Rotated Polar Stereographic | `polarstereo` + 2D rotation about grid center | Rotated by `head->ymax` (deg) |
| `10` | Lambert Conformal Conic (LCC) | `lambert_init()`, `lambert()`, `lambert_inv()` | North-up |
| `11` | Rotated Lambert Conformal Conic | `lambert` + 2D rotation about `(xmin, ymin)` center | Rotated by `head->ymax` (deg) |

---

## Global Variables (`code/subr/j_proj.c`, `code/subr/wgs.h`)

`j_proj.c` defines the global ellipsoid and projection state variables declared in `wgs.h`:
- `int Ellipsoid`: Active reference ellipsoid code (`WGS84 = 1`, `NAD27 = 2`, `CLK66 = 3`, `AGD84 = 4`, `SPHER = 5`, `ATS77 = 6`), automatically synchronized from `head->ellipsoid` on every call.
- `int Proj_Type`: Active projection type identifier.
- `float Map_Rotation`: Active map sheet rotation angle in degrees.
- `char Hemisphere`: Hemisphere indicator (`'n'` or `'s'`, or `0`/`1`).

---

## Public Functions & Signatures

### Forward Projections (Geographic $\rightarrow$ Grid Pixels)
- `void Project(double vlon, double vlat, double *dblex, double *dbley, JHC_header *head)`
  Converts geographic longitude `vlon` and latitude `vlat` (decimal degrees) into fractional raster pixel coordinates `(*dblex, *dbley)` where `dblex` increases rightward from `0` to `head->dx` and **`dbley` increases downward from the top of the raster array** (`0` at top row to `head->dy` at bottom row).
  - For rotated projections (`4`, `5`, `8`, `9`, `11`), applies the clockwise 2D coordinate rotation by `rot_angle = head->ymax * M_PI / 180.0` and shifts origin to the array center `(dx/2.0, dy/2.0)` before flipping Y (`*dbley = head->dy - *dbley`).

- `void Proj_up(double vlon, double vlat, double *dblex, double *dbley, JHC_header *head)`
  Identical to `Project()`, except that **`*dbley` is measured upward from the bottom of the map sheet** (`0` at bottom to `head->dy` at top), suitable for PostScript plotting and Cartesian map coordinates.

### Inverse Projections (Grid Pixels $\rightarrow$ Geographic)
- `void inv_proj(double x_loc, double y_loc, double *lon, double *lat, double *x, double *y, JHC_header *head)`
  Converts raster pixel coordinates `(x_loc, y_loc)` (with `y_loc` measured downward from the top row) back into geographic coordinates `(*lon, *lat)` in decimal degrees, and also outputs the intermediate projected map coordinates `(*x, *y)` in meters (easting/northing).

- `void inv_proj_up(double x_loc, double y_loc, double *lon, double *lat, double *x, double *y, JHC_header *head)`
  Inverse projection when `y_loc` is measured upward from the bottom row (`calls inv_proj(x_loc, head->dy - y_loc, ...)`).

---

## How It Fits Into the OMG Architecture

`j_proj` is one of the most heavily linked foundational modules in `subr/`. Almost every raster gridding tool (`weigh_grid`, `makess`), format converter, oceanographic lookup module (`j_SalishSeaCast`), and visualization GUI (`jview`) calls `Project()` and `inv_proj()` to register geographic observations with 2D OMG arrays.
