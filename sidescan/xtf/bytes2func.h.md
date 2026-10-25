---
layout: default
title: bytes2func.h
parent: XTF Tools
grand_parent: Sidescan Tools
nav_order: 5
tool_name: bytes2func.h
source_path: code/sidescan/xtf/bytes2func.h
category: XTF Sidescan Conversion
input_formats: ["C Header File"]
output_formats: ["Included by bytes2func.c, chxtfhdr.c, xtf_funcs.c, xtf2glo.c"]
related_tools: ["bytes2func", "chxtfhdr", "xtf_funcs", "xtf2glo"]
---

# bytes2func.h

## Description
`bytes2func.h` is the C header file in `code/sidescan/xtf/` that declares the endian-aware byte-unpacking functions implemented in [`bytes2func.c`](bytes2func.md) and the global `SWAP` flag used across the XTF sidescan conversion suite ([`xtf2glo`](xtf2glo.md)).

## Declarations

```c
#define TRUE 1
#define FALSE 0

short  bytes2short(unsigned char *bytes);
int    bytes2int(unsigned char *bytes);
float  bytes2float(unsigned char *bytes);
double bytes2double(unsigned char *bytes);

char SWAP; /* Set to TRUE on big-endian hosts, FALSE on little-endian PCs */
```

## Purpose
Triton `.xtf` files are recorded in little-endian (80x86) byte order with unaligned fields. Including `bytes2func.h` allows [`chxtfhdr.c`](chxtfhdr.md) and [`xtf2glo.c`](xtf2glo.md) to safely decode 16-bit integers, 32-bit integers, 32-bit IEEE floats, and 64-bit IEEE doubles from raw `unsigned char` buffers regardless of host CPU alignment or endianness.
