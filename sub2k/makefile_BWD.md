---
layout: default
title: makefile_BWD (sub2k)
parent: Submetrix ISIS (sub2k) Interferometric Sonar Tools
nav_order: 10
tool_name: makefile_BWD
source_path: sub2k/makefile_BWD
category: sub2k
input_formats:
  - C source files (.c, .h)
output_formats:
  - Executables (readSUB2K, convSUB16, testWrap, readSWA, openISIS)
  - Object library (j_SUB2K.o)
related_tools:
  - makefile
  - readSUB2K
---

# `makefile_BWD` (`sub2k/makefile_BWD`) — Bill Danforth Linux Build File

## Overview

`sub2k/makefile_BWD` is a Linux-adapted version of [`sub2k/makefile`](makefile.html) configured by **Bill Danforth** (U.S. Geological Survey, Woods Hole) in June 2005 for building the Submetrix 2000 / ISIS processing tools on Linux workstations (`CFLAGS = -g -DLINUX -I$(INC_PATH)`).

---

## Usage

```bash
make -f makefile_BWD
```

---

## Differences from `sub2k/makefile`

| Setting | `sub2k/makefile_BWD` | `sub2k/makefile` |
| :--- | :--- | :--- |
| `CFLAGS` | `-g -DLINUX -I$(INC_PATH)` (uncommented by default for Linux little-endian x86 builds) | Platform `CFLAGS` lines commented out at top of file, relying on environment `CFLAGS` |
| Targets | `readSUB2K`, `convSUB16`, `testWrap`, `readSWA`, `openISIS`, `j_SUB2K.o` | Identical target set |

---

## How It Works

By explicitly enabling `-DLINUX` in `CFLAGS`, `makefile_BWD` ensures that the byte-swapping macros and little-endian struct layouts inside `sub2k.h` and `readSUB2K.c` are active during compilation on x86/x86_64 Linux systems, matching the native little-endian byte order of Submetrix Windows/PC `.sub` and `.rrc` recordings or swapping into big-endian OMG `.merged` output files as needed.
