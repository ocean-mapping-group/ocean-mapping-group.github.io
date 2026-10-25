---
layout: default
title: Old Stuff
parent: Beam Tools
grand_parent: Sidescan Tools
nav_order: 1
has_children: true
---

# Legacy GLORIA Beam Pattern Tools (`sidescan/beam/oldstuff`)

The `sidescan/beam/oldstuff` directory (`code/sidescan/beam/oldstuff/`) preserves the 1989–1990 generation of empirical beam pattern estimation and correction programs written by John Hughes Clarke for GLORIA MkII/MkIII long-range sidescan sonar data.

## Overview of the Workflow
Because theoretical transducer directivity and Time-Varying Gain (TVG) functions rarely eliminate all across-track shading artifacts, these utilities derive empirical corrections directly from slant-range corrected (`.slr`) sidescan passes:
1. **Accumulation**: [`glbeam_bypass`](glbeam_bypass.md) (`glbeam2`) or [`glbeambin`](glbeambin.md) scans a pass (`.slr`), calculates the flat-bottom grazing angle $\theta = \arccos(z / R)$ for every across-track sample, and accumulates mean Digital Numbers (DNs) into 1° grazing-angle bins (`0°–90°`), optionally stratified into twenty 500 m depth intervals (`0–10,000 m`).
2. **Multi-Pass Summation**: [`sumbeam.f`](sumbeam.f.md) or [`sumbeambin.f`](sumbeambin.f.md) combines `.beam_pattern` or `.beam_bin` files across multiple passes to suppress local geologic backscatter variations and isolate the repeatable transducer beam pattern.
3. **Visualization**: [`viewbeam.f`](viewbeam.f.md) plots the port and starboard empirical intensity curves or normalized correction factors against grazing angle (`-90°` to `+90°`).
4. **Application**: [`glbeam_bydepth`](glbeam_bydepth.md), [`glbeam_spline`](glbeam_spline.md), [`hack_glbeam`](hack_glbeam.md), or [`special_hack_glbeam`](special_hack_glbeam.md) normalizes the `.slr` scanlines using the derived lookup tables.

## Tools & Files in This Directory
* [`glbeam_bydepth`](glbeam_bydepth.md) — Depth-dependent empirical beam pattern correction.
* [`glbeam_bypass`](glbeam_bypass.md) — Single-pass empirical beam pattern extraction and removal (`glbeam2`).
* [`glbeam_spline`](glbeam_spline.md) — Spline-smoothed grazing-angle beam pattern correction.
* [`glbeambin`](glbeambin.md) — 2D grazing-angle (`91` bins) by water-depth (`20` bins) histogram accumulator.
* [`hack_glbeam`](hack_glbeam.md) — Customized empirical beam pattern remover for non-standard passes.
* [`special_hack_glbeam`](special_hack_glbeam.md) — Specialized beam pattern correction for passes with asymmetric port/starboard gain jumps.
* [`sumbeam.f`](sumbeam.f.md) — Fortran 77 multi-pass `.beam_pattern` averager.
* [`sumbeambin.f`](sumbeambin.f.md) — Fortran 77 multi-pass `.beam_bin` depth-binned summer and normalizer.
* [`viewbeam.f`](viewbeam.f.md) — Fortran 77 GPR/metafile plotter for `.beam_pattern` files.
* [`testbeam`](testbeam.md) & [`testbeam2`](testbeam2.md) — Example invocation scripts on SOPAC 1989 passes (`ps89_353.slr`, `ps89_365.slr`).
* [`makefile`](makefile.md) — Makefile building both C and Fortran 77 targets.
