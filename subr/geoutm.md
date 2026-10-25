---
layout: default
title: geoutm
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/geoutm.c
category: Geodesy, Map Projections & Coordinate Transforms
related_tools:
- dumpXYZ
- convertutm
- make_bases
- make_blank
- r4toASCII
- r4toGRASS
- testutm
- dohypackLNW
- swathed
module_name: geoutm
header_path: code/subr/wgs.h
---

# `geoutm` — Forward Geographic-to-UTM Map Projection

## Overview & Purpose
The `geoutm` module (`code/subr/geoutm.c`, declared in `code/subr/wgs.h`) implements the forward Universal Transverse Mercator (UTM) map projection. Originally written by Alberto Malinverno at Lamont-Doherty Geological Observatory (LDGO) on March 3, 1986 and adopted into the OMG core library, it converts geographic latitude and longitude $(\phi, \lambda)$ in decimal degrees—along with a specified UTM central meridian $\lambda_0$—into metric UTM Easting ($x$) and Northing ($y$) coordinates across multiple reference ellipsoids.

---

## Reference Ellipsoids & Projection Constants (`wgs.h` / `geoutm.c`)

### Supported Reference Ellipsoids (`extern int Ellipsoid`)
`geoutm()` inspects the global `Ellipsoid` selector defined in `code/subr/wgs.h` (defaulting to `WGS84` when `0`) to set the semi-major axis $a$ and squared first eccentricity $e^2$:

| Constant | ID | Ellipsoid / Datum | Semi-Major Axis $a$ (m) | Eccentricity Squared $e^2$ |
| :--- | :--- | :--- | :--- | :--- |
| `WGS84` | `1` (or `0`) | World Geodetic System 1984 | `6378137.0` | `0.0066943800` |
| `CLK66` | `2` | Clarke 1866 | `6378206.4` | `0.006768658` |
| `NAD27` | `3` | North American Datum 1927 | `6378206.4` | `0.006768658` |
| `AGD84` | `4` | Australian Geodetic Datum 1984 | `6378160.0` | `0.006694542` |
| `SPHER` | `5` | Clarke 1866 Authalic Sphere | `6370997.0` | `0.0` |

### UTM Projection Constants
- **Central Meridian Scale Factor (`k0`):** `0.9996` (on a sphere `SPHER`, `k0` is set to `1.0`).
- **False Easting (`x0`):** `500000.0` meters added to all $x$ coordinates.
- **Southern Hemisphere False Northing (`y0`):** `10000000.0` meters added to $y$ when $\phi < 0^\circ$.

---

## Public Function & Algorithm

```c
void geoutm(double phi, double lam, double clam, double *x, double *y);
```

- **Parameters:**
  - `phi`: Geographic latitude $\phi$ in decimal degrees (positive North, negative South).
  - `lam`: Geographic longitude $\lambda$ in decimal degrees (positive East, negative West).
  - `clam`: Central meridian $\lambda_0$ of the target UTM zone in decimal degrees (e.g., `-63.0` for UTM Zone 20).
  - `x`: Output pointer receiving UTM Easting in meters.
  - `y`: Output pointer receiving UTM Northing in meters.
- **Algorithm (Snyder, USGS Bulletin 1532, p. 68, 1982):**
  1. **Unit Conversion & Second Eccentricity:** Converts `phi`, `lam`, and `clam` from degrees to radians (`DEGRAD = 0.0174532925199433`) and computes second eccentricity squared $e'^2 = e^2 / (1 - e^2)$.
  2. **True Meridional Distance ($m$):** Evaluates the 4-term trigonometric series expansion in $\phi$, $\sin(2\phi)$, $\sin(4\phi)$, and $\sin(6\phi)$:
     $$m = a \left( m_1 \phi - m_2 \sin 2\phi + m_3 \sin 4\phi - m_4 \sin 6\phi \right)$$
  3. **Transverse Mercator Power Series:** Computes the prime vertical radius of curvature $n = a / \sqrt{1 - e^2\sin^2\phi}$, $t = \tan^2\phi$, $c = e'^2\cos^2\phi$, and reduced longitude offset $b = (\lambda - \lambda_0)\cos\phi$, then evaluates the 5th-order expansion for Easting (`*x`) and 6th-order expansion for Northing (`*y`).
  4. **False Origin Offsets:** Adds `x0 = 500000.0` to `*x`, and if $\phi < 0.0$, adds `y0 = 10000000.0` to `*y`.

---

## How It Fits Into the OMG Architecture
`geoutm` is paired with its inverse `utmgeo` (`code/subr/utmgeo.c`) and higher-level wrapper `proj.c` (`geoutm_skew`) to provide UTM coordinate projection across the OMG toolset:
- **Sounding & Navigation Export (`dumpXYZ`, `convertutm`, `dohypackLNW`, `testutm`):** Projects WGS84 swath soundings and ship tracklines into UTM Easting/Northing coordinates for hydrographic charting.
- **Grid Initialization & GIS Export (`make_bases`, `make_blank`, `r4toASCII`, `r4toGRASS`, `swathed`):** Projects geographic bounding boxes and unprojected `.r4` digital terrain models into UTM map sheets.
