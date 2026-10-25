---
layout: default
title: readore
parent: SEGY Tools
nav_order: 4
tool_name: readore
source_path: segy/readore.c
category: format_conversion
input_formats: [SEGY_ORE_SE880]
output_formats: [BINARY_RASTER, ASCII_STDOUT]
related_tools: [klein, upAGCDIG, readSB_SEGY]
---

# readore

## Overview

`readore` is an interactive diagnostic and unpacking program for ORE SE880 4-channel SEG-Y disk files. It reads the 3200-byte EBCDIC reel header and 400-byte binary header block, prompts the user whether to display the binary header fields, and then iterates through the 240-byte trace headers and 16-bit trace data, applying logarithmic 16-to-8-bit scaling and splitting the 4 interleaved trigger channels into `channel1`, `channel2`, `channel3`, and `channel4` in the current working directory.

## Usage

```
readore
```
*(Interactive prompts on `stdin`:)*
1. `Enter File name to read : <input_segy_file>`
2. `Enter File name to write : <unused_placeholder>`
3. `Display the header info (y/n) ? <y|n>`

## CLI Options

`readore` takes no command-line flags; all parameters are read interactively from standard input (`scanf`).

| Prompt | Input | Description |
| :--- | :--- | :--- |
| `Enter File name to read :` | `<filein>` | Path to the input ORE SE880 SEG-Y file (up to 19 characters). |
| `Enter File name to write :` | `<fileout>` | Placeholder string (read by `scanf`, but output is always written to `channel1`, `channel2`, `channel3`, `channel4`). |
| `Display the header info (y/n) ?` | `y` or `n` | If `y`, prints all 26 fields of the 400-byte `BCDHD` binary tape header (`jobid`, `line`, `reel`, `ntr`, `mdt`, `nt`, etc.). |

## How It Works

1. **Tape Header Inspection**: Reads the 3200-byte textual header and 400-byte `struct BCDHD` binary header, printing all header parameters if requested.
2. **Trace Loop & 8-Bit Logarithmic Scaling**: Loops up to 100,000 traces. For each trace:
   - Reads the 240-byte `struct TRACE` header (`trcrec`) and `trcrec.nttr * 2` bytes of 16-bit samples (`reclng.data`).
   - Transforms each sample via `value = -200.0 + 15.0 * log10(reclng.data[j] + 5000) * 255.0 / 4.57` into an 8-bit byte (`bytes[j]`).
   - Demultiplexes trace `x1` by `x1 % 4` into `channel1` (typically calibration channel 0), `channel2`, `channel3`, or `channel4`, and prints the trace header metadata (sequence numbers, timestamp, lat/lon, course, sweep length, sample interval, delay).

## Practical Examples

### Interactively unpack an ORE SE880 SEG-Y file

```bash
printf "ore_line1.sgy\ndummy\ny\n" | readore
```
This prints the binary header and trace headers and writes 8-bit trace rasters to `channel1`, `channel2`, `channel3`, and `channel4`.
