---
layout: default
title: bpdemo Tools
has_children: true
nav_order: 3
---

# Interactive Beamforming & Array Geometry Demo (`bpdemo`)

The `bpdemo` directory contains **`BPdemo`**, an interactive X11/Motif and OpenGL educational demonstration program for exploring acoustic phased-array beamforming, shading windows, steering angles, and 2D/3D directivity patterns.

---

## Main Application & Core Calculation Modules

* [`BPdemo`](BPdemo.md) — Main entry point and Motif widget hierarchy setup for the interactive beam-pattern demonstrator.
* [`bpfunc`](bpfunc.md) — Mathematical beamforming engine computing discrete element summation, continuous line-array sinc approximations, shading weights (uniform, cosine, Hamming, Blackman, Dolph-Chebyshev), and steered array response.
* [`do_parse`](do_parse.md) — Command-line and configuration parser for `BPdemo`.
* [`work_proc`](work_proc.md) — Background Motif `XtWorkProc` idle handler for continuous animation updates.

---

## 2D & 3D Drawing Canvases and Event Handlers

* [`draw_main`](draw_main.md) — Renders Cartesian and polar 2D beam-pattern directivity curves.
* [`draw_threeD`](draw_threeD.md) & [`threeD_window`](threeD_window.md) — Renders 3D Mills Cross transmit/receive cone intersections and array geometry.
* [`da_main_events`](da_main_events.md), [`da_polar_events`](da_polar_events.md), [`da_tl_events`](da_tl_events.md), [`threeD_events`](threeD_events.md) — Mouse and expose event callbacks for the Cartesian, Polar, Transmission Loss, and 3D viewports.
* [`callbacks`](callbacks.md), [`about`](about.md), [`error`](error.md), [`warning`](warning.md) — Motif slider/menu UI callbacks and dialog boxes.
