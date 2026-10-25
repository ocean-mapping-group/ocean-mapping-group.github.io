---
layout: default
title: makefile (mock)
parent: Mock Tools
grand_parent: Sidescan Tools
nav_order: 30
tool_name: makefile
source_path: code/sidescan/mock/makefile
category: Build Configuration
input_formats: [".c"]
output_formats: ["Executable binaries (synthetic, build_back, build_back_mos, back_char, back_stack, selective_back, view_sel, beams, modarray, modbeam, showgains, etc.)"]
related_tools: ["synthetic", "build_back", "build_back_mos", "back_char", "back_stack", "selective_back", "view_sel", "beams", "modarray", "modbeam", "showgains"]
---

# makefile (`sidescan/mock`)

## Overview
The `makefile` in `code/sidescan/mock/` compiles the C-based synthetic sidescan forward-modeling, transducer beam directivity simulation, TVG modeling, and angular backscatter analysis tools.

## Build Targets

Targets link against `$(LIBS)` (`-llocal -ljhc -lm`), with `view_sel` additionally linking `-lX11` for interactive X Window plotting:

* **Forward Modeling & Bathymetric Co-Registration**:
  * [`synthetic`](synthetic.md) — Synthetic sidescan generator from 3D bathymetric DTMs.
  * [`build_back`](build_back.md) & [`build_back_mos`](build_back_mos.md) — Computes true 3D seafloor grazing angles by combining sidescan records with gridded bathymetry.
* **Angular Backscatter Analysis**:
  * [`back_char`](back_char.md) & [`back_stack`](back_stack.md) — Characterizes and stacks angular backscatter curves.
  * [`selective_back`](selective_back.md) — Extracts backscatter vs. grazing angle within selected regions.
  * [`view_sel`](view_sel.md) — X11 interactive viewer for `selective_back` outputs.
* **Transducer Directivity & TVG Simulation**:
  * [`beams`](beams.md), [`oldbeams`](oldbeams.md), [`modarray`](modarray.md), [`modbeam`](modbeam.md) — Array directivity and beam pattern models.
  * [`showgains`](showgains.md), [`test_tvg_effect`](test_tvg_effect.md), [`test_tvg_dirindex`](test_tvg_dirindex.md), [`testbell`](testbell.md), [`offtrack`](offtrack.md), [`binplot`](binplot.md) — Gain, TVG, and angular response diagnostics.

## Usage
```bash
cd code/sidescan/mock
make synthetic build_back build_back_mos back_char back_stack selective_back view_sel
```
