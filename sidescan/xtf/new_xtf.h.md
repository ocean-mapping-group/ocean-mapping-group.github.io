---
layout: default
title: new_xtf.h
parent: XTF Tools
grand_parent: Sidescan Tools
nav_order: 9
tool_name: new_xtf.h
source_path: code/sidescan/xtf/new_xtf.h
category: XTF Sidescan Conversion
input_formats: ["C Header File"]
output_formats: ["Included by xtf2glo.c"]
related_tools: ["xtf2glo", "xtf_doc.h", "xtf_funcs.h"]
---

# new_xtf.h

## Description
`new_xtf.h` is the configuration header file for [`xtf2glo`](xtf2glo.md) in `code/sidescan/xtf/`. It defines buffer limits, 16-bit-to-8-bit dynamic range normalization methods, processing bitflags, and the geographic Minimum Bounding Rectangle (`MBR`) structure.

## Constants, Bitflags & Structures

### Buffer & Array Sizes
* `BUFFER_SIZE` (`64000`): Maximum byte size of a single XTF packet read buffer.
* `MAX_PINGS` (`20000`): Maximum pings buffered per pass.

### Dynamic Range Normalization Methods
Used when scaling 16-bit XTF sonar samples into 8-bit JCU GLORIA (`0..255`) pixels:
* `RAW_METHOD` (`1`): Direct bit-shift / raw truncation.
* `MINMAX_METHOD` (`2`): Linear stretch between minimum and maximum ping amplitudes.
* `STDDEV_METHOD` (`3`): Linear stretch across `mean ± N * stddev`.
* `AVG_METHOD` (`4`): Scaling normalized by the mean amplitude (`AVG_MULT = 2`).

### Processing Bitflags
* `RAW_FLAG` (`1`): Preserve raw slant-range samples without ground-range resampling.
* `AUX_DEPTH` (`2`): Extract water depth from auxiliary XTF telemetry fields.
* `INTERP_NADIR` (`4`): Interpolate across the nadir gap between port and starboard channels.
* `BOTTOM_DETECT` (`8`): Perform automated first-return bottom detection (`THRESH_MULT = 1.15`).
* `CMG` (`16`): Compute Course Made Good azimuth from ship/towfish navigation coordinates.

### `MBR` Structure
```c
typedef struct {
   double minX;
   double maxX;
   double minY;
   double maxY;
} MBR;
```
Stores the geographic bounding box written to `<outfile>.mbr` by `xtf2glo`.
