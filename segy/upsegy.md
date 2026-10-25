---
layout: default
title: upsegy
parent: SEGY Tools
nav_order: 6
tool_name: upsegy
source_path: segy/upsegy.c
category: format_conversion
input_formats: [SEGY_EGG_CHIRP]
output_formats: [BINARY_RASTER, JCU_NAV, ASCII_PICKS]
related_tools: [mergePick, readSB_SEGY, readore]
---

# upsegy

## Overview

`upsegy` unpacks fixed-length complex (in-phase and quadrature) SEG-Y sub-bottom traces acquired by an EG&G Chirp sub-bottom profiler. For each ping, it computes the analytic signal envelope and in-phase waveform across 1600 samples, picks the seabed arrival, and generates 5 output files: `<outf>.envelope` (8-bit envelope waterfall), `<outf>.inphase` (8-bit bipolar in-phase waterfall), `<outf>.aligned` (water-column-aligned envelope waterfall), `<outf>.nav` (JCU binary navigation), and `<outf>.picks` (12-column ASCII pick table for use with [`mergePick`](mergePick)).

## Usage

```
upsegy (-v) (-skip 3600) (-length 8192) (-envelope) (-align) (-showpick) \
       (-log | -sqrt) (-max value) inf outf
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `<inf>` | `<path>` | *required* | First positional argument: input EG&G Chirp SEG-Y file. |
| `<outf>` | `<prefix>` | *required* | Second positional argument: output prefix used to create `<outf>.aligned`, `<outf>.envelope`, `<outf>.inphase`, `<outf>.nav`, and `<outf>.picks`. |
| `-skip` | `<bytes>` | `3600` | Initial byte offset to skip at the start of `<inf>` (default skips the 3600-byte SEG-Y tape header). |
| `-length` | `<bytes>` | `8192` | Byte length of each trace record (240-byte trace header + interleaved 16-bit in-phase/quadrature samples). |
| `-envelope` | none | `1` (enabled) | Compute the quadrature amplitude envelope `sqrt(I^2 + Q^2)`. |
| `-align` | none | `0` | Automatically pick the first sample `>= 5000.0` (starting from sample 100) and shift the trace in `<outf>.aligned` to align the seabed arrival at pixel 100. |
| `-showpick` | none | `0` | Enable `showpick_flag`. |
| `-log` | none | `0` | Apply base-10 logarithmic scaling (`log10`) to envelope and in-phase amplitudes. |
| `-sqrt` | none | `0` | Apply square-root scaling (`sqrt`) to envelope and in-phase amplitudes. |
| `-max` | `<value>` | per-ping max | Fix the maximum amplitude ceiling used for 8-bit image normalization. |
| `-v` | none | `0` | Enable verbose output (prints per-ping min/max and pick sample). |

## How It Works

1. **Navigation Extraction**: Seeks past `skip` bytes (`3600` by default) and reads fixed `length`-byte (`8192`) records. Extracts 32-bit integer longitude (`stuff[40..41]`) and latitude (`stuff[42..43]`) in `0.0001` arc-minutes, converts to decimal degrees (`* 0.0001 / 60.0`), and writes `jcu_nav_rec` records to `<outf>.nav`.
2. **Complex Envelope & In-Phase Computation**: Starting after the 240-byte trace header (`stuff[120]`), reads 1600 interleaved 16-bit pairs (`inphase[i] = stuff[120 + 2*i]`, `quadrat[i] = stuff[120 + 2*i + 1]`), computes `envelope[i] = sqrt(inphase[i]^2 + quadrat[i]^2)`, and applies optional `-log` or `-sqrt` scaling.
3. **Image & Pick Output**: Quantizes the 1600-sample envelope to inverted 8-bit grayscale (`255 - envelope * 240 / max`) in `<outf>.envelope`, writes the shifted seabed-aligned trace to `<outf>.aligned`, writes the signed in-phase trace centered at 136 (`136 + inphase * 120 / max`) to `<outf>.inphase`, and logs `lat lon pick 0 0 0 0 0 0 0 0 0` to `<outf>.picks`.

## Practical Examples

### Unpack an EG&G Chirp SEG-Y file with seabed alignment and square-root scaling

```bash
upsegy -sqrt -align -max 15000 chirp_raw.sgy chirp_line01
```
