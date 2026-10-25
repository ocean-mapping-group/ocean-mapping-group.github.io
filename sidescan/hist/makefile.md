---
layout: default
title: makefile (hist)
parent: Histogram Tools
grand_parent: Sidescan Tools
nav_order: 10
tool_name: makefile
source_path: code/sidescan/hist/makefile
category: Build Configuration
input_formats: [".c"]
output_formats: ["Executable binaries (glhist, glfill, glfudge)"]
related_tools: ["glhist", "glfill", "glfudge"]
---

# makefile (`sidescan/hist`)

## Overview
The `makefile` in `code/sidescan/hist/` compiles the histogram equalization and missing-pixel interpolation tools for JCU GLORIA (`.ss`) and EM-12 sidescan files.

## Build Targets

All targets link against `-llocal -ljhc -lm` and output executables to `$(HOME)/bin/`:

* **`glhist`** ([`glhist.c`](glhist.md)) — Chavez-style Gaussian/uniform histogram equalization for `.ss` sidescan records.
* **`glfill`** ([`glfill.c`](glfill.md)) — Across-track gap interpolation for invalid pixels (`0` or `255`) in `.ss` scanlines.
* **`glfudge`** ([`glfudge.c`](glfudge.md)) — 2D (across-track and along-track) neighborhood interpolation for missing samples in `.ss` files.

## Usage
```bash
cd code/sidescan/hist
make glhist glfill glfudge
```
