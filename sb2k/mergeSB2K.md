---
layout: default
title: mergeSB2K
parent: SB2K Tools
nav_order: 2
tool_name: mergeSB2K
source_path: sb2k/mergeSB2K.c
category: sidescan_processing
input_formats: [GLORIA, OMG_HDCS]
output_formats: [OMG_HDCS]
related_tools: [unravelSB2K, SwathEd, make_mos2]
---

# mergeSB2K

## Overview

`mergeSB2K` merges SeaBeam 2000 sidescan imagery (stored in GLORIA format) onto existing OMG HDCS `.merged` bathymetry files in-place. For each ping profile in the `.merged` file, it searches the GLORIA sidescan file by timestamp and populates beam `61` with the byte offset, sample count (`1024`), center pixel (`512`), and pixel size of the matching sidescan record so OMG tools can display sidescan alongside bathymetry.

## Usage

```
mergeSB2K (-v) (-date year month day) (-base_offset value) -ss ss_file mergefile(s)
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-ss` | `<ss_file>` | *required* | Path to the GLORIA-format sidescan file. |
| `<mergefile(s)>` | `<file1> [file2 ...]` | *required* | One or more OMG HDCS `.merged` files to update in-place. |
| `-v` | none | `0` | Enable verbose output. |
| `-date` | `<year> <month> <day>` | none | Override the reference date (`summary.refTime`) in the `.merged` summary header. |
| `-base_offset` | `<mm>` | `0` | Integer base offset (in millimeters) added during processing. |

## How It Works

1. **Header & Date Update**: Opens the GLORIA sidescan file and each target `.merged` file (`r+`). If `-date` is supplied, updates `summary.refTime` in the `.merged` summary header.
2. **Time Matching & Beam Pointer Update**: For each profile in the `.merged` file, computes the absolute ping time, locates the closest GLORIA record using `jcu_time_search()`, and stores the GLORIA record's file byte offset in `beams[61].offset`, `1024` in `beams[61].no_samples`, `512` in `beams[61].centre_no`, and `pixel_size` in `beams[61].sample_interval`.

## Practical Examples

### Link a GLORIA sidescan file onto a SeaBeam 2000 `.merged` file

```bash
mergeSB2K -v -ss line01.reflect line01.depth
```
