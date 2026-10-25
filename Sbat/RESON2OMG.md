---
layout: default
title: RESON2OMG
parent: Sbat Tools
nav_order: 3
tool_name: RESON2OMG
source_path: Sbat/RESON2OMG.c
category: format_conversion
input_formats: [UNB_RESON]
output_formats: [OMG_HDCS]
related_tools: [Sbat2OMG, 8101toOMG, GSF9002toOMG]
---

# RESON2OMG

## Overview

`RESON2OMG` converts 60-beam UNB-Reson binary format SeaBat 9001 multibeam files (`RESON_NAV`, `RESON_DEPTH`, `RESON_SVP`, and `RESON_PARAMETER` telegrams framed by `RESON_STX`) into OMG HDCS v1 `.depth` files (`toolType = Seabat9001`, `numDepths = 60`).

## Usage

```
RESON2OMG (-v) (-allowed 3) -old linename -new linename
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-old` | `<linename>` | *required* | Input UNB-Reson binary file. |
| `-new` | `<linename>` | *required* | Output file prefix; creates `<linename>.depth`. |
| `-allowed` | `<min_quality>` | `3` | Minimum acceptable beam quality flag (`quality_flag >= allowed`); beams with lower quality are marked `status = 22`. |
| `-v` | none | `0` | Enable verbose output (prints telegram types, navigation, SVP, and per-beam depth/across/along/quality values). |

## How It Works

1. **Telegram Framing**: Scans the input file for `RESON_STX` start bytes and dispatches by telegram code (`reson_begin[1]`):
   - **`RESON_NAV_CODE`**: Reads `RESON_NAV` and prints navigation coordinates, UTM zone, and ellipsoid parameters (`write_nav`).
   - **`RESON_SVP_CODE`**: Reads `RESON_SVP` and prints sound velocity profile depth/velocity pairs (`write_svp`).
   - **`RESON_PARAM_CODE`**: Reads `RESON_PARAMETER` and prints roll/pitch/gyro offsets and transducer/antenna/VRU lever arms (`write_parameter`).
   - **`RESON_DEPTH_CODE`**: Reads `RESON_DEPTH` and writes a 60-beam swath profile to `<linename>.depth` (`write_depth`).
2. **Depth & Beam Conversion (`write_depth`)**:
   - Converts nanoradians (`lat_nR`, `lon_nR`) to degrees (`180.0 * val / 2.0e09`).
   - Scales 60 beam depths, across-track, and along-track values from centimeters to millimeters (`* 10`), projects geographic beam offsets (`latOffset`, `longOffset`) using vessel heading, and flags beams with `quality_flag < allowed` as `status = 22`.

## Practical Examples

### Convert a UNB-Reson binary SeaBat 9001 file into an OMG `.depth` file

```bash
RESON2OMG -v -allowed 3 -old line01.dat -new line01
```
This creates `line01.depth`.
