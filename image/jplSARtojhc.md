---
layout: default
title: jplSARtojhc
parent: Raster Image Processing (image)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 27
tool_name: jplSARtojhc
source_path: code/image/jplSARtojhc.c
category: Satellite, SAR & Format Conversion
input_formats:
- JPL AIRSAR / SIR-C VAX float (SY) or compressed Stokes matrix (-CM) files
output_formats:
- OMG1 32-bit float (.tp.r4, .hh.r4, .hv.r4, .vh.r4, .vv.r4) and 8-bit (.8bit) arrays
- ASCII header (.header)
related_tools:
- 8bit2acres
- PCItoJHC
- r4to8bit
- stretchacres
---

# jplSARtojhc

## Description
`jplSARtojhc` imports NASA/JPL AIRSAR and SIR-C polarimetric Synthetic Aperture Radar (SAR) imagery—in either older VAX floating-point `SY` format or Newer Compressed Stokes Matrix (`-CM`) format—into `OMG1` (`JHC_header`) 32-bit floating-point (`.r4`) and 8-bit (`.8bit`) rasters, while extracting embedded ASCII engineering headers into `<out>.header`.

## CLI Options & Usage

```bash
jplSARtojhc -in <sar_file> -out <prefix> [-CM]
```
* **`-in <sar_file>`**: Input JPL SAR data file.
* **`-out <prefix>`**: Output filename prefix.
* **`-CM`**: Parses compressed polarimetric Stokes matrix records (`10 bytes/pixel`), outputting five separate 32-bit float `OMG1` files:
  * `<prefix>.tp.r4` — Total Power (`M11`).
  * `<prefix>.hh.r4` — Co-polarized `HH` power (`0.5 * M11 + M12`).
  * `<prefix>.vv.r4` — Co-polarized `VV` power (`0.5 * M11 - M12`).
  * `<prefix>.hv.r4` & `<prefix>.vh.r4` — Cross-polarized `HV`/`VH` power (`0.5 * (M11 - M33 - M44)`).

## Algorithm
1. **Default `SY` Mode**: Extracts two 5120-byte ASCII headers into `<prefix>.header`, skips to byte offset `25600`, converts each 4-byte VAX floating-point sample to IEEE 754 float (scaling by `0.25` and taking `10 * log10(val)` for decibels), and writes `<prefix>.r4` and `<prefix>.8bit` (`1280 × 1024`).
2. **Compressed Stokes Matrix Mode (`-CM`)**: Parses `NUMBER OF SAMPLES PER RECORD` (`width`), `NUMBER OF LINES` (`height`), and byte offsets from the JPL header, decodes the 10-byte-per-pixel Stokes matrix (`exponent`, `mantissa` for `M11`, and scaled `M12`, `M33`, `M44` terms), converts each polarization channel to decibels (`10 * log10`), and writes the five `.r4` `OMG1` files.
