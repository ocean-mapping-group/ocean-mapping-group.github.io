---
layout: default
title: klein
parent: SEGY Tools
nav_order: 1
tool_name: klein
source_path: segy/klein.c
category: format_conversion
input_formats: [KLEIN_SYS5000]
output_formats: [SEGY_ORE_SE880]
related_tools: [readore, klein2omg, upAGCDIG]
---

# klein

## Overview

`klein` reads raw binary data from a Klein System 5000 multi-beam sidescan sonar (which records 10 dynamically focused port/starboard beams plus auxiliary channels per ping) and converts the 10 primary sidescan beams (`pingdata0`–`pingdata9`) into an ORE SE880-compatible SEG-Y file, interleaving port and starboard channels (`0, 6, 1, 7, 2, 8, ...`) and subsampling by a configurable decimation factor.

## Usage

```
klein -i input_file -o output_file (-s system_type) (-f decimation_factor)
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-i` | `<input_file>` | `stdin` (`"1"`) | Input raw Klein System 5000 binary file. |
| `-o` | `<output_file>` | `stdout` (`"2"`) | Output ORE SE880-flavored SEG-Y file. |
| `-s` | `<0\|1>` | `0` (`UNIX`) | Host byte-order system type: `0` for big-endian `UNIX` (swaps little-endian Klein headers), `1` for little-endian `PC`. |
| `-f` | `<factor>` | `5` | Decimation factor listed in usage (note: `factor = 5` is hardcoded in the main loop). |

## How It Works

1. **SEG-Y Reel Header**: Writes an initial 3600-byte SEG-Y tape header (`header[0] = 'C'`) to the output stream.
2. **Klein System 5000 Header & Channel Unpacking**: For each ping, calls `readheader()` to read `SYS5000_Header` (applying byte-swapping via `swapheaderbytes()` when `g_system_type == UNIX`). Reads 28 channel blocks (`j = 0..27`), storing the first 10 sidescan beams (`j = 0..9`) into `pingdata0` through `pingdata9`.
3. **Trace Header Construction & Channel Interleaving**:
   - Populates `s_segy_trace_header` (240 bytes) with ship latitude/longitude (converted from radians to degrees), year, day, hour, minute, second, millisecond, heading (`azimuth`), altitude (`source_depth`), decimated sample count (`size_of_data / factor`), and microsecond sample interval.
   - Alternates port and starboard beam channels (`0, 6, 1, 7, 2, 8, 3, 9, 4, 5`), decimates each channel by `factor` via `sub_sample_klein_data()`, sets `SE880_channel` to `0` (port) or `1` (starboard), and writes the 240-byte trace header followed by the 16-bit subsampled trace data.

## Practical Examples

### Convert a raw Klein System 5000 file to SEG-Y on Linux (little-endian PC byte order)

```bash
klein -i klein5000.raw -o klein5000.sgy -s 1
```
