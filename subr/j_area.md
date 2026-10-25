---
layout: default
title: j_area
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/j_area.c
category: Map Projections & Geographic Bounds
related_tools:
- inArea
- checkSD
- getGraz
- weigh_grid
- jview
module_name: j_area
header_path: code/subr/j_area.h
---

# `j_area` — Geographic Bounding Box & Gridding Area Setup Library

## Overview & Purpose in the OMG Architecture

`j_area` (`code/subr/j_area.c`, `code/subr/j_area.h`), created by John E. Hughes Clarke in July 1991, defines the shared global variables and interactive/command-line setup prototypes used across OMG gridding, plotting, and spatial subsetting utilities to specify a geographic survey region, map projection parameters, and raster grid dimensions (`JHC_header`).

In the OMG software suite, tools that construct new raster grids (`.r4` bathymetries, `.u1` sidescan mosaics, or PostScript plot sheets) or filter swath soundings by geographic bounds share a common set of global bounding coordinates (`tlat`, `blat`, `tlon`, `blon`) and projection parameters (`merid_val`, `proj_lat`, `proj_lon`, `lat_std1`, `lat_std2`, `scale`). `j_area` centralizes these declarations so that library routines in `subr/` and application programs in `code/omg/` and `code/JV/` can exchange region definitions seamlessly.

---

## Key Global Variables (`code/subr/j_area.h`, `code/subr/j_area.c`)

### Geographic Bounding Coordinates
- `double tlat, blat, tlon, blon`: Primary top/bottom latitude and top/bottom (or left/right) longitude bounds of the target area (in decimal degrees).
- `double ttlat, bblat, ttlon, bblon`: Secondary/transformed bounding coordinates (used when rotating projections or computing corner envelopes).
- `int dateline_flag`: Flag indicating whether the geographic region crosses the $180^\circ$ International Date Line.

### Map Projection & Grid Parameters
- `double merid_val`: Central meridian (degrees) for UTM (`projection == 2` or `4`) or Mercator projections.
- `double proj_lat, proj_lon`: Reference origin latitude and longitude for projected coordinate systems.
- `double lat_std1, lat_std2`: First and second standard parallels (degrees) for Lambert Conformal Conic projections (`projection == 10` or `11`).
- `double scale`: Map scale or resolution factor.
- `int got_lambert_projected_bounds`: Flag indicating whether Lambert projected bounding coordinates have been explicitly initialized.

---

## Public Functions & Signatures

While `code/subr/j_area.c` instantiates the global state variables, `code/subr/j_area.h` declares the standard interactive region-Prompting and grid-sizing routines (linked with OMG gridding utilities):

- `void get_region()`
  Prompts the user or parses configuration state to establish the geographic region of interest (`tlat`, `blat`, `tlon`, `blon`) and projection type.
- `void get_area()`
  Computes the projected extent of the bounding box in meters or map units based on the active ellipsoid (`Ellipsoid` from `wgs.h`) and projection settings.
- `void gridsize(float *mpp, int *xno, int *yno, JHC_header *head)`
  Given a desired grid cell resolution in meters per pixel (`*mpp`) and the active geographic bounds, computes the required raster width (`*xno`), height (`*yno`), origin offsets (`xmin`, `ymin`), and populates the corresponding fields of a `JHC_header` structure (`array.h`).
- `void read_lat_long(int input_format, double *lat, double *lon)`
  Reads latitude and/or longitude values from standard input according to `input_format` (e.g., decimal degrees vs. degrees and decimal minutes). Either `lat` or `lon` may be passed as `NULL` if only a single coordinate component is requested.

---

## How It Fits Into the OMG Architecture

`j_area` is included by spatial filtering and analysis utilities in `code/omg/` (such as `inArea`, `checkSD`, `getGraz`) and by the main interactive visualization environment `code/JV/jview` (`JV_global.h`). It works directly alongside `array.h` (`JHC_header`), `wgs.h` (ellipsoid constants), `j_proj.h`, `mercator.h`, `utm.h`, and `lambert.h` to initialize raster headers and test whether swath pings fall within a target map sheet.
