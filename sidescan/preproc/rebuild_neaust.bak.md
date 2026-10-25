---
layout: default
title: rebuild_neaust.bak
parent: Preprocessing Tools
grand_parent: Sidescan Tools
nav_order: 3
tool_name: rebuild_neaust.bak
source_path: code/sidescan/preproc/rebuild_neaust.bak
category: Sidescan Preprocessing
input_formats: ["Raw IOS GLORIA (.ios)"]
output_formats: ["Slant-range corrected (.slr)", "Beam-corrected (.beam)"]
related_tools: ["rebuild_neaust", "neaust_fixazi", "mapbeam", "debeam"]
---

# rebuild_neaust.bak

## Description
`rebuild_neaust.bak` is an earlier backup revision of [`rebuild_neaust`](rebuild_neaust.md) (Guy Carpenter, November 7, 1990) in `code/sidescan/preproc/` before the addition of the post-beam azimuth repair (`neaust_fixazi`), time-mark repair (`fixmark`), and multi-survey beam map joining (`joinbeam`) stages.

## Pipeline Stages Executed
1. **Stage 1 (`gainmed_neaust`)**: Computes median gain tables (`gain.ave`, `gain.pass`) across all raw `.ios` files in `/home/daintree/data/neaust/gloria/raw/`.
2. **Stage 2 (`preprocI_plus`)**: Loops through passes `001` to `062`, converting raw `.ios` files into slant-range corrected `.slr` files.
3. **Stage 3 ([`mapbeam`](../beammap/mapbeam.md))**: Iteratively builds the 2D depth-vs-across-track empirical beam map (`neaust.map`, `neaust.cnt`) from all 62 `.slr` passes.
4. **Stage 4 (`debeam2`)**: Removes the empirical beam shading from each `.slr` pass using `neaust.map` and `neaust.cnt`, writing output `.beam` files to `/u/guy/data/neaust/gloria/beam/`.
