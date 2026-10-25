---
layout: default
title: unravelSB2100
parent: SB2K Tools
nav_order: 4
tool_name: unravelSB2100
source_path: sb2k/unravelSB2100.c
category: format_conversion
input_formats: [SB2100]
output_formats: [OMG_HDCS, OMG_SS_DATA]
related_tools: [unravelSB2K, refoSB_Classic, deApparent, SwathEd]
---

# unravelSB2100

## Overview

`unravelSB2100` converts raw SeaBeam 2100 (`SB2100`) multibeam files containing `PR` (Parameter), `TR` (Text), `DR` (Depth), and `SS` (Sidescan) records into OMG HDCS v3 `.merged` bathymetry files (`toolType = SB2100`, up to 151 beams) and companion `.merged.ss_data` raw sidescan trace files.

## Usage

```
unravelSB2100 (-v) (-declin 10) (-no_abort) infile
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `<infile>` | `<path>` | *required* | Positional argument specifying the input SeaBeam 2100 file. Outputs `<infile>.merged`, `<infile>.ss`, and `<infile>.merged.ss_data`. |
| `-v` | none | `0` | Enable verbose output (prints full contents of `PR`, `TR`, `DR`, and `SS` records; otherwise prints single-character progress codes `P`, `T`, `D`, `S`). |
| `-declin` | `<degrees>` | `0.0` | Magnetic declination offset in degrees added to `dr.TX_heading` before storing `profile.vesselHeading`. |
| `-no_abort` | none | `0` | Increment `override_abort` so the parser continues past non-fatal record format errors. |

## How It Works

1. **Start-of-Frame Scanning**: Scans the input file using `jSB2100_find_next_SOF(infile, ID)` to locate 2-character record identifiers:
   - **`PR` (Parameter Record)**: Read via `jSB2100_read_parameter_record()`.
   - **`TR` (Text Record)**: Skipped or printed when `-v` is active.
   - **`DR` (Depth Record)**: Read via `jSB2100_read_depth_record()` into `dr` and marks `got_depth`.
   - **`SS` (Sidescan Record)**: Read via `jSB2100_read_sidescan_record()` into `sr`. If a depth record has been read (`got_depth`), invokes `dump_swath()`.
2. **Swath & Sidescan Output (`dump_swath`)**:
   - Appends raw sidescan pixel pairs (`sr.no_pixels * 4` bytes) to `<infile>.merged.ss_data` and records the byte offset in `ss_offset`.
   - Applies any `-declin` magnetic declination correction to `dr.TX_heading` (wrapping into `[0, 360)`), populates `OMG_HDCS_profile_header` (attitude, gain, pulse width, surface sound velocity), and writes 151 `OMG_HDCS_beam` structures with calibrated backscatter and across-track/along-track offsets to `<infile>.merged`.

## Practical Examples

### Convert a SeaBeam 2100 raw file with a 12.5-degree magnetic declination correction

```bash
unravelSB2100 -declin 12.5 sb2100_line01.raw
```
This creates `sb2100_line01.raw.merged` and `sb2100_line01.raw.merged.ss_data`.
