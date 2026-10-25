---
layout: default
title: viewbeam.f
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 9
tool_name: viewbeam
source_path: code/sidescan/beam/oldstuff/viewbeam.f
category: Sidescan Beam Pattern Processing
input_formats:
- ASCII .beam_pattern (ps89_<pass>.beam_pattern)
output_formats:
- Interactive GPR display
- Mutoh / HP7475 / Report plot metafile
related_tools:
- glbeam_bypass
- sumbeam.f
- sumbeambin.f
---

# viewbeam.f (`viewbeam`)

## Description
`viewbeam.f` is an interactive Fortran 77 plotting utility (John Hughes Clarke, December 1989) that visualizes empirical GLORIA port and starboard beam pattern curves (`ps89_<pass>.beam_pattern`) across grazing angles from `-90°` (port) to `+90°` (starboard). It supports both interactive Apollo GPR graphics display and hardcopy plotfile output (Mutoh, HP7475, or Report sizes).

## Usage & Interactive Prompts

```bash
viewbeam
```
Interactive prompts:
1. **`plot to screen (0) or plotfile(1)?`** — Selects interactive screen preview or metafile output (`enter plotfile name` and format: `1=mutoh`, `2=hp7475`, `3=report`).
2. **`do you want to see corrections (0) or averages (1)?`** — Selects either the normalized gain correction factors (Y-axis `0.0` to `2.0`) or the raw mean DN values (Y-axis `0.0` to `255.0`).
3. **`enter Pass no.`** — 3-character pass identifier (`pass`), opening `/u/jhc/data/sopac/gloria/ps89_<pass>.beam_pattern`.
4. After drawing the axes, grid ticks (every `10°` horizontally), title (`GLORIA Empirical Beam Pattern`), and port (`-90°..0°`) / starboard (`0°..+90°`) curves, prompts **`another pass ? (y/n)`** to overplot additional passes for comparison.
