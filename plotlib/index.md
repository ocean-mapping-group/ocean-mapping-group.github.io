---
layout: default
title: PostScript & Vector Plot Library (plotlib)
parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 3
has_children: true
---

# Vector Plotting Library & Metafile Drivers (`plotlib`)

The `plotlib` directory contains the Ocean Mapping Group's device-independent 2D vector plotting library (`plotlib`), along with its X11 metafile viewer (`viewmeta`), HP-GL/PostScript hardware drivers (`hpgl`, `plotdriver`), pen-sorting optimizer (`pensort`), and Fortran-77 bindings (`plotlibf77`).

All 2D scientific plotting programs in the [`plot/`](../plot/), [`ray/`](../ray/), [`class/`](../class/), and [`vers/`](../vers/) directories call `plotlib` routines (`plot_open`, `plot_move`, `plot_line`, `plot_pen`, `plot_text`, `plot_close`) to generate binary vector metafiles (typically `plot.meta`), which can then be inspected interactively or converted to PostScript/HP-GL.

---

## Core Library & Language Bindings

* [`plotlib`](plotlib.html) — Core C API for generating device-independent 2D vector plot metafiles (`plot_open`, `plot_move`, `plot_line`, `plot_text`, `plot_pen`, `plot_close`).
* [`plotlibf77`](plotlibf77.html) — Fortran-77 wrapper routines exposing `plotlib` primitives to legacy Fortran acoustic and ray-tracing programs.
* [`unix`](unix.html) — Low-level Unix file I/O, process spawning, and environment helpers for `plotlib`.

---

## Metafile Viewers, Drivers & Post-Processors

* [`viewmeta`](viewmeta.html) — Interactive X11 viewer for inspecting binary `plot.meta` vector graphics files on screen.
* [`plotdriver`](plotdriver.html) — Backend device driver translating `plot.meta` instructions into target plotter commands.
* [`hpgl`](hpgl.html) — Hewlett-Packard Graphics Language (HP-GL) output generator (paired with `hpgl2ps` for PostScript conversion).
* [`pensort`](pensort.html) — Sorts vector drawing commands by pen number/color to minimize mechanical pen changes on physical flatbed/drum plotters.
* [`penstat`](penstat.html) — Reports pen usage statistics, bounding boxes, and total stroke lengths in a metafile.
* [`plottest`](plottest.html) — Diagnostic test program exercising `plotlib` line styles, text scaling, and pen colors.
