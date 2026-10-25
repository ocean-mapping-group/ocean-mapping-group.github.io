---
layout: default
title: edbathy
parent: HAWAII MR1 Towed Sidescan (mr1)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 2
tool_name: edbathy
source_path: mr1/edbathy.c
category: interactive_editing
input_formats:
- OMG_MR1_SS
- OMG_MR1_ZX
- MR1_LUT
output_formats:
- OMG_MR1_ZX
- MR1_LUT
related_tools:
- plotmr1
- mr1_proc
- mergeMWascii
---

# edbathy

## Overview

`edbathy` is an interactive Xlib graphical tool for editing HAWAII MR1 phase-differencing bathymetry and calibrating the electrical-phase-to-acoustic-angle Look-Up Table (LUT). Once raw MR1 data has been unpacked by [`plotmr1`](plotmr1) into `.slr_ss` / `.slr_mer` and `.dep_zx` files, `edbathy` displays the slant-range-corrected sidescan alongside the phase/bathymetry swaths and allows the operator to interactively adjust the port/starboard LUT curves and flag noisy phase or depth soundings, saving the cleaned bathymetry to `.dep_ok`.

## Usage

```
edbathy (-v) (-SUN) -look (-lut lut.file) MR1yyjjjhh.mm [MR1yyjjjhh.mm ...]
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-look` | none | *required* | Launch the X11 graphical editing interface (`edbathy` exits with an error if `-look` is omitted). |
| `<MR1_prefix>` | `<prefix1> [...]` | *required* | One or more MR1 file prefixes; opens `<prefix>.slr_mer`, `<prefix>.slr_ss`, `<prefix>.dep_zx`, and writes `<prefix>.dep_ok`. |
| `-lut` | `<lut.file>` | default internal LUT | Load an external phase-to-depression-angle Look-Up Table file. |
| `-SUN` | none | `0` | Configure colormap/visual handling for Sun OpenWindows displays. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **Data & LUT Initialization**: Initializes default port and starboard phase-to-angle look-up tables (`load_LUT()`), optionally overrides them from `-lut`, and loads up to 300 pings of `.slr_mer` (`OMG_MR1_ss_rec`) and `.dep_zx` (`OMG_MR1_zx_rec`) records (`load_up_data()`).
2. **Phase-to-Topography Recalculation**: Converts electrical phase difference and slant range into across-track offset and depth for port and starboard swaths (`recalc_bathymetry(MR1_PORT)` and `recalc_bathymetry(MR1_STBD)` via `convert_phase_to_topo()`).
3. **Interactive X11 Editing**: Displays 6 graphical sub-windows (sidescan waterfall, depth waterfall, cross-track profile, phase vs. angle scatter, LUT curve editor, and control buttons) so the user can rubber-band flag bad phase/depth regions (`flag_phase_data`, `flag_depth_data`), smooth phase (`filter_phase`), save updated LUTs (`dump_LUT`), and write cleaned `.dep_ok` records (`write_out_topo`).

## Practical Examples

### Interactively edit MR1 phase bathymetry and LUTs in X11

```bash
edbathy -v -look -lut mw9204.lut MR19208512.00
```
