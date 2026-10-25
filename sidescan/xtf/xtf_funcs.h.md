---
layout: default
title: xtf_funcs.h
parent: XTF Tools
grand_parent: Sidescan Tools
nav_order: 11
tool_name: xtf_funcs.h
source_path: code/sidescan/xtf/xtf_funcs.h
category: XTF Sidescan Conversion
input_formats: ["C Header File"]
output_formats: ["Included by xtf_funcs.c, xtf2glo.c"]
related_tools: ["xtf_funcs", "xtf2glo", "xtf_doc.h", "chxtfhdr.h"]
---

# xtf_funcs.h

## Description
`xtf_funcs.h` is the C header file in `code/sidescan/xtf/` declaring the high-level `.XTF` file header and data packet reader functions implemented in [`xtf_funcs.c`](xtf_funcs.md).

## Function Prototypes

```c
int readXTFheader(FILE *fp, XTFFILEHEADER *XTFhdr);
int readXTFdata(FILE *fp, unsigned char *buffer);
```

* **`readXTFheader(FILE *fp, XTFFILEHEADER *XTFhdr)`**: Reads the initial 1024-byte XTF file header (plus any extended channel headers if total channel count exceeds 6), unpacks it via `convXTFFILEHEADER()`, and returns the number of channel headers read (`>0` on success, `0` on failure).
* **`readXTFdata(FILE *fp, unsigned char *buffer)`**: Reads the next variable-length packet (`XTF_HEADER_SONAR`, `XTF_HEADER_ATTITUDE`, `XTF_HEADER_NOTES`, etc.) from `fp` into `buffer` by inspecting the magic byte `0xFACE` and the 32-bit `NumBytesThisRecord` field at byte offset 10.
