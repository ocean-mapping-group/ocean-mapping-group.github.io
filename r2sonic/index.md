---
layout: default
title: R2Sonic 2020/2022/2024 (r2sonic)
parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 3
has_children: true
---

# R2Sonic Multibeam Tools (`r2sonic/`)

The `r2sonic/` directory contains utilities for inspecting and converting raw **R2Sonic Sonic 2020, 2022, 2024, and 2026** broadband multibeam echosounder `.bth` / `.r2s` network packet logs into Ocean Mapping Group (OMG) `.merged` swath bathymetry, `.param` sonar telemetry, and `.bck` snippet backscatter files.

> **Note:** For R2Sonic data recorded inside Triton Extended Triton Format (`.xtf`) containers (such as QINSy or Hypack XTF recordings holding `2024` / `BTH0` / `SNI0` packets), see [`xtf2omg_r2sonic`](../xtf/xtf2omg_r2sonic.html) in the [`xtf/`](../xtf/index.html) directory.

---

## Tool Inventory

| Tool | Source File | Primary Purpose | Input Formats | Output Formats |
| :--- | :--- | :--- | :--- | :--- |
| [`bth2omg`](r2sonic2omg.html) | `r2sonic/bth2omg.c` | Convert raw R2Sonic `.bth` / `.r2s` bathymetry (`BTH0`) and snippet (`SNI0`) logs along with external navigation into OMG `.merged`, `.param`, and `.bck` files | `.bth`, `.r2s`, `.nav` | `.merged`, `.param`, `.bck` |
| [`r2sTool`](r2sonic2omg.html) | `r2sonic/r2sTool.c` | Interactive Motif/X11 and CLI packet analyzer for R2Sonic `BTH0` (`H0`) bathymetry and `SNI0` (`I0`) snippet packets | `.bth`, `.r2s` | Diagnostic text, X11 beam plots |

---

## R2Sonic Packet Structure Overview

R2Sonic Sonic series transceivers broadcast UDP datagrams composed of modular 4-character ASCII-tagged sections:
- **`BTH0` (`H0` Header):** Bathymetry packet header containing ping number, UTC time (seconds and nanoseconds), sound speed, absorption, spreading, transmit power, pulse width, receiver gain, frequency, and range resolution.
- **`R0`:** Per-beam two-way travel time ranges (scaled 16-bit integers).
- **`A0` / `A2`:** Beam pointing angles (either equi-angle spacing bounds or explicit per-beam angles in radians).
- **`I0` / `I1`:** Per-beam acoustic backscatter intensities at bottom detection.
- **`G0` / `G1`:** Straight-line / variable-gain TVG curve points applied by the sonar receiver.
- **`Q0`:** Per-beam 4-bit detection quality flags (phase vs. amplitude detection, signal-to-noise, brightness, and colinearity metrics).
- **`SNI0` (`S0` / `S1`):** High-rate snippet time series for each beam, specifying snippet start sample, stop sample, and linear amplitude values.

---

## Typical Workflow

```bash
# 1. Inspect R2Sonic packet headers, beam angles, and quality flags
r2sTool -in line01.bth

# 2. Convert R2Sonic .bth file to OMG .merged and .param, merging external navigation
bth2omg -in line01.bth -out line01 -nav survey.nav
```
