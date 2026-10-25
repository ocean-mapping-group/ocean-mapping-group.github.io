---
layout: default
title: ssmock.f
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 21
tool_name: ssmock (mockss)
source_path: code/sidescan/mock/ssmock.f
category: Sidescan & Backscatter Modeling
input_formats:
- Bathymetric DTM (512x512 float)
- GLORIA / SeaMARC I track file
output_formats:
- Synthetic grazing-angle array (512x512 float)
related_tools:
- fullmock.f
- ssmock.for
- rrmos.f
- synthetic
---

# ssmock.f (`mockss`)

## Description
`ssmock.f` is a Fortran 77 synthetic sidescan generator (`program mockss`, John Hughes Clarke, 1989) that forward-models the true 3D seafloor grazing angle for every cell in a 512×512 bathymetric DTM illuminated along an actual SeaMARC I or GLORIA sonar track, assuming straight-line acoustic propagation (`atan(range / height)`).

## Interactive Inputs
1. **`enter bathy filename`** — 512×512 floating-point bathymetry array (`rbathy`, `recl=2048`).
2. **`enter output mock filename`** — 512×512 floating-point synthetic grazing-angle array (`rmock`, initialized to `-999.0`).
3. **`enter sidescan filename`** — Input SeaMARC I or GLORIA file containing track navigation (`rlat`, `rlon`), heading (`head`), and towfish depth (`fdepth`).
4. **`enter top lat and left long of area (degrees)`** and **`enter grid spacing of data in metres`**.
5. **`type of track?`** — `1`: SeaMARC I (`1=5km`, `2=2km`, `3=1km` swath) or `2`: GLORIA MkIII (`1=30s`, `2=20s` pulse repetition period).

## Algorithm
1. Interpolates the sonar track at half-grid-cell steps (`step = grid / 2`) between consecutive pings.
2. Casts port and starboard across-track rays out to maximum horizontal swath half-width `hmax` (`2500/1000/500 m` for SeaMARC I; `22500/15000 m` for GLORIA), tracking the minimum depression angle (`minang`) along each ray to mask acoustic shadow zones (`rmock = 0.0` in shadows).
3. For illuminated cells, calls `vectangle(ix, iy, ray, fdepth, rangle)` to compute the 3D angle between the incident vector `(range, height)` and the local seafloor surface normal derived from 4-connected depth gradients, storing `rangle` in `rmock(ix, iy)`.
4. Optionally exported to an 8-bit image via [`to8bit`](to8bit.html).
