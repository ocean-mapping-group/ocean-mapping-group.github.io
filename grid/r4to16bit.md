---
layout: default
title: r4to16bit
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: r4to16bit
source_path: code/grid/r4to16bit.c
category: gridding
input_formats:
- .r4 (JHC 32-bit float grid)
output_formats:
- JHC_header + 16-bit unsigned short array
related_tools:
- r4to8bit
- 8bittor4
- r4toESRI
---

# r4to16bit

## Overview

`r4to16bit` linearly scales an OMG `JHC_header` 32-bit floating-point (`.r4`) grid (`data_type == 3`) into a 16-bit unsigned integer array (`unsigned short`, dynamic range `0..65535`) preceded by a 1024-byte `JHC_header`.

---

## Syntax & CLI Options

```bash
r4to16bit [-low <min_val>] [-high <max_val>] [-nozero] <floatfile> <16bitfile>
```

| Option | Description | Default |
|---|---|---|
| `<floatfile>` | **Required.** Input 32-bit float `JHC_header` file (`data_type == 3`). | None |
| `<16bitfile>` | **Required.** Output 16-bit unsigned short `JHC_header` file. | None |
| `-low <value>` | Minimum floating-point value mapped to `0` (or `1` if `-nozero` is set). If both `-low` and `-high` are `0`, scans the input file for the actual min and max. | `0.0` (auto-detect) |
| `-high <value>` | Maximum floating-point value mapped to `65535`. | `0.0` (auto-detect) |
| `-nozero` | Clamp valid non-zero input floats that scale to `0` up to `1`, reserving `0` strictly for nodata (`*p == 0.0`) pixels. | Disabled |

---

## How It Works

1. **Header Reading & Range Detection:**
   - Reads the `JHC_header` from `<floatfile>` and verifies `JHChead.data_type == 3`.
   - If `-low` and `-high` are both `0`, scans all non-zero pixels (`*p != 0.0`) in `<floatfile>` to determine `low_limit` and `high_limit`.
   - Stores `low_limit` and `high_limit` in `JHChead.min_value` and `JHChead.max_value`, sets `JHChead.data_type = 1`, and writes the 1024-byte header to `<16bitfile>`.
2. **16-Bit Quantization:**
   - For each pixel `*p`:
     - If `*p == 0.0`, outputs `0`.
     - Otherwise, computes:
       $$\text{temp} = \frac{(\text{*p} - \text{low\_limit}) \times 65535}{\text{high\_limit} - \text{low\_limit}}$$
       clamps `temp` to `[0, 65535]` (or `[1, 65535]` if `-nozero` is set), and writes `dx` `unsigned short` values per row.

---

## Examples

**Scale a bathymetric `.r4` grid spanning `-3500 m` to `0 m` into 16-bit unsigned integers, reserving `0` for nodata:**

```bash
r4to16bit -low -3500 -high 0 -nozero deep_survey.r4 deep_survey.16bit
```

---

## Workflow Context

- **Counterpart:** [`8bittor4`](8bittor4.html) (`-short` flag) converts 16-bit integer `JHC_header` grids back to 32-bit `.r4` floating-point grids.
- **See Also:** [`r4to8bit`](r4to8bit.html) for standard 8-bit (`0..255`) conversion.
