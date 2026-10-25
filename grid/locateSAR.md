---
layout: default
title: locateSAR
parent: Grid Tools
tool_name: locateSAR
source_path: code/grid/locateSAR.c
category: gridding
input_formats: [".r4 (topographic DTM)", ".r4 or .8bit (JPL synoptic SAR image)"]
output_formats: [".slr (slant-range corrected radar)", ".mock (synthetic grazing-angle image)", ".depth (co-registered depth image)", ".locate (georeferenced mosaic)"]
related_tools: ["jplto8bit", "addSUN", "r4to8bit"]
---

# locateSAR

## Overview

`locateSAR` performs terrain-aware slant-range correction, grazing-angle calculation, acoustic/radar cast-shadow detection, and geographic registration of JPL airborne Synthetic Aperture Radar (SAR) synoptic imagery (`1280` pixels wide) over a digital terrain model (`.r4` DTM).

Depending on the mode flag (`-radar`, `-mock`, or `-depth`), it outputs an 8-bit co-registered swath image (`.slr`, `.mock`, or `.depth`) and optionally maps the pixels onto a $2\times$-oversampled georeferenced grid (`<toponame>locate` when `-locate` is specified).

---

## Syntax & CLI Options

```bash
locateSAR -topo (<dep.r4> | flat) (-radar | -mock | -depth) [OPTIONS] <sar_image_files...>
```

| Option | Description | Default |
|---|---|---|
| `-topo <dep.r4 \| flat>` | **Required.** Input `.r4` topographic DTM file, or the keyword `flat` to assume a flat datum at nadir. | None |
| `<sar_image_files...>` | **Required.** One or more input SAR image files (`1280` columns, 32-bit float by default or 8-bit with `-8bit`). | None |
| `-radar` | Output slant-range corrected radar backscatter to `<sar_file>.slr`. | Disabled |
| `-mock` | Output synthetic grazing-angle difference (`rgraze - true_grazing_angle`) image to `<sar_file>.mock`. | Disabled |
| `-depth` | Output DTM elevation along the SAR swath geometry to `<sar_file>.depth`. | Disabled |
| `-locate` | Simultaneously map output pixels onto a $2\times$-resolution georeferenced `JHC_header` grid named `<toponame>locate`. | Disabled |
| `-8bit` | Read input SAR image as 8-bit unsigned char (`datatype = 1`) instead of 32-bit float (`datatype = 3`). | `datatype = 3` (float) |
| `-azi <deg>` | Aircraft flight track azimuth in degrees. | `91.2` |
| `-eastshift <m>` | Shift aircraft reference track center eastward by `<m>` meters. | `0.0` |
| `-northshift <m>` | Shift aircraft reference track center northward by `<m>` meters. | `0.0` |
| `-min <dB>` / `-max <dB>` | Minimum and maximum dB values mapped to `[16..255]` when quantizing float `-radar` data. | `0.0` / `1.0` |
| `-maxangle <deg>` | Maximum grazing angle difference (`+-maxangle`) mapped across the greyscale range in `-mock` mode. | `25.0` |
| `-cast_shadow` | Detect radar cast shadows along each cross-track scanline (`old_beam_angle > beam_angle`) and color shadowed pixels `GREEN`. | Disabled |
| `-clip_beam <deg>` | Mask pixels where `beam_angle < clip_beam` as `YELLOW`. | `0.0` |
| `-v` | Enable verbose per-pixel raytracing diagnostics. | Disabled |

---

## How It Works

1. **DTM & Projection Setup:** Reads the `.r4` DTM into memory and initializes a Mercator projection (`merc_init`). If `-locate` is enabled, allocates an 8-bit registration grid (`Regist`) at $2\times$ the spatial resolution (`Expand = 2.0`) of the input DTM.
2. **Swath Raytracing:**
   - For each along-track scanline `i` (spaced at `8.2311 m` from the track midpoint at `altitude = 8400 m`) and each of the `1280` cross-track horizontal range bins (`2500 m` to `15300 m` at `10 m` spacing), projects the ground pixel `(xpos, ypos)` onto the DTM.
3. **Terrain & Grazing-Angle Evaluation:**
   - Samples the local DTM elevation `value` and adjacent east/south neighbors (`peast`, `psouth`).
   - In `-mock` mode, calls `vectangle` to compute the true 3D surface grazing angle and checks for radar cast shadows (`-cast_shadow`). Unimageable or shadowed pixels are flagged with diagnostic palette colors (`RED`, `GREEN`, `BLUE`, `YELLOW`, `MAGENTA`, `CYAN`).
   - In `-radar` mode, computes the true 3D slant range:
     $$R_{\text{slant}} = \sqrt{R_{\text{horiz}}^2 + (\text{altitude} - \text{elevation})^2}$$
     and samples the corresponding slant-range pixel `needed_pixel = (slant_range - 8664.0) / 6.6621` from the SAR scanline.

---

## Examples

**1. Slant-range correct a float SAR image using a topographic DTM and project onto a map grid:**
```bash
locateSAR -topo huon_dtm.r4 -radar -locate -azi 271.0 -min -30.0 -max 0.0 sar_strip.r4
```

**2. Generate a synthetic radar grazing-angle illumination model with cast shadows:**
```bash
locateSAR -topo huon_dtm.r4 -mock -cast_shadow -maxangle 20 -azi 271.0 sar_strip.r4
```

---

## Workflow Context

- Designed for co-registering and terrain-correcting airborne SAR imagery (such as the Markham Canyon / Huon Gulf Papua New Guinea surveys) against multibeam and land DTMs.
