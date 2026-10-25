---
layout: default
title: MB-System .mb1 Format (mb1)
parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 10
has_children: true
source_path: code/mb1/
category: Raw Data Unraveling & Format Conversion
related_tools:
- mbone2omg
- mboneTool
- makess
- get_ADH_SRA
- swathed
---

# Teledyne MB1 Tools (`mb1/`)

## Overview

The `mb1/` (`code/mb1/`) directory contains command-line tools authored by Jonathan Beaudoin (circa August 2013) for inspecting and unpacking **Teledyne Reson / Odom `.tdy` (Teledyne MB1 / RTA1)** multibeam sonar files into the **OMG-HDCS Version 4** format.

Teledyne's `.tdy` data format encapsulates multibeam bathymetry, raw sonar settings, per-beam time-series backscatter snippets, and full beamformed water column amplitude/phase records inside `TDYMB01` packets (`MB1_ID_TDYMB01`), alongside file header packets (`MB1_ID_FILE_HEADER`) and real-time appliance packets (`TDYRTA1`, `MB1_ID_TDYRTA1_0..4`). The tools in `mb1/` provide packet-level diagnostics and full conversion into OMG `.merged`, `.merged.ss_data`, `.sonar_settings`, and `.watercol` files.

---

## Tools in `mb1/`

| Tool | Source File | Primary Role | Input Formats | Output Formats |
| :--- | :--- | :--- | :--- | :--- |
| **[`mbone2omg`](mbone2omg.html)** | `code/mb1/mbone2omg.c` | Unpacks Teledyne `.tdy` (`TDYMB01`) multibeam files into OMG-HDCS v4 `.merged`, `.merged.ss_data` (float snippets), `.sonar_settings`, `.watercol`, and `wc_image.r4`. | `.tdy` (Teledyne MB1) | `.merged`, `.merged.ss_data`, `.sonar_settings`, `.watercol`, `wc_image.r4` |
| **[`mboneTool`](mboneTool.html)** | `code/mb1/mboneTool.c` | Diagnostic packet scanner and inventory tool that counts, validates, and pretty-prints `FILE_HEADER`, `TDYMB01`, and `TDYRTA1` records in a `.tdy` file. | `.tdy` (Teledyne MB1) | Terminal packet inventory & header dumps |

---

## Core Library Architecture (`omg_mb1.h`)

Both tools rely on the Teledyne MB1 parser and radiometric calibration library declared in `/home/iwc/local/include/omg_mb1.h` (linked via `liblocal.a`) and integrated with downstream OMG tools (`code/omg/makess.c` and `code/omg/get_ADH_SRA.c`):

| Struct / Constant | Description |
| :--- | :--- |
| `MB1_MAX_NUM_BEAMS` (`512`) | Maximum beam slots allocated per ping in `OMG_HDCS_summary_header` (`toolType = Teledyne_MB1`). |
| `MB1_File_Header` (`61` bytes) | File-level header containing a 48-byte `header_id`, UTC start date/time (`year`, `month`, `day`, `hour`, `minute`, `second`, `milliseconds`), and 4 reserved bytes. |
| `MB1_MB01_Header` (`81` bytes base) | Master ping header containing `packet_size`, `version`, `sonar_head`, `model[8]`, `serial_number`, firmware versions (`DSP`, `COMM`, `RTA`, `TSPU`), `ping` number, segment byte offsets (`offset_TIME_segment`, `offset_RAW_segment`, `offset_PROC_segment`, `offset_AR_segment`, `offset_QUAL_segment`, `offset_SNIPPET_segment`, `offset_SS_segment`, `offset_WC_segment`), and embedded sub-record structs: `MB1_TDY_TIME`, `MB1_TDY_RAW`, `MB1_TDY_PROC`, `MB1_TDY_AR`, `MB1_TDY_QUAL`, `MB1_TDY_SS`, `MB1_TDY_SNIP`, and `MB1_TDY_WC`. |
| `MB1_RTA1_Header` (`31` bytes base) | Real-Time Appliance packet header (`sub_id` `0`, `1`, `2`, or `4`, timestamp, `data_length`, and `OMG_Buffer buffer`). |
| `MB1_Calibrator` | Used by `makess` (`calibrate_mb1()`) together with `<prefix>.sonar_settings` (`load_MB1_sonar_settings()`) to radiometrically calibrate Teledyne MB1 snippet amplitudes into 8-bit dB backscatter. |
