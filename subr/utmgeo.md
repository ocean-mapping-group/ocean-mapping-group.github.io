---
layout: default
title: utmgeo
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/utmgeo.c
category: Map Projections, Ellipsoids & Geodesy
related_tools:
- utm
- geoutm
- j_proj
- geographic
module_name: utmgeo
---

# utmgeo

## Overview
`utmgeo` (`utmgeo.c`) is the standalone K&R C implementation of the **inverse Universal Transverse Mercator (UTM) projection** (`utmgeo()`), converting UTM grid Easting (`x`) and Northing (`y`) in meters back into geographic latitude (`*phi`) and longitude (`*lam`) in decimal degrees.

Written by A. Malinverno (March 3, 1986) from J.P. Snyder's *Map projections used by the U.S.G.S.* (USGS Bulletin 1532, p. 68, 1982), `utmgeo.c` is the companion to [`geoutm.c`](geoutm.html). Note that both `geoutm()` and `utmgeo()` are also consolidated with ANSI C prototypes in [`utm.c` / `utm.h`](utm.html).

---

## Dependencies & Global State

`utmgeo.c` includes `wgs.h` and `j_phi.h` and reads the global `extern int Ellipsoid` variable (`wgs.h`) to select the reference ellipsoid parameters ($a$ and $e^2$):
- `WGS84` (`1`): $a = 6378137.0\text{ m}$, $e = 0.0818191908417579$
- `NAD27` (`2`): $a = 6378206.4\text{ m}$, $e = 0.082271854$
- `CLK66` (`3`): $a = 6378206.4\text{ m}$, $e = 0.082271684$
- `AGD84` (`4`): $a = 6378160.0\text{ m}$, $e = 0.08182018$
- `SPHER` (`5`): $a = 6378137.0\text{ m}$, $e = 0.0$

If `Ellipsoid` does not match one of these five constants, `utmgeo()` prints `"invalid Elliposid it UTM conversion\n"` and terminates via `exit(-1)`.

---

## Public Function

### `utmgeo`

```c
void utmgeo(double *phi, double *lam, double clam, double x, double y, char hem);
```

| Parameter | Type | Direction | Description |
|---|---|---|---|
| `phi` | `double *` | Out | Output geographic latitude ($\phi$) in decimal degrees (positive North, negative South). |
| `lam` | `double *` | Out | Output geographic longitude ($\lambda$) in decimal degrees (positive East, negative West). |
| `clam` | `double` | In | Central meridian ($\lambda_0$) of the UTM zone in decimal degrees (e.g., `-63.0` for UTM Zone 20W). |
| `x` | `double` | In | UTM Easting in meters (standard false easting $x_0 = 500,000.0\text{ m}$ is subtracted internally). |
| `y` | `double` | In | UTM Northing in meters (if `hem` is `'s'` or `'S'`, southern hemisphere false northing $y_0 = 10,000,000.0\text{ m}$ is subtracted internally). |
| `hem` | `char` | In | Hemisphere flag: `'n'` or `'N'` for Northern Hemisphere; `'s'` or `'S'` for Southern Hemisphere. |

---

## Algorithm Summary
1. Subtracts false easting $dx = x - 500000.0$ and, if `hem == 's' || hem == 'S'`, subtracts false northing $dy = y - 10000000.0$.
2. Computes meridional distance $M = dy / k_0$ ($k_0 = 0.9996$) and rectifying latitude $\mu = \frac{M}{a(1 - e^2/4 - 3e^4/64 - 5e^6/256)}$.
3. Computes the footpoint latitude $\phi_1$ via the $e_1 = \frac{1-\sqrt{1-e^2}}{1+\sqrt{1-e^2}}$ trigonometric series up to $\sin(6\mu)$.
4. Evaluates radius of curvature in the prime vertical $N_1 = \frac{a}{\sqrt{1 - e^2\sin^2\phi_1}}$ and in the meridian $R_1 = \frac{a(1-e^2)}{(1 - e^2\sin^2\phi_1)^{3/2}}$, and expands $\phi$ (to $D^6$) and $\lambda$ (to $D^5$) around $\phi_1$ and `clam`.

---

## Architectural Role
`utmgeo.c` (or its consolidated counterpart [`utm.c`](utm.html)) provides inverse UTM coordinate conversion for [`j_proj`](j_proj.html) and older standalone projection utilities.
