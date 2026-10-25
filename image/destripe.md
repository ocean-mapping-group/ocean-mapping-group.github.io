---
layout: default
title: destripe (image)
parent: Image Tools
nav_order: 17
tool_name: destripe
source_path: code/image/destripe.c
category: Satellite, SAR & Format Conversion
input_formats: ["ACRES 8-bit Landsat MSS image", "Optional 6-detector ratio file (-ratio)"]
output_formats: ["Destriped ACRES 8-bit image (<infile>.des)"]
related_tools: ["lsfilter", "add_hilo", "limit_change", "fix_zigzag"]
---

# destripe (`image`)

## Description
`destripe` (`code/image/destripe.c`, written by A. Y. / JCU, May 1990) removes 6-line periodic radiometric detector striping from ACRES-format Landsat MSS (Multispectral Scanner) imagery. Because Landsat MSS sweeps 6 detectors per spectral band on each mirror scan, detector gain drift creates a 6-row repeating stripe pattern. `destripe` either applies an external 6-detector gain/offset table (`-ratio`) or automatically calibrates detectors 2–6 against detector 1 using inter-line difference histograms and linear regression.

## CLI Options & Usage
```bash
destripe -in <acres_file> [-ratio <ratio_file>]
```
* **`-in <acres_file>`**: Input ACRES-format 8-bit Landsat image (with 90-byte header). Writes output to `<acres_file>.des`.
* **`-ratio <ratio_file>`**: Optional ASCII file containing 5 lines of pre-computed `(ratio, dmean)` coefficients for detectors 2–6 relative to detector 1.

## Algorithm
1. **Automatic Detector Calibration (when `-ratio` is omitted)**:
   * Accumulates histograms of pixel differences (`abs(line_1 - line_k) < 10`) between detector 1 (`row % 6 == 0`) and each of detectors 2–6 (`row % 6 == 1..5`) across the scene, ignoring clouds (`> 60`) and background (`0`).
   * Computes the mean difference (`dmean`), standard deviation, covariance, correlation, and linear gain `ratio` (`std_dev_1 / std_dev_k`) for each detector `k = 1..5`.
2. **Radiometric Normalization**:
   * For every scanline belonging to detectors 2–6 (`i = row % 6 != 0`), rescales valid pixels (`1..254`) via:
     `out = ((pixel - mean[i]) * ratio[i-1]) + mean[0]` (clamped to `1..255`), and writes the destriped image to `<acres_file>.des`.
