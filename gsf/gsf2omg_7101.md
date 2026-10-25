---
layout: default
title: gsf2omg_7101
parent: Generic Sensor Format — GSF (gsf)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 2
tool_name: gsf2omg_7101
source_path: code/gsf/gsf2omg_7101.c
category: Raw Data Unraveling
input_formats:
- .gsf
output_formats:
- .merged
- .merged.ss_data
- .sonar_settings
- .nav
related_tools:
- gsf2omg
- 7k2omg
- gsftest
- omg2gsf
- mergeNav
---

# gsf2omg_7101

## Overview
`gsf2omg_7101` converts GSF (`GSF_RECORD_SWATH_BATHYMETRY_PING`) files logged from Reson SeaBat 7101 / 7125 systems (or Kongsberg EM122 systems when `-sonar_EM122` is specified) into OMG-HDCS v4 `.merged`, `.merged.ss_data`, `.sonar_settings`, and `.nav` files using the full `gsf_lib` library. For Reson 7100-series data, it reconstructs synthetic 7k `7000` Sonar Settings records (`RESON_7K_7000_SIZE`) from the `t_gsfReson7100Specific` subrecord and extracts Bathymetric Receive Beam (`brb_inten`) snippet time series into `.merged.ss_data`.

## Usage

```bash
gsf2omg_7101 [-sonar_EM122] -in <filename.gsf> -omg <prefix>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<filename.gsf>` | **Required** | Path to the input `.gsf` file. |
| `-omg` | `<prefix>` | **Required** | Output prefix for `<prefix>.merged`, `<prefix>.merged.ss_data`, `<prefix>.sonar_settings`, and `<prefix>.nav`. |
| `-sonar_EM122` | None | `SeaBat_7101` | Set OMG `toolType` to Kongsberg `EM122` and skip Reson 7100-specific `.sonar_settings` and `brb_inten` snippet extraction. |

## How It Works
1. **GSF Reading & Summary Setup:** Opens the input file via `gsfOpen(inname, GSF_READONLY, &handle)` and iterates through `GSF_RECORD_SWATH_BATHYMETRY_PING` records. Initializes an OMG-HDCS v4 summary header with `toolType = SeaBat_7101` (or `EM122`).
2. **Reson 7000 Settings Reconstruction:** When `-sonar_EM122` is not set, `pack_raw_settings()` serializes the `gsfReson7100Specific` fields (serial numbers, ping number, frequency, sample rate, bandwidth, pulse width, power, gain, projector/hydrophone beamwidths and windows, absorption, sound velocity, and spreading) into a little-endian `RESON_7K_7000_SIZE` byte buffer written to `<prefix>.sonar_settings`.
3. **Beam & Snippet Extraction:** Converts `travel_time`, `beam_angle` (negated to match OMG convention), `depth`, `across_track`, and `along_track` into `OMG_HDCS_beam` structures. For Reson 7100 data, writes 16-bit big-endian snippet traces from `in_record.mb_ping.brb_inten->time_series[j]` to `<prefix>.merged.ss_data` and computes a 10-sample window mean around `detect_sample` for `beams[j].reflectivity` (`2 * 20 * log10(mean)`). Also writes per-ping navigation fixes to `<prefix>.nav`.

## Practical Examples

**1. Convert a Reson 7101/7125 GSF file into OMG-HDCS v4 files:**

```bash
gsf2omg_7101 -in survey_7101.gsf -omg survey_7101
```

**2. Convert a Kongsberg EM122 GSF file (e.g., USNS Maury) into OMG-HDCS v4:**

```bash
gsf2omg_7101 -sonar_EM122 -in maury_em122.gsf -omg maury_em122
```
