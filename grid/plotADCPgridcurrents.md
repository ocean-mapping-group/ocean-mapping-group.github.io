---
layout: default
title: plotADCPgridcurrents
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: plotADCPgridcurrents
source_path: code/grid/plotADCPgridcurrents.c
category: gridding
input_formats:
- .r4 (JHC 32-bit float ADCP tangential velocity section grid)
output_formats:
- .meta (OMG plotlib vector metafile)
related_tools:
- convertSectionUVtoRadTan
- extractVertSection
- plotProfile
---

# plotADCPgridcurrents

## Overview

`plotADCPgridcurrents` reads a 2D 32-bit floating-point (`.r4`) vertical section grid of ADCP current velocities (such as tangential velocity produced by [`convertSectionUVtoRadTan`](convertSectionUVtoRadTan.html)), block-averages the velocities over configurable along-section distance (`-distAv`) and depth (`-depthAv`) bins, and renders a stick/vector profile plot in OMG `plotlib` metafile format (`plot.meta` by default).

---

## Syntax & CLI Options

```bash
plotADCPgridcurrents [OPTIONS] -infile <vel_section.r4> [-outfile <plot.meta>]
```

| Option | Description | Default |
|---|---|---|
| `-infile <filename>` | **Required.** Input 32-bit float (`.r4`) ADCP velocity section grid (`data_type == 3`). | None |
| `-outfile <filename>` | Output `plotlib` vector metafile name. | `plot.meta` |
| `-distAv <meters>` | Along-track horizontal averaging interval in meters (`AvDistanceBins = distAv / JHChead.ystep`). | `50.0` |
| `-depthAv <meters>` | Vertical depth averaging interval in meters (`AvDepthBins = depthAv / JHChead.xstep`). | `2.0` |
| `-maxvel <m/s>` | Reference maximum velocity scale in m/s (`maxvel`). | `1.0` |
| `-point` | Sets internal `point_flag`. | Disabled |
| `-v` | Enable verbose output. | Disabled |

---

## How It Works

1. **Grid Orientation & Aspect Ratio:** Reads `JHChead` from `-infile` (where `dy` represents binned pings along distance `ymin..ymax` with step `ystep`, and `dx` represents vertical depth bins `xmin..xmax` with step `xstep`). Scales the plot frame (`20 cm` along the longer axis) to preserve the grid's aspect ratio.
2. **2D Block Averaging:**
   - Steps through the along-section rows by `AvDistanceBins = distAv / ystep`, averaging all non-zero velocity samples in each depth column into `dist_fbuf`.
   - Steps through depth bins by `AvDepthBins = depthAv / xstep`, averaging non-zero values in `dist_fbuf` to obtain the bin-averaged velocity `current`.
3. **Vector Plotting:** At each bin center `(xpos, ypos)`, draws a horizontal velocity vector line from `(xpos, ypos)` to `(xpos + current, ypos)` and closes the `plotlib` metafile.

---

## Examples

**Average an ADCP tangential velocity section into 50 m horizontal by 3 m vertical bins and plot:**

```bash
plotADCPgridcurrents -distAv 50 -depthAv 3 -maxvel 1.5 -infile adcp_tang.r4 -outfile adcp_sticks.meta
```

---

## Workflow Context

- **Upstream:** [`extractVertSection`](extractVertSection.html) and [`convertSectionUVtoRadTan`](convertSectionUVtoRadTan.html).
