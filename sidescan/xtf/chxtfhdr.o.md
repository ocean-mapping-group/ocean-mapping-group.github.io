---
layout: default
title: chxtfhdr.o
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 8
tool_name: chxtfhdr.o
source_path: code/sidescan/xtf/chxtfhdr.c
category: XTF Sidescan Conversion
input_formats:
- chxtfhdr.c
- chxtfhdr.h
- xtf_doc.h
output_formats:
- Linked into xtf2glo
related_tools:
- chxtfhdr
- chxtfhdr.h
- bytes2func
- xtf2glo
---

# chxtfhdr.o

## Description
`chxtfhdr.o` is the compiled object module produced from [`chxtfhdr.c`](chxtfhdr.html) in `code/sidescan/xtf/`.

## Exported Functions
Linked into [`xtf2glo`](xtf2glo.html) via [`sidescan/xtf/makefile`](makefile.html), `chxtfhdr.o` exports the seven header conversion routines (`convXTFFILEHEADER`, `convCHANINFO`, `convXTFPINGHEADER`, `convXTFPINGCHANHEADER`, `convXTFATTITUDEDATA`, `convXTFNOTESHEADER`, and `convXTFRAWSERIALHEADER`) that unpack unaligned on-disk byte arrays ([`chxtfhdr.h`](chxtfhdr.h.html)) into native C structures ([`xtf_doc.h`](xtf_doc.h.html)) using [`bytes2func`](bytes2func.html).

See **[`chxtfhdr`](chxtfhdr.html)** for full documentation.
