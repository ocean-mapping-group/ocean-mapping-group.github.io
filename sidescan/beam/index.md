---
layout: default
title: Beam Tools
parent: Sidescan Tools
nav_order: 2
has_children: true
---

# Beam Tools (`sidescan/beam`)

The `beam` directory (`code/sidescan/beam/`) houses legacy empirical beam-pattern estimation, depth-binning, and visualization utilities developed for GLORIA long-range sidescan sonar surveys (such as the 1989 SOPAC and Northeast Australia cruises). These tools were subsequently superseded by the 2D depth-vs-angle lookup architecture in [`beammap/`](../beammap/index.md) (`mapbeam`, `debeam`, and `joinbeam`).

## Subdirectories & Tools

* **[Legacy Beam Pattern Suite (`oldstuff/`)](oldstuff/index.md)**
  * [`glbeam_bydepth`](oldstuff/glbeam_bydepth.md) — Applies depth-stratified empirical beam pattern corrections to slant-range corrected GLORIA scanlines.
  * [`glbeam_bypass`](oldstuff/glbeam_bypass.md) — Computes and removes pass-averaged port and starboard grazing-angle beam patterns (`glbeam2`).
  * [`glbeam_spline`](oldstuff/glbeam_spline.md) — Fits cubic splines across empirical grazing-angle intensity curves for smooth radiometric compensation.
  * [`glbeambin`](oldstuff/glbeambin.md) — Accumulates port and starboard acoustic intensities into 91 grazing-angle bins (`0°–90°`) by 20 water-depth bins (`0–10000 m` in `500 m` increments).
  * [`hack_glbeam`](oldstuff/hack_glbeam.md) & [`special_hack_glbeam`](oldstuff/special_hack_glbeam.md) — Custom pass-specific beam pattern correction utilities for anomalous transducer gain states.
  * [`sumbeam.f`](oldstuff/sumbeam.f.md) & [`sumbeambin.f`](oldstuff/sumbeambin.f.md) — Fortran 77 programs for summing and normalizing empirical beam patterns across multiple survey passes.
  * [`viewbeam.f`](oldstuff/viewbeam.f.md) — Fortran 77 interactive plotting tool for inspecting port/starboard empirical beam patterns vs. grazing angle.
  * [`testbeam`](oldstuff/testbeam.md) & [`testbeam2`](oldstuff/testbeam2.md) — C-shell test scripts for running `glbeam2` on SOPAC GLORIA `.slr` passes.
  * [`makefile`](oldstuff/makefile.md) — Build rules for compiling the C and Fortran 77 beam pattern tools.
