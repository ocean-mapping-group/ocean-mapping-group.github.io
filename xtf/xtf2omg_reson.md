---
layout: default
title: xtf2omg_reson
parent: XTF Tools
nav_order: 10
tool_name: xtf2omg_reson
source_path: code/xtf/xtf2omg_reson.c
category: Raw Data Unraveling
input_formats: [".xtf", ".idx"]
output_formats: [".merged", ".merged.ss_data"]
related_tools: ["7k2omg", "xtf2nav", "xtf2orientation", "xtf2param", "xtfTool", "makess"]
---

# xtf2omg_reson

## Overview
`xtf2omg_reson` converts Reson SeaBat 8100-series (`8101`, `8111`, `8125`, `8150`, `8160`) multibeam bathymetry (`XTF_HEADER_BATHY`, ID 2), sidescan traces (`XTF_HEADER_SONAR`, ID 0), and snippets (`XTF_HEADER_RESON_SNIPPET`, ID 19) from an XTF file into OMG-HDCS v3 `.merged` and `.merged.ss_data` files.

## Usage
```bash
xtf2omg_reson [OPTIONS] -xtf <inputfile.xtf> -omg <name_prefix>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-xtf` | `<inputfile.xtf>` | **Required** | Path to the input `.xtf` file (automatically loads `<basename>.idx` if present). |
| `-omg` | `<name_prefix>` | **Required** | Output prefix for `<name_prefix>.merged` and `<name_prefix>.merged.ss_data`. |
| `-sonar` | `8101`\|`8111`\|`8125`\|`8150`\|`8160` | Auto from packet | Override or specify the Reson SeaBat model number when not encoded in the Reson bathymetry packet (`resonBathy.sonar_model`). |
| `-fa` | `<degrees>` | Off | Reject beams whose sonar-relative angle (not roll-stabilized) exceeds `<degrees>` from nadir. |
| `-fq` | None | Off | Filter beams using Reson processor quality flags (rejects beams with quality $\le$ threshold). |
| `-rx_beamwidth` | `<hundredths_deg>` | From packet | Override receiver beamwidth (specified in hundredths of a degree, e.g., `150` for $1.5^\circ$); required for legacy `8150` packets (`< 0x17`). |
| `-ER` | None | Off | Specify that an Extended Range (`-ER`) projector was used on a SeaBat 8101 (increases default source level `txLevel` from 210 dB to 220 dB). |
| `-skipSS` | None | Off | Do not extract sidescan trace packets (`XTF_HEADER_SONAR`, ID 0). |
| `-ignoreSSTimeDuration` | None | Off | Compute sidescan sample interval from `SlantRange / (velocity / 2) / NumSamples` instead of trusting `portPingChan.TimeDuration`. |
| `-ss_old` | None | `0` (New) | Flag sidescan as legacy Reson format (`profile.params[1].txBeamIndex = 1`). |
| `-head_temp` | None | Off | Store Reson transducer head temperature (`resonBathy.temperature`) into `profile.params[1].bscatClass` instead of sound velocity (for downstream use with `headtemp2speed`). |
| `-force_sync` | `<method_id>` | Auto-detect | Force a specific XTF time synchronization method (`get_xtf_synchro`). |
| `-ping` | `<ping_num>` | `-1` (Off) | Dump trace, beam, and snippet ASCII debug files for a single specified ping index. |
| `-whine` | `<count>` | `0` | Maximum number of missing sidescan or snippet warnings to print. |
| `-v` | None | Off | Enable verbose diagnostic output. |
| `-debug` | None | Off | Print detailed calibration and parameter packing diagnostics. |

## How It Works
1. **Indexing & Synchronization:** Reads `<basename>.idx` or builds an XTF index via `buildXTFIndex()`, auto-detects the clock synchronization scheme (`get_xtf_synchro()`), and determines `baseTime`.
2. **Calibration & Parameter Packing:** Stores Reson acoustic parameters (source level `txLevel`, `pulse_width`, `tvg_spread`, `tvg_absorp`, sound velocity or head temperature, transmit/receive beamwidths, and pitch steering angle) into `profile.params[0]` and `profile.params[1]`.
3. **Sidescan & Beam Intensity Packing:**
   * Matches `XTF_HEADER_SONAR` packets via `gimme_matching_ss()`, reverses port trace sample order, promotes 8-bit traces to 16-bit if `bytesPerSample == 1`, and writes big-endian 16-bit traces to `<prefix>.merged.ss_data`.
   * For `8101`/`8111`, packs 8-bit beam intensities into `profile.params[0..1].rxtime`. For `8125`/`8150`/`8160`, writes 16-bit beam intensities to `.merged.ss_data` and stores the file offset in `profile.params[0].rxtime`.
4. **Snippet Matching:** If `XTF_HEADER_RESON_SNIPPET` (ID 19) records exist, tracks any ping number offset (`snippet_ping_offset`), writes snippet samples to `.merged.ss_data`, and records `no_samples`, `centre_no`, and `offset` per beam.

## Practical Examples

**1. Convert a Reson 8101 XTF file with quality filtering and attitude/nav extraction:**
```bash
xtf2omg_reson -sonar 8101 -fq -xtf line01.xtf -omg line01
xtf2orientation -xtf line01.xtf -omg line01.orientation
xtf2nav -nav sensor -hdg sensor -xtf line01.xtf -omg line01
```
