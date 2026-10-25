---
layout: default
title: xtf2omg_r2sonic
parent: eXtended Triton Format — XTF (xtf)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 9
tool_name: xtf2omg_r2sonic
source_path: code/xtf/xtf2omg_r2sonic.c
category: Raw Data Unraveling
input_formats:
- .xtf
- .idx
output_formats:
- .merged
- .merged.ss_data
- .sonar_settings
related_tools:
- r2sonic2omg
- xtf2nav
- xtf2orientation
- xtf2param
- xtfTool
---

# xtf2omg_r2sonic

## Overview
`xtf2omg_r2sonic` converts R2Sonic multibeam sonar data (Sonic 2022 and 2024) logged in Triton XTF (`.xtf`) format into OMG-HDCS v4 files (`.merged`, `.merged.ss_data`, and `.sonar_settings`). It supports both native R2Sonic bathymetry packets (XTF packet ID 65) and QINSy Multibeam Entry (`QMBE`, XTF packet ID 28) packets, and pairs them with R2Sonic Footprint Time Series (`FTS`, XTF packet ID 66) snippet packets when present.

## Usage

```bash
xtf2omg_r2sonic [-v] [-debug] [-sonar <2022|2024>] -xtf <input.xtf> -omg <omg_prefix>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-xtf` | `<input.xtf>` | **Required** | Path to the input `.xtf` file (reads `<basename>.idx` if present). |
| `-omg` | `<omg_prefix>` | **Required** | Output prefix for `.merged`, `.merged.ss_data`, and `.sonar_settings`. Cannot match `-xtf`. |
| `-sonar` | `2022` \| `2024` | Auto from FTS | Specify the R2Sonic model number (`2022` or `2024`). **Required** if the XTF file does not contain FTS snippet packets (ID 66), because model string metadata is read from the FTS header. |
| `-v` | None | Off | Enable verbose progress output. |
| `-debug` | None | Off | Enable debug diagnostics. |

## How It Works
1. **Indexing & Packet Selection:** Reads `<basename>.idx` or builds an XTF index. Checks for bathymetry packets in ID 28 (`XTFHEADERQMBEENTRY`) or ID 65 (`R2SONIC_BATHY`), preferring ID 28 if both exist.
2. **FTS Matching & Sonar Settings:** Checks for R2Sonic FTS snippet packets (ID 66) and sets `fts.qinsy_flag = 1` to handle QINSy's unfragmented FTS packet size quirk. For each ping, `gimme_matching_FTS_packet()` searches forward/backward in packet ID 66 to match `AttitudeTimeTag`, writing the raw FTS H0 header (`R2SONIC_FTS_H0_SIZE`) to `<prefix>.sonar_settings` and storing the byte offset in `profile.sonar_settings_offset`.
3. **Beam & Snippet Conversion:**
   * Negates R2Sonic beam angles (`Rc_steer = -angle * 100.0`) to match the OMG sign convention (positive to starboard, whereas R2Sonic uses positive to port).
   * Extracts phase/amplitude detection flags from `bathy.beam[i].quality & 0x08`.
   * Computes preliminary `observedDepth` and `acrossTrack` coordinates in millimeters.
   * Writes big-endian 16-bit FTS snippet samples to `<prefix>.merged.ss_data` and computes mean snippet reflectivity in 0.5 dB OMG units (`2 * 20 * log10(mean)`).

## Output Files
* `<omg_prefix>.merged`: OMG-HDCS v4 bathymetry file (`R2Sonic_2022` or `R2Sonic_2024`).
* `<omg_prefix>.merged.ss_data`: Big-endian 16-bit FTS snippet trace data.
* `<omg_prefix>.sonar_settings`: Raw R2Sonic FTS H0 header blocks (created only when FTS ID 66 packets are present).

## Practical Examples

**1. Convert an R2Sonic 2024 XTF file containing both Bathy (ID 65) and FTS Snippets (ID 66):**

```bash
xtf2omg_r2sonic -v -xtf r2s_line01.xtf -omg r2s_line01
```

**2. Convert a QINSy XTF file with QMBE Bathy (ID 28) and no FTS packets:**

```bash
xtf2omg_r2sonic -sonar 2024 -xtf qinsy_line01.xtf -omg qinsy_line01
```
