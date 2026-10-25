---
layout: default
title: fullmock.f
parent: Mock Tools
grand_parent: Sidescan Tools
nav_order: 19
tool_name: fullmock (mockss)
source_path: code/sidescan/mock/fullmock.f
category: Sidescan & Backscatter Modeling
input_formats: ["Ray-traced grazing angle table (175x750)", "Bathymetric DTM (512x512 float)", "GLORIA / SeaMARC I track file"]
output_formats: ["Synthetic grazing-angle difference array (512x512 float)"]
related_tools: ["ssmock.f", "rrmos.f", "synthetic"]
---

# fullmock.f (`mockss`)

## Description
`fullmock.f` is a Fortran 77 synthetic sidescan forward-modeling program (`program mockss`, written by John Hughes Clarke, 1989) that improves upon flat-earth straight-line ray geometry ([`ssmock.f`](ssmock.f.md)) by incorporating a pre-computed 2D ray-traced grazing-angle lookup table (`grazearray(175, 750)`) alongside a 512×512 bathymetric Digital Terrain Model (`rbathy`) and an actual SeaMARC I or GLORIA ship track file.

## Interactive Inputs
When executed, `fullmock` prompts for:
1. **`enter grazing-angle array filename`** — Binary file (`recl=700`) containing 750 horizontal range rows (`20 m` step) by 175 depth columns (`20 m` step) of ray-traced flat-bottom grazing angles.
2. **`enter bathy filename`** — 512×512 floating-point bathymetry grid (`rbathy`, `recl=2048`).
3. **`enter output mock filename`** — Output 512×512 floating-point synthetic sidescan array (`rmock`, initialized to `-999.0`).
4. **`enter sidescan filename`** — Input GLORIA or SeaMARC I file providing ship track coordinates (`rlat`, `rlon`), heading (`head`), and fish depth (`fdepth`).
5. **`enter top lat and left long of area (degrees)`** and **`enter grid spacing of data in metres`**.
6. **`type of track?`** — SeaMARC I (`5 km`, `2 km`, or `1 km` swath) or GLORIA MkIII (`30 s` or `20 s` pulse period).

## Algorithm
1. Steps along the ship track at half-grid-cell intervals, projecting across-track rays on both port (`head - π/2`) and starboard (`head + π/2`) out to maximum swath range (`hmax`).
2. At each grid cell `(ix, iy)`, looks up the ray-traced flat-bottom grazing angle `graze` from `grazearray(idepth, irange)` using height above seafloor (`height = rbathy(ix,iy) - fdepth`) and horizontal range.
3. Calls `bangle(ix, iy, ray, tslope)` to compute the local 3D seafloor slope component along the look azimuth (`vectangle` using 3×3 neighboring depth facets), and stores `rmock(ix, iy) = graze - tslope`.
