---
layout: default
title: Plotlib Tools
nav_order: 14
has_children: true
---

# Vector Plotting Library & Metafile Drivers (`plotlib`)

The `plotlib` directory contains the Ocean Mapping Group's device-independent 2D vector plotting library (`plotlib`), along with its X11 metafile viewer (`viewmeta`), HP-GL/PostScript hardware drivers (`hpgl`, `plotdriver`), pen-sorting optimizer (`pensort`), and Fortran-77 bindings (`plotlibf77`).

All 2D scientific plotting programs in the [`plot/`](../plot/index.md), [`ray/`](../ray/index.md), [`class/`](../class/index.md), and [`vers/`](../vers/index.md) directories call `plotlib` routines (`plot_open`, `plot_move`, `plot_line`, `plot_pen`, `plot_text`, `plot_close`) to generate binary vector metafiles (typically `plot.meta`), which can then be inspected interactively or converted to PostScript/HP-GL.

---

## Core Library & Language Bindings

* [`plotlib`](plotlib.md) — Core C API for generating device-independent 2D vector plot metafiles (`plot_open`, `plot_move`, `plot_line`, `plot_text`, `plot_pen`, `plot_close`).
* [`plotlibf77`](plotlibf77.md) — Fortran-77 wrapper routines exposing `plotlib` primitives to legacy Fortran acoustic and ray-tracing programs.
* [`unix`](unix.md) — Low-level Unix file I/O, process spawning, and environment helpers for `plotlib`.

---

## Metafile Viewers, Drivers & Post-Processors

* [`viewmeta`](viewmeta.md) — Interactive X11 viewer for inspecting binary `plot.meta` vector graphics files on screen.
* [`plotdriver`](plotdriver.md) — Backend device driver translating `plot.meta` instructions into target plotter commands.
* [`hpgl`](hpgl.md) — Hewlett-Packard Graphics Language (HP-GL) output generator (paired with `hpgl2ps` for PostScript conversion).
* [`pensort`](pensort.md) — Sorts vector drawing commands by pen number/color to minimize mechanical pen changes on physical flatbed/drum plotters.
* [`penstat`](penstat.md) — Reports pen usage statistics, bounding boxes, and total stroke lengths in a metafile.
* [`plottest`](plottest.md) — Diagnostic test program exercising `plotlib` line styles, text scaling, and pen colors.
