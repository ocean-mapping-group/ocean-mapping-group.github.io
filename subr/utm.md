---
layout: default
title: utm
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/utm.c
category: Map Projections, Ellipsoids & Geodesy
related_tools:
- geoutm
- utmgeo
- j_proj
- geographic
- array
module_name: utm
header_path: code/subr/utm.h
---

# utm

## Overview
`utm` (`utm.c` / `utm.h`) provides both the forward (`geoutm`) and inverse (`utmgeo`) **Universal Transverse Mercator (UTM)** map projection transformations in a single ANSI C compilation unit.

Originally implemented by A. Malinverno (March 3, 1986) from J.P. Snyder's *Map Projections — A Working Manual* (USGS Bulletin 1532, p. 68, 1982) and integrated into the Ocean Mapping Group library by John Hughes Clarke, `utm.c` supersedes the older K&R-style standalone files [`geoutm.c`](geoutm.html) and [`utmgeo.c`](utmgeo.html). It converts between geographic coordinates $(\phi, \lambda)$ in decimal degrees and standard UTM grid coordinates $(X, Y)$ in meters relative to a user-specified central meridian $\lambda_0$ (`clam`).

---

## Ellipsoid & Convention Parameters

`utm.c` reads the global `extern int Ellipsoid` variable defined in `wgs.h` to select the reference ellipsoid semi-major axis $a$ and eccentricity squared $e^2$:

| `Ellipsoid` Macro (`wgs.h`) | ID | Semi-Major Axis $a$ (m) | Eccentricity $e$ |
|---|---|---|---|
| `WGS84` | `1` | `6378137.0` | `0.0818191908417579` |
| `NAD27` | `2` | `6378206.4` | `0.082271854` |
| `CLK66` (Clarke 1866) | `3` | `6378206.4` | `0.082271684` |
| `AGD84` | `4` | `6378160.0` | `0.08182018` |
| `SPHER` (Sphere) | `5` | `6378137.0` | `0.0` |

### Standard UTM Constants
- Central meridian scale factor: $k_0 = 0.9996$
- False Easting: $x_0 = 500,000.0\text{ m}$
- Southern Hemisphere False Northing: $y_0 = 10,000,000.0\text{ m}$ (added when $\phi < 0$ in `geoutm`, or subtracted when `hem == 's' || hem == 'S'` in `utmgeo`).

---

## Public Functions

| Function | Signature | Description |
|---|---|---|
| `geoutm` | `void geoutm(double phi, double lam, double clam, double *x, double *y)` | **Forward UTM Projection**: Converts latitude `phi` ($\phi$, decimal degrees, positive North) and longitude `lam` ($\lambda$, decimal degrees, positive East) with central meridian `clam` ($\lambda_0$, decimal degrees) into UTM Easting `*x` (meters, including $500,000\text{ m}$ false easting) and Northing `*y` (meters, including $10,000,000\text{ m}$ false northing if $\phi < 0$). |
| `utmgeo` | `void utmgeo(double *phi, double *lam, double clam, double x, double y, char hem)` | **Inverse UTM Projection**: Converts UTM Easting `x` (m) and Northing `y` (m) with central meridian `clam` ($\lambda_0$, decimal degrees) and hemisphere indicator `hem` (`'N'`/`'n'` for Northern, `'S'`/`'s'` for Southern) into latitude `*phi` and longitude `*lam` (decimal degrees) using Snyder's footpoint latitude ($\phi_1$) series expansion. |

---

## Mathematical Formulation (Snyder, 1982)

1. **Forward (`geoutm`)**:
   - Computes meridional arc distance $M(\phi) = a(m_1\phi - m_2\sin 2\phi + m_3\sin 4\phi - m_4\sin 6\phi)$, prime vertical radius of curvature $N = a/\sqrt{1 - e^2\sin^2\phi}$, $T = \tan^2\phi$, $C = e'^2\cos^2\phi$, and $A = (\lambda - \lambda_0)\cos\phi$.
   - Evaluates 5th-order series for Easting $X = x_0 + k_0 N \left[A + (1-T+C)\frac{A^3}{6} + \dots\right]$ and 6th-order series for Northing $Y = k_0\left[M + N\tan\phi\left(\frac{A^2}{2} + \dots\right)\right] (+ y_0\text{ if }\phi < 0)$.
2. **Inverse (`utmgeo`)**:
   - Removes false easting/northing ($dx = x - x_0$, $dy = y - y_0$ if Southern), computes $\mu = \frac{dy / k_0}{a m_1}$, and expands footpoint latitude $\phi_1$ up to $\sin 6\mu$.
   - Evaluates $\phi$ and $\lambda$ from $D = \frac{dx}{N_1 k_0}$ up to $D^6$ and $D^5$.

---

## Architectural Role
`utm` is called directly by [`j_proj`](j_proj.html) and [`array`](array.html) whenever an OMG grid or mosaic uses UTM (`utm_proj`) or Rotated UTM (`rotutm_proj`) coordinates.
