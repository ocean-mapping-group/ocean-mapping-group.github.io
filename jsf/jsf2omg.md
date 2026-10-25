---
layout: default
title: jsf2omg
parent: JSF Tools
nav_order: 3
tool_name: jsf2omg
source_path: code/jsf/jsf2omg.c
category: Raw Data Unraveling
input_formats: [".jsf"]
output_formats: [".merged", ".merged.ss_data", ".sonar_settings", ".param"]
related_tools: ["jsf2nav", "jsf2orientation", "jsf2glo", "jsfTool", "mergeAtt", "mergeNav"]
---

# jsf2omg

## Overview
`jsf2omg` converts EdgeTech interferometric bathymetry data (`JSF_Bathymetric_3000_Data`, message type `3000`) and pressure/sound-speed sensor data (`JSF_Pressure_3002_Data`, message type `3002`) from an EdgeTech `.jsf` file (such as EdgeTech 4600, 6205, or Gavia AUV 2205 systems) into a 1000-beam OMG-HDCS v4 `.merged` file (`toolType = EdgeTech_4600`), along with a `.param` file containing the $60^\circ$ port/starboard transducer mount angles. Because interferometric sonars produce thousands of raw angle/range samples per ping channel, `jsf2omg` filters samples by quality factor, amplitude, angle, and water-column/non-seabed flags, and averages them into 1000 across-track spatial bins (500 port, 500 starboard) or preserves raw sample indices when `-dontbin` is specified.

## Usage
```bash
jsf2omg (-bin <m> | -dontbin) [OPTIONS] -jsf <input_name.jsf> -omg <omg_file_prefix>
```

> [!IMPORTANT]
> You **must** specify either `-bin <meters>` or `-dontbin` on the command line; otherwise `jsf2omg` exits with `Must specify across-track binsize (m)`.

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-jsf` | `<input_name.jsf>` | **Required** | Path to the input EdgeTech `.jsf` file. |
| `-omg` | `<omg_file_prefix>` | **Required** | Output prefix for `.merged`, `.merged.ss_data`, `.sonar_settings`, and `.param`. |
| `-bin` | `<meters>` | **Required** (or `-dontbin`) | Across-track bin width in meters used to average interferometric soundings into the 1000 OMG beam slots (bins `0..499` port, `500..999` starboard). |
| `-dontbin` | None | Off | Do not spatially bin across-track; assign port samples directly to beams `499 - i` and starboard samples to `501 + i`. |
| `-min_qf` | `<0.0..1.0>` | `0.70` | Minimum bathymetry quality factor (`((quality & 0xFF00) >> 8) / 255.0`) required to accept a sample. |
| `-min_amplitude` | `<int>` | `10` | Minimum raw sample amplitude required to accept a sounding. |
| `-max_angle` | `<degrees>` | `90.0` | Maximum vertically referenced angle (degrees from nadir) to accept. |
| `-min_angle` | `<degrees>` | `-20.0` | Minimum vertically referenced angle (degrees) to accept (prevents cross-nadir leakage). |
| `-ignore_wc` | None | Off | Reject samples flagged as water column (`quality & 0x0001`). |
| `-ignore_nonseabed` | None | Off | Reject samples flagged as non-seabed (`quality & 0x0002`). |
| `-v` | None | Off | Print parsed message structures and per-sample binning details. |
| `-debug` | None | Off | Enable debug flag. |

## How It Works
1. **Initial Scan:** Scans the `.jsf` file for the first message `3002` (`JSF_Pressure_3002_Data`) to obtain initial `sound_speed` and the first message `3000` (`JSF_Bathymetric_3000_Data`) to establish `base_time`, then rewinds to the start of the file.
2. **Quality Filtering & Across-Track Binning:** For each message `3000` (channel `0` = port, channel `1` = starboard), filters each sample by `-min_qf`, `-ignore_wc`, `-ignore_nonseabed`, `-min_amplitude`, `-max_angle`, and `-min_angle`. Computes slant range (`twtt * sound_speed / 2.0`), across-track distance (`-range * sin(angle)`), and depth (`range * cos(angle)`), and accumulates valid samples into `binned_beams[0..999]`, subtracting the $60^\circ$ transducer mount angle so `Rc_steer` is stored relative to the transducer normal.
3. **AUV Pressure Depth & OMG Output:** When both port and starboard channels of a ping have been accumulated, incorporates any AUV/towfish pressure depth (`last_good_pressure_depth` from message `3002`) into `profile.deepdraftoffset_in_metres`, `profile.draft_at_Tx`, and `beams[i].observedDepth`, stores the sample count per bin in `beams[i].Q_factor`, and writes the 1000-beam profile to `<prefix>.merged`. Finally, writes `dRoll = +60.0` and `-60.0` to `<prefix>.param`.

## Practical Examples

**1. Convert an EdgeTech 4600/6205 JSF file using 0.20 m across-track bins:**
```bash
jsf2omg -bin 0.20 -min_qf 0.75 -ignore_wc -ignore_nonseabed -jsf line01.jsf -omg line01
```
