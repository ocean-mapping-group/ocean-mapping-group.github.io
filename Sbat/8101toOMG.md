---
layout: default
title: 8101toOMG
parent: Sbat Tools
nav_order: 1
tool_name: 8101toOMG
source_path: Sbat/8101toOMG.c
category: format_conversion
input_formats: [GSF]
output_formats: [OMG_HDCS]
related_tools: [GSF9002toOMG, RESON2OMG, Sbat2OMG, gsf2omg]
---

# 8101toOMG

## Overview

`8101toOMG` reads 101-beam Reson SeaBat 8101 multibeam bathymetry stored in Generic Sensor Format (GSF) files and converts it into OMG HDCS v2 `.merged` format (`toolType = SeaBat_8101`, `numDepths = 101`). Beams whose GSF quality factor falls below a user-specified threshold (`-allowed`) are flagged as rejected (`status = 22`).

## Usage

```
8101toOMG (-v) (-allowed 12) -old linename -new linename
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-old` | `<linename>` | *required* | Input GSF file containing SeaBat 8101 pings. |
| `-new` | `<linename>` | *required* | Output OMG HDCS v2 `.merged` file path. |
| `-allowed` | `<min_quality>` | `3` | Minimum acceptable GSF beam quality factor (`quality_factor[i] >= allowed`); beams below this value are flagged with `status = 22`. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **GSF Indexed Open**: Opens the input GSF file with `gsfOpen(fanname, GSF_READONLY_INDEX, &gsfHandle)` and forces `TZ=GMT`.
2. **Swath Bathymetry Conversion (`write_depth`)**:
   - Reads `GSF_RECORD_SWATH_BATHYMETRY_PING` records in a sequential loop.
   - Initializes the OMG HDCS v2 summary header (`toolType = SeaBat_8101`, `numDepths = 101`) using the first ping's latitude, longitude, and UTC timestamp.
   - Populates `OMG_HDCS_profile_header` with vessel position offsets, heading, heave, pitch, and roll.
   - Converts 101 beam depths, across-track distances, and along-track distances from meters to millimeters (`* 1000.0`).
   - Checks `gsfRec.mb_ping.quality_factor[i]`: if `>= allowed`, sets `beams[i].status = 0`; otherwise sets `beams[i].status = 22`. Stores the raw quality factor in `beams[i].range` and copies `mr_amplitude` (`reflectivity`) and `mc_amplitude` (`pseudoAngleIndependentBackscatter`).

## Practical Examples

### Convert a SeaBat 8101 GSF file with a minimum quality threshold of 3

```bash
8101toOMG -v -allowed 3 -old line01.gsf -new line01.merged
```
