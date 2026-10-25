---
layout: default
title: make_knudsen_ss
parent: Knudsen Chirp Sub-Bottom (knudsen)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 9
tool_name: make_knudsen_ss
source_path: knudsen/make_knudsen_ss.c
category: sidescan_processing
input_formats:
- OMG_HDCS
- OMG_SS_DATA
- ASCII_BEAM_PATT
output_formats:
- GLORIA
- ASCII_PICKS
- OMG_HDCS
related_tools:
- knud2glo
- pickSS
- make_mos2
---

# make_knudsen_ss

## Overview

`make_knudsen_ss` (source header `makeSS.c`) converts dual-channel Knudsen sidescan/echosounder trace data stored in OMG HDCS `.merged` and `.merged.ss_data` files into JCU GLORIA 1024-pixel sidescan format (`.ss`). It also supports automatic seabed first-break re-picking (`-repick`, `-just_pick`), in-place updating of `.merged` depths (`-replace`, `-replace_both`), and angular beam-pattern removal (`-beam_patt`).

## Usage

```
make_knudsen_ss (-v) (-log) (-first 100 -last 300) (-port | -stbd | -both) (-swapsides) \
                (-beam_patt file.beam_patt -paintBP -sonar_relative) \
                (-just_pick) (-hfpick | -lfpick) \
                (-repick (-replace | -replace_both) (-minpick 0.5) (-maxpick 20.0) \
                 -pickthresh 50 -thresh_per_m 1 -pickwin 20 -ofwhich 15 -extrapix 25) \
                (-time_series) (-pixel 1.0) -in infilename.merged -out outfilename.ss
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<infilename.merged>` | *required* | Input OMG HDCS `.merged` file (with companion `<infilename.merged>.ss_data`). |
| `-out` | `<outfilename.ss>` | *required* (unless `-just_pick`) | Output JCU GLORIA sidescan file. |
| `-port` / `-stbd` / `-both` | none | `-stbd` (`0`) | Select port (`1`), starboard (`0`), or both (`2`) channels for GLORIA output. |
| `-swapsides` | none | `0` | Swap port and starboard channels in the output GLORIA record. |
| `-pixel` | `<meters>` | `1600/512 * dt` | Output GLORIA pixel size in meters. |
| `-time_series` | none | `0` | Output raw slant-range time series without slant-range-to-ground-range projection. |
| `-log` | none | `0` | Apply logarithmic lookup table (`loglut`) to 8-bit trace samples. |
| `-repick` | none | `0` | Re-pick the seabed arrival on each ping and write `<prefix>.picks`. |
| `-just_pick` | none | `0` | Perform bottom re-picking (`-repick`) without writing a GLORIA output file. Note: `USAGE` shows `-justpick`, while `argv` checks `-just_pick`. |
| `-hfpick` / `-lfpick` | none | `-lfpick` (`1`) | Pick the seabed arrival on the HF (`0`) or LF (`1`) channel. |
| `-replace` / `-replace_both` | none | `0` | Replace the observed depth in the `.merged` file (and save original picks to `<prefix>.orig_picks`) for the picked channel or both channels. |
| `-minpick` / `-maxpick` | `<meters>` | `2.0` / `100.0` | Minimum and maximum depth gate in meters for bottom picking. |
| `-pickthresh` | `<0..255>` | `50` | 8-bit amplitude threshold for bottom picking. |
| `-thresh_per_m` | `<val>` | `0.0` | Depth-dependent threshold slope added per meter of range. |
| `-pickwin` / `-ofwhich` | `<samples>` | `20` / `15` | Confirmation window length (`pickwin`) and required number of samples above threshold (`ofwhich`). |
| `-extrapix` | `<cm>` | `0` | Extra altitude offset in centimeters added to the bottom pick. |
| `-beam_patt` | `<file>` | none | Load a 180-degree beam-pattern correction table (`angle pattern corrector count`). |
| `-paintBP` | none | `0` | Paint the beam pattern directly into the output trace for diagnostic verification. |
| `-sonar_relative` | none | `0` | Apply beam-pattern correction relative to the sonar roll angle (`profile.vesselRoll`). |
| `-first` / `-last` | `<ping>` | all | First and last ping indices to process. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **Bottom Re-Picking**: When `-repick` or `-just_pick` is specified, reads the 8-bit trace for `chanpick` from `.merged.ss_data`, searches between `minTWTT` and `maxTWTT` for the first sample where at least `ofwhich` of the next `pickwin` samples exceed `pickthresh`, writes the picked depth to `<prefix>.picks`, and optionally updates `beams[side].observedDepth` and `beams[side].centre_no` in-place (`-replace`).
2. **GLORIA Sidescan Generation (`get_ss_trace`)**: Resamples the 8-bit port/starboard trace into 512 pixels per side (`gloria_rec`), optionally applies angular beam-pattern compensation (`Beam_Corrector`) and slant-range correction using the transducer altitude, and writes each record to `-out`.

## Practical Examples

### Convert a dual-channel Knudsen `.merged` file into a GLORIA sidescan file

```bash
make_knudsen_ss -both -pixel 0.25 -in knud_line01.merged -out knud_line01.ss
```
