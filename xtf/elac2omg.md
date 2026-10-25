---
layout: default
title: elac2omg
parent: XTF Tools
nav_order: 1
tool_name: elac2omg
source_path: code/xtf/elac2omg.c
category: Raw Data Unraveling
input_formats: [".xtf"]
output_formats: [".merged", ".merged.ss_data", ".orientation", ".nav", ".latency", ".ss_NNN"]
related_tools: ["refoELAC", "qualityFlag", "xtfTool", "xtf2param", "mergeAtt", "mergeNav"]
---

# elac2omg

## Overview
`elac2omg` converts ELAC HydroStar multibeam sonar data logged in Triton XTF (`.xtf`) format into the OMG-HDCS (`.merged`), sidescan (`.merged.ss_data`), attitude (`.orientation`), and navigation (`.nav`) formats. Unlike other XTF converters that handle only bathymetry, `elac2omg` simultaneously extracts embedded attitude (packet ID 3) and navigation fixes from the ELAC HydroStar bathymetry headers (packet ID 16), estimates attitude latency per ping, and unfolds the 3-fan ELAC transmit sequence into sequential 42-beam OMG profile records.

## Usage
```bash
elac2omg [OPTIONS] -nav <ship|sensor> -hdg <ship|sensor> -xtf <input.xtf> -omg <output_prefix>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-xtf` | `<input.xtf>` | **Required** | Path to the input XTF file containing ELAC HydroStar packets (`XTF_HEADER_HYDROSTAR_BATHY`, ID 16). |
| `-omg` | `<output_prefix>` | **Required** | Prefix for output OMG files (`.merged`, `.merged.ss_data`, `.orientation`, `.nav`, `.latency`). |
| `-nav` | `ship` \| `sensor` | **Required** | Select navigation coordinate source from the XTF bathymetry header (`ShipX/Ycoordinate` vs. `SensorX/Ycoordinate`). |
| `-hdg` | `ship` \| `sensor` | **Required** | Select heading source from the XTF bathymetry header (`ShipGyro` vs. `SensorHeading`). |
| `-v` | None | Off | Enable verbose progress output. |
| `-fa` | `<degrees>` | Off | Filter (reject) beams whose beam angle exceeds `<degrees>` from nadir. |
| `-fq` | None | Off | Filter beams by ELAC quality flag (rejects beams where `cQuality != 1`). |
| `-b0` | None | Off | Blank (mark invalid) all beams belonging to ELAC transmit fan 0. |
| `-b1` | None | Off | Blank (mark invalid) all beams belonging to ELAC transmit fan 1. |
| `-b2` | None | Off | Blank (mark invalid) all beams belonging to ELAC transmit fan 2. |
| `-roll` | `<deg>` | `0.0` | Apply an additive roll offset (in degrees) when matching attitude latency and populating profile roll. |
| `-pitch` | `<deg>` | `0.0` | Apply an additive pitch offset (in degrees) when matching attitude latency and populating profile pitch. |
| `-heave` | `<m>` | `0.0` | Apply an additive heave offset (in meters) when matching attitude latency and populating profile heave. |
| `-delay` | `<sec>` | Auto | Override automatic attitude latency estimation with a fixed delay in seconds (converted internally to milliseconds). |
| `-skipSS` | None | Off | Skip extracting sidescan trace data (`XTF_HEADER_SONAR`, ID 0) into `.merged.ss_data`. |
| `-gl` | None | Off | Write 8-bit 1024-pixel JCU GLORIA sidescan files (`<prefix>.ss_001`, `.ss_002`, etc., splitting automatically when pixel size changes). Required `-skipSS` to enter the GLORIA branch. |
| `-plotBeams` | None | Off | When writing GLORIA sidescan (`-gl`), overlay beam sounding positions as bright (`255`) pixels on the sidescan trace. |
| `-whine` | `<count>` | `0` | Maximum number of warnings to print when bathymetry records lack matching sidescan packets. |

## How It Works
1. **Indexing & Verification:** Scans the XTF file with `buildXTFIndex()` and verifies the presence of `XTF_HEADER_HYDROSTAR_BATHY` (ID 16) records. Matches sidescan packets (`XTF_HEADER_SONAR`, ID 0) to bathymetry packets using `matchXTFPackets()`.
2. **Attitude Extraction & Latency Estimation:** Reads all `XTF_HEADER_ATTITUDE` (ID 3) packets into memory arrays (`rollSeries`, `pitchSeries`, `heaveSeries`, `timeSeries`) and writes them to `<prefix>.orientation`. For each bathymetry ping, if `-delay` is not set, `getLatency()` cross-correlates the roll/pitch/heave values embedded in the ELAC beam triplets against the asynchronous attitude time series to estimate the timestamp latency, logging `<ping> <delay_ms>` to `<prefix>.latency`.
3. **3-Fan Unfolding:** Each ELAC HydroStar bathymetry record contains up to 126 beams acquired across 3 sequential transmit fans (42 beams per fan, interleaved every 3rd beam index `3*i + fan`). `elac2omg` sorts the 3 fans chronologically by their `dDelay` offset (`minFan`, `medFan`, `maxFan`) and writes 3 separate 42-beam `OMG_HDCS_profile_header` records per XTF bathymetry packet.
4. **Triplet Packing:** Packs the roll, pitch, heave, and delay of the 3 fans into a 48-byte big-endian `tripletBuffer` stored inside the `profile.params` structure for downstream use by [`refoELAC`](../elac/refoELAC.md).

## Output Files
* `<prefix>.merged`: OMG-HDCS v3 bathymetry file (42 beams per profile, 3 profiles per ELAC ping).
* `<prefix>.merged.ss_data`: Big-endian 16-bit sidescan trace samples.
* `<prefix>.orientation`: OMG-HDCS asynchronous attitude file.
* `<prefix>.nav`: Binary `jcu_nav_rec` navigation file.
* `<prefix>.latency`: ASCII log of ping index and estimated attitude latency (ms).
* `<prefix>.ss_001`, `.ss_002`...: Optional JCU GLORIA sidescan files (when `-gl` and `-skipSS` are used).

## Practical Examples

**1. Standard ELAC XTF conversion using sensor coordinates and quality filtering:**
```bash
elac2omg -v -fq -nav sensor -hdg sensor -xtf line04.xtf -omg line04
```

**2. Blank outer fan 0 and apply a fixed 0.15 s latency:**
```bash
elac2omg -b0 -delay 0.15 -nav ship -hdg ship -xtf line04.xtf -omg line04
```
