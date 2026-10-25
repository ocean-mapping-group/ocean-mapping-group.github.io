---
layout: default
title: xtfTool
parent: eXtended Triton Format — XTF (xtf)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 14
tool_name: xtfTool
source_path: code/xtf/xtfTool.c
category: Diagnostics & Indexing
input_formats:
- .xtf
output_formats:
- .idx
- .port_trace
- .stbd_trace
- .beam_NNN
- raw binary extraction
related_tools:
- xtf2omg_reson
- xtf2omg_r2sonic
- xtf2omg_simrad
- xtf2nav
- xtf2orientation
- xtf2param
---

# xtfTool

## Overview
`xtfTool` is the primary diagnostic, indexing, and packet-extraction utility for Triton XTF (`.xtf`) files. It scans an XTF file, prints a summary inventory of all packet types present, optionally writes a binary packet index (`<basename>.idx`) to accelerate subsequent runs of `xtf2nav`, `xtf2orientation`, `xtf2omg_*`, and `xtf2gloria`, and can dump decoded packet structures or raw binary payloads for Reson, Simrad, ELAC, R2Sonic, and QINSy QMBE records.

## Usage

```bash
xtfTool [OPTIONS] -in <file.xtf>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<file.xtf>` | **Required** | Path to the input `.xtf` file. |
| `-write_index` | None | Off | Write the compiled `XTFFileIndex` to `<basename>.idx` to speed up subsequent XTF processing tools. |
| `-v` | None | Off | Print the 1024-byte `XTFFILEHEADER` and every packet's byte offset, packet ID, and record length. |
| `-vb` | None | Off | Verbose dump of bathymetry packets (packet ID 2). |
| `-vs` | None | Off | Verbose dump of sidescan packets (packet ID 0). |
| `-va` | None | Off | Verbose dump of attitude packets (packet ID 3). |
| `-vS` | None | Off | Verbose dump of raw serial ASCII packets (packet ID 6). |
| `-vSnip` | None | Off | Verbose dump of Reson snippet packets (packet ID 19). |
| `-vid` | `<PACKET_ID>` | Off | Verbose dump of a specific XTF packet ID (e.g., `16` for ELAC, `28` for QMBE, `65` for R2Sonic Bathy, `66` for R2Sonic FTS, `100` for Reson Nav, `107` for POS/MV). |
| `-vAll` | None | Off | Enable verbose dumping for all XTF packet IDs. |
| `-sonar` | `<type_id>` | Header `SonarType` | Override the XTF file header `SonarType` code (e.g., `15` for Reson SeaBat 8101, `31` for Simrad EM3000). |
| `-LE` | None | Unknown | Specify Little-Endian byte order when decoding Simrad (`-sonar 31`) packets. |
| `-BE` | None | Unknown | Specify Big-Endian byte order when decoding Simrad (`-sonar 31`) packets. |
| `-tracedump` | None | Off | Dump sidescan trace time series (`<time_s> <amp>`) for ping `-rec <N>` to `<basename>.port_trace` and `<basename>.stbd_trace`. |
| `-snipdump` | None | Off | Dump Reson snippet time series (ID 19) for ping `-rec <N>` to per-beam ASCII files `<basename>.beam_000`, `.beam_001`, etc. |
| `-rec` | `<ping_index>` | `0` | Specify the 0-based packet record index to dump when using `-tracedump` or `-snipdump`. |
| `-log` | None | Linear | Output `-tracedump` and `-snipdump` amplitudes in decibels (`10 * log10(val^2)`). |
| `-extract_bathy` | None | Off | Extract raw R2Sonic bathymetry payloads (from packet ID 65, stripping the 256-byte XTF bathy header) to `-extract_file`. |
| `-extract_snippets` | None | Off | Extract raw R2Sonic FTS snippet payloads (from packet ID 66, fixing the QINSy record size field at byte offset 4) to `-extract_file`. |
| `-extract_file` | `<outfile>` | None | Output binary file for `-extract_bathy` and/or `-extract_snippets` (creates a native `.r2s` stream readable by `r2sonic2omg`). |

## How It Works
1. **Indexing:** Reads `XTFFILEHEADER`, builds an `XTFFileIndex` via `buildXTFIndex()`, prints the packet count summary table, and writes `<basename>.idx` if `-write_index` is specified.
2. **Packet Synchronization & Decoding:** Scans sequentially through the file searching for the `0xFACE` XTF magic number (`peekPACKETPEEKER`), tracking any skipped corrupted bytes (`bytes_skipped`), and dispatches each `HeaderType` (`0, 2, 3, 6, 8, 16, 19, 28, 62, 65, 66, 100, 107, 202`) to its corresponding parser and printer.
3. **R2Sonic Native Stream Extraction:** When `-extract_bathy` and/or `-extract_snippets` are combined with `-extract_file <out.r2s>`, `xtfTool` strips the XTF wrapper headers from packet IDs 65 (`BTH0`) and 66 (`SNI0`), repairs the byte-count header in QINSy-logged FTS records, and writes a clean native R2Sonic binary stream.

## Practical Examples

**1. Inspect an XTF file and generate a `.idx` index file:**

```bash
xtfTool -v -write_index -in survey01.xtf
```

**2. Dump Reson snippet traces in dB for record 150:**

```bash
xtfTool -snipdump -rec 150 -log -in reson01.xtf
```

**3. Extract embedded R2Sonic Bathy (ID 65) and FTS (ID 66) packets into a native `.r2s` file:**

```bash
xtfTool -extract_bathy -extract_snippets -extract_file line01.r2s -in qinsy_r2s.xtf
```
