---
layout: default
title: makefile (merge)
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 10
tool_name: makefile
source_path: code/sidescan/merge/makefile
category: Build Configuration
input_formats:
- .c
output_formats:
- Executable binaries (glmerge, azimerge, addheader, appendSS)
related_tools:
- glmerge
- azimerge
- addheader
- appendSS
---

# makefile (`sidescan/merge`)

## Overview
The `makefile` in `code/sidescan/merge/` compiles utilities that merge external navigation, layback-adjusted towfish azimuth, headers, or sequential passes into JCU GLORIA (`.ss`) sidescan files.

## Build Targets

All targets link against `-llocal -ljhc -lm` and install to `$(HOME)/bin/`:

* **`glmerge`** ([`glmerge.c`](glmerge.html)) — Merges navigation and attitude time series into GLORIA `.ss` headers.
* **`azimerge`** ([`azimerge.c`](azimerge.html)) — Computes towfish layback geometry (`-layback`) and merges smoothed course/heading azimuths into `.ss` records.
* **`addheader`** ([`addheader.c`](addheader.html)) — Prepends or updates JCU GLORIA scanline headers on raw sidescan arrays.
* **`appendSS`** ([`appendSS.c`](appendSS.html)) — Concatenates multiple `.ss` sidescan pass files into a continuous file.

## Usage

```bash
cd code/sidescan/merge
make glmerge azimerge addheader appendSS
```
