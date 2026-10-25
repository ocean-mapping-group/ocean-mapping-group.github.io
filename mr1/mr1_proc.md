---
layout: default
title: mr1_proc
parent: MR1 Tools
nav_order: 7
tool_name: mr1_proc
source_path: mr1/mr1_proc.c
category: library_module
input_formats: [MR1_RAW, OMG_MR1_SS, OMG_MR1_ZX]
output_formats: [OMG_MR1_SS, OMG_MR1_ZX]
related_tools: [plotmr1, mr1_noise, edbathy, mr1_raw]
---

# mr1_proc

## Overview

`mr1_proc` (`mr1/mr1_proc.c` and `mr1/mr1_proc.h`) is the core signal-processing module linked into [`plotmr1`](plotmr1) and [`mr1_noise`](mr1_noise). It implements the acoustic packet loader, automatic 90° phase-inversion detector, multi-ping complex phase/amplitude accumulator, first-break seabed altitude picker, TVG and slant-range corrector, and phase-to-bathymetry converter for the HAWAII MR1 interferometric swath system.

## Usage

`mr1_proc.c` is compiled and linked with `plotmr1` and `mr1_noise` rather than invoked as a standalone executable:

```c
#include "mr1_proc.h"
```

## Key Functions

| Function | Signature | Description |
| :--- | :--- | :--- |
| `load_up_preexisting_data` | `void load_up_preexisting_data(void)` | Reads existing `.raw_ss`, `.slr_ss`, and `.dep_zx` records into the 512x600 X11 image buffers for interactive review. |
| `load_up_acoustic_data` | `int load_up_acoustic_data(int no_packets)` | Unpacks 64-sample MR1 telemetry packets, separating odd sequence numbers into `port_raw_data` and even sequence numbers into `stbd_raw_data` while scaling by `expons[a_packet.expon]`. |
| `check_raw_for_invert` | `void check_raw_for_invert(void)` | Computes the mean A/B phase lag over the last 10 packets (640 ms) of the ping; sets `port_invert = 1` or `stbd_invert = 1` if the mean phase lag exceeds 45° (indicating a 90° hardware channel swap). |
| `proc_up_acoustic_data` | `void proc_up_acoustic_data(void)` | Computes per-sample magnitude and phase lag (`fl_get_amplitude`, `fl_get_phase_lag` or `get_cmplxXcorr`), corrects 90° phase inversions, and accumulates amplitude-weighted real/imaginary phase components. |
| `normalise_stacked_data` | `void normalise_stacked_data(void)` | Divides stacked amplitude and vector phase components by `port_stack[i]` and `stbd_stack[i]`. |
| `decimate_amplitude_phase_phaseSD` | `void decimate_amplitude_phase_phaseSD(void)` | Averages full-rate 1 kHz samples into 512 port and 512 starboard bins and computes phase standard deviation. |
| `pick_first_break` | `void pick_first_break(void)` | Detects the seabed first return on port and starboard channels using `port_threshold`, `stbd_threshold`, `pick_window`, and `min_above`. |
| `slant_range_correct` | `void slant_range_correct(void)` | Applies spherical spreading and absorption TVG (`volt_gain_boost`) and projects slant-range samples onto horizontal ground-range pixels (`pixel_size`). |

## How It Works

1. **Packet Decommutation**: HAWAII MR1 acoustic telemetry interleaves 64-sample packets from the port and starboard arrays (`seq_no % 2 != 0` for port, `seq_no % 2 == 0` for starboard), where each sample consists of four 8-bit mantissas (`ar`, `ai`, `br`, `bi`) for transducer rows A and B sharing a block exponent (`expon`).
2. **Hardware Phase-Swap Mitigation**: Because the MR1 acquisition hardware occasionally introduced a 90° phase shift between rows A and B, `check_raw_for_invert()` inspects the ambient noise tail at the end of each ping and automatically negates and shifts the phase by +90° when a swap is detected.
3. **Bathymetry & Imagery Reduction**: Decimates the 1 kHz complex stream into 1024-pixel sidescan records (`OMG_MR1_ss_rec`) and 180-beam interferometric phase bathymetry records (`OMG_MR1_zx_rec`).

## Practical Examples

### Build and run `plotmr1` (which links `mr1_proc.c`)

```bash
plotmr1 -v -look MR19208512.00
```
