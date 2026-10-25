---
layout: default
title: xtf2gloria
parent: XTF Tools
nav_order: 7
tool_name: xtf2gloria
source_path: code/xtf/xtf2gloria.c
category: Sidescan Conversion
input_formats: [".xtf", ".idx"]
output_formats: [".slr (JCU GLORIA)"]
related_tools: ["klein2omg", "stripSS", "xtfTool", "mos2"]
---

# xtf2gloria

## Overview
`xtf2gloria` converts sidescan sonar packets (`XTF_HEADER_SONAR`, packet ID 0) in an XTF file into 1024-pixel 8-bit JCU GLORIA (`.slr`) sidescan records. It supports multi-beam dynamically focused sidescan systems (such as Klein 5000/3000) by automatically grouping pings with identical centisecond timestamps into along-track beam numbers (`-2, -1, 0, +1, +2`) and storing the along-track beam offset (`cb_depth[0]`) and towfish layback (`cb_depth[1]`) inside the GLORIA record header.

## Usage
```bash
xtf2gloria [-v] [-swap] [-log] [-min <val>] [-max <val>] [-plot_bottom] [-other_lalo_azi] -xtf <input.xtf> -omg <output.slr>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-xtf` | `<input.xtf>` | **Required** | Path to the input `.xtf` file (automatically uses `<basename>.idx` if present). |
| `-omg` | `<output.slr>` | **Required** | Path to the output JCU GLORIA sidescan file. |
| `-min` | `<val>` | `0` | Minimum 16-bit threshold for 16-to-8-bit scaling (`jK_collapse_16_to_8`). |
| `-max` | `<val>` | `65535` | Maximum 16-bit threshold for 16-to-8-bit scaling (`jK_collapse_16_to_8`). |
| `-log` | None | Linear (`PACK16_LINEAR`) | Use logarithmic 16-to-8-bit packing (`PACK16_LOG`). |
| `-swap` | None | Little-endian | Read 16-bit sidescan trace samples as big-endian (`fread_BE_short`) instead of little-endian. |
| `-plot_bottom` | None | Off | Mark the towfish altitude sample (`SensorPrimaryAltitude`) as bright white (`255`) on both port and starboard channels. |
| `-other_lalo_azi` | None | Off | Populate GLORIA header `lat`, `lon`, and `azi` from `SensorYcoordinate`, `SensorXcoordinate`, and `SensorHeading` (note: without this flag, only `ShipGyro` is set and `lat`/`lon` remain unpopulated in the loop). |
| `-v` | None | Off | Print XTF index, file header, downsampling factor, and progress every ping. |

## How It Works
1. **Index & Klein Beam Sequence Detection:** Reads `<basename>.idx` (or builds an XTF index) and calls `get_klein_beam_numbers()`, which inspects consecutive ping timestamps (`Hour`, `Minute`, `Second`, `HSeconds`) to identify multi-beam Klein ping bursts (1 to 5 beams per ping cycle) and assigns along-track beam indices (`-2..+2`, scaled by `beam_spacing = 0.2 m` into `header.cb_depth[0]`).
2. **16-to-8-Bit Conversion & Downsampling:** Reads port and starboard 16-bit channels, flips the port channel sample order, converts both to 8-bit via `jK_collapse_16_to_8()`, and boxcar-averages (`down_sample = NumSamples / 512`) each channel down to 512 pixels (1024 pixels total across-track).
3. **GLORIA Record Assembly:** Copies starboard (`0..511`, flipped so nadir is at center) and port (`512..1023`) into `gloria_out_rec.all_data`, sets `fishdepth`, `altitude`, `layback`, and `small_pixel`, and writes each record via `jcu_writegloria()`.

## Practical Examples

**1. Convert a Klein XTF sidescan file to GLORIA format with sensor navigation and linear stretching:**
```bash
xtf2gloria -v -other_lalo_azi -min 100 -max 8000 -xtf klein01.xtf -omg klein01.slr
```
