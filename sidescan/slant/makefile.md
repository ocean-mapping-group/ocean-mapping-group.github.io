---
layout: default
title: makefile (slant)
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 10
tool_name: makefile
source_path: code/sidescan/slant/makefile
category: Build Configuration
input_formats:
- .c
output_formats:
- Executable binaries (glslant, bpick, downGrade)
related_tools:
- glslant
- bpick
- downGrade
---

# makefile (`sidescan/slant`)

## Overview
The `makefile` in `code/sidescan/slant/` compiles the bottom-picking, slant-range rectification, and scanline decimation tools for JCU GLORIA (`.ss`) sidescan data.

## Build Targets

All targets link against `-llocal -ljhc -lm` and output executables to `$(HOME)/bin/`:

* **`glslant`** ([`glslant.c`](glslant.html)) — Converts slant-range sampled `.ss` scanlines into ground-range rectified `.slr` records.
* **`bpick`** ([`bpick.c`](bpick.html)) — Automated/interactive seafloor first-return picker for `.ss` files.
* **`downGrade`** ([`downGrade.c`](downGrade.html)) — Decimates high-density sidescan records into standard GLORIA scanline resolution.

## Usage

```bash
cd code/sidescan/slant
make glslant bpick downGrade
```
