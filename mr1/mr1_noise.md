---
layout: default
title: mr1_noise
parent: HAWAII MR1 Towed Sidescan (mr1)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 6
tool_name: mr1_noise
source_path: mr1/mr1_noise.c
category: diagnostics
input_formats:
- MR1_RAW
- MR1_BIN_NOISE
output_formats:
- OMG_MR1_SS
- MR1_BIN_NOISE
related_tools:
- graph_noise
- plotmr1
- mr1_proc
- mr1_raw
---

# mr1_noise

## Overview

`mr1_noise` analyzes raw HAWAII MR1 telemetry files collected with the acoustic transmitters turned off (`xmtrs_on_flag == 0`) to characterize port and starboard receiver array noise and self-noise across the listen window. It provides an interactive X11 graphical interface (`-look`) and batch stacking mode to average complex quadrature samples over multiple pings and export a binary noise profile (`noise_data.file`) that can be subtracted during [`plotmr1`](plotmr1) processing or plotted with [`graph_noise`](graph_noise).

## Usage

```
mr1_noise (-v) (-SUN) (-look) (-load noise.data) MR1yyjjjhh.mm
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `<MR1yyjjjhh.mm>` | `<path>` | *required* | Input raw HAWAII MR1 data file; creates or opens `<MR1yyjjjhh.mm>.noise_ss`. |
| `-look` | none | `0` | Launch the interactive X11 `MR1 Noise Viewer` GUI (required if `<infile>.noise_ss` already exists for `EDIT` mode). |
| `-load` | `<noise.data>` | `"noise_data.file"` | Load a pre-existing binary noise file containing 4 arrays of `20000` floats (`noise_port_ampl`, `noise_stbd_ampl`, `noise_port_phas`, `noise_stbd_phas`). |
| `-SUN` | none | `0` | Configure X11 visuals for Sun OpenWindows displays. |
| `-v` | none | `0` | Enable verbose output (prints MR1 ping headers and power/attitude packet lengths). |

## How It Works

1. **Packet Unpacking & Phase Inversion Check**: Reads `HDR` headers, port/starboard power diagnostics, and 64-sample quadrature telemetry packets (`load_up_acoustic_data()`), checking the last 10 packets of the listen window for 90° A/B receiver channel phase inversions (`check_raw_for_invert()`).
2. **Multi-Ping Stacking & Normalization**: Accumulates complex amplitude and vector phase across `1 + no_stacked` pings (`proc_up_acoustic_data()`), normalizes by stack count (`normalise_stacked_data()`), decimates amplitude, phase, and phase standard deviation (`decimate_amplitude_phase_phaseSD()`), and compresses the result into 8-bit `<infile>.noise_ss` records (`OMG_MR1_ss_rec`).
3. **Interactive X11 Noise Viewer (`-look`)**: Allows interactive inspection of real/imaginary and phase/magnitude curves and exporting stacked noise arrays to `noise_data.file`.

## Practical Examples

### Interactively inspect and stack passive MR1 array noise

```bash
mr1_noise -v -look MR19208510.00
```
