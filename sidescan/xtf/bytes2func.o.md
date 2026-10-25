---
layout: default
title: bytes2func.o
parent: XTF Tools
grand_parent: Sidescan Tools
nav_order: 6
tool_name: bytes2func.o
source_path: code/sidescan/xtf/bytes2func.c
category: XTF Sidescan Conversion
input_formats: ["bytes2func.c", "bytes2func.h"]
output_formats: ["Linked into xtf2glo"]
related_tools: ["bytes2func", "bytes2func.h", "chxtfhdr", "xtf2glo"]
---

# bytes2func.o

## Description
`bytes2func.o` is the compiled object module generated from [`bytes2func.c`](bytes2func.md) and [`bytes2func.h`](bytes2func.h.md) in `code/sidescan/xtf/`.

## Exported Symbols
When linked into [`xtf2glo`](xtf2glo.md) via [`sidescan/xtf/makefile`](makefile.md), `bytes2func.o` provides:
* `bytes2short(unsigned char *)` — Unpacks a 2-byte signed `short`, reversing byte order if `SWAP == TRUE`.
* `bytes2int(unsigned char *)` — Unpacks a 4-byte signed `int`, reversing byte order if `SWAP == TRUE`.
* `bytes2float(unsigned char *)` — Unpacks a 4-byte IEEE `float`, reversing byte order if `SWAP == TRUE`.
* `bytes2double(unsigned char *)` — Unpacks an 8-byte IEEE `double`, reversing byte order if `SWAP == TRUE`.

See **[`bytes2func`](bytes2func.md)** for full implementation details.
