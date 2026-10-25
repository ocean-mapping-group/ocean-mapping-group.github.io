---
layout: default
title: r4interp
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: r4interp
source_path: code/grid/r4interp.c
category: gridding
input_formats:
- .r4 (JHC 32-bit float grid)
output_formats:
- .r4 (JHC 32-bit float grid)
related_tools:
- fillGap
- r4filter
- interp
- weigh_grid
---

# r4interp

## Overview

`r4interp` (`code/grid/r4interp.c`) is an incomplete legacy prototype intended to interpolate across sparse gaps in a 32-bit floating-point (`.r4`) array within a circular search radius (`-radius <pixels>`).

> **Note:** In the source repository (`code/grid/r4interp.c`), the inner interpolation loop (`lines 97–102`) is an empty stub and contains uncompiled syntax typos (`flaot radialrange[20][20];`). For production gap interpolation on `.r4` grids, use [`fillGap`](fillGap.html), [`r4filter`](r4filter.html) (`-low`), or [`surface`](surface.html).

---

## Syntax & CLI Options

```bash
r4interp -radius <pixels> <floatfile> <interpfile>
```

| Option | Description | Default |
|---|---|---|
| `-radius <pixels>` | Search radius in pixels (`radius`). | Uninitialized unless specified |
| `<floatfile>` | **Required.** Input `.r4` float grid file. | None |
| `<interpfile>` | **Required.** Output `.r4` float grid file. | None |

---

## How It Works

1. Opens `<floatfile>` and `<interpfile>`, reads `JHChead`, and writes the header to `<interpfile>`.
2. Allocates a sliding strip buffer of height `2 * radius` (`dx * radius * 2` floats) and copies the leading `radius` rows, but the inner `(i, j)` loop body is unimplemented.

---

## Examples

**Recommended production alternatives for `.r4` grid interpolation:**

```bash
# Use fillGap to interpolate empty (0.0) pixels in an .r4 grid:
fillGap -in sparse_grid.r4 -out filled_grid.r4

# Or use r4filter -low to average across small gaps:
r4filter -xbox 5 -ybox 5 -low sparse_grid.r4 smoothed_grid.r4
```

---

## Workflow Context

- Superseded by [`fillGap`](fillGap.html) and [`surface`](surface.html).
