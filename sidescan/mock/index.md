---
layout: default
title: Mock Tools
parent: Sidescan Tools
nav_order: 7
has_children: true
---

# Synthetic Sidescan & Backscatter Modeling Tools (`sidescan/mock`)

The `mock` directory (`code/sidescan/mock/`) contains C and Fortran 77 tools developed by John Hughes Clarke for forward-modeling synthetic sidescan sonar imagery over 3D gridded bathymetry (DTMs), simulating acoustic transducer beam patterns and Time-Varying Gain (TVG) curves, and extracting empirical angular backscatter response curves ($\text{dB}$ vs. true grazing angle) by co-registering sidescan passes with multibeam bathymetry.

## Tool Categories

### 1. Synthetic Sidescan Forward Modeling
* **[`synthetic`](synthetic.md)** — Generates synthetic GLORIA sidescan records over a bathymetric grid using 3D seafloor facet normals and ray-traced or flat-earth grazing angles.
* **[`fullmock.f`](fullmock.f.md)** — Fortran 77 forward model (`mockss`) that combines a ray-traced grazing-angle lookup table (`grazearray(175,750)`), a 512×512 bathymetric DTM, and actual GLORIA/SeaMARC I ship track geometry to compute true local grazing angles (`vectangle`) and synthetic sidescan imagery.
* **[`ssmock.f`](ssmock.f.md)** & **[`ssmock.for`](ssmock.for.md)** — Unix and VAX/VMS Fortran 77 synthetic sidescan generators (`mockss`) using straight-line ray geometry over a 512×512 bathymetric grid for SeaMARC I (5/2/1 km) or GLORIA MkIII (30/20 s) tracks.
* **[`rrmos.f`](rrmos.f.md)** — Fortran 77 3D translocation mosaicker (`mosaic`) that projects GLORIA scanlines onto a 3D bathymetric surface using a ray-traced travel-time table (`timearray(175,750)`).
* **[`to8bit`](to8bit.md)** — C-shell helper script converting floating-point synthetic backscatter arrays into 8-bit XFB raster images.

### 2. Angular Backscatter Extraction & Characterization
* **[`build_back`](build_back.md)** & **[`build_back_mos`](build_back_mos.md)** — Co-registers sidescan scanlines with a bathymetric DTM to calculate true 3D seafloor incidence/grazing angles and compile backscatter vs. grazing-angle tables and mosaics.
* **[`back_char`](back_char.md)** & **[`back_stack`](back_stack.md)** — Characterizes and stacks empirical backscatter intensity vs. grazing-angle curves across geological provinces.
* **[`selective_back`](selective_back.md)** — Extracts angular backscatter curves from user-selected geographic polygons or acoustic facies.
* **[`view_sel`](view_sel.md)** & **[`view_sel.c_10`](view_sel.c_10.md)** — Interactive X11 viewer for inspecting angular backscatter response curves selected via `selective_back`.

### 3. Transducer Array, Beam Directivity & TVG Simulation
* **[`beams`](beams.md)** & **[`oldbeams`](oldbeams.md)** — Simulates GLORIA transducer array vertical directivity patterns and grazing-angle sensitivity.
* **[`modarray`](modarray.md)** & **[`modbeam`](modbeam.md)** — Models multi-row acoustic transducer phased-array beam patterns and steering angles.
* **[`showgains`](showgains.md)** & **[`doshow`](doshow.md)** — Computes and plots Time-Varying Gain (TVG), spreading/attenuation loss, and beam directivity curves at a specified water depth.
* **[`test_tvg_effect`](test_tvg_effect.md)** & **[`test_tvg_dirindex`](test_tvg_dirindex.md)** — Evaluates residual radiometric errors caused by TVG depth mismatches and transducer directivity index variations.
* **[`testbell`](testbell.md)**, **[`offtrack`](offtrack.md)** & **[`binplot`](binplot.md)** — Utilities for testing bell-shaped angular response curves, off-track beam geometry, and binned scatter plots.
* **[`makefile`](makefile.md)** — Build configuration for all C and X11 targets in `code/sidescan/mock/`.
