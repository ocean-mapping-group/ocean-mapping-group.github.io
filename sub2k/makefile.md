---
layout: default
title: makefile (sub2k)
parent: Submetrix ISIS (sub2k) Interferometric Sonar Tools
nav_order: 9
tool_name: makefile
source_path: sub2k/makefile
category: sub2k
input_formats:
  - C source files (.c, .h)
output_formats:
  - Executables (readSUB2K, convSUB16, testWrap, readSWA, openISIS)
  - Object library (j_SUB2K.o)
related_tools:
  - makefile_BWD
  - readSUB2K
  - convSUB16
  - readSWA
  - openISIS
  - testWrap
---

# `makefile` (`sub2k/makefile`) — Build Configuration for Submetrix ISIS Tools

## Overview

`sub2k/makefile` is the primary GNU/UNIX Makefile for compiling the command-line Submetrix ISIS / Submetrix 2000 processing utilities in `sub2k/` (`readSUB2K`, `convSUB16`, `testWrap`, `readSWA`, and `openISIS`) as well as the embeddable object module `j_SUB2K.o` (compiled from `readSUB2K.c` with `-DNO_MAIN`) used by external GUI programs such as [`RTsubx`](../sub2k_motif/RTsubx.html) in `sub2k_motif/`.

---

## Usage

```bash
# Build default targets (readSUB2K, convSUB16, testWrap, readSWA, openISIS, j_SUB2K.o)
make -f makefile

# Build a specific binary and copy it to $BIN_DIR
make -f makefile readSUB2K
```

---

## Build Targets & Compiler Flags

| Target | Source & Dependencies | Compiler / Linker Flags | Output Action |
| :--- | :--- | :--- | :--- |
| `all` | `readSUB2K`, `convSUB16`, `testWrap`, `readSWA`, `openISIS`, `j_SUB2K.o` | Builds all tools and the shared object module | Default target |
| `j_SUB2K.o` | `readSUB2K.c`, `sub2k.h` | `cc $(CFLAGS) -DNO_MAIN -c readSUB2K.c -o j_SUB2K.o` | Compiles `readSUB2K.c` without `main()` for linking into GUI/Motif applications |
| `readSUB2K` | `readSUB2K.c`, `sub2k.h`, `LIB_PATH/liblocal.a` | `cc $(CFLAGS) -o readSUB2K readSUB2K.c -L$(LIB_PATH) -llocal -lm` | Copies binary to `$(BIN_DIR)` |
| `openISIS` | `openISIS.c`, `sub2k.h`, `LIB_PATH/liblocal.a` | `cc $(CFLAGS) -o openISIS openISIS.c -L$(LIB_PATH) -llocal -lm` | Copies binary to `$(BIN_DIR)` |
| `readSWA` | `readSWA.c`, `sub2k.h`, `LIB_PATH/liblocal.a` | `cc $(CFLAGS) -o readSWA readSWA.c -L$(LIB_PATH) -llocal -lm` | Copies binary to `$(BIN_DIR)` |
| `convSUB16` | `convSUB16.c`, `sub2k.h`, `LIB_PATH/liblocal.a` | `cc $(CFLAGS) -o convSUB16 convSUB16.c -L$(LIB_PATH) -llocal -lm` | Copies binary to `$(BIN_DIR)` |
| `testWrap` | `testWrap.c`, `LIB_PATH/liblocal.a` | `cc $(CFLAGS) -o testWrap testWrap.c -L$(LIB_PATH) -llocal -lm` | Copies binary to `$(BIN_DIR)` |

---

## How It Works

- **Environment Variables:** Uses `$(INC_PATH)` for OMG shared headers (`-I$(INC_PATH)`), `$(LIB_PATH)` for `liblocal.a` (`-L$(LIB_PATH) -llocal`), and `$(BIN_DIR)` as the installation directory where compiled binaries are copied immediately after linking.
- **Dual-Mode Compilation (`-DNO_MAIN`):** `readSUB2K.c` is structured so that defining `NO_MAIN` omits the CLI `main()` entry point while exporting its interferometric decoding and bathymetric binning functions inside `j_SUB2K.o`.
