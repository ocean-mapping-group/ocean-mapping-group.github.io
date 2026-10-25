---
layout: default
title: gsf2param
parent: Generic Sensor Format — GSF (gsf)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 4
tool_name: gsf2param
source_path: code/gsf/gsf2param.c
category: Lever-Arm & Calibration
input_formats:
- .gsf
output_formats:
- .param
related_tools:
- gsf2omg
- gsf2orientation
- gsf2svp
- gsfTool
- r2v
---

# gsf2param

## Overview
`gsf2param` extracts sensor lever-arm and angular alignment parameters from the first `GSF_SENSOR_PARAMETERS` record in a `.gsf` file and writes them to an ASCII OMG `.param` file.

## Usage

```bash
gsf2param [-v] -gsf <input_name.gsf> -omg <omgfile.param>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-gsf` | `<input_name.gsf>` | **Required** | Path to the input `.gsf` file. |
| `-omg` | `<omgfile.param>` | **Required** | Path to the output ASCII OMG `.param` file. |
| `-v` | None | Off | Print all `KEY=VALUE` pairs in the `GSF_Sensor_Parameters` record. |

## How It Works
1. **Record Lookup:** Seeks to the first `GSF_SENSOR_PARAMETERS` record via `seek_GSF_packet()` and parses the `num_params` ASCII `KEY=VALUE` strings (`parse_GSF_Sensor_Parameters`).
2. **Key-Value Mapping:** Splits each parameter string on `=` and maps recognized GSF keys to `OMG_HDCS_sonar_params`:
   * `ROLL_OFFSET`, `PITCH_OFFSET`, `GYRO_OFFSET` $\rightarrow$ `sonar[0].dRoll`, `dPitch`, `dHeading`
   * `TRANSDUCER_X_OFFSET`, `TRANSDUCER_Y_OFFSET`, `TRANSDUCER_Z_OFFSET` $\rightarrow$ `sonar[0].Xloc`, `Yloc`, `Zloc`
   * `TRANSDUCER_DEPTH`, `TRANSDUCER_Z_OFFSET` $\rightarrow$ `WLZ` (`Zloc - TRANSDUCER_DEPTH`)
   * `NAV_REFERENCE_X`, `Y`, `Z` $\rightarrow$ `pos[0].Xloc`, `Yloc`, `Zloc`
   * `MOTION_SENSOR_X`, `Y`, `Z` $\rightarrow$ `imu[0].Xloc`, `Yloc`, `Zloc`
3. **Output:** Calls `OMG_HDCS_write_params()` to format and write `<omgfile.param>`.

## Practical Examples

**1. Extract lever-arm offsets from a GSF file into an OMG `.param` file:**

```bash
gsf2param -v -gsf line01.gsf -omg line01.param
```
