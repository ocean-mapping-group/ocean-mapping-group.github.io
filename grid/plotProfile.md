---
layout: default
title: plotProfile
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: plotProfile
source_path: code/grid/plotProfile.c
category: gridding
input_formats:
- .r4 (JHC 32-bit float grid)
- .8bit (JHC 8-bit unsigned char grid)
output_formats:
- .meta (OMG plotlib vector metafile)
- plot.list (ASCII distance vs. value listing)
related_tools:
- extractProfile
- extractNodeProf
- makeStrat
---

# plotProfile

## Overview

`plotProfile` extracts a cross-sectional profile along a straight line between two pixel coordinates (`-start <sx> <sy>` and `-end <ex> <ey>`) from either a 32-bit floating-point (`.r4`) or 8-bit (`.8bit`) `JHC_header` grid. It outputs both a framed, grid-lined vector plot (`plot.meta` by default, or `-outfile <file.meta>`) and a 2-column ASCII listing (`plot.list` containing `distance_m value`).

---

## Syntax & CLI Options

```bash
plotProfile [OPTIONS] -start <sx> <sy> -end <ex> <ey> [-outfile <file.meta>] <infile>
```

| Option | Description | Default |
|---|---|---|
| `<infile>` | **Required.** Input `JHC_header` `.r4` (`data_type == 3`) or `.8bit` (`data_type == 1`) grid file. | None |
| `-start <sx> <sy>` | **Required.** Starting pixel coordinates (`X`, `Y`) of the profile line. | None |
| `-end <ex> <ey>` | **Required.** Ending pixel coordinates (`X`, `Y`) of the profile line. | None |
| `-yrange <Ymin> <Ymax>` | Vertical axis range (depth or digital number) for the output plot. | `-60.0 0.0` |
| `-point` | Plot discrete crosshair symbols at each sampled pixel along the profile instead of a continuous connected polyline. | Disabled (connected polyline) |
| `-outfile <filename>` | Output `plotlib` metafile filename. | `plot.meta` |
| `-v` | Enable verbose flag. | Disabled |

---

## How It Works

1. **Plot Frame & Grid Lines:** Opens an $18 \times 10$ unit `plotlib` canvas (`plot.meta`) and draws labeled vertical distance grid lines every `1000 m` and horizontal depth/value grid lines every `50` units across `[Ymin, Ymax]`.
2. **Bresenham/Linear Ray Stepping:**
   - Computes `x_range = |start_x - end_x|`, `y_range = |start_y - end_y|`, and total metric length `distance = sqrt(x_range^2 + y_range^2) * JHChead.xstep`.
   - Steps pixel-by-pixel along the dominant axis (`X` if `x_range > y_range`, else `Y`), seeking directly to byte offset `1024 + 4*(Xpos + Ypos*Dx)` (for `.r4`) or `1024 + (Xpos + Ypos*Dx)` (for `.8bit`).
3. **Output Generation:** For every sampled point whose `(xpos, ypos)` falls inside the plot box, writes `xval yval` (metric distance and grid value) to `plot.list` and draws either a line segment or crosshair (`-point`) in the `plotlib` metafile.

---

## Examples

**Extract and plot a bathymetric cross-section between pixel `(100, 250)` and `(850, 600)`:**

```bash
plotProfile -yrange -120 -10 -start 100 250 -end 850 600 -outfile canyon_prof.meta canyon.r4
# Also writes 2-column ASCII profile to plot.list
```

---

## Workflow Context

- **See Also:** [`extractProfile`](extractProfile.html) and [`extractNodeProf`](extractNodeProf.html) for non-graphical profile extraction, and [`locate_fix`](locate_fix.html) to convert geographic `(lat, lon)` endpoints into pixel `(sx, sy)` coordinates.
