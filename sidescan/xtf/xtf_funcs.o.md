---
layout: default
title: xtf_funcs.o
parent: XTF Tools
grand_parent: Sidescan Tools
nav_order: 12
tool_name: xtf_funcs.o
source_path: code/sidescan/xtf/xtf_funcs.c
category: XTF Sidescan Conversion
input_formats: ["xtf_funcs.c", "xtf_funcs.h", "xtf_doc.h", "chxtfhdr.h"]
output_formats: ["Linked into xtf2glo"]
related_tools: ["xtf_funcs", "xtf_funcs.h", "xtf2glo", "chxtfhdr"]
---

# xtf_funcs.o

## Description
`xtf_funcs.o` is the compiled object module built from [`xtf_funcs.c`](xtf_funcs.md) in `code/sidescan/xtf/`.

## Exported Functions
Linked into [`xtf2glo`](xtf2glo.md) via [`sidescan/xtf/makefile`](makefile.md), `xtf_funcs.o` provides:
* `readXTFheader(FILE *fp, XTFFILEHEADER *XTFhdr)` — Parses the 1024-byte `.XTF` file header and channel descriptor blocks.
* `readXTFdata(FILE *fp, unsigned char *buffer)` — Reads sequential variable-length `.XTF` data records into memory after verifying the `0xFACE` packet synchronization marker.

See **[`xtf_funcs`](xtf_funcs.md)** for full details.
