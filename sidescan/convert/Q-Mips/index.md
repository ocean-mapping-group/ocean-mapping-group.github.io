---
layout: default
title: sidescan/convert/Q-Mips Suite
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 1
---

# Q-MIPS Conversion Tools (`sidescan/convert/Q-Mips`)

The `Q-Mips` subdirectory (`code/sidescan/convert/Q-Mips/`) contains the format converter for importing digital sidescan sonar data recorded by the Q-MIPS (and Triton Isis Q-MIPS) acquisition system into the Ocean Mapping Group's JCU GLORIA (`.ss`) processing pipeline.

## Available Tools

* **[`qmips2glo`](qmips2glo.html)** — Reads raw Q-MIPS digital sonar files (parsing the file header and per-ping telemetry blocks including navigation, towfish altitude, slant range, and multi-channel imagery), resamples port and starboard sonar channels to 496/512 pixels per side, and writes standard 1024-byte `gloria_rec` (`.ss`) scanlines.

## Workflow Context
After converting Q-MIPS files with [`qmips2glo`](qmips2glo.html), use [`azibat/smthazi`](../../azibat/smthazi.html) to smooth towfish headings, [`slant/bpick`](../../slant/bpick.html) and [`slant/glslant`](../../slant/glslant.html) for bottom tracking and slant-range rectification, and [`mapmos/mapmos`](../../mapmos/mapmos.html) for geographic mosaicking.
