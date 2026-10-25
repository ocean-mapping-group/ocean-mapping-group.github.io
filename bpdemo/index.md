---
layout: default
title: 3D Beam Pattern Visualizer (bpdemo)
parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 11
has_children: true
---

# Interactive Beamforming & Array Geometry Demo (`bpdemo`)

The `bpdemo` directory contains **`BPdemo`**, an interactive X11/Motif and OpenGL educational demonstration program for exploring acoustic phased-array beamforming, shading windows, steering angles, and 2D/3D directivity patterns.

---

## Main Application & Core Calculation Modules

* [`BPdemo`](BPdemo.html) — Main entry point and Motif widget hierarchy setup for the interactive beam-pattern demonstrator.
* [`bpfunc`](bpfunc.html) — Mathematical beamforming engine computing discrete element summation, continuous line-array sinc approximations, shading weights (uniform, cosine, Hamming, Blackman, Dolph-Chebyshev), and steered array response.
* [`do_parse`](do_parse.html) — Command-line and configuration parser for `BPdemo`.
* [`work_proc`](work_proc.html) — Background Motif `XtWorkProc` idle handler for continuous animation updates.

---

## 2D & 3D Drawing Canvases and Event Handlers

* [`draw_main`](draw_main.html) — Renders Cartesian and polar 2D beam-pattern directivity curves.
* [`draw_threeD`](draw_threeD.html) & [`threeD_window`](threeD_window.html) — Renders 3D Mills Cross transmit/receive cone intersections and array geometry.
* [`da_main_events`](da_main_events.html), [`da_polar_events`](da_polar_events.html), [`da_tl_events`](da_tl_events.html), [`threeD_events`](threeD_events.html) — Mouse and expose event callbacks for the Cartesian, Polar, Transmission Loss, and 3D viewports.
* [`callbacks`](callbacks.html), [`about`](about.html), [`error`](error.html), [`warning`](warning.html) — Motif slider/menu UI callbacks and dialog boxes.
