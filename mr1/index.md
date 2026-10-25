---
layout: default
title: MR1 Tools
has_children: true
nav_order: 15
---

# MR1 Tools

Tools in the `mr1/` directory process raw phase-differencing sidescan and bathymetry data collected by the Hawaii Institute of Geophysics **HAWAII MR1** towed swath mapping system (originally developed aboard R/V *Moana Wave* cruise MW9204 in the Western Solomon Sea), converting raw complex quadrature packets into OMG MR1 sidescan (`.raw_ss`, `.slr_ss`), phase bathymetry (`.dep_zx`), and Sun raster images.

## Tool Summary

| Tool | Source | Description |
| :--- | :--- | :--- |
| [combineMW](combineMW) | `mr1/combineMW.c` | Merges R/V *Moana Wave* fixed-width ASCII navigation and depth files into a single `lat lon depth` ASCII table. |
| [edbathy](edbathy) | `mr1/edbathy.c` | Interactive X11 graphical editor for adjusting phase-to-angle look-up tables (LUTs) and flagging bad beams in MR1 `.dep_zx` and `.slr_mer` files. |
| [graph_noise](graph_noise) | `mr1/graph_noise.c` | Converts binary stacked MR1 noise float arrays into ASCII plot files or port/starboard amplitude tables. |
| [jhc2SUN](jhc2SUN) | `mr1/jhc2SUN.c` | Converts an 8-bit `JHC_header` grid/image file into a standard Sun Rasterfile (`RAS_MAGIC`). |
| [mergeMWascii](mergeMWascii) | `mr1/mergeMWascii.c` | Merges R/V *Moana Wave* ASCII navigation, speed/azimuth, and depth files onto OMG MR1 `.slr_ss` sidescan records with towfish layback lag. |
| [mr1_noise](mr1_noise) | `mr1/mr1_noise.c` | X11/CLI analyzer that stacks raw HAWAII MR1 receive packets (with transmitters off) to characterize array phase and amplitude noise. |
| [mr1_proc](mr1_proc) | `mr1/mr1_proc.c` | Core signal-processing library routines for unpacking MR1 quadrature packets, detecting 90° phase inversions, decimating phase/amplitude, and slant-range correcting imagery. |
| [mr1_raw](mr1_raw) | `mr1/mr1_raw.c` | Low-level mathematical and header routines for MR1 complex phase lag, cross-correlation, spherical spreading/absorption TVG, and exponent tables. |
| [plotmr1](plotmr1) | `mr1/plotmr1.c` | Interactive X11 and batch converter that unpacks raw HAWAII MR1 files into `.raw_ss`, `.slr_ss`, and `.dep_zx` files. |
| [subsetAscii](subsetAscii) | `mr1/subsetAscii.c` | Filters an ASCII `lat lon depth` track file to a geographic bounding box (`-area`), inserting `9999.0 -9999.0 9999.0` line-break markers when the track exits and re-enters. |
| [swapascii](swapascii) | `mr1/swapascii.c` | Reverses the line order of an ASCII `lat lon depth` file from last record to first record. |
