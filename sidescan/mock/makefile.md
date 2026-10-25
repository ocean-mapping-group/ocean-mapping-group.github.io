---
layout: default
title: makefile (mock)
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 30
tool_name: makefile
source_path: code/sidescan/mock/makefile
category: Build Configuration
input_formats:
- .c
output_formats:
- Executable binaries (synthetic, build_back, build_back_mos, back_char, back_stack, selective_back, view_sel, beams, modarray, modbeam, showgains, etc.)
related_tools:
- synthetic
- build_back
- build_back_mos
- back_char
- back_stack
- selective_back
- view_sel
- beams
- modarray
- modbeam
- showgains
---

# makefile (`sidescan/mock`)

## Overview
The `makefile` in `code/sidescan/mock/` compiles the C-based synthetic sidescan forward-modeling, transducer beam directivity simulation, TVG modeling, and angular backscatter analysis tools.

## Build Targets

Targets link against `$(LIBS)` (`-llocal -ljhc -lm`), with `view_sel` additionally linking `-lX11` for interactive X Window plotting:

* **Forward Modeling & Bathymetric Co-Registration**:
  * [`synthetic`](synthetic.html) — Synthetic sidescan generator from 3D bathymetric DTMs.
  * [`build_back`](build_back.html) & [`build_back_mos`](build_back_mos.html) — Computes true 3D seafloor grazing angles by combining sidescan records with gridded bathymetry.
* **Angular Backscatter Analysis**:
  * [`back_char`](back_char.html) & [`back_stack`](back_stack.html) — Characterizes and stacks angular backscatter curves.
  * [`selective_back`](selective_back.html) — Extracts backscatter vs. grazing angle within selected regions.
  * [`view_sel`](view_sel.html) — X11 interactive viewer for `selective_back` outputs.
* **Transducer Directivity & TVG Simulation**:
  * [`beams`](beams.html), [`oldbeams`](oldbeams.html), [`modarray`](modarray.html), [`modbeam`](modbeam.html) — Array directivity and beam pattern models.
  * [`showgains`](showgains.html), [`test_tvg_effect`](test_tvg_effect.html), [`test_tvg_dirindex`](test_tvg_dirindex.html), [`testbell`](testbell.html), [`offtrack`](offtrack.html), [`binplot`](binplot.html) — Gain, TVG, and angular response diagnostics.

## Usage

```bash
cd code/sidescan/mock
make synthetic build_back build_back_mos back_char back_stack selective_back view_sel
```
