---
layout: default
title: projectForwardVideo
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 39
tool_name: projectForwardVideo
source_path: code/image/projectForwardVideo.c
category: Multibeam Water Column & Acoustic Modeling
input_formats:
- OMG1 8-bit forward-looking video frame
output_formats:
- Annotated camera frame (<outfile>)
- Georeferenced plan-view sea-surface map (<outfile>.map)
related_tools:
- TAtoXZ
- stackPIEs
- patchArea
- distortImage
---

# projectForwardVideo

## Description
`projectForwardVideo` orthorectifies a shipboard oblique forward-looking video camera frame (in 8-bit `OMG1` format) onto a flat sea-surface plan-view grid (`<outfile>.map`, `600 × 600` pixels at `1.0 m` resolution in rotated Mercator coordinates) so that surface slicks, boil fronts, or wake features can be directly correlated with subsurface multibeam water-column imagery.

## CLI Options & Usage

```bash
projectForwardVideo -in <video_frame.8bit> -out <outfile> \
  [-xfactor <fx>] [-yfactor <fy>]
```
* **`-in <video_frame.8bit>`**: Input 8-bit `OMG1` video frame (`720 × 480`).
* **`-out <outfile>`**: Output annotated camera frame (`<outfile>`) and projected sea-surface map (`<outfile>.map`).
* **`-xfactor <fx> -yfactor <fy>`**: Optional camera field-of-view scale adjustments (default: `1.0`).

## Camera Geometry & Algorithm
1. Models a mast-mounted camera at height `cam_z = 9.0 m` above the waterline with downward depression angle `cam_dip = 6.72°`, horizontal FOV `44.0°`, and vertical FOV `33.0°`.
2. Draws the projected horizon line and range grid ticks (`50 m` to `600 m` forward, `-300 m` to `+300 m` across-track) onto `<outfile>` for visual calibration verification.
3. For each cell `(x, y)` in the `600 × 600` sea-surface map (`0..600 m` ahead of the bow, `-300..+300 m` port/starboard), computes the 3D ray angle into the camera lens (`angle_z = atan2(cam_z, range) - cam_dip`, `angle_x = atan2(across, forward)`), samples the corresponding video pixel `(px, py)`, and writes `<outfile>.map` as a rotated Mercator `OMG1` mapsheet.
