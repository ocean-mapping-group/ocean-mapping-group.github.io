---
layout: default
title: makefile (xtf)
parent: XTF Tools
grand_parent: Sidescan Tools
nav_order: 20
tool_name: makefile
source_path: code/sidescan/xtf/makefile
category: Build Configuration
input_formats: ["xtf2glo.c", "xtf_funcs.c", "chxtfhdr.c", "bytes2func.c"]
output_formats: ["Executable binary (xtf2glo)"]
related_tools: ["xtf2glo", "xtf_funcs", "chxtfhdr", "bytes2func"]
---

# makefile (`sidescan/xtf`)

## Overview
The `makefile` in `code/sidescan/xtf/` builds the [`xtf2glo`](xtf2glo.md) converter from its four modular C source files and header definitions.

## Object Modules & Dependencies

* **`xtf2glo.o`**: Compiled from [`xtf2glo.c`](xtf2glo.md) (depends on [`xtf_doc.h`](xtf_doc.h.md), [`new_xtf.h`](new_xtf.h.md), [`xtf_funcs.h`](xtf_funcs.h.md), [`chxtfhdr.h`](chxtfhdr.h.md), [`bytes2func.h`](bytes2func.h.md)).
* **`xtf_funcs.o`**: Compiled from [`xtf_funcs.c`](xtf_funcs.md) — XTF packet reading functions.
* **`chxtfhdr.o`**: Compiled from [`chxtfhdr.c`](chxtfhdr.md) — Unaligned byte-array header unpacking routines.
* **`bytes2func.o`**: Compiled from [`bytes2func.c`](bytes2func.md) — Endian-swapping primitive readers.

All four objects are linked with `-llocal -ljhc -lm` to produce the `xtf2glo` executable.

## Usage
```bash
cd code/sidescan/xtf
make xtf2glo
```
