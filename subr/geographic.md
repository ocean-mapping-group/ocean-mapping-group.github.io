---
layout: default
title: geographic
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/geographic.c
category: Geodesy, Map Projections & Coordinate Transforms
related_tools:
- grazing_angle
- swathed
- EKlook
- tidecor2.42
- synSwath
- edhead
- make_blank
- r4toESRI
module_name: geographic
header_path: code/subr/geographic.h
---

# `geographic` — WGS84 Ellipsoidal Curvature, Scale Factors, and Geodesic Distance

## Overview & Purpose
The `geographic` module (`code/subr/geographic.c` and `code/subr/geographic.h`) provides core geodetic calculations on the WGS84 reference ellipsoid. It computes meridional and prime-vertical radii of curvature, local meter-per-degree coordinate scale factors, Universal Transverse Mercator (UTM) zone/meridian lookups, and three distinct tiers of geographic distance calculation ranging from fast local tangent-plane approximations to high-precision iterative Vincenty ellipsoidal geodesics.

---

## Geodetic Constants & Formulations (`geographic.c`)
- **WGS84 Reference Ellipsoid Parameters:**
  - Semi-major axis: $a = 6,378,137.0\text{ m}$
  - Semi-minor axis (Vincenty): $b = 6,356,752.314245\text{ m}$
  - Flattening: $f = 1 / 298.257223563$
  - First eccentricity: $e = 0.0818191908417579$
- **Reference Literature:** Radii of curvature formulations follow Vaníček & Krakiwsky, *Geodesy: The Concepts* (pp. 112, 324).

---

## Public Functions & Signatures

### 1. Ellipsoidal Radii of Curvature & Local Scale Factors

```c
int radii_of_curvature(double latitude, double *M, double *N);
int get_lat_lon_scales(double base_latitude, double *lat_scale, double *lon_scale);
```
- **`radii_of_curvature()`:** Given `latitude` $\phi$ in decimal degrees, computes:
  - Meridional radius of curvature (North-South):
    $$M = \frac{a(1 - e^2)}{(1 - e^2 \sin^2\phi)^{3/2}}$$
  - Prime vertical radius of curvature (East-West):
    $$N = \frac{a}{\sqrt{1 - e^2 \sin^2\phi}}$$
- **`get_lat_lon_scales()`:** Calls `radii_of_curvature(base_latitude, &M, &N)` and converts the radii into local linear scale factors in **meters per degree**:
  - `*lat_scale` $= M \cdot \frac{\pi}{180}$
  - `*lon_scale` $= N \cdot \cos\phi \cdot \frac{\pi}{180}$

### 2. UTM Zone and Central Meridian Lookups

```c
signed int gimme_UTM_meridian(unsigned int zone);
unsigned int gimme_UTM_zone(float longitude);
```
- **`gimme_UTM_meridian()`:** Returns the central meridian in integer degrees $(-177 + (\text{zone} - 1) \times 6)$ for a standard UTM `zone` in $[1, 60]$, or `-999` if out of range.
- **`gimme_UTM_zone()`:** Validates that `longitude` is a valid central meridian (an odd multiple of $3^\circ$ within $[-180^\circ, +180^\circ]$) and returns the corresponding UTM zone number $((longitude + 177.0) / 6 + 1)$, or `0` if invalid.

### 3. Three-Tier Geographic Distance Functions

```c
double compute_distance(double lat1, double lon1, double lat2, double lon2);
double compute_distance_ian(double lat1, double lon1, double lat2, double lon2);
double compute_distance_2(double lat1, double lon1, double lat2, double lon2);
```
- **`compute_distance()` (Local Tangent-Plane Euclidean):** Evaluates `get_lat_lon_scales()` at the midpoint latitude $(\text{lat}_1 + \text{lat}_2)/2$ and returns $\sqrt{(\Delta\text{lat}\cdot S_{\text{lat}})^2 + (\Delta\text{lon}\cdot S_{\text{lon}})^2}$ in meters. Fast and accurate for short sonar-swath baselines.
- **`compute_distance_ian()` (Spherical Great-Circle):** Applies the spherical law of cosines $\arccos(\sin\phi_1\sin\phi_2 + \cos\phi_1\cos\phi_2\cos\Delta\lambda)$ scaled by a mean Earth radius of $6,357,000\text{ m}$.
- **`compute_distance_2()` (Vincenty Inverse Ellipsoidal Geodesic):** Implements T. Vincenty's (1975) iterative inverse formula on the WGS84 ellipsoid. Reduces latitudes via $\tan U = (1 - f)\tan\phi$, iterates $\lambda$ up to 100 times until $|\lambda - \lambda_p| \le 10^{-12}\text{ rad}$, and applies ellipsoidal series corrections ($A, B, \Delta\sigma$) to return sub-millimeter geodesic distance in meters.

---

## How It Fits Into the OMG Architecture
`geographic` is used throughout the OMG navigation, bathymetric gridding, and backscatter processing tools:
- **3D Seafloor Grazing Angles (`grazing_angle`):** `get_lat_lon_scales()` converts geographic sounding offsets $(\Delta\text{lat}, \Delta\text{lon})$ into local metric East/North coordinates when fitting 3D least-squares seafloor planes across neighboring pings.
- **Swath Editing & Interactive Viewers (`swathed`, `EKlook`, `synSwath`):** Computes vessel speed-over-ground, along-track ping spacing, and cursor measurement distances.
- **Grid Header & GIS Utilities (`edhead`, `make_blank`, `r4toESRI`, `tidecor2.42`):** Converts between geographic bounds, UTM zones, and metric grid cell sizes.
