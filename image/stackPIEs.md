---
layout: default
title: stackPIEs
parent: Image Tools
nav_order: 48
tool_name: stackPIEs
source_path: code/image/stackPIEs.c
category: Multibeam Water Column & Acoustic Modeling
input_formats: ["OMG1 .wcim water-column polar fan ('pie') images"]
output_formats: ["Stacked/averaged .wcim or .pgm water-column fan images", "Optional horiz/vert slice composites"]
related_tools: ["TAtoXZ", "patchTA", "comboTAs", "comboVPs", "stretchacres"]
---

# stackPIEs

## Description
`stackPIEs` (written by John Hughes Clarke, 2002) stacks and averages sliding windows of multibeam water-column polar fan ("pie") `.wcim` images to suppress acoustic speckle, optionally overlaying range/depth graticules (`-add_graticule`), frame sequence counters (`-add_sequence`), tidal vertical datum shifts (`-tide`), rotational cross-correlation alignment (`-try_rot_correl`), and simultaneous horizontal/vertical curtain slices (`-appendSlice`).

## CLI Options & Usage
```bash
stackPIEs [-stack <n>] [-nostacks <max>] [-preserve_frame_no] [-startframeno <n>] \
  [-add_graticule] [-add_sequence] [-pgm] [-str_result <min> <max>] \
  [-appendSlice -horiz <depth_m> -verti <across_m> -window <m>] \
  [-tide <tidefile>] [-try_rot_correl <x> <y> <rad> -DN_threshold <val>] \
  -out <outprefix> <file1.wcim> [<file2.wcim> ...]
```
* **`-stack <n>`**: Number of consecutive `.wcim` frames averaged per output frame (default: `8`).
* **`-nostacks <max>`**: Maximum number of stacked output frames to generate.
* **`-preserve_frame_no` / `-startframeno <n>`**: Controls output frame numbering (`<outprefix>.0001.wcim`).
* **`-add_graticule`**: Draws horizontal depth lines and vertical across-track offset ticks (`10 m` and `50 m` intervals) plus the transducer apex onto each fan.
* **`-add_sequence`**: Annotates ping timestamp (`YYYY/DDD HH:MM:SS`) and frame counter using embedded bitmap digits (`digits.h`).
* **`-pgm`**: Writes Netpbm `.pgm` images instead of `OMG1` `.wcim` files.
* **`-str_result <min> <max>`**: Linearly stretches stacked pixel intensities between `<min>` and `<max>`.
* **`-appendSlice -horiz <z> -verti <x> -window <w>`**: Appends time-series curtain slices extracted at depth `<z>` and across-track offset `<x>` alongside the polar fan.
* **`-tide <tidefile>`**: Shifts each frame vertically according to predicted/observed tide height (`read_predicted_tide()`).
* **`-try_rot_correl <x> <y> <rad>`**: Estimates rotational flow velocity inside a circular ROI between consecutive frames.

## Algorithm
Maintains a circular buffer of `<stack>` `.wcim` frames, computes the per-pixel temporal mean across the window, applies optional contrast stretch, graticule/timestamp rendering, and slice appending, and writes sequential `.wcim` or `.pgm` animation frames.
