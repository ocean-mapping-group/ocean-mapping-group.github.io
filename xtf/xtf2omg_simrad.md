---
layout: default
title: xtf2omg_simrad
parent: eXtended Triton Format — XTF (xtf)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 11
tool_name: xtf2omg_simrad
source_path: code/xtf/xtf2omg_simrad.c
category: Raw Data Unraveling
input_formats:
- .xtf
- .idx
output_formats:
- .merged
- .merged.ss_data
related_tools:
- em3002omg
- RTlite
- xtf2nav
- xtf2orientation
- xtf2param
- xtfTool
---

# xtf2omg_simrad

## Overview
`xtf2omg_simrad` converts Kongsberg/Simrad EM3000 and EM3002 multibeam data logged inside Triton XTF (`XTF_HEADER_BATHY`, packet ID 2) into OMG-HDCS v4 `.merged` and `.merged.ss_data` files. It parses embedded Simrad Raw Range and Beam Angle datagrams (both legacy `EM3000_RAW_TANG_CODE` and new `EM3000_NEW_RAW_TANG_CODE`) as well as Seabed Image snippet datagrams (`EM3000_IMAGE_CODE`).

## Usage

```bash
xtf2omg_simrad (-LE | -BE) [-v] [-v_bathy] [-debug] [-dual_head] [-check_drift] -xtf <inputfile.xtf> -omg <outputfile.merged>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-xtf` | `<inputfile.xtf>` | **Required** | Path to the input `.xtf` file (automatically uses `<basename>.idx` if available). |
| `-omg` | `<outputfile.merged>` | **Required** | Path to the output `.merged` file (also writes `<outputfile.merged>.ss_data` if Simrad Seabed Image telegrams are present). |
| `-LE` | None | **Required** (or `-BE`) | Set input Simrad datagram byte ordering to Little-Endian (`SIMRAD_LITTLE_ENDIAN`). |
| `-BE` | None | **Required** (or `-LE`) | Set input Simrad datagram byte ordering to Big-Endian (`SIMRAD_BIG_ENDIAN`). |
| `-dual_head` | None | Single head | Force dual-head OMG tool type (`EM3000D` instead of `EM3000`, or `EM3002D` instead of `EM3002`). |
| `-check_drift` | None | Off | Store the millisecond clock drift (`xtfBathy.AttitudeTimeTag - simradRangeAngle.header.raw_ms_time`) in `profile.clock_drift_millis`. |
| `-v` | None | Off | Enable verbose progress output. |
| `-v_bathy` | None | Off | Print detailed XTF bathy headers, Simrad range/angle structures, and Seabed Image structures for every ping. |
| `-debug` | None | Off | Enable debug flag. |

## How It Works
1. **Byte Order & Indexing:** Requires explicit specification of `-LE` or `-BE` for the embedded Simrad telegrams. Loads `<basename>.idx` or builds an XTF index via `buildXTFIndex()`, and computes `baseTime` using `SIMRAD_SYNCHRO`.
2. **Seabed Image Matching:** Calls `check_for_image_telegram()` to test whether `XTF_HEADER_BATHY` records alternate between Raw Range/Angle and Seabed Image (`EM3000_IMAGE_CODE`) datagrams. If image datagrams exist, `match_image_telegrams()` pairs them with range/angle datagrams by matching `simradHeader.counter` and opens `<outname>.ss_data`.
3. **Range/Angle Promotion & Summary Init:** Legacy `EM3000_RAW_TANG_CODE` datagrams are promoted in-memory to `Simrad_Range_Angle_new` structures (with default sampling frequency `14621 Hz`). The summary header is initialized with 128 beams (`EM3000`/`EM3000D`) or 256 beams (`EM3002`/`EM3002D`).
4. **Beam & Snippet Output:** Marks unpopulated beam slots with `status = 22`, stores `raw_twtt / 2` in `range` (and `raw_twtt` in `other_range`), writes 8-bit snippet trace samples to `<outname>.ss_data`, and records `Tx_steer` and `Rc_steer` angles.

## Practical Examples

**1. Convert a Little-Endian Simrad EM3000 Dual-Head XTF file:**

```bash
xtf2omg_simrad -LE -dual_head -v -xtf em3000d_line01.xtf -omg em3000d_line01.merged
```
