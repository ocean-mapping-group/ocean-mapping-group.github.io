---
layout: default
title: knud2glo
parent: Knudsen Chirp Sub-Bottom (knudsen)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 6
tool_name: knud2glo
source_path: knudsen/knud2glo.c
category: format_conversion
input_formats:
- KNUDSEN_KEL
output_formats:
- OMG_HDCS
- OMG_SS_DATA
- OMG_16_DATA
- GLORIA
- JCU_NAV
- ASCII_XYZ
related_tools:
- k16to8
- makeSeisPlot
- make_knudsen_ss
- pickSS
---

# knud2glo

## Overview

`knud2glo` is the primary converter for **Knudsen Engineering** (320M, 320B/R, 3260) KEL binary envelope files (`.keb` / `.kea`). It supports legacy 8-bit/16-bit KEL records as well as 16-bit `-VX`/`-B9`, 4-channel USB `-D3`, and `-E0` packet formats, converting dual-frequency (HF and LF) traces and bottom detections into OMG HDCS `.merged`, `.merged.ss_data` (8-bit), and `.merged.16_data` (16-bit) files (default `-omg`) or JCU GLORIA format (`-glo`), alongside a `.nav` binary navigation file and an ASCII `.xyz` file of HF depths.

## Usage

```
knud2glo (-head) (-omg | -glo) (-allow_non1600) (-VX | -B9) \
         (-D3 (-D3_HF 2 -D3_LF 4) (-noD3chan 4)) \
         (-E0 (-E0_HF 2 -E0_LF 4) (-noE0chan 4)) \
         (-HF_ahead 4.3 -HF_right 2.4 -HF_draft 1.2) \
         (-LF_ahead 4.3 -LF_right 2.4 -LF_draft 0.8) \
         (-year 1999 -jday 315) (-fixMSEC) (-time_shift_sec 3600) \
         (-noLF | -noHF | -hasBOTH) (-utm2geo -merid -63) (-v) (-log) \
         (-max16_LF 8000 -max16_HF 20000 -min16_LF 10 -min16_HF 100) \
         -out outfileprefix -in infile(s)
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-out` | `<outfileprefix>` | *required* | Output file prefix for `.merged`, `.merged.ss_data`, `.merged.16_data`, `.nav`, and `.xyz` (or GLORIA output with `-glo`). |
| `-in` | `<file1> [file2 ...]` | *required* | Input Knudsen KEL binary file(s). **Must be placed at the end of the command line.** |
| `-omg` / `-glo` | none | `-omg` | Output OMG HDCS format (`-omg`, default) or JCU GLORIA sidescan format (`-glo`). |
| `-allow_non1600` | none | `0` | Allow traces with sample counts other than 1600 (`OMG_HDCS` v3 `Knudsen_320`). |
| `-VX` / `-B9` | none | `0` | Unpack 16-bit Knudsen `VX` / `B9` record format (also outputs `.merged.16_data`). |
| `-D3` | none | `0` | Unpack 16-bit Knudsen USB `D3` multi-channel format. |
| `-noD3chan` | `<1..4>` | `4` | Total number of active channels in `-D3` files. |
| `-D3_HF` / `-D3_LF` | `<1..4>` | `1` / `2` | Channel numbers (1–4) assigned to HF (`beam[0]`) and LF (`beam[1]`) in `-D3` mode. |
| `-E0` | none | `0` | Unpack 16-bit Knudsen USB `E0` multi-channel format. |
| `-noE0chan` | `<1..4>` | `4` | Total number of active channels in `-E0` files. |
| `-E0_HF` / `-E0_LF` | `<1..4>` | `1` / `2` | Channel numbers (1–4) assigned to HF (`beam[0]`) and LF (`beam[1]`) in `-E0` mode. |
| `-noLF` / `-noHF` / `-hasBOTH` | none | `-hasBOTH` | Specify whether only HF (`-noLF`), only LF (`-noHF`), or both channels are recorded. |
| `-log` | none | linear | Use logarithmic 16-to-8-bit compression (`PACK16_LOG`). |
| `-min16_HF` / `-max16_HF` | `<val>` | `1` / `32000` | 16-bit min/max amplitude bounds for HF 8-bit scaling. |
| `-min16_LF` / `-max16_LF` | `<val>` | `1` / `32000` | 16-bit min/max amplitude bounds for LF 8-bit scaling. |
| `-HF_ahead` / `-HF_right` / `-HF_draft` | `<meters>` | `0.0` | Lever-arm offsets (forward, starboard, draft) for the HF transducer. |
| `-LF_ahead` / `-LF_right` / `-LF_draft` | `<meters>` | `0.0` | Lever-arm offsets (forward, starboard, draft) for the LF transducer. |
| `-year` / `-jday` | `<val>` | header date | Override the year and Julian day if missing from the KEL file header. |
| `-fixMSEC` | none | `0` | Synthesize sub-second millisecond timestamps when the KEL header only logs integer seconds. |
| `-time_shift_sec` | `<seconds>` | `0.0` | Constant time offset in seconds added to all ping timestamps. |
| `-utm2geo` / `-merid` | `<deg>` | `0` / `0.0` | Convert UTM coordinates in the KEL header to geographic lat/lon using central meridian `<deg>`. |
| `-head` | none | `0` | Write a `JHC_header` on raw waterfall outputs. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **KEL Envelope & Channel Parsing**: Iterates through all input KEL files, reading `KEL_preamble`, `KEL_record_info`, `KEL_envelope`, or `E0`/`D3` channel blocks (`currentChannel[0..3]`).
2. **16-to-8-Bit Trace Extraction**: For 16-bit formats (`-VX`, `-B9`, `-D3`, `-E0`), writes big-endian 16-bit samples to `<out>.merged.16_data` (which can later be reprocessed with [`k16to8`](k16to8)) and compresses samples into `<out>.merged.ss_data` using `min16_HF`/`max16_HF` and `min16_LF`/`max16_LF`.
3. **OMG HDCS Profile & Beam Population**: Writes 2-beam `Knudsen_320` profiles (`beams[0]` = HF, `beams[1]` = LF) to `<out>.merged`, encoding the trace window top delay and bottom detection sample in `beams[side].range` and `beams[side].centre_no`, and writes unique GPS positions to `<out>.nav`.

## Practical Examples

### Convert Knudsen USB `-E0` `.keb` files into OMG HDCS format

```bash
knud2glo -E0 -allow_non1600 -log -max16_HF 15000 -max16_LF 25000 \
         -out survey_line01 -in *001.keb *002.keb
```
