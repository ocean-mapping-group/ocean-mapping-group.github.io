---
layout: default
title: plotmr1
parent: HAWAII MR1 Towed Sidescan (mr1)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 9
tool_name: plotmr1
source_path: mr1/plotmr1.c
category: format_conversion
input_formats:
- MR1_RAW
- MR1_BIN_NOISE
output_formats:
- OMG_MR1_SS
- OMG_MR1_ZX
related_tools:
- edbathy
- mr1_noise
- mergeMWascii
- mr1_proc
- mr1_raw
---

# plotmr1

## Overview

`plotmr1` unpacks raw HAWAII MR1 interferometric sidescan and bathymetry files (`MR1yyjjjhh.mm`) and converts them into three OMG MR1 binary files: `<infile>.raw_ss` (raw slant-range sidescan `OMG_MR1_ss_rec`), `<infile>.slr_ss` (TVG and slant-range-corrected sidescan `OMG_MR1_ss_rec`), and `<infile>.dep_zx` (180-beam interferometric phase bathymetry `OMG_MR1_zx_rec`). It can be run in batch mode or with an interactive X11 graphical interface (`-look`) that displays the raw imagery, slant-range-corrected imagery, bottom-track picks, and phase scatter plots in real time so the operator can tune detection thresholds and signal scaling.

## Usage

```
plotmr1 (-v) (-SUN) (-look) (-notvg) (-noimage) (-dumpascii) \
        (-max_signal 7000000) (-min_depth 500.0) (-pixel_size 18) \
        (-pickport | -pickstbd | -pickboth | -pickshallow | -pickdeep) \
        (-port_thresh 3000000 -stbd_thresh 4000000) (-pickwin 10 6) \
        (-port vert_angle factor) (-stbd vert_angle factor) \
        (-load noise.file seconds) MR1yyjjjhh.mm
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `<MR1yyjjjhh.mm>` | `<path>` | *required* | Input raw HAWAII MR1 file; creates or opens `<infile>.raw_ss`, `<infile>.slr_ss`, and `<infile>.dep_zx`. |
| `-look` | none | `0` | Open the interactive X11 `MR1 Conversion to OMG` GUI (required if `.raw_ss` already exists to enter `EDIT` mode). |
| `-notvg` | none | TVG enabled | Disable Time-Varying Gain (`tvg_flag = 0`). |
| `-max_signal` | `<value>` | `6000000` | Maximum signal amplitude ceiling used for 8-bit greyscale compression. |
| `-min_depth` | `<meters>` | `500.0` | Minimum altitude/depth gate in meters before searching for the seabed first break. |
| `-pixel_size` | `<meters>` | `18` | Across-track ground-range pixel size in meters for the 1024-pixel `.slr_ss` image. |
| `-port_thresh` | `<value>` | `2000000` | Amplitude threshold for port-channel seabed first-break picking. |
| `-stbd_thresh` | `<value>` | `1800000` | Amplitude threshold for starboard-channel seabed first-break picking. |
| `-pickwin` | `<win> <min_above>` | `10 6` | Confirmation window length (`pick_window`) and minimum number of samples above threshold (`min_above`) required to accept a bottom pick. |
| `-pickshallow` | none | *default* | Use the shallower of the port and starboard bottom picks (`PICK_SHALLOW`). |
| `-pickdeep` | none | `0` | Use the deeper of the port and starboard bottom picks (`PICK_DEEP`). |
| `-pickport` / `-pickstbd` | none | `0` | Use only the port (`PICK_PORT`) or starboard (`PICK_STBD`) bottom pick. |
| `-pickboth` | none | `0` | Use independent port and starboard bottom picks (`PICK_BOTH`). |
| `-port` | `<vert> <factor>` | `170.0 3.5` | Set port phase-to-angle vertical zero offset and slope factor. |
| `-stbd` | `<vert> <factor>` | `170.0 3.5` | Set starboard phase-to-angle vertical zero offset and slope factor. |
| `-load` | `<noise.file> <sec>` | none | Load a binary stacked noise file (from `mr1_noise`) of length `<sec>` seconds (`max_num_samples = sec * 1000`) to subtract array self-noise. |
| `-dumpascii` | none | `0` | Dump ASCII diagnostic tables during processing. |
| `-noimage` | none | `0` | Set `noimage_flag = 0`. |
| `-SUN` | none | `0` | Configure X11 visuals for Sun OpenWindows displays. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **Initialization & Pre-existing Check**: Precomputes block-floating-point exponents (`exp_fill()`) and TVG boost tables (`spread_table()`). If `<infile>.raw_ss` does not exist, creates new `.raw_ss`, `.slr_ss`, and `.dep_zx` files (`SINGLE` mode with `-look`, or `CONT` batch mode without `-look`). If `.raw_ss` already exists and `-look` is set, loads the pre-existing files into `EDIT` mode (`load_up_preexisting_data()`).
2. **Acoustic Unpacking & Noise Subtraction**: For each ping, reads `HDR`, power diagnostics, and 64-sample quadrature telemetry packets (`load_up_acoustic_data()`), detects and corrects 90° hardware phase swaps (`check_raw_for_invert()`), computes complex phase and amplitude (`proc_up_acoustic_data()`), and optionally subtracts stacked noise loaded via `-load`.
3. **Bottom Picking, Slant-Range Correction & Bathymetry**: Picks the nadir first arrival (`pick_first_break()`), applies TVG and slant-range ground projection (`slant_range_correct()`), converts phase angles into 180 bathymetric beams (`OMG_MR1_zx_rec`), and writes `.raw_ss`, `.slr_ss`, and `.dep_zx`.

## Practical Examples

### Unpack a raw HAWAII MR1 file interactively with noise subtraction

```bash
plotmr1 -v -look -pixel_size 18 -min_depth 1500 \
        -load noise_data.file 12 MR19208512.00
```
