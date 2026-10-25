---
layout: default
title: xse2omg
parent: XSE Tools
nav_order: 1
tool_name: xse2omg
source_path: xse/xse2omg.c
category: format_conversion
input_formats: [XSE]
output_formats: [OMG_HDCS, JCU_NAV, OMG_ORIENTATION, GLORIA, OMG_PARAM, OMG_SVP]
related_tools: [xseTool, mergeNav, mergeOrientation, SwathEd]
---

# xse2omg

## Overview

`xse2omg` converts binary `.xse` (eXtended Sensor Exchange) files from L-3 / ELAC Nautik / SeaBeam multibeam systems into a suite of OMG processing files: `.merged` (OMG HDCS v3 bathymetry, `toolType = SB2100`, 151 beams), `.nav` (1 Hz navigation with heading), `.orientation` (roll, pitch, heave), `.ss` (1024-pixel GLORIA sidescan), `.param` (lever arms and alignment offsets from the XSE Ship frame), and `.svp` (sound velocity profiles). It also includes specialized beam-repointing and cone-intersection logic (`-dead_sea`) developed to correct hypersaline Dead Sea surveys (~1810 m/s) where the acquisition system used an incorrect 1500 m/s surface sound speed.

## Usage

```
xse2omg (-v) (-log) (-dead_sea) (-real_mount 38.0) (-fake_mount 30.0) \
        (-repoint_from 1500.0) (-repoint_to 1810.0) (-extend_sv 500.0 1817.9) \
        (-min_ss 3000) (-max_ss 25000) (-min_depth 5) (-draft 0.78) \
        (-dont_raytrace) -in infile.xse -out outfile_prefix
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<infile.xse>` | *required* | Input `.xse` binary file. |
| `-out` | `<outfile_prefix>` | *required* | Prefix for output `.merged`, `.nav`, `.orientation`, `.ss`, `.param`, and `.svp` files. |
| `-v` | none | `0` | Enable verbose output. |
| `-log` | none | `PACK16_LINEAR` | Use logarithmic 16-to-8-bit compression (`PACK16_LOG`) for sidescan amplitudes instead of linear scaling. |
| `-min_ss` | `<value>` | `0` | Minimum 16-bit sidescan amplitude threshold for 8-bit scaling. |
| `-max_ss` | `<value>` | `30000` | Maximum 16-bit sidescan amplitude threshold for 8-bit scaling. |
| `-min_depth` | `<meters>` | `-999` | Minimum depth threshold; beams with depth `<= min_depth` are omitted. |
| `-draft` | `<meters>` | `0` (from Ship frame) | Override transducer draft from the XSE Ship frame with a user-specified value in meters. |
| `-dont_raytrace` | none | raytrace enabled | Disable raytracing through the `.xse` sound velocity profile and compute constant-velocity depths instead. |
| `-extend_sv` | none | `0` | Append a terminal depth/velocity pair (`500.0 m`, `1817.9 m/s`) to the sound velocity profile (note: the parser consumes `-extend_sv` as a flag without reading numeric arguments). |
| `-dead_sea` | none | `0` | Enable hypersaline Dead Sea beam-repointing and 3D cone intersection (`1810 m/s`). |
| `-real_mount` | `<deg>` | `38.0` | True physical transducer mounting angle in degrees (used with `-dead_sea`). |
| `-fake_mount` | `<deg>` | `38.0` | Assumed mounting angle in degrees used by the acquisition system for both transducers. |
| `-fake_mount_port` | `<deg>` | `fake_mount` | Assumed port transducer mounting angle in degrees. |
| `-fake_mount_stbd` | `<deg>` | `fake_mount` | Assumed starboard transducer mounting angle in degrees. |
| `-repoint_from` | `<m/s>` | `0` | Original (incorrect) sound speed in m/s used during beam steering (`repoint_angle`). |
| `-repoint_to` | `<m/s>` | `0` | True sound speed in m/s for re-steering beam angles (`repoint_angle`). |

## How It Works

1. **Initial Navigation Scan**: Scans the `.xse` file for the first Frame ID `1` (Navigation Frame) with valid position (`valid_group[2]`) to initialize `base_time`, `base_lat`, and `base_long` in the `.merged` summary header (`fileVersion = 3`, `toolType = SB2100`, `numDepths = 151`).
2. **Frame Dispatch Loop**:
   - **Frame ID 1 (Navigation Frame)**: Group 2 position records (`x`, `y` in radians, `heading` in radians) are converted to degrees and written to `<outfile_prefix>.nav`. Because XSE places heading in the navigation group rather than the attitude group, `mergeNav -hdg` must be run afterwards to transfer heading to `.merged`. Group 7 attitude records (roll, pitch, heave) are written to `<outfile_prefix>.orientation`.
   - **Frame ID 2 (Sound Velocity Frame)**: Frames with `num_samples > 1` are written to `<outfile_prefix>.svp` via `jWC_write()` and interpolated to 1 m bins (`jWC_interp_zv`) for in-line raytracing.
   - **Frame ID 4 (Ship Frame)**: Converts XSE ship coordinate offsets (where X is port-positive and Y is bow-forward) to OMG sensor coordinates (X forward, Y starboard-positive, Z down) and writes `<outfile_prefix>.param`.
   - **Frame ID 5 (Sidescan Frame)**: Compresses 16-bit slant-range-corrected amplitudes to 8-bit (`jK_collapse_16_to_8`), resamples the swath into 1024 pixels (reversing the sample order to match OMG convention), and writes GLORIA records to `<outfile_prefix>.ss`.
   - **Frame ID 6 (Multibeam Frame)**: Reverses beam numbering from XSE's starboard-to-port order (`num_beams - i - 1`) to OMG's port-to-starboard order, rejects beams with `quality >= 8` or `depth <= min_depth`, optionally applies `-dead_sea` Snell's law repointing (`repoint_angle` + `intersect_cones`) and raytracing (`raytrace`), converts 0.1 dB amplitudes to 0.5 dB OMG `reflectivity` units, and writes profiles and beams to `<outfile_prefix>.merged`.

## Practical Examples

### Standard conversion of an XSE file to OMG formats

```bash
xse2omg -v -in line04.xse -out line04
mergeNav -hdg line04.nav line04.merged
mergeOrientation -in line04.orientation -merged line04.merged
```

### Reprocess Dead Sea XSE data with beam repointing

```bash
xse2omg -dead_sea -real_mount 38.0 -fake_mount 30.0 \
        -repoint_from 1500.0 -repoint_to 1810.0 -extend_sv \
        -in deadsea_01.xse -out deadsea_01
```
