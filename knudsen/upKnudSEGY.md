---
layout: default
title: upKnudSEGY
parent: Knudsen Tools
nav_order: 15
tool_name: upKnudSEGY
source_path: knudsen/upKnudSEGY.c
category: format_conversion
input_formats: [SEGY_KNUDSEN]
output_formats: [BINARY_RASTER]
related_tools: [readSB_SEGY, knud2glo, makeSeisPlot]
---

# upKnudSEGY

## Overview

`upKnudSEGY` unpacks 16-bit SEG-Y sub-bottom profiler files recorded by a Knudsen 320 echosounder (originally developed for 3.5 kHz data from R/V *Moana Wave*), scaling the 16-bit trace samples into 8-bit unsigned byte traces (`<outfile_prefix>.120_rawss`) using linear, logarithmic (`-log`), or square-root (`-sqrt`) compression.

## Usage

```
upKnudSEGY (-v) (-search 1998) (-nohead) (-log | -sqrt) \
           (-min -2048 -max 2048) -in infile -out outfile_prefix
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<infile>` | *required* | Input Knudsen 320 SEG-Y file. |
| `-out` | `<outfile_prefix>` | *required* | Output file prefix; creates `<outfile_prefix>.120_rawss`. |
| `-nohead` | none | `0` | Skip reading the 3600-byte SEG-Y tape header at the start of the file. |
| `-search` | `<year>` | `0` (`1998`) | Scan a corrupted SEG-Y file for the first valid trace header matching `<year>` via `jump_to_SO_first_trace_header()`. |
| `-log` / `-sqrt` | none | linear | Use logarithmic or square-root compression when converting 16-bit samples to 8-bit. |
| `-min` / `-max` | `<value>` | `-2048` / `2048` | Minimum and maximum 16-bit sample values mapped to `[0, 255]`. |
| `-v` | none | `0` | Enable verbose output (prints trace header fields, sample counts, sample intervals, and per-trace dynamic range). |

## How It Works

1. **Header & Trace Sync**: Skips or reads the 3600-byte SEG-Y tape header (`read_segy_tape_headers()`), or searches for `<year>` if `-search` is specified.
2. **Trace Unpacking & 8-Bit Quantization**: For each trace, reads and byte-swaps the 240-byte `ctrace` header into `trcrec`, reads `trcrec.nttr` 16-bit samples via `jswapshort_fread()`, scales each sample into `bytes[j]` using `[min_value, max_value]` (linear, `-log`, or `-sqrt`), and writes the 8-bit trace to `<outfile_prefix>.120_rawss`.

## Practical Examples

### Unpack a Knudsen 3.5 kHz SEG-Y file with logarithmic scaling

```bash
upKnudSEGY -v -log -min 1 -max 8192 -in knud35.sgy -out knud35
```
