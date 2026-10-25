---
layout: default
title: jplto8bit
parent: Grid Tools
tool_name: jplto8bit
source_path: code/grid/jplto8bit.c
category: gridding
input_formats: [".r4 (JHC 32-bit float SAR/backscatter array)"]
output_formats: [".8bit (JHC 8-bit unsigned char array)"]
related_tools: ["r4to8bit", "locateSAR", "8bittor4"]
---

# jplto8bit

## Overview

`jplto8bit` converts a 1280-column OMG `JHC_header` 32-bit floating-point (`.r4`) airborne SAR or radar backscatter array into an 8-bit unsigned char (`.8bit`) array while normalizing cross-track slant-range angular response across a reference swath (`scanlines 2100..3200`, `pixels 0..270`).

---

## Syntax & CLI Options

```bash
jplto8bit [-low <min>] [-middle <mid>] [-high <max>] [-nozero] <floatfile> <8bitfile>
```

| Option | Description | Default |
|---|---|---|
| `<floatfile>` | **Required.** Input 32-bit float `JHC_header` file (`data_type == 3`). | None |
| `<8bitfile>` | **Required.** Output 8-bit unsigned char `JHC_header` file (`data_type = 1`). | None |
| `-low <value>` | Minimum float value mapped to digital number `0` (or `1` if `-nozero`). If both `-low` and `-high` are `0.0`, auto-scans the file for min/max. | `0.0` (auto-detect) |
| `-high <value>` | Maximum float value mapped to digital number `255`. | `0.0` (auto-detect) |
| `-middle <value>` | Midpoint float value mapped to digital number `128` for piecewise two-slope linear scaling. | `(low + high) / 2.0` |
| `-nozero` | Clamp non-zero input pixels that scale to `0` up to `1`, preserving `0` strictly for nodata/background pixels. | Disabled |

---

## How It Works

1. **Cross-Track Angular Normalization Table (`sum[0..1279]`):**
   - Seeks to scanline `2100` (`firstscan = 2100`, `lastscan = 3200`, assuming `dx = 1280`) and averages the floating-point pixel intensities across `firstpixel = 0` to `lastpixel = 270`.
   - Normalizes `sum[0..269]` by `sum[269]` and sets `sum[270..1279] = 1.0`.
2. **Range Determination:** If `-low` and `-high` are both `0.0`, scans the input float array to find the minimum and maximum non-zero values and updates `JHChead.min_value` and `JHChead.max_value` in both the output and input headers.
3. **Normalization & Piecewise 8-bit Quantization:**
   - Divides each non-zero pixel `*p` at column `x` by `sum[x]`.
   - Scales values below `middle` linearly into `[0, 128]` and values above `middle` into `[128, 255]`, clamping to `[0, 255]` (or `[1, 255]` with `-nozero`).

---

## Examples

**Normalize and convert a JPL SAR floating-point image to 8-bit:**
```bash
jplto8bit -low 0.0 -middle 0.25 -high 1.0 -nozero jpl_sar.r4 jpl_sar.8bit
```

---

## Workflow Context

- **See Also:** [`locateSAR`](locateSAR.md) (for slant-range terrain correction of JPL SAR imagery) and [`r4to8bit`](r4to8bit.md) (for standard general-purpose `.r4` to `.8bit` conversion without JPL SAR cross-track normalization).
