---
layout: default
title: wassp2omg
parent: WASSP Tools
nav_order: 1
tool_name: wassp2omg
source_path: wassp/wassp2omg.c
category: format_conversion
input_formats: [WASSP]
output_formats: [OMG_HDCS, SONAR_SETTINGS]
related_tools: [wasspTool, mergeNav, SwathEd]
---

# wassp2omg

## Overview

`wassp2omg` converts binary data files acquired by ENL WASSP (Wide Angle Sonar Seafloor Profiler) multibeam systems (typically `.000` files) into OMG HDCS v4 `.merged` bathymetry files and companion `.sonar_settings` files. It extracts `GENBATHY` packets, computes preliminary observed depths and across-track distances from range, beam angle, and surface sound speed, and archives the raw `GENBATHY` packet header for each ping.

## Usage

```
wassp2omg (-v) -in input.000 -omg omg_file_prefix
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<input.000>` | *required* | Input WASSP binary file (`GENBATHY` packet stream). |
| `-omg` | `<omg_file_prefix>` | *required* | Output file prefix used to create `<omg_file_prefix>.merged` and `<omg_file_prefix>.sonar_settings`. |
| `-v` | none | `0` | Enable verbose diagnostic output. |

## How It Works

1. **Base Time Discovery**: `wassp2omg` scans the input WASSP file using `seek_next_WASSP_Packet()` until it finds the first `GENBATHY` packet. It decodes the UTC day, month, year, and milliseconds via `read_WASSP_Gen_Bathy()` to establish the reference epoch (`summary.refTime`) for the OMG HDCS v4 summary header (`toolType = WASSP`, `numDepths = WASSP_MAX_NUM_BEAMS`).
2. **Packet Iteration & Settings Archival**: After rewinding the file, it iterates through all `GENBATHY` packets. For each ping, it records the current byte offset of `<omg_file_prefix>.sonar_settings` in `profile.sonar_settings_offset` and writes the raw `WASSP_GEN_BATHY_HEADER_SIZE` header buffer (`bathy.header.inbuffer`) to `.sonar_settings`.
3. **Beam Geometry & Backscatter Population**:
   - Populates `profile.ping_number`, `profile.bathy_sample_rate` (`sampling_rate`), `profile.num_beams`, and `profile.td_sound_speed` (`sound_speed * 10.0`).
   - For each beam, computes two-way travel time `twtt = range / sampling_rate`, stores receive steering angle `Rc_steer = angle * 100.0`, and computes preliminary constant-velocity depth (`range * cos(angle) * 1000.0` mm) and across-track distance (`-range * sin(angle) * 1000.0` mm) where `range = twtt * sound_speed / 2.0`.
   - Stores beam backscatter (in dB) rounded to an unsigned byte in `beams[i].reflectivity`.
4. **Output**: Writes each profile and beam array to `<omg_file_prefix>.merged`.

## Practical Examples

### Convert a WASSP `.000` file to OMG HDCS format

```bash
wassp2omg -v -in survey_001.000 -omg survey_001
```
This generates `survey_001.merged` and `survey_001.sonar_settings`.
