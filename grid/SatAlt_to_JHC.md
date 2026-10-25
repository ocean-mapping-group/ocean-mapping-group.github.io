---
layout: default
title: SatAlt_to_JHC
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: SatAlt_to_JHC
source_path: code/grid/SatAlt_to_JHC.c
category: gridding
input_formats:
- Global 2-minute satellite altimetry / bathymetry 16-bit integer grid (10800 x 6336)
output_formats:
- ASCII lat lon depth
related_tools:
- USGS_30sec_to_JHC
- ASCIItoJHC
- weigh_grid
- patchWORLD
---

# SatAlt_to_JHC

## Overview

`SatAlt_to_JHC` extracts a geographic subset from a global 16-bit integer satellite altimetry / predicted bathymetry grid (`10800` columns $\times$ `6336` rows spanning $72^\circ\text{S}$ to $72^\circ\text{N}$) and writes valid soundings (`!= -9999`) as 3-column ASCII `lat lon depth` records.

---

## Syntax & CLI Options

```bash
SatAlt_to_JHC [-maxlat <N>] [-minlat <S>] [-minlon <W>] [-maxlon <E>] <SatAlt_infile> <ASCII_outfile>
```

| Option | Description | Default |
|---|---|---|
| `<SatAlt_infile>` | **Required.** Input global 16-bit integer binary grid (`10800 x 6336` shorts). | None |
| `<ASCII_outfile>` | **Required.** Output 3-column ASCII file (`lat lon depth`). | None |
| `-maxlat <deg>` | Northern latitude bound (decimal degrees). | `72.0` |
| `-minlat <deg>` | Southern latitude bound (decimal degrees). | `-72.0` |
| `-minlon <deg>` | Western longitude bound (decimal degrees, `-180` to `+180`). | `0.0` |
| `-maxlon <deg>` | Eastern longitude bound (decimal degrees). | `360.0` |

---

## How It Works

1. Iterates through `dy = 6336` rows from North (`72.0°N`) to South (`-72.0°S`), reading `dx = 10800` 16-bit signed integers (`shortline`) per row.
2. Computes row latitude as `lat = 72.0 - i * (1.0 / 44.0)` and column longitude as `lon = j * (1.0 / 30.0)` (wrapping longitudes $> 180^\circ$ to negative West longitudes via `lon -= 360.0`).
3. For every cell within `[minlat, maxlat]` and `[minlon, maxlon]` whose value is not `-9999`, writes `lat lon depth` (`%f %f %.0f\n`) to `<ASCII_outfile>`.

---

## Examples

**Extract satellite altimetry bathymetry for the Northeast Pacific:**

```bash
SatAlt_to_JHC -minlat 30 -maxlat 60 -minlon -130 -maxlon -115 topo_global.img ne_pacific.llz
```

---

## Workflow Context

- **Downstream:** The output ASCII `lat lon depth` file can be gridded onto an OMG `.r4` mapsheet using [`weigh_grid`](weigh_grid.html) (`-xyz`) or [`ASCIItoJHC`](ASCIItoJHC.html).
- **See Also:** [`USGS_30sec_to_JHC`](USGS_30sec_to_JHC.html) and [`patchWORLD`](patchWORLD.html).
