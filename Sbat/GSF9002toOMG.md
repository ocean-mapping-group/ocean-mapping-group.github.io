---
layout: default
title: GSF9002toOMG
parent: Reson SeaBat 9001/8101 Legacy (Sbat)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 2
tool_name: GSF9002toOMG
source_path: Sbat/GSF9002toOMG.c
category: format_conversion
input_formats:
- GSF
output_formats:
- OMG_HDCS
related_tools:
- 8101toOMG
- RESON2OMG
- Sbat2OMG
- gsf2omg
---

# GSF9002toOMG

## Overview

`GSF9002toOMG` reads 60-beam Reson SeaBat 9001/9002 multibeam bathymetry from Generic Sensor Format (GSF) files and converts it into OMG HDCS v2 `.merged` format (`toolType = Seabat9001`, `numDepths = 60`). It extracts SeaBat-specific sensor parameters (transmit power, receive gain, sonar range, mode), interprets HMPS beam edit flags (`gsfRec.mb_ping.beam_flags`), and computes 8-bit calibrated backscatter via `EM_convert_amplitude()`.

## Usage

```
GSF9002toOMG (-v) (-allowed 12) -old linename -new linename
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-old` | `<linename>` | *required* | Input GSF file containing 60-beam SeaBat 9001/9002 swath pings. |
| `-new` | `<linename>` | *required* | Output OMG HDCS v2 `.merged` file path. |
| `-allowed` | `<min_quality>` | `3` | Minimum acceptable GSF beam quality threshold. |
| `-v` | none | `0` | Enable verbose output (prints `gsfSeaBatSpecific` parameters and decoded HMPS beam flag bits). |

## How It Works

1. **GSF Reading & Sensor Metadata**: Opens the GSF file via `gsfOpen(..., GSF_READONLY_INDEX, ...)` and reads `GSF_RECORD_SWATH_BATHYMETRY_PING` records. Copies `gsfSeaBatSpecific.transmit_power`, `receive_gain`, `sonar_range`, and `mode` into the OMG HDCS profile header (`power`, `TVG`, `attenuation`, `mode`).
2. **HMPS Beam Flag Interpretation**: Inspects `gsfRec.mb_ping.beam_flags[i]`. If bit `1` (`HMPS_IGNORE` / do not use) is set (and the flag is not `1`), sets `beams[i].status = 22` (rejected) and optionally logs the rejection reason (`manually edited`, `filter edited`, `> 2 x IHO`, `exceeds maximum`).
3. **Backscatter Calibration**: Copies `mr_amplitude` to `reflectivity`, `mc_amplitude` to `pseudoAngleIndependentBackscatter`, and computes `calibratedBackscatter` via `EM_to_8bit(EM_convert_amplitude(...))`.

## Practical Examples

### Convert a SeaBat 9002 GSF file to OMG HDCS format

```bash
GSF9002toOMG -v -old sb9002_survey.gsf -new sb9002_survey.merged
```
