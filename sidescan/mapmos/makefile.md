---
layout: default
title: makefile (mapmos)
parent: Mapmos Tools
grand_parent: Sidescan Tools
nav_order: 10
tool_name: makefile
source_path: code/sidescan/mapmos/makefile
category: Build Configuration
input_formats: ["mapmos.c"]
output_formats: ["Executable binary (mapmos)"]
related_tools: ["mapmos", "printmos"]
---

# makefile (`sidescan/mapmos`)

## Overview
The `makefile` in `code/sidescan/mapmos/` builds the [`mapmos`](mapmos.md) sidescan sonar mosaicking executable.

## Build Target

* **`mapmos`** (from [`mapmos.c`](mapmos.md)): Links against `-llocal -ljhc -lm` and installs to `$(HOME)/bin/mapmos`. Projects slant-range and beam-corrected JCU GLORIA (`.ss` / `.beam`) scanlines onto a georeferenced Mercator or geographic raster grid (`OMG1` / `JHC_header`).

## Usage
```bash
cd code/sidescan/mapmos
make mapmos
```
