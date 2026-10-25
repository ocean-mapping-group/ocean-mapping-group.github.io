---
layout: default
title: unravelSB2K
parent: SB2K Tools
nav_order: 5
tool_name: unravelSB2K
source_path: sb2k/unravelSB2K.c
category: format_conversion
input_formats: [SIO_SB2K]
output_formats: [OMG_HDCS, JCU_NAV, OMG_SVP, GLORIA, OMG_SS_DATA]
related_tools: [mergeSB2K, deApparent, unravelSB2100, SwathEd]
---

# unravelSB2K

## Overview

`unravelSB2K` extracts bathymetry (`.depth`), sidescan imagery (`.reflect` and `.merged.ss_data`), navigation (`.nav`), and sound velocity profiles (`.svp`) from Scripps Institution of Oceanography (SIO) SeaBeam 2000 (`SB2K`, 121 beams) multibeam files into OMG HDCS v1 and GLORIA formats.

## Usage

```
unravelSB2K (-korean) (-utm) (-em12s) (-navcockup) (-skipnav N) (-v) \
            (-nav | -depth | -reflect) infile outfile
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `<infile>` | `<path>` | *required* | First positional argument: input SIO SeaBeam 2000 file. |
| `<outfile>` | `<prefix>` | *required* | Second positional argument: output prefix used to generate `<outfile>.depth`, `<outfile>.reflect`, `<outfile>.merged.ss_data`, `<outfile>.nav`, or `<outfile>.svp`. |
| `-depth` | none | `0` | Extract 121-beam swath bathymetry (`SR` records) into `<outfile>.depth` (OMG HDCS v1, `toolType = SB2K`). |
| `-reflect` | none | `0` | Extract 1000-pixel sidescan traces into `<outfile>.reflect` (GLORIA format) and `<outfile>.merged.ss_data`. |
| `-nav` | none | `0` | Open `<outfile>.nav` and `<outfile>.svp` for navigation/SVP extraction. |
| `-v` | none | `0` | Enable verbose output. |
| `-korean` | none | `0` | Scan for `SR` 3-byte ID codes and dump 1819-byte raw scan blocks (used for specific Korean SeaBeam 2000 datasets). |
| `-em12s` | none | `0` | Set maximum depth beam count parameter `MaxDep = 81` (for Simrad EM12S data packed in SIO format) instead of `60`. |
| `-navcockup` | none | `0` | Set `cockup_nav_flag = 1` for corrupted navigation timestamps. |
| `-skipnav` | `<N>` | `1` | Decimate navigation records by keeping every `N`-th record. |
| `-utm` | none | `0` | Set `old_flag` for legacy UTM coordinate records. |

## How It Works

1. **Header Skipping (`-depth` mode)**: Because SIO SeaBeam 2000 files begin with variable-length ASCII header text, `unravelSB2K` scans 16-bit words until it finds a valid year in `[1995, 1999]`, rewinds 2 bytes, and begins reading binary `SIO_header` structures via `jSIO_read_swath_header()`.
2. **Swath Bathymetry (`SR` records)**: Reads `SIO_profile` and 121-point `SIO_soundings` records, converts scaled depth and across-track pairs into millimeters, projects beam `latOffset` and `longOffset` from the vessel heading, and writes OMG HDCS v1 profiles and beams to `<outfile>.depth`.
3. **Sidescan Imagery (`-reflect` mode)**: Reads 1000-byte sidescan amplitude arrays per ping, scales values into 8-bit GLORIA records (`ssrec.stbd_data`), and writes `<outfile>.reflect`. Use `mergeSB2K` afterwards to link `<outfile>.reflect` onto `<outfile>.depth`.

## Practical Examples

### Extract bathymetry and sidescan from an SIO SeaBeam 2000 file

```bash
unravelSB2K -depth sio_sb2k.raw line01
unravelSB2K -reflect sio_sb2k.raw line01
mergeSB2K -ss line01.reflect line01.depth
```
