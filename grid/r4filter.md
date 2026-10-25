---
layout: default
title: r4filter
parent: Grid Tools
tool_name: r4filter
source_path: code/grid/r4filter.c
category: gridding
input_formats: [".r4 (JHC 32-bit float grid)", ".8bit (JHC 8-bit unsigned char grid)", "Raw 32-bit float binary (-rawfloat)"]
output_formats: [".r4 (filtered 32-bit float grid)", ".8bit (filtered 8-bit unsigned char grid)"]
related_tools: ["r4interp", "fillGap", "subtractSurface", "r4to8bit"]
---

# r4filter

## Overview

`r4filter` applies a 2D spatial convolution or statistical filter over an asymmetric sliding rectangular kernel (`-xbox <nx> -ybox <ny>`, where both dimensions must be positive odd integers) on an OMG `JHC_header` 32-bit floating-point (`.r4`) or 8-bit (`.8bit`) array.

It supports **low-pass mean filtering (`-low`)**, **high-pass residual filtering (`-high`)**, and **median filtering (`-median`)**, automatically excluding nodata/ignored pixels (`-ignore <val>`, default `0.0`) from the kernel statistics.

---

## Syntax & CLI Options

```bash
r4filter -xbox <nx_odd> -ybox <ny_odd> (-low | -high | -median | -vert_grad | -horiz_grad) [OPTIONS] <infile> <outfile>
```

| Option | Description | Default |
|---|---|---|
| `<infile>` | **Required.** Input `JHC_header` `.r4` (`data_type == 3`) or `.8bit` (`data_type == 1`) grid file (or headerless float file with `-rawfloat`). | None |
| `<outfile>` | **Required.** Output filtered `JHC_header` grid file (matching the data type of `<infile>`). | None |
| `-xbox <nx>` | **Required.** Horizontal kernel width in pixels (must be a positive **odd** integer, e.g., `3`, `5`, `7`). | None |
| `-ybox <ny>` | **Required.** Vertical kernel height in pixels (must be a positive **odd** integer, e.g., `1`, `3`, `5`, `7`). | None |
| `-low` | Apply a **low-pass mean filter**: outputs the average of all non-ignored pixels inside the `xbox x ybox` kernel. | None (must specify a filter type) |
| `-high` | Apply a **high-pass residual filter**: outputs `centre_pixel - kernel_average` (if `centre_pixel != ignore`). For 8-bit inputs, offsets the residual by `+128` and clamps to `[0, 255]`. | None |
| `-median` | Apply a **median filter**: sorts all valid (`!= ignore`) pixels in the kernel and outputs the middle value (`data[valid / 2]`). | None |
| `-vert_grad` / `-horiz_grad` | Scaffolded template options for 1D directional gradient (`do_gradient`); currently returns the last valid pixel in the kernel. | None |
| `-ignore <val>` | Pixel value to exclude from kernel calculations (`0.0` by default for `.r4` grids; use `-ignore 255` for `.mos` sidescan mosaics). | `0.0` |
| `-rawfloat <rawdx>` | Read `<infile>` as a headerless raw 32-bit float array with `<rawdx>` columns (`dy` is inferred from file size), and prepend a 1024-byte `OMG1` `JHC_header` to `<outfile>`. | Disabled |

---

## How It Works

1. **Validation & Header Inspection:**
   - Verifies that both `-xbox` and `-ybox` are positive odd integers (`xbox % 2 != 0 && ybox % 2 != 0`) and that a filter mode is specified.
   - Reads the `JHC_header` from `<infile>` and automatically detects whether the array is 32-bit float (`data_type == 3`) or 8-bit unsigned char (`data_type == 1`).
2. **Sliding Kernel Extraction:**
   - Loops over interior rows `y = ystep .. dy - ystep - 1` (`ystep = ybox / 2`) and columns `x = xstep .. dx - xstep - 1` (`xstep = xbox / 2`), extracting the `xbox x ybox` neighborhood into a floating-point `kernel` buffer.
3. **Filter Evaluation:**
   - **Low-Pass (`do_hilo(..., LOW)`):** Sums all kernel elements `!= ignore_value` and divides by `count`. Notice that if the center pixel is `0.0` (nodata) but neighboring pixels in the kernel are valid, `-low` interpolates/fills the gap with the neighborhood mean!
   - **High-Pass (`do_hilo(..., HIGH)`):** Computes `centre - average` when `centre != ignore_value` (preserving `ignore_value` at empty nodes). For 8-bit arrays, adds `128` so zero-mean high-pass residuals are centered on mid-grey (`128`).
   - **Median (`do_median`):** Removes all `ignore_value` entries from the kernel, bubble-sorts the `valid` remaining values, and returns `data[valid / 2]`.

---

## Examples

**1. Smooth a noisy `.r4` bathymetric grid with a $5 \times 5$ median filter:**
```bash
r4filter -xbox 5 -ybox 5 -median survey_raw.r4 survey_med5x5.r4
```

**2. Extract short-wavelength bedforms (high-pass residual) using a $15 \times 15$ boxcar:**
```bash
r4filter -xbox 15 -ybox 15 -high survey.r4 survey_hpf15.r4
```

**3. Filter an 8-bit sidescan mosaic while ignoring background `255` pixels:**
```bash
r4filter -xbox 3 -ybox 3 -median -ignore 255 mosaic.mos mosaic_despeckled.mos
```

---

## Workflow Context

- **See Also:** [`fillGap`](fillGap.md) (for targeted gap interpolation without smoothing valid nodes) and [`subtractSurface`](subtractSurface.md) (for subtracting two `.r4` surfaces).
