---
layout: default
title: convSUB16.c2
parent: GeoSwath+ / Submetrix 2000 CLI (sub2k)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 11
tool_name: convSUB16.c2
source_path: sub2k/convSUB16.c2
category: sub2k
input_formats:
- Submetrix 16-bit raw (.sub)
output_formats:
- OMG Swath Bathymetry (.merged)
- OMG Sidescan (.ss_data)
related_tools:
- convSUB16
- readSUB2K
---

# `convSUB16.c2` — Alternate Revision of `convSUB16`

## Overview

`sub2k/convSUB16.c2` is an archived development revision of [`convSUB16.c`](convSUB16.html) preserved in the `sub2k/` source directory. Like `convSUB16`, it reads 16-bit Submetrix ISIS interferometric sonar files (`.sub`) and converts the multi-stave phase and amplitude time series into Ocean Mapping Group `.merged` swath bathymetry and `.ss_data` sidescan files.

---

## Usage

`convSUB16.c2` is not compiled by default in [`sub2k/makefile`](makefile.html) (which compiles `convSUB16.c`). If compiled manually, its command-line syntax matches [`convSUB16`](convSUB16.html):

```bash
convSUB16 -in <input.sub> -out <output_prefix> [options]
```

---

## Key Details & Relationship to `convSUB16.c`

- **Purpose:** Retained in the repository as a backup/intermediate checkpoint during updates to 16-bit Submetrix interferometric amplitude scaling and Vernier phase-unwrapping logic.
- **Production Equivalent:** Use [`convSUB16`](convSUB16.html) or [`readSUB2K`](readSUB2K.html) for production conversion of Submetrix `.sub` and `.rrc` datasets.
