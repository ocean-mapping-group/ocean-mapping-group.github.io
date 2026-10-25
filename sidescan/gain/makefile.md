---
layout: default
title: makefile (gain)
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 10
tool_name: makefile
source_path: code/sidescan/gain/makefile
category: Build Configuration
input_formats:
- .c
output_formats:
- Executable binaries (glgain, glcosmetic)
related_tools:
- glgain
- glcosmetic
---

# makefile (`sidescan/gain`)

## Overview
The `makefile` in `code/sidescan/gain/` builds the radiometric gain adjustment utilities for JCU GLORIA (`.ss`) sidescan sonar files.

## Build Targets

Both targets compile their `.c` sources and link against `-llocal -ljhc -lm`:

* **`glgain`** ([`glgain.c`](glgain.html)) — Applies multiplicative or additive gain adjustments and balances port/starboard intensity levels across GLORIA scanlines.
* **`glcosmetic`** ([`glcosmetic.c`](glcosmetic.html)) — Applies cosmetic across-track and along-track gain normalization to suppress residual seam shading prior to mosaicking.

## Usage

```bash
cd code/sidescan/gain
make glgain glcosmetic
```
