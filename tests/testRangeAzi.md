---
layout: default
title: testRangeAzi
parent: tests (Test, Simulation & Diagnostic Suite)
nav_order: 22
tool_name: testRangeAzi
source_path: code/tests/testRangeAzi.c
category: Attitude Error & Geometry Plotting (tests)
input_formats:
  - Interactive stdin prompts (lat/lon format choice, starting coordinates, radial distance in m, azimuth in deg)
output_formats:
  - Projected geographic coordinates on stdout (decimal degrees and degrees/decimal minutes)
related_tools:
  - testrot
  - checkBounds
  - getBounds
---

# testRangeAzi

## Overview
`testRangeAzi` (`code/tests/testRangeAzi.c`, authored by John Hughes Clarke in August 1998) is an interactive command-line geodetic dead-reckoning calculator. Given a starting geographic coordinate (entered either as decimal degrees or as integer degrees + decimal minutes) and a polar offset consisting of radial distance $R$ (in meters) and azimuth $\alpha$ (in degrees clockwise from True North, $0^\circ\text{–}360^\circ$), it computes and prints the target latitude and longitude in both decimal degrees (`DD.DDDDDD`) and degrees + decimal minutes (`DD MM.MMMM`).

It runs in a continuous interactive loop (`goto again;`) so hydrographers can quickly project sonar target offsets, layback vectors, or mooring drop positions during survey operations.

---

## Syntax & CLI Options

```bash
testRangeAzi [-v] [-depth <m>]
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `-v` | Increment verbose flag (`verbose_flag++`). | `0` |
| `-depth <m>` | Optional integer depth parameter parsed via `strtoint()` (retained from template CLI). | `100.0` |

---

## Interactive Prompts & Local Tangent-Plane Equations

### 1. Input Coordinate Format Selection
At each iteration, `testRangeAzi` prompts:
```text
 do you want to enter lat lon as:
 --- decimal_lat decimal_lon      (1) (43.23534 -63.435346)
 --- latdeg latmin londeg lonmin  (2) (43 34.22 -63 -43.22)
```
* **Option `1`:** Reads two doubles `lat` and `lon` in decimal degrees.
* **Option `2`:** Reads `latdeg`, `latmin`, `londeg`, `lonmin` and converts to decimal degrees via:
  $$\phi_0 = \text{latdeg} + \frac{\text{latmin}}{60.0}, \qquad \lambda_0 = \text{londeg} + \frac{\text{lonmin}}{60.0}$$
  *(Note: For negative western longitudes or southern latitudes in Option `2`, both `londeg` and `lonmin` must be entered with a negative sign, e.g., `-63 -43.22`, because they are summed directly).*

### 2. Polar-to-Cartesian Offset & Spherical Conversion
Next, the user enters `raddist` ($R$ in meters) and `azi` ($\alpha$ in degrees). The North ($\Delta N$) and East ($\Delta E$) metric offsets are:

$$\Delta N = R \cos\!\left(\alpha \frac{\pi}{180}\right), \qquad \Delta E = R \sin\!\left(\alpha \frac{\pi}{180}\right)$$

Using a standard nautical mile of $1853.0\text{ m}$ ($1^\circ\text{ latitude} = 60 \times 1853.0 = 111,180\text{ m}$), the angular increments (`dlat`, `dlon`) are computed in `testRangeAzi.c` (lines 139–144) as:

$$\Delta\phi = \frac{\Delta N}{1853.0 \times 60.0}, \qquad \Delta\lambda = \frac{\Delta E}{1853.0 \times 60.0} \cos\!\left(\phi_0 \frac{\pi}{180}\right)$$

$$\phi_1 = \phi_0 + \Delta\phi, \qquad \lambda_1 = \lambda_0 + \Delta\lambda$$

*(Implementation note: Line 141 multiplies `dlon` by `cos(lat)` rather than dividing by `cos(lat)`; at mid/high latitudes, true meridian convergence requires dividing the eastward linear distance by $\cos\phi_0$).*

---

## Example Interactive Session

```text
$ testRangeAzi
 do you want to enter lat lon as:
 --- decimal_lat decimal_lon      (1) (43.23534 -63.435346)
 --- latdeg latmin londeg lonmin  (2) (43 34.22 -63 -43.22)
1
 well enter it then...:
45.000000 -66.000000
 using 45.000000 -66.000000

enter the radial distance (m) and the azimuth (0-360)
1000.0 45.0
shifting 707.106781m to north and 707.106781 m to east

 you should be at:  45.006360 -65.995504 (45 0.381601 -65 -59.730268)
```
