---
layout: default
title: gsf2omg
parent: Generic Sensor Format — GSF (gsf)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 1
tool_name: gsf2omg
source_path: code/gsf/gsf2omg.c
category: Raw Data Unraveling
input_formats:
- .gsf
output_formats:
- .merged
- .merged.ss_data
related_tools:
- gsf2omg_7101
- gsf2orientation
- gsf2param
- gsf2svp
- gsfTool
- omg2gsf
---

# gsf2omg

## Overview
`gsf2omg` converts Generic Sensor Format (`.gsf`) Swath Bathymetry Ping records (`GSF_SWATH_BATHYMETRY_PING`) into OMG-HDCS v3 `.merged` and `.merged.ss_data` files using the lightweight `omg_gsf` parser. It primarily targets Reson SeaBat 8100-series (`8101` and `8125`) GSF files where navigation and attitude have already been merged into the ping headers.

## Usage

```bash
gsf2omg [-v] [-debug] -gsf <input_name.gsf> -omg <omg_file_prefix>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-gsf` | `<input_name.gsf>` | **Required** | Path to the input `.gsf` file. |
| `-omg` | `<omg_file_prefix>` | **Required** | Output prefix for `<omg_file_prefix>.merged` and `<omg_file_prefix>.merged.ss_data`. |
| `-v` | None | Off | Print every parsed `GSF_Swath_Bathymetry_Ping` record. |
| `-debug` | None | Off | Enable debug flag. |

## How It Works
1. **Valid Reference Coordinate Scan:** Scans forward through `GSF_SWATH_BATHYMETRY_PING` packets until it finds a ping with valid geographic coordinates ($\text{lat} \in (-90^\circ, 90^\circ)$, $\text{lon} \in (-180^\circ, 180^\circ)$) to avoid corrupting `summary.refLat` and `summary.refLong` with initial zeroed/invalid fixes.
2. **Summary Initialization:** Checks `gsf_bathy.reson_8100.sonar_model` (`8101` $\rightarrow$ `SeaBat_8101`, `8125` $\rightarrow$ `SeaBat_8125`) and writes an `OMG_HDCS_summary_header` (version 3).
3. **Ping & Beam Conversion:** For each `GSF_SWATH_BATHYMETRY_PING`, converts `tide_corrector` and `depth_corrector` from centimeters to millimeters (`* 10.0`), converts embedded ping latitude, longitude, roll, pitch, heave, and heading into OMG profile header units, unscales `depth`, `across_track`, and `along_track` using the GSF subrecord `scale_factors` table, marks beams with `flag & 0x01` as rejected (`status = 22`), and writes each ping to `<prefix>.merged`.

## Practical Examples

**1. Convert a Reson 8101 GSF file into OMG `.merged` format:**

```bash
gsf2omg -v -gsf line01.gsf -omg line01
```
