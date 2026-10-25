---
layout: default
title: TAtoXZ
parent: Image Tools
nav_order: 6
tool_name: TAtoXZ
source_path: code/image/TAtoXZ.c
category: Multibeam Water Column & Acoustic Modeling
input_formats: ["SM2000 Time-Angle rasters (<prefix>.TA_inten, <prefix>.TA_phase)"]
output_formats: ["Across-track / depth fan rasters (<prefix>.XZ_inten, <prefix>.XZ_phase)"]
related_tools: ["comboTAs", "comboVPs", "patchTA", "stackPIEs"]
---

# TAtoXZ

## Description
`TAtoXZ` projects Simrad/Kongsberg Mesotech SM2000 multibeam sonar water-column frames from raw polar Time-Angle coordinates (`782` time samples × `120` beams in `<prefix>.TA_inten` and `<prefix>.TA_phase`) into Cartesian across-track vs. depth (`XZ`) fan coordinates (`1024 × 512` pixels in `<prefix>.XZ_inten` and `<prefix>.XZ_phase`).

## CLI Options & Usage
```bash
TAtoXZ -in <sm2kprefix>
```
* **`-in <sm2kprefix>`**: Input/output prefix. Reads `<sm2kprefix>.TA_inten` and `<sm2kprefix>.TA_phase` (`782 × 120` 8-bit `OMG1` files) and writes `<sm2kprefix>.XZ_inten` and `<sm2kprefix>.XZ_phase` (`1024 × 512` 8-bit `OMG1` files).

## Algorithm
1. Reads the `782 × 120` `TA_inten` and `TA_phase` arrays and initializes two `1024 × 512` output arrays (`XZ_inten`, `XZ_phase`) filled with `255` (background).
2. For each pixel `(i, j)` in the `1024 × 512` Cartesian output fan (centered horizontally at column `512` at the transducer apex):
   * Computes polar slant range `range = hypot(i - 512, j) * 782.0 / 512.0`.
   * Computes beam angle `angle = atan2(i - 512, j)` within the `±60°` (`120°` total) SM2000 sector (`angle_index = (angle + 60°) / 120° * 120`).
   * If `range < 782` and `0 <= angle_index < 120`, copies `TA_inten[range, angle_index]` and `TA_phase[range, angle_index]` into the `XZ` fan arrays.
3. Writes `<sm2kprefix>.XZ_inten` and `<sm2kprefix>.XZ_phase` with updated `OMG1` headers (`xmax = 1024`, `ymax = 512`).
