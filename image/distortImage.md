---
layout: default
title: distortImage
parent: Image Tools
nav_order: 18
tool_name: distortImage
source_path: code/image/distortImage.c
category: Image & Raster Processing
input_formats: ["OMG1 8-bit input image", "OMG1 8-bit reference image (-ref)", "2-point control file (-coords)"]
output_formats: ["Warped/registered OMG1 8-bit image"]
related_tools: ["control_points", "patchArea", "rotateimage", "subimage"]
---

# distortImage

## Description
`distortImage` geometrically warps (translates, rotates, and isotropically scales) an 8-bit `OMG1` (`JHC_header`) image onto either an existing reference `OMG1` image (`-ref`) or a WGS84 Mercator grid (`-geo`) using a two-point control file (`-coords`).

## CLI Options & Usage
```bash
distortImage -in <infile> -out <outfile> -coords <cfile> \
  [-ref <reffile> | -geo [-projlat <deg>]] \
  [-blank] [-alternate] [-latshift <deg>] [-lonshift <deg>]
```
* **`-in <infile>`**: Input 8-bit `OMG1` image to be warped.
* **`-out <outfile>`**: Output registered 8-bit `OMG1` image.
* **`-coords <cfile>`**: ASCII control-point file containing two lines:
  * With `-ref`: `in_x1 in_y1 ref_x1 ref_y1` (in pixels).
  * With `-geo`: `in_x1 in_y1 lon1 lat1` (in pixels and decimal degrees).
* **`-ref <reffile>`**: Reference `OMG1` image onto which `<infile>` is overlaid.
* **`-geo`**: Warps `<infile>` into a WGS84 Mercator projection defined by the two geographic control points (`-projlat` sets the Mercator projection latitude; defaults to `lat1`).
* **`-blank`**: Initializes the output canvas to `255` (white/no-data) instead of keeping the `-ref` background image.
* **`-alternate`**: Checkerboards overlapping pixels (`(i + j) % 2 == 0`) between `<infile>` and `<reffile>` for visual registration quality control.
* **`-latshift <deg> -lonshift <deg>`**: Applies datum shifts to the control point coordinates in `-geo` mode.

## Algorithm
Computes the 2D similarity transform (scale `scale = dist_ref / dist_in` and rotation angle `rot_angle = dir_in - dir_ref`) between the two control-point pairs, then inverse-maps every output pixel `(i, j)` back into source image coordinates `(orig_x, orig_y)` to sample `<infile>`.
