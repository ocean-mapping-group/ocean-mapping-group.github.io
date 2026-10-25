---
layout: default
title: sdf2omg
parent: Klein Sonar Data Format — SDF (sdf)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 2
tool_name: sdf2omg
source_path: code/sdf/sdf2omg.c
category: Raw Data Unraveling
input_formats:
- .sdf
output_formats:
- .merged
- .merged.ss_data
- .sonar_settings
- .param
- .orientation
- .ss_5902
- .ss_5902.slr
- .ss_5910
- .ss_5910.slr
- .ss_5920
- .ss_3501
- .ss_3502
- .nav_5902
- .nav_5910
- .nav_5920
- .nav_3501
- .nav_3502
related_tools:
- sdf2nav
- sdf2orientation
- sdfTool
- mergeAtt
- mergeNav
---

# sdf2omg

## Overview
`sdf2omg` converts Klein Sonar Data Format (`.sdf`) interferometric bathymetry and multi-channel sidescan records into OMG-HDCS v4 (`.merged`, `.merged.ss_data`, `.sonar_settings`, `.param`, `.orientation`) and JCU GLORIA sidescan (`.ss_*`) and navigation (`.nav_*`) files. It supports both Klein HydroChart 5000 (`page_version == 5004`) and Klein 5900 / 3500 series (`page_version == 5911`, `5902`, `5910`, `5920`, `3501`, `3502`) packets, including embedded Greensea INS attitude/position telegrams.

## Usage

```bash
sdf2omg [OPTIONS] -sdf <input_name.sdf> -omg <omg_file_prefix>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-sdf` | `<input_name.sdf>` | **Required** | Path to the input Klein `.sdf` file. |
| `-omg` | `<omg_file_prefix>` | **Required** | Output prefix for all generated `.merged`, `.orientation`, `.param`, `.ss_*`, and `.nav_*` files. |
| `-bin` | `<meters>` | `2 * range / 1000` | Across-track bin size (in meters) for reducing interferometric soundings into the 1000 OMG beam slots (`0..499` port, `500..999` starboard). |
| `-qf` | `<0.0..1.0>` | `0.65` | Minimum bathymetry quality factor required to include a sample when binning. |
| `-ignore_qf` | None | Off | Ignore quality factor filtering (`min_quality_factor = 0.0`). |
| `-frac_swath` | `<fraction>` | `0.0` (Full) | Extract only a fraction of the slant range when generating GLORIA sidescan records to preserve higher across-track pixel resolution. |
| `-logrange` | `<min_exp> <max_exp>` | `4.0 8.5` | Set the $\log_{10}$ dynamic range (`10^min` to `10^max`) used by `to8bit()` when compressing sidescan amplitudes to 8-bit GLORIA format. |
| `-override_minmax` | `<min> <max>` | Off | Override min/max scaling bounds for GLORIA sidescan conversion. |
| `-v` | None | Off | Print page versions and progress diagnostics. |
| `-debug` | None | Off | Enable debug flag. |

## How It Works
1. **Summary & Attitude Initialization:** Reads the first SDF record to determine `base_time` and initial towfish coordinates (`fish_lat`, `fish_lon`), initializes a 1000-beam OMG-HDCS v4 summary header (`toolType = HC5K`), and opens output files for bathymetry, Greensea attitude (`.orientation`), parameters (`.param`), and page-specific GLORIA sidescan/navigation streams.
2. **Page Version Dispatch:**
   * **`5004` (HydroChart 5000):** Writes raw SDF headers to `<prefix>.sonar_settings`, writes the 10 sidescan beams (5 port, 5 starboard) to `<prefix>.merged.ss_data`, filters `channel_5004` bathymetry samples by quality factor (`min_quality_factor`, default `0.65`), bins them across-track into 1000 beams, and writes `<prefix>.merged`.
   * **`5911` (Klein 5900 Bathymetry):** Extracts associated Greensea INS attitude/position/depth records (`reader->greensea`) to `<prefix>.orientation`, filters invalid (`-32768` / `0x8000`) and low-quality samples from `channel_5911`, bins across-track into 1000 OMG beams, and writes `<prefix>.merged`.
   * **`5902`, `5910`, `5920`, `3501`, `3502` (Sidescan):** Calls `write_out_glss_trace()` and `write_out_nav_fix()` to produce 8-bit GLORIA sidescan files (`.ss_5902`, `.ss_5902.slr`, `.ss_5910`, `.ss_5910.slr`, `.ss_5920`, `.ss_3501`, `.ss_3502`) and companion `.nav_*` files.
3. **Installation Angles:** Writes transducer roll mounting angles (`90.0 - depression_angle[0]` and `depression_angle[1] - 90.0`) to `<prefix>.param`.

## Practical Examples

**1. Convert a Klein HydroChart 5000 or 5900 `.sdf` file with 0.25 m across-track binning:**

```bash
sdf2omg -v -bin 0.25 -qf 0.65 -sdf line01.sdf -omg line01
```
