---
layout: default
title: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 7
has_children: true
---

# 2. Gridding, Mosaicking & Interactive Editors

Weighted bathymetric gridding (.r4), artificial sun-illumination (.sun), range-buffered sidescan mosaicking (.mos), interactive 6-panel swath editing (swathed), 3D visualization (jview), and GIS exports.

---

## Directory Modules in This Category

| Module | Directory | Purpose & Key Tools |
| :--- | :--- | :--- |
| **[Bathymetric Gridding & Export (grid)](../grid/)** | `grid/` | Distance-weighted bathymetric gridding (`weigh_grid`), sun-illuminated hillshading (`meds_sun`), slope/roughness derivatives, and GIS exports (`r4toESRI`, `r4toTIFF`, `ASCII2r4`). |
| **[Sidescan Mosaicking (newmos)](../newmos/)** | `newmos/` | Range-buffered backscatter mosaicking (`mos2`, `comboMOS`) and raster coordinate projection (`rasterCoords`). |
| **[Swath Editor — swathed (SE)](../SE/)** | `SE/` | Interactive 6-panel X11/Motif multibeam sounding editor, patch test calibrator (`CALWIN`), refraction sliders (`REFTOOL`), and water-column viewer. |
| **[2D/3D Interactive Viewer — jview (JV)](../JV/)** | `JV/` | Interactive OpenGL/X11 raster and 3D surface viewer (`jview`) with SVP editor, 2D FFT filtering, and acoustic `.wav` playback. |
| **[Latency & Delay Editor (DE)](../DE/)** | `DE/` | Interactive roll, pitch, heave, and positioning time-delay calibration tool (`DelayEditor`). |
| **[Raster Image Processing (image)](../image/)** | `image/` | 8-bit (`OMG1`) raster manipulation, header editing (`edhead`, `addheader`), histogram equalization, and TIFF/PGM/SUN rasters. |
| **[PostScript & Vector Plotting (plot)](../plot/)** | `plot/` | Publication-quality PostScript map frames, trackline plots (`plot_track`), colorbars, and contour generators. |
| **[Bathymetric & Backscatter Colormaps (cmaps)](../cmaps/)** | `cmaps/` | Lookup table (`.lut` / `.cmap`) generators and converters for `jview`, `meds_sun`, and `swathed`. |
| **[OpenGL 3D Visualization (gl)](../gl/)** | `gl/` | Interactive 3D OpenGL terrain fly-through, point cloud, and lighting utilities. |
| **[OpenGL 3D Seismic & Curtain Viewer (glseis)](../glseis/)** | `glseis/` | 3D OpenGL viewer combining multibeam bathymetry grids with vertical sub-bottom seismic curtains. |
| **[3D Beam Pattern Visualizer (bpdemo)](../bpdemo/)** | `bpdemo/` | Interactive Motif/OpenGL 3D acoustic transducer array beam-forming and side-lobe simulator (`BPdemo`). |
