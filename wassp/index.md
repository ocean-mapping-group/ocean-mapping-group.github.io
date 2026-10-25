---
layout: default
title: Furuno WASSP Multibeam (wassp)
parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 4
has_children: true
---

# WASSP Tools

Tools in the `wassp/` directory inspect and convert binary data packets acquired by ENL **WASSP** (Wide Angle Sonar Seafloor Profiler) multibeam systems (typically stored in `.000` files containing `GENBATHY` and `GEN_SENS` packets) into OMG HDCS formats.

## Tool Summary

| Tool | Source | Description |
| :--- | :--- | :--- |
| [wassp2omg](wassp2omg) | `wassp/wassp2omg.c` | Converts WASSP `GENBATHY` multibeam bathymetry packets into OMG HDCS v4 `.merged` and `.sonar_settings` files. |
| [wasspTool](wasspTool) | `wassp/wasspTool.c` | Diagnostic utility that scans WASSP binary files and prints `GENBATHY` and `GEN_SENS` packet headers and contents. |

## Typical Workflow

1. **Inspect WASSP file contents:** Run `wasspTool -v -in line01.000` to verify `GENBATHY` and `GEN_SENS` packet counts and metadata.
2. **Convert bathymetry to OMG HDCS:** Run `wassp2omg -in line01.000 -omg line01` to produce `line01.merged` and `line01.sonar_settings`.
3. **Merge navigation and attitude:** Merge external navigation (`.nav`) and orientation (`.orientation`) streams onto `line01.merged` for full raytracing and swath editing.
