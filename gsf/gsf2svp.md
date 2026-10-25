---
layout: default
title: gsf2svp
parent: Generic Sensor Format — GSF (gsf)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 5
tool_name: gsf2svp
source_path: code/gsf/gsf2svp.c
category: Sound Velocity Profiles
input_formats:
- .gsf
output_formats:
- _001, _002... (OMG watercolumn SVP)
related_tools:
- gsf2omg
- gsf2orientation
- gsf2param
- gsfTool
- r2v
---

# gsf2svp

## Overview
`gsf2svp` extracts all `GSF_SOUND_VELOCITY_PROFILE` records from a Generic Sensor Format (`.gsf`) file and writes each profile into a numbered OMG `watercolumn` format v2 file (`<prefix>_001`, `<prefix>_002`, etc.).

## Usage

```bash
gsf2svp [-v] -gsf <input_name.gsf> -omg <omgfile.svp_prefix>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-gsf` | `<input_name.gsf>` | **Required** | Path to the input `.gsf` file. |
| `-omg` | `<omgfile.svp_prefix>` | **Required** | Output prefix; creates `<omgfile.svp_prefix>_001`, `<omgfile.svp_prefix>_002`, etc. |
| `-v` | None | Off | Print every parsed `GSF_Sound_Velocity_Profile` record to stdout. |

## How It Works
1. **Packet Scanning:** Loops through the `.gsf` file using `seek_GSF_packet(infile, GSF_SOUND_VELOCITY_PROFILE, &buffer)` and decodes each SVP record via `parse_GSF_Sound_Velocity_Profile()`.
2. **Conversion to OMG `watercolumn`:** For each SVP record `N`, opens `<outname>_NNN`, populates `time_of_obs`, `time_of_rec`, `lat_obs`, `lon_obs`, and converts each `(depth[i], sound_speed[i])` pair from centimeters and cm/s into meters and m/s (`/ 100.0`), writing the structure via `jWC_write()`.

## Practical Examples

**1. Extract all sound velocity profiles from a GSF file:**

```bash
# Creates line01.svp_001, line01.svp_002, etc.
gsf2svp -v -gsf line01.gsf -omg line01.svp
```
