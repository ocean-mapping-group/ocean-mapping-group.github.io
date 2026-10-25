---
layout: default
title: readSUB2K.c.pre_danforth_20071016
parent: GeoSwath+ / Submetrix 2000 CLI (sub2k)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 12
tool_name: readSUB2K.c.pre_danforth_20071016
source_path: sub2k/readSUB2K.c.pre_danforth_20071016
category: sub2k
input_formats:
- Submetrix 2000 (.sub, .rrc)
output_formats:
- OMG Swath Bathymetry (.merged)
- OMG Sidescan (.ss_data)
- OMG Navigation (.nav)
related_tools:
- readSUB2K
- makefile_BWD
---

# `readSUB2K.c.pre_danforth_20071016` — Pre-2007 Baseline Snapshot of `readSUB2K`

## Overview

`sub2k/readSUB2K.c.pre_danforth_20071016` is the preserved baseline source file of [`readSUB2K.c`](readSUB2K.html) prior to modifications contributed by Bill Danforth (U.S. Geological Survey) on October 16, 2007.

---

## Usage

This file is an archived C source snapshot and is not built by default in [`sub2k/makefile`](makefile.html). For active usage, CLI options, and processing details, see [`readSUB2K`](readSUB2K.html):

```bash
readSUB2K -in <input.rrc> -out <output_prefix> [-spacing <m>] [-thresh <val>]
```

---

## Key Historical Context

- **Snapshot Date:** October 16, 2007.
- **Role in Repository:** Preserves the original OMG Submetrix 2000 (`.sub` / `.rrc`) interferometric phase-unwrapping, stave angle calibration, and bathymetric across-track binning implementation prior to USGS Linux portability and processing updates.
- **Production Equivalent:** [`readSUB2K`](readSUB2K.html) (`sub2k/readSUB2K.c`).
