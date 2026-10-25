---
layout: default
title: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 10
has_children: true
---

# 5. Core Libraries, Researcher Suites & Utilities

Foundational C libraries (libj.a, subr_graphics, plotlib, gsf_lib, shapelib), researcher toolboxes (Ian Church, Jonathan Beaudoin, James Muggah, Steve Brucker), shell pipelines, and test harnesses.

---

## Directory Modules in This Category

| Module | Directory | Purpose & Key Tools |
| :--- | :--- | :--- |
| **[Core Shared C Library — libj.a (subr)](../subr/)** | `subr/` | 94 core C modules implementing `OMG_HDCS` v1–v4 I/O, `JHC_header` (`OMG1`) rasters, `jcu_nav_rec`, endian swapping (`swapio`), geodesy (`j_proj`, `utm`), and ray-tracing. |
| **[X11 / Motif / OpenGL Graphics Library (subr_graphics)](../subr_graphics/)** | `subr_graphics/` | Shared X11 window management (`jX_win`), OpenGL context wrappers (`jGL_draw`), and Motif widget helpers. |
| **[PostScript & Vector Plot Library (plotlib)](../plotlib/)** | `plotlib/` | Low-level PostScript page layout, vector font rendering, and axis drawing library. |
| **[Embedded GSF C Library (gsf_lib)](../gsf_lib/)** | `gsf_lib/` | Standard Generic Sensor Format (GSF) C reference library linked by `gsf/` tools. |
| **[ESRI Shapefile C Library (shapelib-1.3.0a2)](../shapelib-1.3.0a2/)** | `shapelib-1.3.0a2/` | Frank Warmerdam's Shapelib C library and CLI utilities (`shpcreate`, `shpadd`, `dbfadd`, `shpdump`) used to build `shpFiles/`. |
| **[Ian Church — Hydrodynamic & 3D Ray-Trace Suite (ianc)](../ianc/)** | `ianc/` | FVCOM/HYCOM 3D hydrodynamic model readers (`oceanReader`, `HycomSSP`), 4D water-column ray-tracing, and POS MV nav tools. |
| **[Jonathan Beaudoin — SVP, Refraction & Snippets (jonnyb)](../jonnyb/)** | `jonnyb/` | SVP cast editors, empirical TVG removal (`deTVG`), refraction diagnostics, and backscatter snippet tools. |
| **[James Muggah — Global Mapper Tiles & Utils (james)](../james/)** | `james/` | Tiled export pipelines (`merged2GMTiles`), swath footprint calculators, and survey utilities. |
| **[Steve Brucker — Backscatter & Calibration (steve)](../steve/)** | `steve/` | Multibeam backscatter angular calibration, sector bias analysis, and beam-pattern tools. |
| **[Environment & Shell Wrappers (bin)](../bin/)** | `bin/` | OMG environment initialization and execution wrapper scripts. |
| **[Automated Processing Scripts (scripts)](../scripts/)** | `scripts/` | Production shell scripts (`unravel_KMALL_*`, `unravel_ALL_*`, parallel GNU Parallel / xargs runners) for end-to-end processing. |
| **[Miscellaneous Coordinate & File Utilities (misc-tools)](../misc-tools/)** | `misc-tools/` | Standalone coordinate converters, time calculators, and binary file inspectors. |
| **[Survey Line Export Utilities (line)](../line/)** | `line/` | Survey line summary and ASCII trackline exporters (`line_export`). |
| **[Version Control & Build Stamps (vers)](../vers/)** | `vers/` | Compile-time version stamping utilities for OMG binaries. |
| **[Acoustic & Mathematical Test Harnesses (tests)](../tests/)** | `tests/` | 25 standalone verification programs for Bessel functions, FIR filters, FM chirp correlation, sphere target strength, and seawater attenuation. |
| **[Graduate Course Lab Exercises (labs)](../labs/)** | `labs/` | UNB Geodesy & Geomatics Engineering (GGE) graduate lab exercises (`EM_unpack`, `mkbp`). |
| **[Developer How-To Guides (howto)](../howto/)** | `howto/` | Internal C developer guides on writing `OMG_HDCS` loops, adding new `toolType` codes, and building Motif GUIs. |
| **[Historical Format & System Notes (doc)](../doc/)** | `doc/` | Original ASCII architectural specifications for `OMG_HDCS`, `JHC_header`, and GLORIA sidescan formats. |
| **[Legacy OMG Code Wiki Archive (wiki)](../wiki/)** | `wiki/` | Preserved historical UNB OMG wiki pages (`nuliajuk.omg.unb.ca`) cross-linked to modern tools. |
