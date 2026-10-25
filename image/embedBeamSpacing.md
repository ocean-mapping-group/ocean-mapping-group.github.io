---
layout: default
title: embedBeamSpacing
parent: Image Tools
nav_order: 19
tool_name: embedBeamSpacing
source_path: code/image/embedBeamSpacing.c
category: Multibeam Water Column & Acoustic Modeling
input_formats: ["OMG1 8-bit terrain/backscatter image"]
output_formats: ["Annotated OMG1 8-bit image with simulated multibeam beam footprints"]
related_tools: ["showCoverage", "stretchacres", "OMGtoPS"]
---

# embedBeamSpacing

## Description
`embedBeamSpacing` (written by John Hughes Clarke, May 2014) models and draws multibeam echo-sounder across-track/along-track beam spacing crosses and actual `-3 dB` elliptical beam footprints (`fa_beamwidth × ps_beamwidth`) directly onto a georeferenced 8-bit `OMG1` seafloor image. It supports single-sector, multi-sector yaw/pitch-stabilized (`-no_sectors 3`), and dual-swath (`-multi_swath`) Kongsberg EM-style transmission geometries.

## CLI Options & Usage
```bash
embedBeamSpacing -in <infile> -out <outfile> \
  [-depth <m>] [-angle_on_target <deg>] [-speed_knots <kn>] \
  [-ping_period_percent_max_twtt <pct>] [-max_angle <deg>] [-no_beams <n>] \
  [-multi_swath] [-no_sectors <1|3>] \
  [-fa_beamwidth <deg> -ps_beamwidth <deg> [-draw_aspect]]
```
* **`-in <infile> -out <outfile>`**: Input and output 8-bit `OMG1` images (uses `head.dx` for pixel scale in meters).
* **`-depth <m>`**: Simulated water depth in meters (default: `100.0 m`) or derived from `-angle_on_target <deg>`.
* **`-speed_knots <kn>`**: Vessel survey speed in knots (default: `10.0 kn`).
* **`-ping_period_percent_max_twtt <pct>`**: Ping repetition period as a percentage of two-way travel time at the outer beam (default: `120%`).
* **`-max_angle <deg>`**: Maximum outer beam launch angle (default: `60.0°`).
* **`-no_beams <n>`**: Number of equidistant or equiangular (`>1000` flag) beams per swath (default: `100`).
* **`-multi_swath`**: Simulates dual-swath (2 swaths per ping cycle) along-track spacing.
* **`-no_sectors <1|3>`**: Models 3 transmit sectors (`-65°..-35°`, `-35°..+35°`, `+35°..+65°`) with along-track sector offsets.
* **`-fa_beamwidth <deg> -ps_beamwidth <deg>`**: Fore-aft and port-starboard transducer beamwidths at nadir (scales with `1/cos(steer)` and `1/cos(angle)` across the swath).
* **`-draw_aspect`**: Draws the full projected 2D beam footprint ellipse (`DN = 0`) in addition to the sounding center cross (`DN = 254`).

## Algorithm
Calculates the outer-beam slant range `max_r = depth / cos(max_angle)`, two-way travel time `max_twtt = 2 * max_r / 1500`, and along-track ship advance per ping (`along_step`). Then iterates over pings and beams inside the image bounds, drawing each sounding cross and optional footprint ellipse (`hypot(across/across_fp, along/along_fp) <= 1.0`).
