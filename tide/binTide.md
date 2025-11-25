---
layout: default
title: binTide
parent: Tide Tools
---

# binTide

## Description
`binTide` is a utility that converts ASCII listings of tide data into the jcu_nav binary format for merging with other navigation data. It reads time and tide height values from an ASCII file and outputs them in a structured binary format suitable for integration into OMG processing workflows.

## Usage
```bash
binTide (-v) (-1970time) (-addsine) (-scale 0.01) (-offset -0.63) (-delay 180) (-position lat lon) -year 1996 (or -V2 -V3) asciitidefile binarytidefile
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output |
| `-1970time` | Use 1970-based time format |
| `-addsine` | Add sine wave component |
| `-scale` | Scale factor for tide values |
| `-offset` | Offset to apply after scaling |
| `-delay` | Time delay in seconds |
| `-position lat lon` | Position coordinates |
| `-year` | Year for date calculation |
| `-V2` | Version 2 format (has year) |
| `-V3` | Version 3 format (has yyyymmdd) |
| `asciitidefile` | Input ASCII tide file |
| `binarytidefile` | Output binary tide file |

## How It Works
1. **Input Parsing:** Reads ASCII tide data with time and height values
2. **Format Conversion:** Converts to jcu_nav binary format
3. **Optional Processing:** Applies scaling, offsets, delays, and position information as specified
4. **Output:** Writes structured binary file for merging
