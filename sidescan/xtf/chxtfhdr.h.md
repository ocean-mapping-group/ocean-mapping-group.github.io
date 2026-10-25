---
layout: default
title: chxtfhdr.h
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 7
tool_name: chxtfhdr.h
source_path: code/sidescan/xtf/chxtfhdr.h
category: XTF Sidescan Conversion
input_formats:
- C Header File
output_formats:
- Included by chxtfhdr.c, xtf_funcs.c, xtf2glo.c
related_tools:
- chxtfhdr
- xtf_doc.h
- xtf_funcs
- xtf2glo
---

# chxtfhdr.h

## Description
`chxtfhdr.h` is the C header file in `code/sidescan/xtf/` that defines raw byte-packed character-array structures (`cCHANINFO`, `cXTFFILEHEADER`, `cXTFPINGHEADER`, `cXTFPINGCHANHEADER`, `cXTFATTITUDEDATA`, `cXTFNOTESHEADER`, `cXTFRAWSERIALHEADER`) matching the exact on-disk layout of Triton `.XTF` packets without compiler struct padding.

## Unaligned Structures & Conversion Prototypes

Because RISC and 64-bit C compilers insert alignment padding between `char` (`1` byte), `short` (`2` bytes), `int`/`float` (`4` bytes), and `double` (`8` bytes) struct members, `fread()` cannot read `.xtf` headers directly into native C structs (`XTFFILEHEADER`, etc. in [`xtf_doc.h`](xtf_doc.h.html)). Instead, `chxtfhdr.h` defines every multi-byte field as `unsigned char field[2/4/8]` and declares the unpacking functions implemented in [`chxtfhdr.c`](chxtfhdr.html):

* `void convXTFFILEHEADER(cXTFFILEHEADER *, XTFFILEHEADER *)`
* `void convCHANINFO(cCHANINFO *, CHANINFO *)`
* `void convXTFPINGHEADER(cXTFPINGHEADER *, XTFPINGHEADER *)`
* `void convXTFPINGCHANHEADER(cXTFPINGCHANHEADER *, XTFPINGCHANHEADER *)`
* `void convXTFATTITUDEDATA(cXTFATTITUDEDATA *, XTFATTITUDEDATA *)`
* `void convXTFNOTESHEADER(cXTFNOTESHEADER *, XTFNOTESHEADER *)`
* `void convXTFRAWSERIALHEADER(cXTFRAWSERIALHEADER *, XTFRAWSERIALHEADER *)`
