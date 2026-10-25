---
layout: default
title: mercator
parent: Core Shared Libraries (subr)
module_name: mercator
source_path: code/subr/mercator.c
header_path: code/subr/mercator.h
category: Map Projections & Coordinate Transformations
related_tools:
  - j_proj
  - weigh_grid
  - makess
  - inArea
  - checkSD
  - getGraz
  - showPingRate
  - correctBS
  - jview
---

# `mercator` — Ellipsoidal Mercator Map Projection Library

## Overview & Purpose in the OMG Architecture

`mercator` (`code/subr/mercator.c`, `code/subr/mercator.h`), originally written by Guy Carpenter on November 13, 1989 and extended by John E. Hughes Clarke in 1993 (adding Snyder's ellipsoidal inverse Mercator) and Bill Danforth (`merc_fixBWD`), provides forward and inverse **Ellipsoidal Mercator** map projection transformations for OMG grids and navigation tools.

In the OMG raster header specification (`JHC_header` in `array.h`), Mercator is used for projection codes `1` (North-up Mercator) and `5` (Rotated Mercator). Beyond raster gridding, many standalone OMG analysis tools (`inArea`, `checkSD`, `getGraz`, `showPingRate`, `correctBS`) call `merc_init()` and `mercator()` directly with `scale = 1.0` to convert geographic `(lon, lat)` degrees into local metric $(x, y)$ displacements (in meters) around a survey area's central latitude (`proj_lat`).

---

## Key Global Variables, Types & Macros (`code/subr/mercator.h`, `code/subr/mercator.c`)

### Global State Variables
- `double merc_eccen`: Eccentricity $e$ of the active reference ellipsoid (defaults to `WGS84_ECCEN = 0.0818191908417579`).
- `double merc_earthrad`: Equatorial radius $a$ in meters (defaults to `WGS84_RADIUS = 6378137.0`).
- `double merc_eqscale`: Scale factor at the equator derived from the standard parallel `proj_lat` ($\cos\phi_0 / \sqrt{1 - e^2\sin^2\phi_0}$).
- `double merc_scaledrad`: Effective scaled radius (`merc_earthrad * merc_eqscale / scale`).
- `double merc_xoffset`, `double merc_yoffset`: Projected map origin offsets corresponding to `(origin_lon, origin_lat)`.
- `char merc_signflag`: Hemisphere/longitude sign handling flag.

### Enums & Macros
- `mapproj_type`: Enumeration `{no_proj, mercator_proj, utm_proj, amg_proj, rotutm_proj}`.
- `DEGTORAD(D)`: `((double)(D) * M_PI / 180.0)`
- `RADTODEG(D)`: `((double)(D) * 180.0 / M_PI)`

---

## Public Functions & Signatures

- `void merc_init(double scale, double proj_lat, double origin_lon, double origin_lat)`
  Initializes the Mercator projection state before calling `mercator()` or `inv_merc()`:
  1. Sets `merc_eccen` and `merc_earthrad` from the active `Ellipsoid` (`wgs.h`).
  2. Computes the true-scale parallel factor `merc_eqscale` at latitude `proj_lat` (degrees) and divides by `scale` (e.g., meters per pixel `head->xstep`, or `1.0` for raw meters) to set `merc_scaledrad`.
  3. Projects `(origin_lon, origin_lat)` to establish the grid origin offsets `(merc_xoffset, merc_yoffset)`.

- `void merc_fixBWD(int ellipsoid, double proj_lat)`
  Explicitly updates the ellipsoid parameters (`merc_eccen`, `merc_earthrad`) and standard-parallel scale factor (`merc_eqscale`) for a specified `ellipsoid` ID and reference latitude `proj_lat`.

- `void mercator(double lon, double lat, double *x, double *y)`
  **Forward Ellipsoidal Mercator Projection**: Converts longitude `lon` and latitude `lat` (decimal degrees) into projected map units `(*x, *y)` relative to `(origin_lon, origin_lat)`:
  $$x = R_{\text{scaled}} \cdot \text{DEGTORAD}(\text{lon}) - x_{\text{offset}}$$
  $$y = R_{\text{scaled}} \cdot \ln\left[\tan\left(\frac{\pi}{4} + \frac{\phi}{2}\right) \left(\frac{1 - e\sin\phi}{1 + e\sin\phi}\right)^{e/2}\right] - y_{\text{offset}}$$

- `void inv_merc(double x, double y, double *lon, double *lat)`
  **Inverse Ellipsoidal Mercator Projection**: Converts projected map coordinates `(x, y)` back into geographic `(*lon, *lat)` in decimal degrees using Snyder's iterative/series expansion for isometric latitude $t = \exp(-(y + y_{\text{offset}}) / R_{\text{scaled}})$ and conformal latitude $\chi = \frac{\pi}{2} - 2\arctan(t)$.

---

## How It Fits Into the OMG Architecture

`mercator` is called by `j_proj.c` for raster projections `1` and `5`, and is directly included by numerous swath and backscatter analysis utilities in `code/omg/` (`inArea`, `checkSD`, `getGraz`, `showPingRate`, `correctBS`) and `code/JV/` (`JV_global.h`) whenever fast local metric coordinate conversion is needed.
