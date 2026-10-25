---
layout: default
title: lineplot
parent: Version Control & Build Stamps (vers)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
tool_name: lineplot
source_path: code/vers/lineplot.c
category: Cartographic & Map Plotting
related_tools:
- scaleimage
- viewmeta
- hpgl
- jview
- make_blank
---

# lineplot

## Overview
`lineplot` (`code/vers/lineplot.c`, written by John E. Hughes Clarke, March 1993) is the Ocean Mapping Group's cartographic vector map plotter. It reads geographic bounds and projection parameters from an OMG `JHC_header` mapsheet (`-area <mapfile>`) or interactive user input, constructs properly projected map frames (Mercator, UTM, Rotated Mercator, Rotated UTM, Lambert Conformal Conic, or linear XY), and overlays ship navigation tracks (`.nav`), soundings, current vectors, acoustic targets, bounding boxes, MVP cast locations, angular response strips, and text annotations into a `plotlib` vector metafile (`plot.meta`).

---

## Usage

```bash
lineplot -area <jhc_mapfile> [OPTIONS]
```

*(Note: After parsing command-line arguments, `lineplot` prompts interactively on `stdin` for the map scale—and projection latitude if Mercator—unless `-linear <xcm> <ycm>` is specified.)*

---

## Command-Line Options

### Map Area, Projection & Graticule Options

| Option | Description |
|---|---|
| `-area <jhcarrayfile>` | **Recommended.** Read map bounds, ellipsoid, and projection (`Mercator`, `UTM`, `RotUTM`, `RotMerc`, `Lambert`) from an existing OMG array/grid header (`JHC_header`). |
| `-linear <xcm> <ycm>` | Plot in linear Cartesian coordinates with explicit page width `<xcm>` and height `<ycm>` in centimeters. |
| `-grid <label_step> <tick_step>` | Set graticule label and tick intervals (in arc-minutes for geographic projections, or meters for UTM projections). Default: `15` label, `5` tick. |
| `-utmgrid <meridian> <label_m> <tick_m>` | Overlay a secondary UTM meter grid (using central `<meridian>`) onto a Rotated Mercator map frame. |
| `-geogrid <label_min> <tick_min>` | Overlay a secondary geographic latitude/longitude graticule onto a Rotated UTM map frame. |
| `-scalebar <length> <step>` | Draw a cartographic scale bar of `<length>` meters subdivided by `<step>` meters. |
| `-noborder` | Suppress the outer map border frame. |
| `-nogridlabels` / `-notitlelabels` / `-nolabellabels` / `-nocontlabels` | Suppress specific text label layers. |
| `-tit1 "<title1>"` / `-tit2 "<title2>"` | Set primary and secondary map title strings (defaults to `header.label_1`). |
| `-small <factor>` | Scale down widget and annotation sizes by `<factor>`. |

### Navigation, Vector & Feature Overlays

| Option | Description |
|---|---|
| `-nav <navfile> <color>` | Plot a single binary JCU navigation file (`.nav`) using pen `<color>`. Can be specified multiple times. |
| `-navlist <nav1> [nav2 ...]` | Plot a list of binary `.nav` files cycling automatically through pen colors `0..5`. |
| `-navlabels` | Annotate the start/end of each plotted `.nav` line with its filename. |
| `-navtimelabels <interval_sec>` | Plot time-tick marks and timestamps along `.nav` tracks every `<interval_sec>` seconds. |
| `-fix_size <cm>` | Size of navigation fix symbols in centimeters (`0.0` = point, default `0.1` cm). |
| `-pencol <n>` | Override navigation pen color with `<n>`. |
| `-currents` / `-currskip <n>` | Treat `.nav` velocity/azimuth fields as current vectors and plot arrow vectors every `<n>` records. |
| `-soundings` | Plot point soundings along the navigation track. |
| `-vector <file> <color>` | Overlay an ASCII vector polyline/contour file in pen `<color>`. |
| `-vectbin <file> <linecol> <labelcol>` | Overlay a binary vector contour file (`bin_vect`) with line color `<linecol>` and contour label color `<labelcol>`. |
| `-maxvector <meters>` | Break vector line segments exceeding `<meters>` length to prevent spurious cross-map lines. |
| `-box <file> <color>` | Plot bounding box outlines from `<file>` in pen `<color>` (with `-boxhead` or `-boxnumber` for annotations). |
| `-targets <file> <color>` | Plot point targets (`lat lon label`) from `<file>` in pen `<color>` (up to 10 target files). |
| `-label <file> <color>` | Plot positioned ASCII text labels from `<file>` in pen `<color>`. |
| `-AR <file>` | Overlay seafloor angular response (`j_ang_resp`)roses/diagrams along the survey track. |
| `-MVP <file>` | Plot Moving Vessel Profiler (MVP) cast locations. |
| `-v` | Enable verbose diagnostic output. |

---

## Output
Generates `plot.meta` in the current working directory, which can be viewed interactively with [`viewmeta`](../plotlib/viewmeta.html) or converted to PostScript/HP-GL via [`hpgl`](../plotlib/hpgl.html).
