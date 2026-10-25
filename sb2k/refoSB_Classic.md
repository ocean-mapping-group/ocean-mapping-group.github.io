---
layout: default
title: refoSB_Classic
parent: SB2K Tools
nav_order: 3
tool_name: refoSB_Classic
source_path: sb2k/refoSB_Classic.c
category: format_conversion
input_formats: [URI_SEABEAM]
output_formats: [OMG_HDCS]
related_tools: [deApparent, unravelSB2K, unravelSB2100, SwathEd]
---

# refoSB_Classic

## Overview

`refoSB_Classic` converts legacy 19-beam "Classic" SeaBeam multibeam data stored in the University of Rhode Island (URI) binary format into OMG HDCS `.merged` format (`toolType = SeaBeam`, `numDepths = 19`). It also includes support for PMEL BSSS (Bathymetric Swath Survey System) data packed into URI records (`-BSSS`) and SNBESS flagged beams (`-snbess`).

## Usage

```
refoSB_Classic (-v) (-noswap) (-BSSS) (-snbess) (-align514) (-packdown) \
               (-force_summ_ll -14.0 145.0) infile outfile
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `<infile>` | `<path>` | *required* | First positional argument: input URI-format Classic SeaBeam file. |
| `<outfile>` | `<path>` | *required* | Second positional argument: output OMG HDCS `.merged` file. |
| `-v` | none | `0` | Enable verbose output (prints record number, timestamp string, and lat/lon). |
| `-noswap` | none | swap enabled | Disable 16-bit byte swapping when reading `sb_urirec` records. |
| `-BSSS` | none | `0` | Handle PMEL BSSS data packed into URI format: doubles across-track distances (`acrossTrack *= 2`) and computes vessel heading (`HOG`) from a 5-ping running position difference. Note: `USAGE` shows `-bsss`, but the parser checks `-BSSS`. |
| `-snbess` | none | `0` | Handle SNBESS flagged beams: any beam with `abs(disp[i]) > 19999` has `20000` subtracted from its magnitude and its `status` set to `22` (rejected). |
| `-align514` | none | `0` | Set `Align_514 = 1` for 514-byte record alignment in `sb_readuri()`. |
| `-packdown` | none | `1` (v2) | Use OMG HDCS `fileVersion = 2` packed format (enabled by default). |
| `-force_summ_ll` | `<lat> <lon>` | 1st ping position | Force the summary header reference latitude and longitude (in decimal degrees). |

## How It Works

1. **Record Reading & Byte Swapping**: Reads 102-byte URI SeaBeam records (`sb_urirec`) via `sb_readuri()`. By default (`swap_flag = 1`), swaps adjacent bytes in every 16-bit word before decoding.
2. **Time & Navigation Decoding**: Extracts timestamp via `sb_stdtime()`, latitude via `sb_declat()`, and longitude via `sb_declon()`. On the first swath, initializes `summary.refTime`, `summary.refLat`, and `summary.refLong`.
3. **BSSS Heading Calculation**: When `-BSSS` is specified, the URI course field is replaced by heading-over-ground (`HOG`) computed from the delta North (`dN`) and delta East (`dE`) over the preceding 5 pings.
4. **Beam Geometry**: Populates 19 beams per swath, converting `depth[i]` and `disp[i]` from meters to millimeters (`* 1000`), handling `-snbess` (`> 19999` flagged as status `22`) and `-BSSS` (`acrossTrack *= 2`), and projecting `latOffset` and `longOffset` from the vessel heading. Rewrites `summary.numProfiles` at EOF.

## Practical Examples

### Convert a URI Classic SeaBeam file to OMG HDCS format

```bash
refoSB_Classic -v cruise94.uri cruise94.merged
```

### Convert PMEL BSSS data stored in URI format

```bash
refoSB_Classic -BSSS -force_summ_ll -14.0 145.0 pmel_bsss.uri pmel_bsss.merged
```
