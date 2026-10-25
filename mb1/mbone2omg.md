---
layout: default
title: mbone2omg
parent: Teledyne MB1 Tools (mb1)
nav_order: 1
tool_name: mbone2omg
source_path: code/mb1/mbone2omg.c
category: Raw Data Unraveling & Format Conversion
input_formats: [".tdy (Teledyne MB1)"]
output_formats: [".merged", ".merged.ss_data", ".sonar_settings", ".watercol", "wc_image.r4"]
related_tools: ["mboneTool", "makess", "get_ADH_SRA", "swathed", "jview"]
---

# mbone2omg

## Overview

`mbone2omg` (`code/mb1/mbone2omg.c`) unpacks **Teledyne `.tdy` (MB1 format)** multibeam echosounder files into **OMG-HDCS Version 4** files (`toolType = Teledyne_MB1`, `numDepths = MB1_MAX_NUM_BEAMS = 512`).

In the Teledyne MB1 architecture, a single acoustic ping can be split across multiple consecutive `TDYMB01` packets (`MB1_ID_TDYMB01`), each carrying a subset of data segments (`TIME`, `RAW`, `PROC`, `AR` angle/range bathy, `QUAL`, `SNIPPET`, `SS`, `WC` water column) tagged with the same `MB01_header.ping` number. `mbone2omg` aggregates all `TDYMB01` segments belonging to a given `ping` into an `OMG_HDCS_profile_header`, an array of 512 `OMG_HDCS_beam` records, and a `j_EM_watercolumn` record, flushing the completed ping to disk whenever `MB01_header.ping != last_ping_read` (and flushing the final ping at EOF).

---

## Usage

```bash
mbone2omg [-v] [-ignore_watercolumn] -tdy <input.tdy> -omg <omg_file_prefix>
```

### Command-Line Options

| Flag | Arguments | Description |
| :--- | :--- | :--- |
| `-tdy` | `<input.tdy>` | **Required.** Input Teledyne `.tdy` binary multibeam file. |
| `-omg` | `<omg_file_prefix>` | **Required.** Output prefix for `<prefix>.merged`, `<prefix>.merged.ss_data`, `<prefix>.sonar_settings`, and `<prefix>.watercol`. |
| `-ignore_watercolumn` | *(none)* | Skips opening `<prefix>.watercol` and skips decoding `MB1_TDY_WC` water column segments. |
| `-v` | *(none)* | Enables verbose logging of record IDs, `MB01` header contents, and per-ping segment conversions. |

---

## Output Files & Segment Conversion Logic

During execution, `mbone2omg` performs a two-pass scan of the `.tdy` file:
- **Pass 1 (Base Time Initialization)**: Scans until the first `MB1_ID_FILE_HEADER` or `MB1_ID_TDYMB01` record to establish `base_time` (Unix epoch seconds) and `summary.refTime = (int)(base_time / 100.0)`, then rewinds to byte `0` and writes the `OMG_HDCS_summary_header` (`fileVersion = 4`, `toolType = Teledyne_MB1`, `numDepths = 512`).
- **Pass 2 (Segment Accumulation & Output)**: Iterates through all `MB1_ID_TDYMB01` packets (skipping `MB1_ID_FILE_HEADER` and `MB1_ID_TDYRTA1_0..4`) and populates up to five output files:

| Output File | Source Segment | Conversion Details |
| :--- | :--- | :--- |
| `<prefix>.merged` | `TIME` + `AR` + `SNIPPET` | OMG-HDCS v4 bathymetry. `AR` soundings (`TDY_ar.num_soundings`) are centered inside the 512-beam slot array at `beam_offset = (512 - num_soundings) / 2`. Across-track angles are sign-inverted from radians to `0.01°` (`Rc_steer = -angle_across * 180/π * 100`), along-track pitch angles are scaled to `0.01°` (`Tx_steer`), and preliminary `observedDepth` and `acrossTrack` (in mm) are computed assuming constant `TDY_ar.sound_speed`. |
| `<prefix>.sonar_settings` | `RAW` (`MB1_TDY_RAW`) | Stores the raw 45-byte `MB1_TDY_RAW` buffer (`inbuffer[45]`) verbatim for each ping and records the byte offset in `profile.sonar_settings_offset` (used later by `makess` via `load_MB1_sonar_settings()`). |
| `<prefix>.merged.ss_data` | `SNIPPET` (`MB1_TDY_SNIP`) | Writes IEEE 32-bit big-endian float snippet amplitudes (`fwrite_BE_float`), records byte offsets in `beams[beam_offset + i].offset`, and computes mean beam `reflectivity` in `0.5 dB` steps (`2 * 20 * log10(mean_amp / 255.0)`). |
| `<prefix>.watercol` | `WC` (`MB1_TDY_WC`) | Converts water column amplitude traces into `j_EM_watercolumn` (`model_no = Teledyne_MB1`, 8-bit `ts_ampl[j]` with `20*log10(amp) - tx_power + 10 + 40*log10(range) + 2*α*range` TVG compensation) and writes them via `j_EM_write_watercolumn()`. |
| `wc_image.r4` | `WC` (`MB1_TDY_WC`) | Writes the first water column ping's phase matrix (`TDY_wc.phase`) as a 32-bit float OMG `.r4` raster in the current working directory via `writeJHC()` and `fwrite_BE_float()`. |

---

## Architectural Fit

After running `mbone2omg`, the resulting `<prefix>.merged`, `<prefix>.merged.ss_data`, and `<prefix>.sonar_settings` files can be inspected in [`swathed`](../SE/swathed.md) or passed to [`makess`](../omg/makess.md) (which invokes `calibrate_mb1()` from `omg_mb1.h`) to generate calibrated `.ss` sidescan files for mosaicking in [`mos2`](../newmos/mos2.md).
