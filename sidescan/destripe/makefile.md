---
layout: default
title: makefile (destripe)
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 20
tool_name: makefile
source_path: code/sidescan/destripe/makefile
category: Build Configuration
input_formats:
- .c
output_formats:
- Executable binaries (destripe, gladd, glboxfilt, nadirdamp, destripe_hack, glsmudge, glreplace, gldiff, gldropStripes)
related_tools:
- destripe
- destripe_hack
- gladd
- glboxfilt
- gldiff
- gldropStripes
- glreplace
- glsmudge
- nadirdamp
---

# makefile (`sidescan/destripe`)

## Overview
The `makefile` in `code/sidescan/destripe/` builds the suite of along-track and across-track radiometric filtering, destriping, nadir damping, and dropout-repair utilities for JCU GLORIA (`.ss`) sidescan files.

## Build Targets

All executables link with `-llocal -ljhc -lm` and install into `$(HOME)/bin/`:

* **`destripe`** ([`destripe.c`](destripe.html)) — Ping-to-ping destriping filter.
* **`destripe_hack`** ([`destripe_hack.c`](destripe_hack.html)) — Modified destriping filter for heavily striped passes.
* **`gladd`** ([`gladd.c`](gladd.html)) — Pixel-by-pixel addition/blending of two GLORIA files.
* **`glboxfilt`** ([`glboxfilt.c`](glboxfilt.html)) — 2D moving-average boxcar filter for `.ss` scanlines.
* **`nadirdamp`** ([`nadirdamp.c`](nadirdamp.html)) — Attenuates excessive near-nadir specular return saturation.
* **`glsmudge`** ([`glsmudge.c`](glsmudge.html)) — Smooths localized across-track gain transitions.
* **`glreplace`** ([`glreplace.c`](glreplace.html)) — Replaces corrupted scanline segments from a secondary `.ss` file.
* **`gldiff`** ([`gldiff.c`](gldiff.html)) — Computes pixel differences between two `.ss` files to inspect filter residuals.
* **`gldropStripes`** ([`gldropStripes.c`](gldropStripes.html)) — Detects and interpolates over dropped/zeroed ping stripes.

## Usage

```bash
cd code/sidescan/destripe
make destripe glboxfilt nadirdamp gldropStripes
```
