---
layout: default
title: Print Tools
parent: Sidescan Tools
nav_order: 9
has_children: true
---

# Mosaic Printing Tools (`sidescan/print`)

The `print` directory (`code/sidescan/print/`) contains utilities for formatting and rendering completed sidescan sonar mosaics onto hardcopy plotters and printers.

## Available Tools

* **[`printmos`](printmos.md)** — Reads a gridded sidescan mosaic produced by [`mapmos`](../mapmos/mapmos.md) and formats the 8-bit acoustic intensity array for hardcopy output with scale bars and geographic annotations.

## Workflow Context
After slant-range correcting (`glslant`), beam-correcting (`debeam`), destriping (`destripe`), and mosaicking (`mapmos`) GLORIA or multibeam sidescan lines, [`printmos`](printmos.md) (or [`image/OMGtoPS`](../../image/OMGtoPS.md) and [`image/stretchacres`](../../image/stretchacres.md)) is used to generate publication and shipboard plotting outputs.
