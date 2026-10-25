---
layout: default
title: Q-Mips Tools
parent: Convert Tools
grand_parent: Sidescan Tools
nav_order: 1
has_children: true
---

# Q-MIPS Conversion Tools (`sidescan/convert/Q-Mips`)

The `Q-Mips` subdirectory (`code/sidescan/convert/Q-Mips/`) contains the format converter for importing digital sidescan sonar data recorded by the Q-MIPS (and Triton Isis Q-MIPS) acquisition system into the Ocean Mapping Group's JCU GLORIA (`.ss`) processing pipeline.

## Available Tools

* **[`qmips2glo`](qmips2glo.md)** — Reads raw Q-MIPS digital sonar files (parsing the file header and per-ping telemetry blocks including navigation, towfish altitude, slant range, and multi-channel imagery), resamples port and starboard sonar channels to 496/512 pixels per side, and writes standard 1024-byte `gloria_rec` (`.ss`) scanlines.

## Workflow Context
After converting Q-MIPS files with [`qmips2glo`](qmips2glo.md), use [`azibat/smthazi`](../../azibat/smthazi.md) to smooth towfish headings, [`slant/bpick`](../../slant/bpick.md) and [`slant/glslant`](../../slant/glslant.md) for bottom tracking and slant-range rectification, and [`mapmos/mapmos`](../../mapmos/mapmos.md) for geographic mosaicking.
