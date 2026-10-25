---
layout: default
title: makefile (beammap)
parent: Beammap Tools
grand_parent: Sidescan Tools
nav_order: 10
tool_name: makefile
source_path: code/sidescan/beammap/makefile
category: Build Configuration
input_formats: [".c", "gl_beam.h"]
output_formats: ["Executable binaries (mapbeam, debeam, joinbeam, jdebeam, debeam_cosmetic)"]
related_tools: ["mapbeam", "debeam", "joinbeam", "gl_beam.h"]
---

# makefile (`sidescan/beammap`)

## Overview
The `makefile` in `code/sidescan/beammap/` builds the 2D depth-vs-grazing-angle empirical beam pattern mapping and removal suite developed by Guy Carpenter (April 1990) for JCU GLORIA sidescan sonar processing.

## Build Targets & Dependencies

All targets depend on [`gl_beam.h`](gl_beam.h.md) and link against `-llocal -ljhc -lm` (with executables installed to `$(HOME)/bin/`):

* **`mapbeam`** (from [`mapbeam.c`](mapbeam.md)): Scans slant-range corrected GLORIA (`.slr`) files and accumulates a 512×992 2D depth-by-across-track intensity map.
* **`debeam`** (from [`debeam.c`](debeam.md)): Removes across-track empirical beam shading from `.slr` files using the 2D beam map produced by `mapbeam` or `joinbeam`.
* **`joinbeam`** (from [`joinbeam.c`](joinbeam.md)): Combines and smooths multiple pass beam maps into a master regional beam pattern lookup table.
* **`jdebeam`** / **`debeam_cosmetic`**: Variant targets built from `jdebeam.c` and `debeam_cosmetic.c` for specialized cosmetic beam balancing.

## Usage
```bash
cd code/sidescan/beammap
make all
```
