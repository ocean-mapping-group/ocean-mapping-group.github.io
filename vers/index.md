---
layout: default
title: Version Control & Build Stamps (vers)
parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 14
has_children: true
---

# Cartographic & Large-Format Map Plotting (`vers`)

The `vers` directory contains large-format cartographic map composition and plotting utilities originally designed for 36-inch (86 cm) wide Versatec electrostatic/drum plotters and HP-GL/PostScript large-format printers.

---

## Tools in `vers/`

* [`lineplot`](lineplot.html) — Cartographic vector map generator that constructs projected graticules (Mercator, UTM, Rotated Mercator, Rotated UTM, Lambert Conformal Conic) from an OMG `JHC_header` mapsheet and overlays ship navigation tracks (`.nav`), current vectors, soundings, targets, bounding boxes, and binary/ASCII vector contours into `plot.meta`.
* [`scaleimage`](scaleimage.html) — Interactive X11 raster-plus-vector map layout editor ("Versatec Plotting Editor") that scales 8-bit OMG raster grids (`.sun`, `.8bit`, `.mos`) to true cartographic scale, overlays vector contours and labels, and provides draggable legend widgets (depth colorbar, 3D sun-illumination rose, title block, and custom logo).
