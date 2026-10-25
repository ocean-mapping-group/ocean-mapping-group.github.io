---
layout: default
title: omg2gsf
parent: Generic Sensor Format — GSF (gsf)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 8
tool_name: omg2gsf
source_path: code/gsf/omg2gsf.c
category: Format Export
input_formats:
- .merged
- .merged.ss_data
- .sonar_settings
- .param
- .orientation
output_formats:
- .gsf
related_tools:
- gsftest
- gsf2omg
- gsf2omg_7101
- 7k2omg
- r2sonic2omg
---

# omg2gsf

## Overview
`omg2gsf` exports processed OMG-HDCS `.merged` multibeam files (along with companion `.param`, `.sonar_settings`, `.merged.ss_data`, and `.orientation` files) into the standard SAIC/Leidos Generic Sensor Format (`.gsf`). For **R2Sonic (`2022`, `2024`)** and **Reson 7k (`SeaBat_7125`, `SeaBat_7160`, `Reson_T20P`)** datasets, `omg2gsf` populates full sensor-specific GSF subrecords and 16-bit Bathymetric Receive Beam (`brb_inten`) snippet time series. When `-correct_imagery` is enabled on SeaBat 7125 data, it computes seafloor grazing angles and applies full radiometric TVG/transmission-loss calibration (`calibrate_reson_7K`), encoding calibrated snippets in 0.1 dB units.

## Usage

```bash
omg2gsf [OPTIONS] -in <filename.merged> [-out <outfile.gsf>]
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<filename.merged>` | **Required** | Path to the input OMG-HDCS `.merged` file. Automatically looks for `<basename>.param`, `<basename>.sonar_settings`, `<filename.merged>.ss_data`, and (if `-dump_orientation` is set) `<basename>.orientation`. |
| `-out` | `<outfile.gsf>` | `<basename>.gsf` | Path to the output `.gsf` file. |
| `-correct_imagery` | None | Off | Radiometrically calibrate Reson 7125 snippet imagery (`calibrate_reson_7K` using 3D seafloor grazing angles) and write 16-bit signed shorts in 0.1 dB resolution (`GSF_INTENSITY_CALIBRATED`). |
| `-dB_shift` | `<dB>` | `0.0` | Additive decibel shift applied during `-correct_imagery` calibration. |
| `-dB_scale` | `<int>` | `2` | Scale factor passed to `calibrate_reson_7K`. |
| `-attenuation` | `<dB/km>` | `0.0` (From settings) | Override seawater absorption coefficient when computing transmission loss during `-correct_imagery`. |
| `-reverse_rx_beam_angle` | None | Off | Negate the OMG receiver steering angle (`-1 * beams[j].rc_steer`) when writing `mb_ping.beam_angle[j]`. |
| `-ignore_tide` | None | Tide applied | Ignore the OMG `profile.tide` field and set `tide_corrector = GSF_NULL_TIDE_CORRECTOR` (by default, `tide` is written and subtracted from `beams[j].depth`). |
| `-dump_orientation` | None | Off | Append all high-rate attitude records from `<basename>.orientation` as `GSF_RECORD_ATTITUDE` packets at the end of the `.gsf` file. |
| `-min_lat` | `<deg>` | `-90.0` | Minimum latitude bounding box filter; pings south of `<deg>` are skipped. |
| `-max_lat` | `<deg>` | `90.0` | Maximum latitude bounding box filter; pings north of `<deg>` are skipped. |
| `-min_lon` | `<deg>` | `-180.0` | Minimum longitude bounding box filter; pings west of `<deg>` are skipped. |
| `-max_lon` | `<deg>` | `360.0` | Maximum longitude bounding box filter; pings east of `<deg>` are skipped. |
| `-verbose` | None | Off | Print imagery array growth and diagnostic messages (note: flag is `-verbose`, not `-v`). |

## How It Works
1. **Companion File Loading:** Reads the `.merged` summary header, loads `<basename>.param` (`OMG_HDCS_load_params`), opens `<basename>.sonar_settings` (required for R2Sonic 2022/2024 and Reson 7125/7160/T20P), and opens `<filename.merged>.ss_data` if available.
2. **GSF Header & Metadata Records:** Creates the output `.gsf` file and writes:
   * `GSF_RECORD_HEADER`
   * `GSF_RECORD_SWATH_BATHY_SUMMARY` (time bounds and geographic bounding box)
   * `GSF_RECORD_PROCESSING_PARAMETERS` (marking roll, pitch, heave, ray-tracing, and optionally tide as `GSF_COMPENSATED`, and depths as `GSF_TRUE_DEPTHS`)
   * `GSF_RECORD_COMMENT` (when `-correct_imagery` is enabled, documenting the 16-bit 0.1 dB calibrated snippet encoding)
3. **Swath Bathymetry & Snippet Export:** For each ping within the lat/lon bounds, reads rationalized profile/beam records (`OMG_get_rational_profile`, `OMG_get_rational_beams`), loads raw sonar settings from `.sonar_settings`, optionally computes full 3D grazing angles (`get_full_grazing_angles`) and calibrates snippets (`calibrate_reson_7K`), populates `gsfR2SonicSpecific` or `gsfReson7100Specific` subrecords, and writes `GSF_RECORD_SWATH_BATHYMETRY_PING`.
4. **High-Rate Attitude Export:** If `-dump_orientation` is set, reads `<basename>.orientation` and writes each record as a `GSF_RECORD_ATTITUDE` packet.

## Practical Examples

**1. Export a processed Reson 7125 `.merged` file to GSF with calibrated 0.1 dB snippet imagery and attitude:**

```bash
omg2gsf -correct_imagery -dump_orientation -in line01.merged -out line01.gsf
```

**2. Export an R2Sonic 2024 `.merged` file within a geographic bounding box without tide correction:**

```bash
omg2gsf -ignore_tide -min_lat 44.5 -max_lat 45.2 -min_lon -66.5 -max_lon -65.8 -in r2s_line.merged -out r2s_line.gsf
```
