---
layout: default
title: XTF Tools
parent: Sidescan Tools
nav_order: 12
has_children: true
---

# eXtended Triton Format (XTF) Tools (`sidescan/xtf`)

The `xtf` directory (`code/sidescan/xtf/`) contains the parser library, byte-order conversion routines, header definitions, and command-line converter for importing Triton Imaging Inc. eXtended Triton Format (`.xtf`, Revision 3 / Sept 1998) digital sidescan sonar files into the Ocean Mapping Group's JCU GLORIA (`.ss`) processing format.

## Executable & Source Modules

* **[`xtf2glo`](xtf2glo.md)** — Main command-line converter that reads 8-bit or 16-bit `.xtf` sidescan sonar files, performs dynamic range normalization (`RAW`, `MINMAX`, `STDDEV`, or `AVG` methods), optionally detects the seabed or interpolates across nadir, computes Course Made Good (`-cmg`), and writes JCU GLORIA `.ss` records plus an `.mbr` Minimum Bounding Rectangle file.
* **[`xtf_funcs`](xtf_funcs.md)** & **[`xtf_funcs.h`](xtf_funcs.h.md)** ([`xtf_funcs.o`](xtf_funcs.o.md)) — File I/O module providing `readXTFheader()` and `readXTFdata()` to parse variable-length XTF packets (`XTF_HEADER_SONAR`, `XTF_HEADER_ATTITUDE`, `XTF_HEADER_NOTES`, etc.).
* **[`chxtfhdr`](chxtfhdr.md)** & **[`chxtfhdr.h`](chxtfhdr.h.md)** ([`chxtfhdr.o`](chxtfhdr.o.md)) — Struct unpacking module that converts packed, byte-unaligned on-disk XTF character structures (`cXTFFILEHEADER`, `cXTFPINGHEADER`, `cXTFPINGCHANHEADER`, etc.) into aligned C structures.
* **[`bytes2func`](bytes2func.md)** & **[`bytes2func.h`](bytes2func.h.md)** ([`bytes2func.o`](bytes2func.o.md)) — Endian-aware conversion functions (`bytes2short`, `bytes2int`, `bytes2float`, `bytes2double`) controlled by the global `SWAP` flag for reading little-endian Intel `.xtf` files on big-endian SGI/Sun or little-endian Linux hosts.
* **[`xtf_doc.h`](xtf_doc.h.md)** — Complete Triton `.XTF` format specification header defining all packet types and C data structures (`XTFFILEHEADER`, `CHANINFO`, `XTFPINGHEADER`, `XTFPINGCHANHEADER`, `XTFATTITUDEDATA`, `XTFNOTESHEADER`, `XTFRAWSERIALHEADER`).
* **[`new_xtf.h`](new_xtf.h.md)** — Header defining `xtf2glo` normalization constants, bitmask flags (`RAW_FLAG`, `AUX_DEPTH`, `INTERP_NADIR`, `BOTTOM_DETECT`, `CMG`), and the `MBR` struct.
* **[`makefile`](makefile.md)** — Build configuration linking `xtf2glo.o`, `xtf_funcs.o`, `chxtfhdr.o`, and `bytes2func.o`.
