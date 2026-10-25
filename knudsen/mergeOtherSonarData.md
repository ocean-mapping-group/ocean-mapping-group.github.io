---
layout: default
title: mergeOtherSonarData
parent: Knudsen Tools
nav_order: 10
tool_name: mergeOtherSonarData
source_path: knudsen/mergeOtherSonarData.c
category: bathymetry_processing
input_formats: [OMG_HDCS, JCU_NAV]
output_formats: [OMG_HDCS, BINARY_DELAY]
related_tools: [knud2glo, pickSS, make_knudsen_ss, SwathEd]
---

# mergeOtherSonarData

## Overview

`mergeOtherSonarData` cross-references a target OMG HDCS `.merged` file (`-in`) against one or more time-synchronous "aiding" OMG HDCS `.merged` files collected simultaneously on the same vessel (for example, using a Simrad EM3000/EM300 multibeam to provide roll/pitch/heave/heading or nadir depth to a Knudsen 320 sub-bottom profiler, or conversely using a rock-solid 3.5 kHz Knudsen nadir depth to pre-filter noisy deep multibeam outer beams). Because independent sonar acquisition clocks (such as the Knudsen PC clock) often drift relative to the primary multibeam UTC clock, `mergeOtherSonarData` can automatically estimate and track time-varying clock latency (`-auto_delay`, `-running_delay`) by matching vessel positions in the two systems' `.nav` files.

## Usage

```
mergeOtherSonarData -in target_file.merged (-v) \
                    (-auto_delay) (-running_delay 2) (-use_nav 0) \
                    (-delay 10.0) (-offset 2.2) \
                    (-replace_attitude) (-replace_depth) (-userealTWTT) \
                    (-draft 7.0 -sound_speed_ratio 1.031) (-tol 5.0) \
                    aiding_file1.merged [aiding_file2.merged ...]
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<target.merged>` | *required* | Target OMG HDCS `.merged` file to be aided (modified in-place). |
| `<aiding_files>` | `<file1.merged> [...]` | *required* | One or more time-synchronous OMG HDCS `.merged` files providing aiding data. |
| `-replace_attitude` | none | `0` | Replace transmit attitude (roll, pitch, heave, heading) in `-in` with the time-matched attitude from the aiding sonar. |
| `-replace_depth` | none | `0` | Replace bottom-track depth in `-in` with the mean depth of the center 20 beams from the aiding multibeam sonar. |
| `-tol` | `<meters>` | `0.0` | Reject beams in `-in` whose depth differs from the aiding sonar's depth by more than `<meters>`. |
| `-userealTWTT` | none | `0` | Compute depth from two-way travel time rather than `observedDepth`. |
| `-draft` | `<meters>` | `0.0` | Transducer draft in meters applied when comparing/replacing depths. |
| `-sound_speed_ratio` | `<ratio>` | `1.0` | Ratio of sound speeds (`e.g., 1500 / 1455`) between the two sonars. |
| `-delay` | `<seconds>` | `0.0` | Fixed clock delay in seconds added to `-in` timestamps when searching aiding files. |
| `-offset` | `<seconds>` | `0.0` | Additional constant delay offset in seconds applied after automatic delay calculation. |
| `-auto_delay` | none | `0` | Estimate clock latency between `-in` and the aiding files by matching GPS positions in their respective `.nav` files. |
| `-running_delay` | `<window_pings>` | `0` (`< 50`) | Run a moving-window filter (`window_pings` forward and behind) on `-auto_delay` estimates and write `<prefix>.running_delay`. |
| `-use_nav` | `<0\|1\|2>` | `0` (`.nav`) | Select which navigation file extension (`.nav`, `.nav_1`, or `.nav_2`) to read for the aiding sonar during `-auto_delay`. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **Chronological Aiding File Sort**: Reads `OMG_HDCS_summary_header` from all aiding `.merged` files and sorts them chronologically by `summary.refTime`.
2. **Clock-Drift Estimation (`-auto_delay` / `-running_delay`)**: Compares the latitude/longitude fix in the target file's `.nav` against the aiding file's `.nav` (`.nav_1`, `.nav_2`) to find the timestamp offset where both files occupy the same geographic position. When `-running_delay` is enabled, smooths the per-ping delay across `+-run_win` pings in a two-pass loop (`redo_search`).
3. **In-Place Aiding Transfer**: Matches each ping `swath_profile.time + delay + delay_offset` via `match_records()` and updates attitude (`-replace_attitude`), nadir bottom-track depth and `centre_no` (`-replace_depth`), or flags outlier beams exceeding `-tol` (`status = 22`).

## Practical Examples

### Transfer multibeam attitude and centerbeam depth to a Knudsen `.merged` file with running clock-drift correction

```bash
mergeOtherSonarData -v -in knud_line01.merged -running_delay 10 \
                    -replace_attitude -replace_depth em3002_*.merged
```
