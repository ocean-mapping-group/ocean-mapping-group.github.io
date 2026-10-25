---
layout: default
title: glseis Tools
has_children: true
nav_order: 10
---

# 3D OpenGL Sub-Bottom & Water-Column Seismic Viewer (`glseis`)

The `glseis` directory contains **`glSeis`**, an interactive 3D OpenGL/GLX visualization tool for rendering georeferenced sub-bottom seismic reflection profiles, chirp traces, and multibeam water-column curtains in 3D geographic space alongside Digital Terrain Models.

---

## Main Executable & Subsystems

* [`glSeis`](glSeis.md) — Main application entry point parsing seismic/water-column files, navigation, and 3D scene options.
* [`SEIS_initialise`](SEIS_initialise.md) — Initializes global OpenGL camera, lighting, trace gain, and viewport variables (`SEIS_global.h`).
* [`SEIS_launcher`](SEIS_launcher.md) — X11/Motif control panel for interactive gain, clipping, and viewpoint adjustments.
* [`SEIS_event_loop`](SEIS_event_loop.md) — X11 mouse and keyboard event loop for 3D scene rotation, zooming, and curtain slicing.
* [`SEIS_oGL_draw`](SEIS_oGL_draw.md) — OpenGL rendering routines for textured 3D seismic curtains and bathymetric surfaces.
* [`SEIS_watercolumn`](SEIS_watercolumn.md) — Loads and textures multibeam water-column fans and acoustic curtains within the 3D `glSeis` scene.
* [`temp`](temp.md) — Auxiliary helper utility in `glseis/`.
