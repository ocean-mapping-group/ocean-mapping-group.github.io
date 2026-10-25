---
layout: default
title: upAGCDIG
parent: SEGY Tools
nav_order: 5
tool_name: upAGCDIG
source_path: segy/upAGCDIG.c
category: format_conversion
input_formats: [SEGY_AGCDIG]
output_formats: [GLORIA, NMEA, BINARY_RASTER]
related_tools: [readSB_SEGY, readore, upsegy, make_mos2]
---

# upAGCDIG

## Overview

`upAGCDIG` unpacks multi-channel SEG-Y sidescan sonar files produced by the Atlantic Geoscience Centre (AGC) digital acquisition system (typically 4 acoustic channels—120 kHz port/starboard and 300 kHz port/starboard—plus a 5th trace containing embedded NMEA `$GPGGA` navigation strings). It performs bottom-tracking (first-break picking), optional slant-range correction (`-doslant`), and converts the dual-frequency sidescan data into GLORIA format (`.120_rawss`, `.300_rawss`, and optionally `.120_slrss`, `.300_slrss`) along with extracted `.nmea` navigation and optional raw channel rasters (`.chan1`–`.chan4`).

## Usage

```
upAGCDIG (-v) (-search 1998) (-chanskip N) (-nohead) (-log | -sqrt) \
         (-pickwin 15 -minabove 10 -minpick 10) (-threshs 50 50 50 50) \
         (-nochans 2) (-bestchan 3) (-force_nttr 1500 -extra_nttr 13) \
         (-isfloat | -isint) (-swapside) (-limit300) (-rawchannels) (-pretty) \
         (-min 1 -max 2048 -autoscale) (-doslant) -in infile -out outfile_prefix
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<infile>` | *required* | Input AGC digitizer SEG-Y file. |
| `-out` | `<outfile_prefix>` | *required* | Output prefix for `.120_rawss`, `.300_rawss`, `.nmea`, and optional `.120_slrss`, `.300_slrss`, `.chan1`–`.chan4`. |
| `-nochans` | `<N>` | `5` | Number of traces per ping cycle (`5` = 4 acoustic channels + 1 NMEA trace; `2` = 2-channel sidescan with nav in trace header). |
| `-chanskip` | `<N>` | `0` | Number of initial traces to skip when syncing with `-search`. |
| `-search` | `<year>` | `0` (`1998`) | Search corrupted files for the first valid trace header matching `<year>` via `jump_to_SO_first_trace_header()`. |
| `-nohead` | none | `0` | Skip reading the 3600-byte SEG-Y tape header. |
| `-isfloat` / `-isint` | none | 16-bit short | Read trace samples as 32-bit floats or 32-bit integers instead of 16-bit shorts. |
| `-force_nttr` | `<samples>` | header `nttr` | Override the number of samples per trace (`trcrec.nttr`). |
| `-extra_nttr` | `<samples>` | `0` | Add `NTTR_shift` to `trcrec.nttr`. |
| `-log` / `-sqrt` | none | linear | Use logarithmic or square-root scaling when compressing samples to 8-bit. |
| `-min` / `-max` | `<val>` | `-140` / `2048` | Minimum and maximum sample values for 8-bit quantization. |
| `-autoscale` | none | `0` | Dynamically compute min/max sample range per trace. |
| `-pickwin` | `<samples>` | `15` | Window length in samples for confirming bottom first-break picks. |
| `-minabove` | `<samples>` | `5` | Minimum number of samples in `pick_window` exceeding threshold to accept a bottom pick. |
| `-minpick` | `<sample>` | `10` | Earliest sample index after time-zero to begin bottom picking. |
| `-threshs` | `<t0> <t1> <t2> <t3>` | `35 35 57 57` | Detection thresholds for the 4 channels (`PORT_120`, `STBD_120`, `PORT_300`, `STBD_300`). |
| `-bestchan` | `<0..3>` | `0` (`PORT_120`) | Preferred channel index for bottom altitude picking. |
| `-doslant` | none | `0` | Perform slant-range correction using the picked altitude and output `.120_slrss` and `.300_slrss`. |
| `-swapside` | none | `0` | Swap port and starboard channels. |
| `-limit300` | none | `0` | Limit 300 kHz output to the first 1536 samples (`small_pixel = dt * 3.0`). |
| `-rawchannels` | none | `0` | Dump raw 8-bit per-channel waterfalls to `.chan1`–`.chan4`. |
| `-pretty` | none | `0` | Annotate bottom pick and water column in raw channel outputs. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **Header & Trace Demultiplexing**: Reads the 3600-byte SEG-Y header (unless `-nohead` or `-search` is used) and cycles through `NOTR` traces per ping (`PORT_120 = 0`, `STBD_120 = 1`, `PORT_300 = 2`, `STBD_300 = 3`, and NMEA trace `4`).
2. **NMEA & Navigation Extraction**: On trace `4` (`i % NOTR == 4`), calls `extract_GGA_from_trace()` to parse embedded ASCII `$GPGGA` sentences and write them to `<outfile_prefix>.nmea`. When `-nochans 2` is used, reads double-precision `seg_lat`, `seg_lon`, and float `seg_azi` directly from the SEG-Y trace header.
3. **First-Break Picking & GLORIA Formatting**: Picks the seabed first arrival on each acoustic channel (`pick_first_break`), decimates each trace into 512 port and 512 starboard 8-bit pixels (`gloria_rec`), writes `.120_rawss` and `.300_rawss`, and if `-doslant` is specified, computes horizontal ground range from the picked altitude to write slant-range-corrected GLORIA files.

## Practical Examples

### Unpack a 5-trace AGC digitizer SEG-Y file with slant-range correction

```bash
upAGCDIG -v -log -doslant -in agc_line01.sgy -out agc_line01
```
