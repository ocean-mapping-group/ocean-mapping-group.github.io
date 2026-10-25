---
layout: default
title: Azibat Tools
parent: Sidescan Tools
nav_order: 1
has_children: true
---

# Azibat Tools (`sidescan/azibat`)

The `azibat` directory (`code/sidescan/azibat/`) provides utilities for inspecting, editing, smoothing, and merging towfish heading (azimuth), navigation fixes, timestamps, and water depth records inside JCU GLORIA (`.ss`) sidescan files. Accurate towfish azimuth and altitude/depth are critical prerequisites for empirical beam pattern removal (`debeam`), slant-range rectification (`glslant`), and geographic mosaicking (`mapmos`).

## Available Tools

* **[`editazi`](editazi.md)** — Inspects and edits per-ping towfish magnetic/true azimuth fields in a JCU GLORIA sidescan file.
* **[`editbat`](editbat.md)** — Edits and interpolates nadir water depth (bathymetry) values embedded in GLORIA scanline headers.
* **[`editfix`](editfix.md)** — Edits navigation fix timestamps and positions in GLORIA scanline headers.
* **[`editpos`](editpos.md)** — Modifies or interpolates ship/towfish latitude and longitude coordinates across scanline ranges.
* **[`interpTime`](interpTime.md)** — Linearly interpolates missing or duplicate ping timestamps across continuous sidescan records.
* **[`makeazi`](makeazi.md)** — Computes course-made-good (CMG) azimuth from consecutive navigation fixes and writes it into the GLORIA header azimuth field.
* **[`mergebat`](mergebat.md)** — Merges external bathymetry time-series profiles into GLORIA scanline headers by matching ping timestamps.
* **[`smthazi`](smthazi.md)** — Applies temporal low-pass smoothing (`-t`, `-f`) to noisy towfish compass headings to prevent fan-like swath overlaps and gaps during mosaicking.
* **[`smthbpick`](smthbpick.md)** — Smooths bottom-pick travel-time/depth profiles along-track prior to slant-range correction (`glslant`).

## Typical Workflow
1. Import raw sidescan data into `.ss` format (`ios2glo`, `usgs2glo`, `xtf2glo`).
2. Repair timestamp and navigation glitches using [`interpTime`](interpTime.md), [`editfix`](editfix.md), and [`editpos`](editpos.md).
3. Compute or merge towfish heading (`makeazi`, `azimerge`) and filter high-frequency yaw oscillation with [`smthazi`](smthazi.md).
4. Merge external echo-sounder depth (`mergebat`) or smooth picked bottom depths (`smthbpick`) before running [`glslant`](../slant/glslant.md).
