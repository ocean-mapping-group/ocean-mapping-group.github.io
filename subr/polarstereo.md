---
layout: default
title: polarstereo
parent: Core Shared Libraries (subr)
module_name: polarstereo
source_path: code/subr/polarstereo.c
header_path: code/subr/polarstereo.h
category: Navigation, Attitude & Geodesy
related_tools:
  - j_proj
  - jview (JV)
  - swathed (SE)
  - weigh_grid
---

# polarstereo

## Overview & Purpose

`polarstereo` defines the global projection state variables and public function prototypes for the Universal Polar Stereographic (UPS) / Ellipsoidal Polar Stereographic map projection (North and South polar aspects) within the Ocean Mapping Group (OMG) geodetic projection subsystem. While `polarstereo.c` instantiates the global state variables declared `extern` in `polarstereo.h`, the forward, inverse, and initialization routines (`polarstereo()`, `polarstereo_inv()`, and `polarstereo_init()`) are linked alongside `j_proj.c` (`code/subr/j_proj.c`) to support high-latitude Arctic and Antarctic hydrographic mapping.

## Key Data Structures, Constants & Macros

### Global Projection & Ellipsoid Variables

Defined in `polarstereo.c` and exposed as `extern` in `polarstereo.h`:
- **Hemisphere / Aspect Control**:
  - `int polars_south`: Boolean flag indicating whether the South Polar aspect (`1`) or North Polar aspect (`0`) is active.
- **Reference Ellipsoid Parameters**:
  - `double polars_a`: Semi-major axis (equatorial radius $a$ in meters) of the active reference ellipsoid.
  - `double polars_e`: First eccentricity ($e = \sqrt{2f - f^2}$) of the active reference ellipsoid.
- **Stereographic Projection Parameters**:
  - `double polars_k0`: Central scale factor at the pole ($k_0$, typically `0.994` for standard Universal Polar Stereographic).
  - `double polars_falseEast`: False Easting offset in meters (typically `2000000.0` m for UPS).
  - `double polars_falseNorth`: False Northing offset in meters (typically `2000000.0` m for UPS).
  - `double polars_C0`: Precomputed conformal scaling constant:
    $$C_0 = \frac{2 a k_0}{\sqrt{1 - e^2}} \left( \frac{1 - e}{1 + e} \right)^{e/2}$$

## Public Functions & Signatures

- `void polarstereo_init(char poleID)`
  - Initializes the polar stereographic projection state for the specified pole (`poleID = 'N'` or `'S'`), setting `polars_south`, false easting/northing offsets, central scale factor `polars_k0`, and precomputing `polars_C0` from the active ellipsoid (`polars_a`, `polars_e`).
- `void polarstereo(double latitude, double longitude, double *x, double *y)`
  - Forward projection: converts geographic coordinates (`latitude`, `longitude`) into Polar Stereographic grid coordinates (`*x` Easting, `*y` Northing in meters) using the conformal latitude tangent formula and `polars_C0`.
- `void polarstereo_inv(double x, double y, double *latitude, double *longitude)`
  - Inverse projection: converts Polar Stereographic grid coordinates (`x`, `y` in meters) back into geographic (`*latitude`, `*longitude`) via iterative conformal latitude inversion using `polars_e`, `polars_C0`, and `polars_south`.

## How It Fits Into the OMG Architecture

`polarstereo.h` is included directly by **`j_proj.c`** (`code/subr/j_proj.c`), which serves as the unified map projection dispatcher (`Project()` and `inv_proj()`) for all OMG raster grids (`JHC_header`). Whenever a grid header specifies the Polar Stereographic projection (`projection == POLAR_STEREO`), `j_proj.c` calls `polarstereo_init(head->hemisphere)`, `polarstereo()`, and `polarstereo_inv()`. This enables seamless polar mapping in **`weigh_grid`**, **`jview` (`JV`)**, **`swathed` (`SE`)**, and all OMG gridding and visualization utilities used in Arctic and Antarctic surveys.
