---
layout: default
title: BatchProcEK
parent: EKlook Tools
nav_order: 1
---
# BatchProcEK

## Description
`BatchProcEK` is a command-line utility for batch processing EK series echosounder data, specifically focusing on extracting bottom backscatter (BS) values and compiling Angular Response Curves (ARCs). It's designed to be used *after* initial tuning and setup have been done using the interactive `EKlook.c` tool. It processes multiple merged EK files, performs bottom detection, calculates various parameters related to bottom classification, and outputs ARCs in different formats (full bandwidth, FFT bin-specific, and 3D). It can also perform debug analysis of ensonified area and attenuation for a given depth.

## Usage
```bash
BatchProcEK [OPTIONS] -ins <procEK_dir/EK_file_prefix*.merged>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-dBdrop <value>` | Specifies the signal drop-off (in dB) from the peak in the envelope for bottom detection. | `3.0` |
| `-phaseOffZero <value>` | Phase offset from zero for bottom detection. | `3.0` |
| `-TwoWayBeamWidth <degrees>` | Two-way beam width in degrees. | `12.0` |
| `-AngleSensitivity <value>` | Angle sensitivity for along and across angles. | `10.0` |
| `-EnvWinSize <size>` | Size of the envelope window for FFT analysis (must be 64, 32, 16, 8, 4, or 2). | `16` |
| `-trimdB <value>` | Manual trim dB value for filtering. | `20.0` |
| `-minfrac_MaxCount_toDump <fraction>` | Minimum fraction of maximum count required for an ARC bin to be dumped (e.g., `0.1` means dump if count > 10% of max count). | `0.0` |
| `-use_area_model <mode>` | Specifies the model for ensonified area calculation. `1` for FFT-based, `2` for Bandwidth-based. | `1` (FFT) |
| `-skipfree` | (Debug only) Do not free memory between processing files. | |
| `-skipArea` | Skip ensonified area calculations. | |
| `-skipBP` | Skip Beam Pattern calculations. | |
| `-skipTL` | Skip Transmission Loss calculations. | |
| `-debug_Areas` | Output debug information for ensonified area calculation to `debug.area`. Requires `-fixed_depth`, `-waterT`, `-waterS`. | |
| `-debug_Atten` | Output debug information for attenuation calculation to `debug.atten`. Requires `-fixed_depth`, `-waterT`, `-waterS`. | |
| `-fixed_depth <meters>` | (Used with `-debug_Areas` or `-debug_Atten`) Specifies a fixed water depth for debug calculations. | `100.0` |
| `-waterT <celsius>` | (Used with `-debug_Areas` or `-debug_Atten`) Specifies water temperature in Celsius for attenuation calculations. | `10.0` |
| `-waterS <psu>` | (Used with `-debug_Areas` or `-debug_Atten`) Specifies water salinity in PSU for attenuation calculations. | `30.0` |
| `-areas <AreaMapFileName(s)>` | Specifies one or more area map files (e.g., custom_rot_mapsheet.r4) for spatial processing. | `custom_rot_mapsheet.r4` |
| `-outprefix <prefix>` | Specifies a prefix for the output ARC files. | `MultiFile` |
| `-ins <procEK_dir/EK_file_prefix*.merged>` | **Required.** One or more input merged EK files for batch processing. Wildcards are supported. | `procEK/survey_001.merged procEK/survey_002.merged` |

## Output Files
*   `<outprefix>.ARC_fullBW`: Full bandwidth Angular Response Curve.
*   `<outprefix>.ARC_3D`: 3D Angular Response Curve (full bandwidth).
*   `<outprefix>.ARC_3D.trim`: Trimmed 3D Angular Response Curve (full bandwidth), based on `-minfrac_MaxCount_toDump`.
*   `<outprefix>.ARC_FFTbins`: FFT bin-specific Angular Response Curves.
*   `<outprefix>.ARC_FFT3D`: 3D FFT bin-specific Angular Response Curve.
*   `<outprefix>.ARC_FFT3D.trim`: Trimmed 3D FFT bin-specific Angular Response Curve, based on `-minfrac_MaxCount_toDump`.
*   `debug.area`: ASCII output for debug areas calculation (if `-debug_Areas` is used).
*   `debug.atten`: ASCII output for debug attenuation calculation (if `-debug_Atten` is used).