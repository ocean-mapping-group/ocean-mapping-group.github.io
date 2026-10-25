---
layout: default
title: makefile (beam/oldstuff)
parent: Old Stuff
grand_parent: Beam Tools
nav_order: 20
tool_name: makefile
source_path: code/sidescan/beam/oldstuff/makefile
category: Build Configuration
input_formats: [".c", ".f"]
output_formats: ["Executable binaries (glbeam2, glbeambin, glbeam_bydepth, hack_glbeam, sumbeam, sumbeambin, viewbeam)"]
related_tools: ["glbeam_bypass", "glbeambin", "glbeam_bydepth", "hack_glbeam", "sumbeam.f", "sumbeambin.f", "viewbeam.f"]
---

# makefile (`sidescan/beam/oldstuff`)

## Overview
The `makefile` in `code/sidescan/beam/oldstuff/` compiles both C and Fortran 77 legacy empirical beam-pattern processing utilities for GLORIA sidescan sonar data.

## Build Targets & Compilation Rules

| Target Binary | Source File | Compiler & Libraries | Purpose |
| :--- | :--- | :--- | :--- |
| `viewbeam` | [`viewbeam.f`](viewbeam.f.md) | `f77` + `$(F77LIBS)` (`-llocalf77`) | Plots `.beam_pattern` curves to screen or metafile. |
| `glbeam2` | [`glbeam_bypass.c`](glbeam_bypass.md) | `cc` + `-llocal -ljhc -lm` | Extracts and removes single-pass empirical beam patterns. |
| `sumbeam` | [`sumbeam.f`](sumbeam.f.md) | `f77` + `$(F77LIBS)` | Averages `.beam_pattern` files across multiple passes. |
| `glbeambin` | [`glbeambin.c`](glbeambin.md) | `cc` + `-llocal -ljhc -lm` | Accumulates 2D grazing-angle × water-depth beam histograms (`.beam_bin`). |
| `sumbeambin` | [`sumbeambin.f`](sumbeambin.f.md) | `f77` + `$(F77LIBS)` | Sums `.beam_bin` files across passes and writes 20 depth-stratified `.beam_pattern` files. |
| `glbeam_bydepth` | [`glbeam_bydepth.c`](glbeam_bydepth.md) | `cc` + `-llocal -ljhc -lm` | Applies depth-stratified empirical beam patterns to `.slr` files. |
| `hack_glbeam` | [`hack_glbeam.c`](hack_glbeam.md) | `cc` + `-llocal -ljhc -lm` | Applies customized beam pattern corrections. |

## Usage
```bash
cd code/sidescan/beam/oldstuff
make glbeam2 glbeambin glbeam_bydepth sumbeam sumbeambin viewbeam
```
