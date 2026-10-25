---
layout: default
title: glfudge.o
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 5
tool_name: glfudge.o
source_path: code/sidescan/hist/glfudge.c
category: Sidescan Histogram & Gap Filling
input_formats:
- glfudge.c
output_formats:
- Executable binary (glfudge)
related_tools:
- glfudge
- glfill
- glhist
---

# glfudge.o

## Description
`glfudge.o` is the compiled ELF/COFF object module generated from [`glfudge.c`](glfudge.html) in `code/sidescan/hist/`.

## Module Summary (`glfudge`)
When linked via [`sidescan/hist/makefile`](makefile.html) (`cc -o $(HOME)/bin/glfudge glfudge.o -llocal -ljhc -lm`), this module provides the `glfudge` executable, which performs 2D (across-track and along-track) spatial interpolation of missing or invalid pixels (`0` or `255`) in JCU GLORIA (`.ss`) sidescan sonar files by averaging valid neighboring pixels across a sliding multi-ping buffer.

For complete command-line syntax and algorithm details, see **[`glfudge`](glfudge.html)**.
