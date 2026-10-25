---
layout: default
title: readEA600
parent: Knudsen Tools
nav_order: 13
tool_name: readEA600
source_path: knudsen/readEA600.c
category: format_conversion
input_formats: [SIMRAD_RAW_EA600_EK60_EK80]
output_formats: [OMG_HDCS, OMG_SS_DATA, OMG_FL_DATA, NMEA, OMG_ORIENTATION, BINARY_RASTER]
related_tools: [kflto8, makeSeisPlot, fcv30-2glo]
---

# readEA600

## Overview

`readEA600` unpacks and processes Kongsberg/Simrad `.raw` scientific echosounder and hydrographic single-beam/ADCP files from **EA600**, **EK60**, **EK80** (both Continuous Wave `CW` and broadband Frequency Modulated `FM` chirp with matched filtering / pulse compression), and **CP300 ADCP** (`-isADCP`) systems. It extracts configuration (`CON0`, `XML0`), filter (`FIL1`), motion (`MRU0`), navigation (`NME0`), and sample (`RAW0`, `RAW3`) datagrams, outputting OMG HDCS `.merged`, `.merged.ss_data`, `.merged.fl_data`, `.nmea`, and `.orientation` files (`-omg`) or per-channel binary rasters.

## Usage

```
readEA600 (-v -show_dgm -debug_fil -debug_mru -debug_param -debug_raw3 -debug_chirp -dont_flip_chirp) \
          (-doFFTConv) (-sort_by_time) (-chancenfreq 38000) (-CW | -FM) \
          (-maxrangem 10.0) (-maxfl 10 -minfl -50) (-skip_matchedfilter) \
          (-useFrobNorm -1) (-dump_ascii_trace_no 510) \
          (-log) (-nosams 500) (-max16 8000 -min16 10) (-chan_to_extract 2) \
          (-isADCP) (-omg -heave_corr) -in infile(s) -out outfile_prefix
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<file1.raw> [...]` | *required* | One or more input Simrad/Kongsberg `.raw` files. |
| `-out` | `<outfile_prefix>` | *required* | Output file prefix for `.merged`, `.merged.ss_data`, `.merged.fl_data`, `.nmea`, `.orientation`, and channel rasters. |
| `-omg` | none | `0` | Output OMG HDCS `.merged`, 8-bit `.merged.ss_data`, and 32-bit float `.merged.fl_data` (or 16-bit `.merged.16_data`). |
| `-heave_corr` | none | `0` | Apply heave compensation (`heave_corr = 1`) to vertical trace samples. |
| `-sort_by_time` | none | `0` | Pre-scan all input `.raw` files (`get_First_EK80_Raw_Time`) and process them in chronological order. |
| `-chancenfreq` | `<Hz>` | `0` | Select EK80 channel by nominal center frequency in Hz (e.g., `38000` for 38 kHz). |
| `-CW` / `-FM` | none | `-FM` (`1`) | Select Continuous Wave (`-CW`, `0`) or broadband Frequency Modulated (`-FM`, `1`) pulse form for EK80 extraction. |
| `-doFFTConv` | none | time-domain | Perform EK80 matched-filter pulse compression via FFT convolution (`doFFTConv = 1`). |
| `-dont_flip_chirp` | none | flip enabled | Do not time-reverse the reference chirp replica during matched filtering. |
| `-skip_matchedfilter` | none | `0` | Bypass matched filtering on EK80 `RAW3` complex traces for fast debugging. |
| `-useFrobNorm` | `<val>` | `0` (`-1`) | Normalize the matched filter using the Frobenius norm (`-1` computes it automatically; otherwise uses `<val>`). |
| `-maxrangem` | `<meters>` | `0.0` (all) | Truncate EK80 output traces at `<meters>` maximum range. |
| `-minfl` / `-maxfl` | `<dB>` | `-50` / `10` | Minimum and maximum dB bounds for scaling floating-point EK80 traces to 8-bit. |
| `-dump_ascii_trace_no` | `<ping>` | `-1` | Dump detailed intermediate stages of EK80 trace `<ping>` to an ASCII file. |
| `-chan_to_extract` | `<chan>` | `1` | Channel index (`1..N`) to extract from EA600/EK60 `RAW0` datagrams. |
| `-nosams` | `<samples>` | `500` | Number of output vertical samples per trace for EA600/EK60 raster output (`0` disables raster output). |
| `-min16` / `-max16` | `<val>` | `1` / `65535` | Min/max 16-bit sample bounds for EA600/EK60 8-bit scaling. |
| `-log` | none | `0` | Apply logarithmic scaling for EA600/EK60 traces. |
| `-isADCP` | none | `0` | Process 4-beam CP300 ADCP `.raw` files. |
| `-show_dgm` | none | `0` | Print every 4-character datagram type (`XML0`, `FIL1`, `MRU0`, `NME0`, `RAW0`, `RAW3`) and size as it is read. |
| `-debug_fil` / `-debug_mru` / `-debug_param` / `-debug_raw3` / `-debug_chirp` | none | `0` | Enable subsystem-specific diagnostic printouts for EK80 XML parameters, filter stages, MRU attitude, `RAW3` complex samples, or reference chirp synthesis. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **Datagram Framing & Time Conversion**: Reads 4-byte datagram length headers, 4-character datagram IDs, and 64-bit Windows NT `FILETIME` timestamps (converting 100-nanosecond ticks since 1601-01-01 to Unix epoch seconds by subtracting `11644473600` seconds).
2. **EA600 / EK60 Processing**: Parses `CON0` configuration headers, `NME0` (`$GPGGA`, `$GPZDA`) navigation telegrams, and `RAW0` power/angle sample datagrams, extracting the selected channel (`-chan_to_extract`) and writing `.merged`, `.merged.ss_data`, and `.nmea`.
3. **EK80 Broadband FM Pulse Compression**: Parses `XML0` configuration/parameter blocks (`libxml2`), `FIL1` decimation filter coefficients, `MRU0` roll/pitch/heave/heading records (written to `.orientation`), and `RAW3` complex baseband quadrature samples. Synthesizes the transmitted linear FM chirp, applies stage-1 and stage-2 decimation filters, performs matched-filter correlation (time-domain or `-doFFTConv`), converts complex voltage into calibrated power/Sv (dB), and writes OMG HDCS `.merged`, 8-bit `.merged.ss_data`, and 32-bit float `.merged.fl_data`.

## Practical Examples

### Extract and pulse-compress a 38 kHz broadband FM channel from EK80 `.raw` files into OMG HDCS format

```bash
readEA600 -omg -sort_by_time -FM -chancenfreq 38000 -doFFTConv \
          -minfl -80 -maxfl -10 -in *.raw -out ek80_38kHz
```
