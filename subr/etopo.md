---
layout: default
title: etopo
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/etopo.c
category: Global Bathymetry & Environmental Databases
related_tools:
- patchWORLD
- svp_rtofs
module_name: etopo
header_path: code/subr/etopo.h
---

# etopo: ETOPO5 Global 5-Arc-Minute Bathymetric/Topographic Database Extractor

## Overview & Purpose
`etopo` (`etopo.c` / `etopo.h`, 150 lines) provides extraction and bilinear depth-interpolation routines for the NOAA ETOPO5 global 5-arc-minute bathymetric and topographic database. Originally written by Guy Carpenter in June 1990 and later extended with `Map`-based bilinear interpolation (`load_ETOPO5_map` / `get_ETOPO5_depth`), it allows OMG gridding and oceanographic tools to extract regional elevation/depth sub-grids (including seamless $360^\circ$ longitude wrapping across the Prime Meridian or International Date Line) or query global background water depth at any `(lat, lon)` coordinate.

---

## Key Constants & Global Variables

```c
#define ETOPO_GRID  (5.0 / 60.0)                      /* 5-arc-minute grid spacing (0.083333 deg) */
#define ETOPO_RLEN  (360 * 12)                        /* 4,320 samples per latitude row */
#define ETOPO_TYPE  short                             /* 16-bit signed integer elevation in meters */
#define ETOPO_DBASE "/usr/people/solomon/jhc/extra/etopo5"

Map ETOPO5_map;                                       /* Global OMG Map structure loaded via ETOPO5_PATH */
```

---

## Public Functions & Signatures

### `float *etopo_extract(char *filename, float lon0, float lat0, float lon1, float lat1, int *rdx, int *rdy, float *min_lon, float *max_lat)`
Extracts a rectangular geographic sub-grid from a raw binary ETOPO5 file (`filename`, containing $2160 \times 4320$ 16-bit integers from $90^\circ\text{N}$ to $90^\circ\text{S}$, $0^\circ\text{E}$ to $360^\circ\text{E}$) and returns a newly allocated row-major `float *` buffer.
* **Parameters:**
  * `filename`: Path to the raw binary ETOPO5 database file.
  * `lon0, lat0`: Minimum longitude and minimum latitude of the desired bounding box (in degrees).
  * `lon1, lat1`: Maximum longitude and maximum latitude of the desired bounding box (in degrees).
  * `rdx, rdy`: Output pointers receiving the extracted grid width (`*rdx`) and height (`*rdy`) in grid cells.
  * `min_lon, max_lat`: Output pointers receiving the snapped grid origin (top-left corner: minimum longitude and maximum latitude, rounded to exact `ETOPO_GRID` $5'$ multiples).
* **Algorithmic Details:**
  1. Normalizes `lon0` into $[0^\circ, 360^\circ)$ by adding $360^\circ$ while `lon0 < 0.0`.
  2. Snaps latitude and longitude bounds to 5-arc-minute grid multiples using `rounddown()` and `roundup()` from `support.h`.
  3. Computes starting row index `r0 = floor((90.0 - mx_lat) / ETOPO_GRID)`, row count `rcount`, starting column `b0 = lon0 / ETOPO_GRID`, and column count `rlen`.
  4. Seeks to row `r0` (`r0 * 4320 * sizeof(short)`), reads `rcount` rows, and copies `rlen` samples per row into `outbuf`, automatically wrapping back to the beginning of the row buffer (`p = buf`) if the requested longitude span crosses $360^\circ$ (even supporting multi-circumference extractions up to $720^\circ$).

### `int load_ETOPO5_map()`
Reads the `ETOPO5_PATH` environment variable (calling `error()` if unset) and loads the OMG-formatted ETOPO5 raster into the global `ETOPO5_map` (`Map` struct from `array.h`) using `load_map(etopo5_path)`.
* **Returns:** `0` on success.

### `float get_ETOPO5_depth(double lat, double lon)`
Queries the pre-loaded `ETOPO5_map` for the interpolated elevation/depth at geographic coordinates `(lat, lon)`:
1. Converts `(lat, lon)` to fractional 5-arc-minute pixel coordinates:
   $$x = \text{lon} \times 12.0 \quad (\text{adding } 4320 \text{ if } \text{lon} < 0), \qquad y = (90.0 - \text{lat}) \times 12.0$$
2. Extracts the $2 \times 2$ surrounding cell values (`data[0..3]`) from `ETOPO5_map.data_float`.
3. Interpolates and returns the depth using `map_bilinear(x - (int)x, y - (int)y, data)`.

---

## How It Fits Into the OMG Architecture
`etopo` is used by:
* **`patchWORLD` (`code/grid/patchWORLD.c`):** Calls `etopo_extract` to build background global/regional bathymetric grids and fill unmapped deep-ocean regions around multibeam surveys.
* **`svp_rtofs` (`code/jonnyb/svp/svp_rtofs.c`):** Calls `load_ETOPO5_map` and `get_ETOPO5_depth` to compare numerical ocean model (RTOFS) profile depths against ETOPO5 seafloor depths when extracting synthetic sound velocity profiles.
