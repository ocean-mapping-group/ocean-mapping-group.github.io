---
layout: default
title: j_SalishSeaCast
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/j_SalishSeaCast.c
category: Oceanographic Models & Water Column
related_tools:
- soundscape
- SYN_internal_wave
- raytracing utilities
module_name: j_SalishSeaCast
header_path: code/subr/j_SalishSeaCast.h
---

# `j_SalishSeaCast` — SalishSeaCast 3D Oceanographic Model Grid & Lookup Library

## Overview & Purpose in the OMG Architecture

`j_SalishSeaCast` (`code/subr/j_SalishSeaCast.c`, `code/subr/j_SalishSeaCast.h`), written by John E. Hughes Clarke in November 2024, provides spatial indexing, coordinate transformation, and 3D volumetric parameter loading for the **SalishSeaCast** hydrodynamic ocean model (a 398 × 898 curvilinear NEMO-based grid covering the Strait of Georgia, Juan de Fuca Strait, and Puget Sound).

Because the SalishSeaCast model uses an irregularly spaced, rotated curvilinear grid (with variable grid spacing especially near the Fraser River plume), directly searching the 398 × 898 latitude/longitude array for every acoustic ping or raytrace step is computationally expensive. `j_SalishSeaCast` solves this by combining pre-gridded OMG `JHC_header` lookup maps (`.mask`, `.xcoord.r4`, `.ycoord.r4`) with point-in-polygon and local neighborhood search fallbacks to rapidly map geographic `(lon, lat)` coordinates into fractional SalishSeaCast grid indices `(rx, ry)`, and to load multi-layer 3D oceanographic fields (salinity, temperature, sound speed, and 3D current velocities `u`, `v`, `w`).

---

## Key Data Structures, Constants & Macros

### Constants
- `SALISHMAXLAYERS` (`200`): Maximum number of vertical depth layers supported for a 3D SalishSeaCast parameter volume.

### Data Structures (`code/subr/j_SalishSeaCast.h`)

#### `SalSea_3dparam`
Represents a 3D oceanographic parameter volume across the model grid:
- `int nolayers`: Number of vertical depth levels loaded from the `.zvals` file.
- `float zval[SALISHMAXLAYERS]`: Depth (m) of each vertical layer.
- `JHC_header header`: Standard OMG 2D raster header describing grid dimensions (`dx`, `dy`).
- `int alloced`: Allocation status flag.
- `float *ParamLayer[SALISHMAXLAYERS]`: Array of pointers to 2D floating-point slices (`dx * dy` floats per depth layer).

#### `SalSea_bits` (and global instance `SalSea_bits SalishSea`)
Master container holding the SalishSeaCast horizontal grid geometry, fast lookup rasters, and 3D parameter volumes:
- `JHC_header lat_head`, `lon_head` and `float *latsalish`, `*lonsalish`: The 2D arrays of node latitudes and longitudes for the curvilinear model grid.
- `JHC_header xco_head`, `yco_head` and `float *xcoord`, `*ycoord`: Precomputed regular OMG `.r4` rasters mapping projected `(x, y)` coordinates directly to fractional model grid indices `(rx, ry)`.
- `JHC_header maskhead` and `unsigned char *maskmap`: Raster mask indicating whether a geographic point lies inside valid ocean cells (`> 1`) or outside/land (`0` or `1`).
- `double cornerlat[4]`, `cornerlon[4]`, `cenlat`, `cenlon`, `coscenlat`, `rotangle[4]`: Bounding polygon corner coordinates, center point, and edge rotation angles used for rapid point-in-polygon rejection.
- `double minSalishlat`, `maxSalishlat`, `minSalishlon`, `maxSalishlon`: Geographic bounding box of the entire model domain.
- `int last_rx`, `last_ry`: Cached grid indices from the previous query.
- `SalSea_3dparam salinity`, `temperature`, `soundSpeed`, `uVelocity`, `vVelocity`, `wVelocity`: 3D volumetric parameter fields sharing the horizontal projection.

---

## Public Functions & Signatures

- `int SalSea_load_latlon(char *latname, char *lonname, char *maskname)`
  Initializes the global `SalishSea` structure:
  1. Opens `maskname` and reads the 8-bit `maskmap` via `get_print_JHC_header()`.
  2. Automatically derives and loads `<mask_prefix>.xcoord.r4` and `<mask_prefix>.ycoord.r4` into `SalishSea.xcoord` and `SalishSea.ycoord` using byte-swapped float I/O (`jswapfloat_fread`).
  3. Loads the curvilinear latitude (`latname`) and longitude (`lonname`) float arrays, computes global min/max geographic bounds, and calculates the four corner coordinates and edge azimuth angles (`rotangle[0..3]`) of the rotated model domain.

- `int SalSea_find_rxry(double lon, double lat, double *rx, double *ry)`
  Maps a geographic coordinate `(lon, lat)` in decimal degrees to fractional SalishSeaCast array coordinates `(*rx, *ry)`:
  - **Primary Fast Path**: Projects `(lon, lat)` into `SalishSea.maskhead` pixel space using `Project()`. If `maskval > 1`, performs bilinear interpolation on `SalishSea.xcoord` and `SalishSea.ycoord` via `get_JHC_lookup_value()` to immediately return sub-cell `(rx, ry)` indices (`returns 1`). If `maskval` is `0` or `1`, returns `-1`.
  - **Fallback Geometric Search**: Tests if the point lies inside the 4-corner rotated bounding polygon and min/max lat/lon bounds, then searches a local 5 × 5 neighborhood (or full grid if uninitialized) for the minimum Euclidean distance in meters (`minradm < 500m`).

- `int load_Salish_parameter(char *paramprefix, SalSea_3dparam *aparam)`
  Loads a 3D oceanographic variable into `aparam`:
  1. Reads layer index and depth values from `<paramprefix>.zvals` into `aparam->zval[]`.
  2. Opens `<paramprefix>.r4`, reads its `JHC_header`, allocates `aparam->nolayers` 2D float slices (`dx * dy`), and populates each depth layer using `jswapfloat_fread()`.

- `int free_Salish_param(SalSea_3dparam *aparam)`
  Frees all dynamically allocated `ParamLayer[i]` buffers and resets `aparam->alloced = 0`.

---

## How It Fits Into the OMG Architecture

`j_SalishSeaCast` bridges high-resolution coastal hydrodynamic models with OMG's acoustic raytracing and synthetic water-column simulation tools (`code/gl/`, `soundscape`, and Salish Sea refraction modeling utilities). It relies on `array.h` (`get_print_JHC_header`, `get_JHC_lookup_value`), `j_proj.h` (`Project`), `swapio.h` (`jswapfloat_fread`), and `support.h` (`mem_strappend`, `mem_stripext`) to integrate NEMO netCDF-derived binary slices into OMG's native raster and water-column ecosystem.
