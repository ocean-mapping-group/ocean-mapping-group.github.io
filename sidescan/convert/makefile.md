---
layout: default
title: makefile (convert)
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 10
tool_name: makefile
source_path: code/sidescan/convert/makefile
category: Build Configuration
input_formats:
- .c
output_formats:
- Executable binaries (ssi2glo, usgs2glo, ios2glo, jwn2glo, xsonar2glo, qmips2glo, restructure_glo)
related_tools:
- ios2glo
- usgs2glo
- xsonar2glo
- ssi2glo
- jwn2glo
- restructure_glo
- qmips2glo
---

# makefile (`sidescan/convert`)

## Overview
The `makefile` in `code/sidescan/convert/` compiles the sidescan format conversion utilities that import external sonar formats into the 1024-byte JCU GLORIA (`gloria_rec`) `.ss` scanline format.

## Build Targets

Each target compiles its corresponding `.c` source file and links against the OMG/JCU libraries (`$(LIBS)` = `-llocal -ljhc -lm`), placing executables into `$(HOME)/bin/`:

* **`ssi2glo`** — Built from [`ssi2glo.c`](ssi2glo.html).
* **`usgs2glo`** — Built from [`usgs2glo.c`](usgs2glo.html).
* **`ios2glo`** — Built from [`ios2glo.c`](ios2glo.html).
* **`jwn2glo`** — Built from [`jwn2glo.c`](jwn2glo.html).
* **`xsonar2glo`** — Built from [`xsonar2glo.c`](xsonar2glo.html).
* **`qmips2glo`** — Built from [`Q-Mips/qmips2glo.c`](Q-Mips/qmips2glo.html).
* **`restructure_glo`** — Built from [`restructure_glo.c`](restructure_glo.html).

## Usage

```bash
cd code/sidescan/convert
make ssi2glo usgs2glo ios2glo jwn2glo xsonar2glo restructure_glo
```
