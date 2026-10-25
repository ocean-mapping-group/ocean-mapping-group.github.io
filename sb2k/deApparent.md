---
layout: default
title: deApparent
parent: SeaBeam 2000 / 2100 (sb2k)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 1
tool_name: deApparent
source_path: sb2k/deApparent.c
category: bathymetry_processing
input_formats:
- OMG_HDCS
- OMG_SVP
output_formats:
- OMG_HDCS
related_tools:
- unravelSB2K
- unravelSB2100
- refoSB_Classic
---

# deApparent

## Overview

`deApparent` removes the "apparent depth" assumption applied by legacy SeaBeam sonar systems, which often output depths scaled to a nominal constant sound velocity of 1500 m/s even when raytraced through an in-situ Sound Velocity Profile (SVP). Using a provided `.svp` file, `deApparent` computes the harmonic mean sound speed to each layer depth and rescales `observedDepth` in-place within one or more OMG HDCS `.merged` files back to true water depth.

## Usage

```
deApparent (-v) (-depscale 0.0105) -svp SVP.file mergefile(s)
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-svp` | `<SVP.file>` | *required* | Path to the Sound Velocity Profile (SVP) file containing depth and in-situ sound velocity pairs. |
| `<mergefile(s)>` | `<file1> [file2 ...]` | *required* | One or more OMG HDCS `.merged` files to modify in-place. |
| `-v` | none | `0` | Enable verbose output. |
| `-depscale` | `<value>` | `0.0105` | Manually specify a initial depth scale factor. |

## How It Works

1. **SVP Reading & Harmonic Mean Calculation**: Reads depth and sound velocity pairs from the `-svp` file and computes the cumulative two-way travel time (TWTT) and harmonic mean sound speed (`harmonic_SSP`) for each layer, deriving the ratio `harmonic_SSP / 1500.0`.
2. **In-Place Depth Rescaling**: Opens each `.merged` file in read/write (`r+`) mode, iterates over every ping and beam, interpolates the harmonic sound speed scale factor at the beam's observed depth, and updates `beams[i].observedDepth` in-place.

## Practical Examples

### Convert apparent depths to true depths in SeaBeam `.merged` files

```bash
deApparent -v -svp cast01.svp line01.merged line02.merged
```
