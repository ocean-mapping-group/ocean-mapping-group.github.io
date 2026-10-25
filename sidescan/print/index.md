---
layout: default
title: sidescan/print Suite
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 9
---

# Mosaic Printing Tools (`sidescan/print`)

The `print` directory (`code/sidescan/print/`) contains utilities for formatting and rendering completed sidescan sonar mosaics onto hardcopy plotters and printers.

## Available Tools

* **[`printmos`](printmos.html)** — Reads a gridded sidescan mosaic produced by [`mapmos`](../mapmos/mapmos.html) and formats the 8-bit acoustic intensity array for hardcopy output with scale bars and geographic annotations.

## Workflow Context
After slant-range correcting (`glslant`), beam-correcting (`debeam`), destriping (`destripe`), and mosaicking (`mapmos`) GLORIA or multibeam sidescan lines, [`printmos`](printmos.html) (or [`image/OMGtoPS`](../../image/OMGtoPS.html) and [`image/stretchacres`](../../image/stretchacres.html)) is used to generate publication and shipboard plotting outputs.
