---
layout: default
title: swapascii
parent: HAWAII MR1 Towed Sidescan (mr1)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 11
tool_name: swapascii
source_path: mr1/swapascii.c
category: navigation_processing
input_formats:
- ASCII_XYZ
output_formats:
- ASCII_XYZ
related_tools:
- combineMW
- subsetAscii
---

# swapascii

## Overview

`swapascii` reads a 3-column ASCII `lat lon depth` file (up to 10,000 records) into memory and writes the records out in reverse chronological/spatial order (`count - 1` down to `0`).

## Usage

```
swapascii (-verbose) infilename outfilename
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `<infilename>` | `<path>` | *required* | First positional argument: input 3-column ASCII `lat lon depth` file (`double lat`, `double lon`, `int depth`). |
| `<outfilename>` | `<path>` | *required* | Second positional argument: output reversed ASCII `lat lon depth` file. |
| `-verbose` | none | `0` | Enable verbose flag. |

## How It Works

1. **In-Memory Ingestion**: Reads `lat[count]`, `lon[count]`, and integer `depth[count]` triples from `<infilename>` until EOF (up to 10,000 rows) and prints `count : <N>`.
2. **Reverse Output**: Loops `i` from `0` to `count - 1`, writing `lat[count - i - 1]`, `lon[count - i - 1]`, and `depth[count - i - 1]` to `<outfilename>`.

## Practical Examples

### Reverse the order of an ASCII bathymetry profile

```bash
swapascii profile_north_to_south.xyz profile_south_to_north.xyz
```
