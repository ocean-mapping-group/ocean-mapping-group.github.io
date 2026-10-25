---
layout: default
title: GM_fillGap
parent: James Muggah (james) Tools
nav_order: 1
tool_name: GM_fillGap
source_path: code/james/GM_fillGap.c
category: Raster Processing & Web Mapping (james)
input_formats: [".r4", ".8bit", ".sun_*"]
output_formats: [".r4", ".8bit", ".sun_*"]
related_tools: ["map2GMTiles", "merged2GMTiles", "weigh_grid", "jfill", "filter"]
---

# GM_fillGap

## Description
`GM_fillGap` (based on John Hughes Clarke's `fillGap.c`, extended in November 2009 for Google Map tile seams) repairs narrow 1- to 3-pixel nodata seams and left/right edge boundary drop-outs (`-edgeit`) in OMG 32-bit floating-point grids (`.r4`, nodata = `0.0`) or 8-bit unsigned char imagery mapsheets (`.8bit`, `.sun_315`, default nodata = `255`).

When adjacent mapsheet tiles or `weigh_grid` patch areas are gridded independently and abut along shared boundaries, rounding in projection coordinates often leaves a 1- to 3-pixel gap between valid regions or along the left/right edges (`x = 0` or `x = dx-3..dx`). `GM_fillGap` scans each interior pixel and interpolates across cardinal North-South or East-West neighbors up to 3 pixels away, while optionally extrapolating valid edge pixels into the 1–3 column border (`-edgeit`).

---

## Usage

```bash
GM_fillGap [-v] [-edgeit] [-ignore <val>] [-box <val>] [-low | -high] <infile> <outfile>
```

### Examples

**1. Fill internal 1–3 pixel seams and left/right boundary drop-outs in a `.r4` bathymetry tile:**
```bash
GM_fillGap -edgeit tile_1024_2048.r4 tile_1024_2048_filled.r4
```

**2. Fill gaps in an 8-bit sun-illuminated mapsheet where nodata is `255`:**
```bash
GM_fillGap -edgeit -ignore 255 tile.sun_315 tile_filled.sun_315
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<infile>` | Input OMG raster file (`.r4` float grid or `.8bit` unsigned byte image with a 1024-byte `JHC_header`). | Required |
| `<outfile>` | Output gap-filled OMG raster file. | Required |
| `-edgeit` | Fix 1- to 3-pixel nodata gaps at the left edge (`x = 0` copied from `x = 1`) and right edge (`x = dx-3`, `dx-2`, `dx-1` copied outward from `dx-4`). Added to fix a right-edge column drop-out in `weigh_grid`. | Disabled |
| `-ignore <val>` | Nodata pixel value for 8-bit mapsheets. Note: for floating-point `.r4` files (`JHChead.data_type != 1`), `ignore_value` is automatically forced to `0.0`. | `255.0` (`0.0` for `.r4`) |
| `-v` | Verbose mode: prints row progress and logs each cardinal interpolation stencil (`NSEW`, `NS`, `NS-2`, `EW+3`, etc.) used to fill a hole. | Disabled |
| `-box <val>` | Parses filter box size parameter (retained from `fillGap.c` template). | Unused |
| `-low` / `-high` | Selects low-pass (`LOW_FILTER`) or high-pass (`HIGH_FILTER`) flag (retained from `fillGap.c`). | `-low` |

---

## How It Works

1. **Header Inspection & Data Type Detection:**
   Reads the 1024-byte `JHC_header` (`JHC_OMG_RECLEN`) via `get_print_JHC_header`. If `JHChead.data_type == 1`, operates in 8-bit `unsigned char` mode (`c8bit_flag = 1`); otherwise operates in 32-bit `float` mode with byte-order swapping (`jswapfloat_fread` / `jswapfloat_fwrite`) and sets `ignore_value = 0.0`.
2. **Top & Bottom 3-Row Margin (`step = 3`):**
   Copies the first 3 rows (`y = 0..2`) and last 3 rows (`y = dy-3..dy-1`) directly from input to output, applying left/right edge replication if `-edgeit` is enabled.
3. **Cardinal Stencil Gap Interpolation (`y = 3 .. dy-4`, `x = 3 .. dx-4`):**
   Whenever a pixel equals `ignore_value`, `GM_fillGap` tests a hierarchy of cardinal neighbor pairs and computes a distance-weighted linear average:
   * **4-neighbor cross (`NSEW`):** If `(x, y+1)`, `(x, y-1)`, `(x-1, y)`, and `(x+1, y)` are all valid, averages all 4 neighbors:
     $$v = \frac{N + S + E + W}{4}$$
   * **1-pixel North-South (`NS`):** If `(x, y+1)` and `(x, y-1)` are valid: $v = (N_1 + S_1)/2$.
   * **Asymmetric 2- to 3-pixel North-South (`NS-2`, `NS+2`, `NS-3`, `NS+3`, `NS+-22`):** Linearly weights bracketing valid pixels at $(y-1, y+2)$, $(y-2, y+1)$, $(y-3, y+1)$, $(y-1, y+3)$, or $(y-2, y+2)$.
   * **1- to 3-pixel East-West (`EW`, `EW-2`, `EW+2`, `EW-3`, `EW+3`, `EW+-22`):** Same inverse-distance weighted linear interpolation along row $y$ for horizontal gaps up to 3 pixels wide.
   * If no cardinal pair brackets the gap within $\pm 3$ pixels, the pixel remains `ignore_value`.
