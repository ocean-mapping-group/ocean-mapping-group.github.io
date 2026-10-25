---
layout: default
title: xtf2orientation
parent: eXtended Triton Format — XTF (xtf)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 12
tool_name: xtf2orientation
source_path: code/xtf/xtf2orientation.c
category: Attitude Extraction
input_formats:
- .xtf
- .idx
output_formats:
- .orientation
- .orientation.POSMV
related_tools:
- xtf2nav
- xtf2param
- xtfTool
- mergeAtt
- newMergeAtt
---

# xtf2orientation

## Overview
`xtf2orientation` extracts asynchronous vessel attitude records (`XTF_HEADER_ATTITUDE`, packet ID 3) and optional Applanix POS/MV raw navigation/attitude records (`XTF_HEADER_POS_RAW_NAVIGATION`, packet ID 107) from an XTF file and writes them to binary OMG-HDCS `.orientation` (and `.orientation.POSMV`) files. It includes options for scaling or shifting roll and pitch, shifting timestamps, unwrapping midnight millisecond rollovers, and splitting output files across large time gaps.

## Usage

```bash
xtf2orientation [OPTIONS] -xtf <input.xtf> -omg <omgfile.orientation>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-xtf` | `<input.xtf>` | **Required** | Path to the input `.xtf` file (automatically uses `<basename>.idx` if available). |
| `-omg` | `<omgfile.orientation>` | **Required** | Path to the output OMG `.orientation` file (also writes `<omgfile.orientation>.POSMV` if packet ID 107 records exist). |
| `-roll_scale` | `<factor>` | `1.0` | Multiply roll values by `<factor>` (use `-1` to invert roll sign). |
| `-pitch_scale` | `<factor>` | `1.0` | Multiply pitch values by `<factor>` (use `-1` to invert pitch sign). |
| `-roll_shift` | `<degrees>` | `0.0` | Add `<degrees>` offset to roll after scaling: `(Roll * roll_scale + roll_shift)`. |
| `-pitch_shift` | `<degrees>` | `0.0` | Add `<degrees>` offset to pitch after scaling: `(Pitch * pitch_scale + pitch_shift)`. |
| `-time_shift` | `<seconds>` | `0.0` | Apply an additive time shift (in seconds) to `baseTime`. |
| `-unwrap_day` | None | Off | Apply modulo `86400000` ms (`MILLIS_PER_DAY`) to `xtfAttitude.TimeTag` when the millisecond counter fails to reset to zero at UTC midnight. |
| `-check_time` | `<ms>` | Off | Split output into numbered orientation files (`<outname>_1`, `<outname>_2`, ...) whenever a time gap between consecutive attitude packets exceeds `<ms>` milliseconds. |
| `-force_sync` | `<method_id>` | Auto-detect | Force a specific XTF time synchronization method (`get_xtf_synchro`). |
| `-v` | None | Off | Print every attitude packet and progress updates. |
| `-debug` | None | Off | Enable debug diagnostics. |

## How It Works
1. **Indexing & Synchronization:** Reads `<basename>.idx` or builds an XTF index via `buildXTFIndex()`, auto-detects the XTF synchronization method (`get_xtf_synchro()`), and calculates `baseTime + time_shift`.
2. **Standard Attitude (ID 3):** Iterates through all `XTF_HEADER_ATTITUDE` packets, skips duplicate timestamps (`old_time == new_time`), converts roll, pitch, heave, and heading into hundredths of degrees/meters (`* 100.0`), applies `-roll_scale`, `-roll_shift`, `-pitch_scale`, and `-pitch_shift`, and writes `OMG_HDCS_attitude` records to `<outname>`.
3. **POS/MV Attitude (ID 107):** If `XTF_HEADER_POS_RAW_NAVIGATION` packets exist, writes a second attitude file `<outname>.POSMV` using the same roll/pitch scale and shift parameters.

## Practical Examples

**1. Standard orientation extraction:**

```bash
xtf2orientation -xtf line01.xtf -omg line01.orientation
```

**2. Invert roll sign and handle midnight rollover:**

```bash
xtf2orientation -roll_scale -1.0 -unwrap_day -xtf midnight_line.xtf -omg midnight_line.orientation
```
