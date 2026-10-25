---
layout: default
title: lambert
parent: Core Shared Libraries (subr)
module_name: lambert
source_path: code/subr/lambert.c
header_path: code/subr/lambert.h
category: Map Projections & Coordinate Transformations
related_tools:
  - j_proj
  - weigh_grid
  - makess
  - jview
---

# `lambert` — Lambert Conformal Conic (LCC) Map Projection Library

## Overview & Purpose in the OMG Architecture

`lambert` (`code/subr/lambert.c`, `code/subr/lambert.h`) defines the state structure (`Lambert`), global projection instance (`projection_vars`), and forward/inverse mathematical transformation prototypes for the **Lambert Conformal Conic (LCC)** map projection with two standard parallels.

In the OMG raster and mapping architecture (`j_proj.c` and `array.h`), Lambert Conformal Conic is supported as projection code `10` (North-up LCC) and projection code `11` (Rotated LCC). It is particularly suited for mid-latitude continental shelf and regional ocean mapping surveys that span wide east-west extents where a single 6°-wide UTM zone would introduce excessive scale distortion.

---

## Key Data Structures & Globals (`code/subr/lambert.h`, `code/subr/lambert.c`)

### `Lambert` (and global `Lambert projection_vars`)
Stores the reference ellipsoid parameters, user-specified standard parallels and origin, and precomputed Snyder (1987) conformal conic constants:
```c
typedef struct {
    /* Ellipsoidal parameters */
    double a;                      /* Semi-major axis (equatorial radius in meters) */
    double e, e2;                  /* Eccentricity and eccentricity squared (e^2)   */

    /* Projection parameters (in radians) */
    double phi_1, phi_2;           /* First and second standard parallels           */
    double lambda_origin;          /* Central meridian longitude                    */
    double phi_origin;             /* Reference origin latitude                     */
    double false_east, false_north;/* False Easting and False Northing (meters)     */

    /* Precomputed Snyder LCC constants */
    double m1, m2;                 /* m = cos(phi) / sqrt(1 - e^2 * sin^2(phi))     */
    double t_phi1, t_phi2;         /* Conformal latitude factors at phi_1, phi_2    */
    double t_phi_origin;           /* Conformal latitude factor at phi_origin       */
    double n;                      /* Cone constant: ln(m1/m2) / ln(t_phi1/t_phi2)  */
    double F;                      /* Scale factor: m1 / (n * t_phi1^n)             */
    double rF;                     /* Radius at origin: a * F * t_phi_origin^n      */
} Lambert;
```

---

## Public Functions & Signatures

- `void lambert_init(double standard_parallel_1, double standard_parallel_2, double ref_lat, double ref_long, double east_offset, double north_offset)`
  Initializes the global `projection_vars` structure for the active ellipsoid (`Ellipsoid` from `wgs.h`). Converts `standard_parallel_1` (`head->lat_std1`), `standard_parallel_2` (`head->lat_std2`), `ref_lat` (`head->proj_lat`), and `ref_long` (`head->proj_merid`) from degrees to radians, sets `false_east` and `false_north`, and precomputes the ellipsoidal LCC cone constants `m1`, `m2`, `t_phi1`, `t_phi2`, `t_phi_origin`, `n`, `F`, and `rF`.
  *Must be called prior to invoking `lambert()` or `lambert_inv()`.*

- `void lambert(double latitude, double longitude, double *x, double *y)`
  **Forward LCC Projection**: Converts geographic `(latitude, longitude)` in decimal degrees into projected Lambert Conformal Conic coordinates `(*x, *y)` (Easting and Northing in meters):
  $$\rho = a F t^n, \quad \theta = n (\lambda - \lambda_0)$$
  $$x = \rho \sin\theta + E_{\text{false}}, \quad y = \rho_0 - \rho \cos\theta + N_{\text{false}}$$

- `void lambert_inv(double *latitude, double *longitude, double x, double y)`
  **Inverse LCC Projection**: Converts projected Easting `x` and Northing `y` (in meters) back into geographic `(*latitude, *longitude)` in decimal degrees by iteratively solving the conformal latitude equation for $\phi$ from $t = (\rho / (a F))^{1/n}$ and recovering $\lambda = \theta / n + \lambda_0$.

---

## How It Fits Into the OMG Architecture

`lambert` is invoked directly by `Project()` and `inv_proj()` in `code/subr/j_proj.c` whenever `head->projection == 10` (standard LCC) or `head->projection == 11` (rotated LCC), and works alongside `j_area.h` (`lat_std1`, `lat_std2`, `got_lambert_projected_bounds`) and `wgs.h` (`Ellipsoid`).
