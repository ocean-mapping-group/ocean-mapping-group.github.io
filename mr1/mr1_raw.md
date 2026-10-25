---
layout: default
title: mr1_raw
parent: MR1 Tools
nav_order: 8
tool_name: mr1_raw
source_path: mr1/mr1_raw.c
category: library_module
input_formats: [MR1_RAW]
output_formats: [ASCII_STDOUT]
related_tools: [mr1_proc, plotmr1, mr1_noise]
---

# mr1_raw

## Overview

`mr1_raw` (`mr1/mr1_raw.c` and `mr1/mr1_raw.h`) provides the low-level mathematical, radiometric, and header-printing routines used by [`mr1_proc`](mr1_proc), [`plotmr1`](plotmr1), and [`mr1_noise`](mr1_noise) to decode HAWAII MR1 quadrature acoustic packets, compute electrical phase difference and complex cross-correlation between transducer rows A and B, populate the block-floating-point exponent lookup table, and generate the time-varying gain (TVG) spreading and absorption curve.

## Usage

`mr1_raw.c` is a library source module linked into the MR1 processing tools:

```c
#include "mr1_raw.h"
```

## Key Functions

| Function | Signature | Description |
| :--- | :--- | :--- |
| `get_phase_lag` | `double get_phase_lag(raw_samp raw)` | Computes the wrapped phase difference `a_phase - b_phase` in `(-180, 180]` degrees from 16-bit integer `ar, ai, br, bi` components. |
| `fl_get_phase_lag` | `double fl_get_phase_lag(out_samp raw)` | Computes the wrapped phase difference `a_phase - b_phase` in `(-180, 180]` degrees from floating-point `A.r, A.i, B.r, B.i` components. |
| `get_amplitude` / `fl_get_amplitude` | `double get_amplitude(short real, short imag)` | Computes complex magnitude `sqrt(real^2 + imag^2)`. |
| `get_phase` / `fl_get_phase` | `double get_phase(short real, short imag)` | Computes four-quadrant phase angle in `[0, 360)` degrees. |
| `get_cmplxXcorr` | `void get_cmplxXcorr(out_samp raw, float *magnitude, float *phase_lag)` | Computes the complex cross-correlation `A * conj(B)` (`dreal = Ar*Br + Ai*Bi`, `dimag = Ai*Br - Ar*Bi`), returning the fourth-root magnitude and wrapped phase lag. |
| `range_decay` | `double range_decay(double slant_range)` | Computes one-way voltage amplitude decay `sqrt(exp(-2 * absorp_coeff * R) / (4 * pi * R^4))`. |
| `printf_header_data` | `void printf_header_data(HDR *head)` | Prints all fields of the HAWAII MR1 `HDR` ping header (port/starboard filter settings, topside trigger/ping interval, timestamps, byte offsets, sample rates, fish depth, pulse lengths). |
| `exp_fill` | `void exp_fill(void)` | Populates `expons[0..255]` with powers of two (`2^i`) for block-floating-point packet scaling. |
| `spread_table` | `void spread_table(int data_period)` | Precomputes the per-packet TVG boost table (`volt_gain_boost`) up to 15 km slant range using `30 log10(R/rdel)` spreading loss and `1.5 dB/km` absorption. |

## How It Works

1. **Interferometric Phase Difference**: Each MR1 array (port and starboard) has two parallel transducer rows (`A` and `B`). `fl_get_phase_lag()` and `get_cmplxXcorr()` compute the electrical phase angle between rows A and B at every sample, which is subsequently mapped via a Look-Up Table (LUT) into depression angle to derive swath bathymetry.
2. **TVG Compensation (`spread_table`)**: Computes a packet-by-packet voltage gain multiplier (`volt_gain_boost[pkt_no]`) assuming two-way sound speed of 750 m/s (one-way range per second), 30 log R spherical spreading, and 1.5 dB/km two-way absorption out to 15,000 m.

## Practical Examples

### Print full `HDR` headers from a raw MR1 file using `plotmr1 -v`

```bash
plotmr1 -v MR19208512.00
```
(Invokes `printf_header_data(&MR1_head)` from `mr1_raw.c` on every ping.)
