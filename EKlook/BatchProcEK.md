---
layout: default
title: BatchProcEK
parent: Simrad EK60/EK80 Echosounder Suite (EKlook)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 1
tool_name: BatchProcEK
source_path: code/EKlook/BatchProcEK.c
category: EKlook
input_formats:
- OMG_HDCS (.merged)
- JHC Float Trace Arrays (.MF_dB, .Raw_dB, .PS_phase, .FA_phase, .MF_IQ)
- Bottom Track Guide (.BottomTrackGuide)
- JHC Float Area Maps (.r4)
output_formats:
- Full-Bandwidth ARC (.ARC_fullBW, .ARC_3D, .ARC_3D.trim)
- Spectral FFT ARC (.ARC_FFTbins, .ARC_FFT3D, .ARC_FFT3D.trim)
related_tools:
- EKlook
- comboCalibEK_ARCs
- EK_BottomBS
- EK_funcs
---

# BatchProcEK

## Description
`BatchProcEK` is a command-line utility for batch processing Kongsberg Simrad EK60/EK80 echosounder files, extracting bottom backscatter ($BS$) values, and compiling both full-bandwidth and spectral FFT Angular Response Curves (ARCs). It is designed to be run after interactive parameter tuning and bottom-track guide creation (`<prefix>.BottomTrackGuide`) in [`EKlook`](EKlook.html), and its output ARC files feed directly into [`comboCalibEK_ARCs`](comboCalibEK_ARCs.html).

## Usage

```bash
BatchProcEK [OPTIONS] -ins <procEK_dir/EK_file_prefix*.merged>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-dBdrop <value>` | Signal drop-off (in dB) from the envelope peak for bottom detection. | `3.0` |
| `-phaseOffZero <value>` | Phase offset from zero (degrees) for split-beam bottom detection. | `3.0` |
| `-TwoWayBeamWidth <degrees>` | Two-way $-3\text{ dB}$ beam width in degrees. | `12.0` |
| `-AngleSensitivity <value>` | Split-beam electrical-to-mechanical angle sensitivity for along and across angles. | `10.0` |
| `-EnvWinSize <size>` | Envelope sub-window size in samples for FFT spectral ARC analysis (must be `64`, `32`, `16`, `8`, `4`, or `2`). | `16` |
| `-trimdB <value>` | Manual amplitude threshold (dB) for target/bottom search. | `20.0` |
| `-minfrac_MaxCount_toDump <fraction>` | Minimum fraction of maximum bin count required for an ARC bin to be exported in `.trim` files. | `0.0` |
| `-use_area_model <mode>` | Ensonified area model: `1` for FFT sub-window duration, `2` for effective pulse bandwidth. | `1` (FFT) |
| `-skipfree` | (Debug) Do not free trace memory between files. | |
| `-skipArea` | Skip ensonified area correction. | |
| `-skipBP` | Skip beam pattern roll-off correction. | |
| `-skipTL` | Skip transmission loss correction. | |
| `-debug_Areas` | Dump ensonified area debug curves to `debug.area` (requires `-fixed_depth`, `-waterT`, `-waterS`). | |
| `-debug_Atten` | Dump acoustic absorption debug curves to `debug.atten` (requires `-fixed_depth`, `-waterT`, `-waterS`). | |
| `-fixed_depth <meters>` | Water depth (m) for `-debug_Areas` / `-debug_Atten`. | `100.0` |
| `-waterT <celsius>` | Water temperature ($^\circ\text{C}$) for `-debug_Areas` / `-debug_Atten`. | `10.0` |
| `-waterS <psu>` | Water salinity (PSU) for `-debug_Areas` / `-debug_Atten`. | `30.0` |
| `-areas <AreaMapFileName(s)>` | One or more JHC `.r4` area map files for spatial subsetting. | `custom_rot_mapsheet.r4` |
| `-outprefix <prefix>` | Prefix for the output ARC files. | `MultiFile` |
| `-ins <procEK_dir/EK_file_prefix*.merged>` | **Required.** One or more input `.merged` EK files (companion `.MF_dB`, `.PS_phase`, `.FA_phase`, `.MF_IQ` files are loaded automatically). | `procEK/survey_*.merged` |

## Output Files
*   `<outprefix>.ARC_fullBW`: 2D full-bandwidth Angular Response Curve.
*   `<outprefix>.ARC_3D` & `<outprefix>.ARC_3D.trim`: 3D full-bandwidth Angular Response Curve (and density-trimmed version).
*   `<outprefix>.ARC_FFTbins`: 2D FFT frequency-bin Angular Response Curves.
*   `<outprefix>.ARC_FFT3D` & `<outprefix>.ARC_FFT3D.trim`: 3D FFT frequency-bin Angular Response Curve (and density-trimmed version).
*   `debug.area` / `debug.atten`: Optional diagnostic tables when `-debug_Areas` or `-debug_Atten` is enabled.
