---
layout: default
title: PCItoJHC
parent: Image Tools
nav_order: 5
tool_name: PCItoJHC
source_path: code/image/PCItoJHC.c
category: Satellite, SAR & Format Conversion
input_formats: ["3-band PCI/CASI interleaved raster", "SIF (-sif)", "Netpbm PPM (-ppm) / PGM (-pgm)", "TIFF World File (-tfw)", "CASI .COR (-snb)"]
output_formats: ["OMG1 8-bit band files (.band1, .band2, .band3)", ".pxm_header"]
related_tools: ["8bit2acres", "makecolcomp", "landsat2acres", "czcs2acres"]
---

# PCItoJHC

## Description
`PCItoJHC` imports 3-band interleaved PCI/CASI airborne hyperspectral imagery, `.sif` imagery (`-sif`), 24-bit Netpbm `.ppm` color images (`-ppm`), or 8-bit `.pgm` greyscale images (`-pgm`) into separate 8-bit `OMG1` (`JHC_header`) band files (`.band1`, `.band2`, `.band3`), while attaching geographic or Transverse Mercator / Mercator projection metadata from either a CASI `.COR` navigation file (`-snb`) or an ESRI TIFF World File (`-tfw`).

## CLI Options & Usage
```bash
PCItoJHC -in <rawimage> -out <prefix> [-ppm | -pgm | -sif] \
  [-rows <n> -cols <n>] [-offset <bytes>] [-invert] [-flip] \
  [-snb <cor_file>] [-tfw <world_file> [-merid <deg> | -merc_meters <lat>]] \
  [-tlon <deg> -tlat <deg> -blon <deg> -blat <deg> -dx <m> -dy <m>]
```
* **`-in <filename>`**: Input PCI, SIF, PPM, or PGM image file.
* **`-out <prefix>`**: Output filename (for `-pgm`) or prefix producing `<prefix>.band1`, `<prefix>.band2`, and `<prefix>.band3` (for 3-band inputs).
* **`-ppm` / `-pgm`**: Reads dimensions from a binary `P6` (PPM) or `P5` (PGM) header and writes the stripped ASCII header to `<out>.pxm_header`.
* **`-sif`**: De-interleaves pixel-interleaved (`RGBRGB...`) 3-band data instead of line-interleaved PCI band rows.
* **`-snb <cor_file>`**: Reads a CASI `.COR` file containing upper-left UTM Northing/Easting and pixel size (hardcoded to Zone 20 / central meridian `-63°W` for St. Andrews / Passamaquoddy Bay), converting bounds to WGS84 latitude/longitude via `tmgrid_to_geog()`.
* **`-tfw <world_file>`**: Reads a 6-line ESRI World File (`dx`, rotation, `dy`, upper-left X/Y). Combine with `-merid <deg>` for Transverse Mercator or `-merc_meters <proj_lat>` for Mercator meters.
* **`-invert` / `-flip`**: Inverts 8-bit values (`255 - val`) or flips vertical row order.

## Algorithm
Reads the input raster according to its interleaving mode (line-interleaved 3-band PCI, pixel-interleaved `-sif`/`-ppm`, or single-band `-pgm`), populates the `JHC_header` projection and corner coordinates from `-snb`, `-tfw`, or explicit `-tlat/-tlon` flags, and writes each band as an independent `OMG1` 8-bit array.
