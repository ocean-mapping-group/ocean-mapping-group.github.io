---
layout: default
title: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 6
has_children: true
---

# 1. Multibeam Unpacking, Nav & Ray-Tracing

Core Kongsberg (.kmall, .kmwcd, .all, .wcd) and OMG_HDCS (.merged) unpacking, navigation filtering, attitude/heave merging, 3D sound velocity ray-tracing, tidal reduction, and real-time monitoring.

---

## Directory Modules in This Category

| Module | Directory | Purpose & Key Tools |
| :--- | :--- | :--- |
| **[Kongsberg .kmall & .kmwcd (kmall)](../kmall/)** | `kmall/` | Modern Kongsberg EM2040 / EM712 / EM304 / EM124 .kmall and .kmwcd datagram parser (`read_kmall`) and split sensor extractors. |
| **[Core Swath & .all Suite (omg)](../omg/)** | `omg/` | Over 130 core `OMG_HDCS` (`.merged`) tools: `unravel` (`.all`), `mergeNav`, `mergeAtt`, `newMergeAtt`, `makess`, `makeWC`, `moveOverWCinfo`, `getBounds`, and swath diagnostics. |
| **[Navigation Processing (nav)](../nav/)** | `nav/` | Binary 48-byte `jcu_nav_rec` (`.nav`, `.decnav`) editors, spike filters (`stripNav`), decimation (`appendNav`), and ASCII/Shapefile exporters. |
| **[Attitude, Heave & Heading (att)](../att/)** | `att/` | Binary `.orientation` and `.net_att` processors, delayed heave integration (`mergeHeave`, `heaveCombo`), and heading/motion editors. |
| **[Ray-Tracing & Refraction (ray)](../ray/)** | `ray/` | Harmonic mean sound speed profiling, Snell's Law beam ray-tracing, and refraction artifact correction (`ray`, `refract`). |
| **[Real-Time KMALL/ALL Monitor (RTLite)](../RTLite/)** | `RTLite/` | Lightweight X11/Motif real-time UDP/file multibeam swath, coverage, and water-column monitor (`RTlite`). |
| **[Real-Time Multibeam Display (RT)](../RT/)** | `RT/` | Full real-time multibeam acquisition display and waterfall visualization suite. |
| **[Tidal Reduction & Constituents (tide)](../tide/)** | `tide/` | Harmonic tidal prediction (`tidepred`) and application of water-level corrections (`tidemerge`) to `.merged` files. |
| **[Finite-Element Tide Modeling (Tidecor)](../Tidecor/)** | `Tidecor/` | 2D finite-element barotropic tidal constituent modeling (`tidecor2.42`) for offshore survey zones. |
| **[Multibeam Quality Control (QC)](../QC/)** | `QC/` | Automated crossline/mainscheme IHO S-44 quality control, beam angle bias, and depth accuracy evaluators. |
