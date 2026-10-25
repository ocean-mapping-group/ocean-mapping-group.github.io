---
layout: default
title: makefile (edit)
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 10
tool_name: makefile
source_path: code/sidescan/edit/makefile
category: Build Configuration
input_formats:
- .c
output_formats:
- Executable binaries (gledit, iosedit, gltimefix)
related_tools:
- gledit
- iosedit
- gltimefix
---

# makefile (`sidescan/edit`)

## Overview
The `makefile` in `code/sidescan/edit/` compiles the scanline header and timestamp editing utilities for JCU GLORIA (`.ss`) and raw IOS GLORIA sidescan files.

## Build Targets

Each target links with `-llocal -ljhc -lm` and installs into `$(HOME)/bin/`:

* **`gledit`** ([`gledit.c`](gledit.html)) — Interactive/command-line record editor and subsets extractor for JCU GLORIA `.ss` files.
* **`iosedit`** ([`iosedit.c`](iosedit.html)) — Record inspection and editing utility for raw IOS format GLORIA files prior to `ios2glo` conversion.
* **`gltimefix`** ([`gltimefix.c`](gltimefix.html)) — Repairs non-monotonic, wrapped, or corrupted ping timestamps in `.ss` scanline headers.

## Usage

```bash
cd code/sidescan/edit
make gledit iosedit gltimefix
```
