---
layout: default
title: sidescan/beam/oldstuff Suite
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 1
---

# Legacy GLORIA Beam Pattern Tools (`sidescan/beam/oldstuff`)

The `sidescan/beam/oldstuff` directory (`code/sidescan/beam/oldstuff/`) preserves the 1989–1990 generation of empirical beam pattern estimation and correction programs written by John Hughes Clarke for GLORIA MkII/MkIII long-range sidescan sonar data.

## Overview of the Workflow
Because theoretical transducer directivity and Time-Varying Gain (TVG) functions rarely eliminate all across-track shading artifacts, these utilities derive empirical corrections directly from slant-range corrected (`.slr`) sidescan passes:
1. **Accumulation**: [`glbeam_bypass`](glbeam_bypass.html) (`glbeam2`) or [`glbeambin`](glbeambin.html) scans a pass (`.slr`), calculates the flat-bottom grazing angle $\theta = \arccos(z / R)$ for every across-track sample, and accumulates mean Digital Numbers (DNs) into 1° grazing-angle bins (`0°–90°`), optionally stratified into twenty 500 m depth intervals (`0–10,000 m`).
2. **Multi-Pass Summation**: [`sumbeam.f`](sumbeam.f.html) or [`sumbeambin.f`](sumbeambin.f.html) combines `.beam_pattern` or `.beam_bin` files across multiple passes to suppress local geologic backscatter variations and isolate the repeatable transducer beam pattern.
3. **Visualization**: [`viewbeam.f`](viewbeam.f.html) plots the port and starboard empirical intensity curves or normalized correction factors against grazing angle (`-90°` to `+90°`).
4. **Application**: [`glbeam_bydepth`](glbeam_bydepth.html), [`glbeam_spline`](glbeam_spline.html), [`hack_glbeam`](hack_glbeam.html), or [`special_hack_glbeam`](special_hack_glbeam.html) normalizes the `.slr` scanlines using the derived lookup tables.

## Tools & Files in This Directory
* [`glbeam_bydepth`](glbeam_bydepth.html) — Depth-dependent empirical beam pattern correction.
* [`glbeam_bypass`](glbeam_bypass.html) — Single-pass empirical beam pattern extraction and removal (`glbeam2`).
* [`glbeam_spline`](glbeam_spline.html) — Spline-smoothed grazing-angle beam pattern correction.
* [`glbeambin`](glbeambin.html) — 2D grazing-angle (`91` bins) by water-depth (`20` bins) histogram accumulator.
* [`hack_glbeam`](hack_glbeam.html) — Customized empirical beam pattern remover for non-standard passes.
* [`special_hack_glbeam`](special_hack_glbeam.html) — Specialized beam pattern correction for passes with asymmetric port/starboard gain jumps.
* [`sumbeam.f`](sumbeam.f.html) — Fortran 77 multi-pass `.beam_pattern` averager.
* [`sumbeambin.f`](sumbeambin.f.html) — Fortran 77 multi-pass `.beam_bin` depth-binned summer and normalizer.
* [`viewbeam.f`](viewbeam.f.html) — Fortran 77 GPR/metafile plotter for `.beam_pattern` files.
* [`testbeam`](testbeam.html) & [`testbeam2`](testbeam2.html) — Example invocation scripts on SOPAC 1989 passes (`ps89_353.slr`, `ps89_365.slr`).
* [`makefile`](makefile.html) — Makefile building both C and Fortran 77 targets.
