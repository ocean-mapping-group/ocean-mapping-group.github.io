---
layout: default
title: ssmock.for
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 22
tool_name: ssmock.for (VAX/VMS mockss)
source_path: code/sidescan/mock/ssmock.for
category: Sidescan & Backscatter Modeling
input_formats:
- URI RR R*4 Bathymetric DTM (512x512 + 50-float header)
- VAX 256-longword SeaMARC I / GLORIA track file
output_formats:
- Synthetic grazing-angle array (512x512 float)
related_tools:
- ssmock.f
- fullmock.f
- rrmos.f
---

# ssmock.for

## Description
`ssmock.for` is the VAX/VMS Fortran 77 implementation of [`ssmock.f`](ssmock.f.html) (`program mockss`, written by John Hughes Clarke, 1989) adapted for URI Graduate School of Oceanography `RR` (`Dpict`) `R*4` bathymetry grids and VAX 256-longword (`recl=256`) unformatted sidescan records.

## Key Differences from Unix `ssmock.f`
1. **RR `R*4` Grid Loader (`subroutine loadrrr4`)**:
   * Reads a sequential unformatted file beginning with a 50-float header (`head(50)`), followed by 512 rows stored bottom-to-top (`j = 512, 1, -1`) to invert the upside-down `Dpict` coordinate convention into top-down row order (`rbathy(1..512, 1..512)`).
   * Prompts the user for the flag value used for unknown data (e.g., `99999.0`) and replaces flagged cells with `-999.0`.
2. **VAX Record Length Units**:
   * Opens unformatted direct-access files with `recl=256` (256 four-byte longwords = 1024 bytes) for sidescan input and `recl=512` (512 floats = 2048 bytes) for `rmock` output.
3. **3D Facet Grazing Angle (`subroutine vectangle`)**:
   * Identical mathematical formulation to [`ssmock.f`](ssmock.f.html), computing the true grazing angle `90° - acos((a² + b² - c²) / (2ab))` between the incident sonar ray and the local 3D seabed normal vector.
