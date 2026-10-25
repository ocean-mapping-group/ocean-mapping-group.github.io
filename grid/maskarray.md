---
layout: default
title: maskarray
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: maskarray
source_path: code/grid/maskarray.c
category: gridding
input_formats:
- .r4 (JHC 32-bit float grid)
- .8bit (JHC 8-bit unsigned char grid)
output_formats:
- '.maskmap (JHC 8-bit binary stencil mask: 0 = nodata, 255 = valid)'
related_tools:
- mix_ci
- mask
- r4to8bit
- add8bit
---

# maskarray

## Overview

`maskarray` reads an OMG `JHC_header` 32-bit floating-point (`.r4`) or 8-bit unsigned char (`-8bit`) grid and generates an 8-bit binary stencil mask (`<infile>.maskmap` by default, or `-m <maskfile>`). Pixels equal to the ignore value (default `0.0`) are written as `0`, and all valid pixels (`!= ignore`) are written as `255`.

---

## Syntax & CLI Options

```bash
maskarray [-8bit] [-ignore <val>] [-m <maskfile>] <bathfile>
```

| Option | Description | Default |
|---|---|---|
| `<bathfile>` | **Required.** Input `JHC_header` `.r4` float grid (or 8-bit grid when `-8bit` is specified). | None |
| `-8bit` | Read `<bathfile>` as an 8-bit unsigned char array (`1` byte/pixel) instead of a 32-bit float array (`4` bytes/pixel). | Disabled (32-bit float) |
| `-ignore <val>` | Pixel value in `<bathfile>` to treat as invalid/nodata (mapped to `0` in the output mask). | `0.0` |
| `-m <maskfile>` | Explicit output filename for the 8-bit mask. | `<bathfile>.maskmap` |

---

## How It Works

1. Reads the `JHC_header` from `<bathfile>`, sets `header.data_type = 1` (8-bit), and writes the updated header to the output mask file.
2. Scans `<bathfile>` row-by-row (`jswapfloat_fread` for float grids, `fread` for `-8bit` grids).
3. Evaluates each pixel:

   ```c
   *q = (*p != ignore) * 255;
   ```
   writing `0` where the input matches `ignore` and `255` everywhere else.

---

## Examples

**1. Create a valid-data stencil mask from a bathymetric `.r4` grid (where `0.0` is nodata):**

```bash
maskarray survey.r4
# Creates survey.r4.maskmap
```

**2. Create a stencil mask from an 8-bit sidescan mosaic where `255` represents background nodata:**

```bash
maskarray -8bit -ignore 255 -m sidescan.mask survey.mos
```

---

## Workflow Context

- **Downstream:** Pass the resulting `.maskmap` to [`mix_ci`](mix_ci.html) (`-mask <maskfile> -ignore 0`) to composite sun-illuminated bathymetry over a background sidescan mosaic, satellite image, or land backdrop.
