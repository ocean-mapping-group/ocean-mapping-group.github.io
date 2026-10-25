---
layout: default
title: subsetAscii
parent: HAWAII MR1 Towed Sidescan (mr1)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 10
tool_name: subsetAscii
source_path: mr1/subsetAscii.c
category: navigation_processing
input_formats:
- ASCII_XYZ
output_formats:
- ASCII_XYZ
related_tools:
- combineMW
- swapascii
---

# subsetAscii

## Overview

`subsetAscii` filters a 3-column ASCII `lat lon depth` trackline file (such as the output of [`combineMW`](combineMW)) against a geographic bounding box specified via `get_area()` (`-area`). Whenever the trackline exits the bounding box and later re-enters it, `subsetAscii` inserts a sentinel line-break record (`9999.000000 -9999.000000 9999.000000`) so plotting tools do not draw spurious straight lines across gaps.

## Usage

```
subsetAscii (-verbose) -area wlon elon slat nlat infilename outfilename
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `<infilename>` | `<path>` | *required* | First positional argument: input 3-column ASCII `lat lon depth` file. |
| `<outfilename>` | `<path>` | *required* | Second positional argument: output subsetted ASCII `lat lon depth` file. |
| `-area` | `<tlon> <blon> <blat> <tlat>` | *required* (via `get_area()`) | Geographic bounding box (west lon, east lon, south lat, north lat) parsed by `get_area()`. |
| `-verbose` | none | `0` | Enable verbose flag. |

## How It Works

1. **Bounding Box Initialization**: Calls `get_area()` to parse the geographic bounds (`blat`, `tlat`, `tlon`, `blon`) from the command line or environment.
2. **Trackline Filtering & Gap Marking**: Reads `lat lon depth` triples from `<infilename>`. If a point lies strictly inside `(blat, tlat)` and `(tlon, blon)`:
   - If the immediately preceding input record (`old_count == count - 1`) was also inside, writes `lat lon depth` directly.
   - If one or more intervening records were outside the box, first writes a pen-up separator line `9999.000000 -9999.000000 9999.000000` and then writes `lat lon depth`.
   - Existing `9999.0` separator lines in the input are preserved without duplication (`!last_999`).

## Practical Examples

### Subset an ASCII trackline file to a Solomon Sea bounding box

```bash
subsetAscii -area 148.0 155.0 -10.0 -5.0 mw9204_track.xyz mw9204_solomon.xyz
```
