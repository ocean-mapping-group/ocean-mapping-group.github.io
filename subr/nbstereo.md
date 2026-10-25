---
layout: default
title: nbstereo
parent: Core Shared Libraries (subr)
module_name: nbstereo
source_path: code/subr/nbstereo.c
header_path: code/subr/nbstereo.h
category: Map Projections & Coordinate Transformations
related_tools:
  - j_proj
  - weigh_grid
  - makess
  - jview
---

# `nbstereo` — New Brunswick Double Stereographic Map Projection Library

## Overview & Purpose in the OMG Architecture

`nbstereo` (`code/subr/nbstereo.c`, `code/subr/nbstereo.h`), written by Jonathan Beaudoin in March 2001, defines the global ellipsoidal and conformal sphere parameters and forward/inverse transformation prototypes for the **New Brunswick Double Stereographic (`NB Stereo`)** map projection.

Because the Ocean Mapping Group was founded at the University of New Brunswick (UNB) in Fredericton, New Brunswick, Canada, a large proportion of OMG's coastal hydrographic surveys (in the Bay of Fundy, Passamaquoddy Bay, Saint John Harbour, and the Gulf of St. Lawrence) are referenced to the official provincial **New Brunswick Stereographic Double** coordinate system (historically on the **ATS77** ellipsoid `Ellipsoid == 6` or NAD83/WGS84 `Ellipsoid == 1`, with origin at $\phi_0 = 46^\circ 30'\text{ N}$, $\lambda_0 = 66^\circ 30'\text{ W}$, scale factor $k_0 = 0.999912$, False Easting $X_0 = 300,000\text{ m}$ or $2,500,000\text{ m}$, and False Northing $Y_0 = 800,000\text{ m}$ or $7,500,000\text{ m}$).

Unlike a simple stereographic projection, the New Brunswick Double Stereographic projection first maps the reference ellipsoid conformally onto an intermediate **Gauss conformal sphere** of radius $R_{rr} = \sqrt{M_0 N_0}$ before projecting conformally from the sphere onto the tangent plane. In `j_proj.c` (`JHC_header`), `nbstereo` is invoked for projection code `6` (North-up NB Double Stereographic) and projection code `8` (Rotated NB Double Stereographic).

---

## Key Global Variables (`code/subr/nbstereo.h`, `code/subr/nbstereo.c`)

### Ellipsoidal Parameters
- `double a`, `double b`: Semi-major and semi-minor axes of the reference ellipsoid (meters).
- `double e2`, `double e`: First eccentricity squared ($e^2 = (a^2 - b^2)/a^2$) and eccentricity ($e = \sqrt{e^2}$).

### Projection Origin & Scale Parameters
- `double phi0`, `cosphi0`, `sinphi0`: Central latitude $\phi_0$ (radians) and its precomputed cosine and sine.
- `double lambda0`: Central meridian $\lambda_0$ (radians).
- `double X0`, `double Y0`: False Easting and False Northing (meters).
- `double R_rr`: Radius of the Gauss conformal sphere at $\phi_0$ (named `R_rr` to avoid symbol collision with `R` on Linux).
- `double k0`: Central point scale factor ($0.999912$).

### Gauss Conformal Sphere Constants
- `double c1`, `double c2`: Conformal sphere exponent and normalizing constant mapping geodetic latitude/longitude $(\phi, \lambda)$ to spherical conformal coordinates $(\chi, \Lambda)$.
- `double chi0`: Conformal latitude $\chi_0$ corresponding to the geodetic origin $\phi_0$.

---

## Public Functions & Signatures

- `void nbstereo_init()`
  Initializes all global ellipsoidal (`a`, `b`, `e2`, `e`), conformal sphere (`c1`, `c2`, `chi0`, `R_rr`), and projection origin (`phi0`, `lambda0`, `X0`, `Y0`, `k0`) constants for the active `Ellipsoid` (`wgs.h`).
  *Must be called prior to calling `nbstereo()` or `nbstereo_inv()`.*

- `void nbstereo(double latitude, double longitude, double *x, double *y)`
  **Forward New Brunswick Double Stereographic Projection**:
  Converts geodetic `latitude` and `longitude` (in decimal degrees) first onto the Gauss conformal sphere $(\chi, \Lambda)$ and then onto the stereographic plane to return projected Easting `*x` and Northing `*y` in meters.

- `void nbstereo_inv(double *latitude, double *longitude, double X, double Y)`
  **Inverse New Brunswick Double Stereographic Projection**:
  Projects planar Easting `X` and Northing `Y` (in meters) inversely onto the Gauss conformal sphere $(\chi, \Lambda)$ and iteratively recovers geodetic `*latitude` and `*longitude` in decimal degrees.

---

## How It Fits Into the OMG Architecture

`nbstereo` is called automatically by `Project()` and `inv_proj()` in `code/subr/j_proj.c` whenever `head->projection == 6` or `head->projection == 8`, and is also directly included by `code/JV/jview.c` for interactive coordinate readouts in Maritime Canada datasets.
