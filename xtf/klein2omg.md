---
layout: default
title: klein2omg
parent: XTF Tools
nav_order: 5
tool_name: klein2omg
source_path: code/xtf/klein2omg.c
category: Raw Data Unraveling
input_formats: [".xtf"]
output_formats: [".merged", ".ss_data"]
related_tools: ["xtf2gloria", "xtf2nav", "xtf2orientation", "xtfTool"]
---

# klein2omg

## Overview
`klein2omg` converts Klein sidescan sonar records (`XTF_HEADER_SONAR`, packet ID 0) from an XTF file into an OMG-HDCS v3 2-beam `.merged` file (with `toolType = Knudsen_320`) and a companion 16-bit little-endian `.ss_data` sidescan trace file.

## Usage
```bash
klein2omg [-v] [-debug] -xtf <input.xtf> -omg <output.merged>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-xtf` | `<input.xtf>` | **Required** | Path to the input `.xtf` file containing sidescan sonar packets. |
| `-omg` | `<output_file>` | **Required** | Path to the output OMG-HDCS `.merged` file (also creates `<output_file>.ss_data`). |
| `-v` | None | Off | Print XTF packet index, file header, and ping conversion progress. |
| `-debug` | None | Off | Enable debug flag. |

## How It Works
1. **Indexing:** Scans the input `.xtf` file with `buildXTFIndex()` and verifies that `XTF_HEADER_SONAR` (ID 0) packets exist.
2. **OMG Summary Initialization:** Reads the first sidescan ping header to obtain reference time and coordinates (`SensorYcoordinate`, `SensorXcoordinate`) and writes an `OMG_HDCS_summary_header` (version 3, `numDepths = 2`, `toolType = Knudsen_320`).
3. **Trace Reversal & Beam Packing:** For each sidescan ping:
   * Reads the port channel 16-bit little-endian samples and reverses their sample order (`raw_port_data[j] = temp[NumSamples - j - 1]`) so slant range increases outward from nadir.
   * Reads the starboard channel 16-bit little-endian samples.
   * Populates an `OMG_HDCS_profile_header` with ping time, sample rate (`NumSamples / TimeDuration`), sensor heading, heave, pitch, roll, tide, and sound velocity (`SoundVelocity * 10`).
   * Populates two `OMG_HDCS_beam` records (`beams[0]` for port, `beams[1]` for starboard) with `observedDepth = SensorPrimaryAltitude * 1000.0` (mm), `no_samples`, and byte `offset` into `<output_file>.ss_data`.

## Practical Examples

**1. Convert a Klein XTF file to OMG-HDCS `.merged` and `.ss_data`:**
```bash
klein2omg -v -xtf klein_line01.xtf -omg klein_line01.merged
```
