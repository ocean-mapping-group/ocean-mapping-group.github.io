---
layout: default
title: sumbeambin.f
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 8
tool_name: sumbeambin
source_path: code/sidescan/beam/oldstuff/sumbeambin.f
category: Sidescan Beam Pattern Processing
input_formats:
- ASCII .beam_bin (ps89_<pass>.beam_bin)
output_formats:
- 20 depth-stratified .beam_pattern files (ps89_025..ps89_975.beam_pattern)
related_tools:
- glbeambin
- glbeam_bydepth
- sumbeam.f
- viewbeam.f
---

# sumbeambin.f (`sumbeambin`)

## Description
`sumbeambin.f` is a Fortran 77 utility (John Hughes Clarke, December 1989) that reads depth-stratified empirical beam histogram files (`ps89_<pass>.beam_bin`, produced by [`glbeambin`](glbeambin.html)) across multiple GLORIA passes, accumulates sample counts and amplitude sums across 91 grazing-angle bins (`0°–90°`) and 20 water-depth bins (`0–10,000 m` in `500 m` increments), and outputs 20 depth-specific `.beam_pattern` files (`ps89_025.beam_pattern` through `ps89_975.beam_pattern`) for use by [`glbeam_bydepth`](glbeam_bydepth.html).

## Usage & Interactive Prompts

```bash
sumbeambin
```
Interactive prompts:
1. **`enter number of beam patterns to sum`** — Number of passes `n` (up to 100).
2. **`enter pass numbers`** — List of 3-character pass IDs (`pass(k)`), reading `/u/jhc/data/sopac/gloria/ps89_<pass>.beam_bin`.

## Algorithm
1. For each pass `k`, reads 20 depth blocks (`j = 1..20`) of 91 grazing-angle rows (`i = 1..91`):
   `port_no`, `port_sum`, `stbd_no`, `stbd_sum` in `(4(i9,2x))` format.
2. Accumulates total sample counts (`tport_no`, `tstbd_no`) and DN sums (`tport_sum`, `tstbd_sum`) for every `(angle, depth)` bin.
3. Computes the mean DN for each bin (`port_ave = tport_sum / tport_no`, `stbd_ave = tstbd_sum / tstbd_no`) and the multiplicative gain factor normalized to mid-grey (`128.0 / ave`, or `1.0` where count is zero).
4. Writes 20 output files named `ps89_<depth>.beam_pattern` (`025`, `075`, ..., `975`, representing bin center depths from `250 m` to `9750 m` in tens of meters).
