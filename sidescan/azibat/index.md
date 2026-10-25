---
layout: default
title: sidescan/azibat Suite
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 1
---

# Azibat Tools (`sidescan/azibat`)

The `azibat` directory (`code/sidescan/azibat/`) provides utilities for inspecting, editing, smoothing, and merging towfish heading (azimuth), navigation fixes, timestamps, and water depth records inside JCU GLORIA (`.ss`) sidescan files. Accurate towfish azimuth and altitude/depth are critical prerequisites for empirical beam pattern removal (`debeam`), slant-range rectification (`glslant`), and geographic mosaicking (`mapmos`).

## Available Tools

* **[`editazi`](editazi.html)** — Inspects and edits per-ping towfish magnetic/true azimuth fields in a JCU GLORIA sidescan file.
* **[`editbat`](editbat.html)** — Edits and interpolates nadir water depth (bathymetry) values embedded in GLORIA scanline headers.
* **[`editfix`](editfix.html)** — Edits navigation fix timestamps and positions in GLORIA scanline headers.
* **[`editpos`](editpos.html)** — Modifies or interpolates ship/towfish latitude and longitude coordinates across scanline ranges.
* **[`interpTime`](interpTime.html)** — Linearly interpolates missing or duplicate ping timestamps across continuous sidescan records.
* **[`makeazi`](makeazi.html)** — Computes course-made-good (CMG) azimuth from consecutive navigation fixes and writes it into the GLORIA header azimuth field.
* **[`mergebat`](mergebat.html)** — Merges external bathymetry time-series profiles into GLORIA scanline headers by matching ping timestamps.
* **[`smthazi`](smthazi.html)** — Applies temporal low-pass smoothing (`-t`, `-f`) to noisy towfish compass headings to prevent fan-like swath overlaps and gaps during mosaicking.
* **[`smthbpick`](smthbpick.html)** — Smooths bottom-pick travel-time/depth profiles along-track prior to slant-range correction (`glslant`).

## Typical Workflow
1. Import raw sidescan data into `.ss` format (`ios2glo`, `usgs2glo`, `xtf2glo`).
2. Repair timestamp and navigation glitches using [`interpTime`](interpTime.html), [`editfix`](editfix.html), and [`editpos`](editpos.html).
3. Compute or merge towfish heading (`makeazi`, `azimerge`) and filter high-frequency yaw oscillation with [`smthazi`](smthazi.html).
4. Merge external echo-sounder depth (`mergebat`) or smooth picked bottom depths (`smthbpick`) before running [`glslant`](../slant/glslant.html).
