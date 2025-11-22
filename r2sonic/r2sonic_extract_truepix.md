---
layout: default
title: r2sonic_extract_truepix
parent: R2Sonic Tools
nav_order: 159
---
# r2sonic_extract_truepix

## Description
`r2sonic_extract_truepix` is a utility designed to extract TruePix data from R2Sonic multibeam sonar `.r2s` files. TruePix is a raw data format from R2Sonic sonars that contains beam-formed magnitude and angle time series for both port and starboard sides.

This tool processes the `.r2s` file, extracts the TruePix data, converts it into 8-bit image data (for magnitude and angle separately), and optionally dumps detailed time-series data for a specific ping to an ASCII file. This is crucial for visualizing the raw backscatter and angle responses, which can be used for advanced bottom classification or quality control.

## Usage
```bash
r2sonic_extract_truepix -r2s <input.r2s> -outprefix <output_prefix> [-ping <ping_number>] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `-r2s <input.r2s>` | **Required.** Path to the input R2Sonic `.r2s` file. |
| `-outprefix <output_prefix>` | **Required.** Prefix for the output files. The tool will generate:
    *   `<output_prefix>_mag.8bit`: 8-bit magnitude image data.
    *   `<output_prefix>_angle.8bit`: 8-bit angle image data.
    *   `<output_prefix>_timeseries.out` (optional): ASCII time-series data for a specific ping. |
| `-ping <ping_number>` | Dumps detailed time-series data for the specified `ping_number` (0-indexed). |
| `-v` | Enable verbose output. |

## How It Works
1.  **Initialization:** Parses command-line arguments to get input/output filenames and the `desired_ping` number.
2.  **File Opening:** Opens the input `.r2s` file for reading. Opens two 8-bit output files (`_mag.8bit`, `_angle.8bit`) for writing magnitude and angle image data. If `desired_ping` is specified, it also opens a `_timeseries.out` file.
3.  **R2Sonic Indexing:** Calls `build_R2SONIC_INDEX()` (an external function) to build an index of the `.r2s` file, locating all TruePix records (`R2SONIC_ID_TPX0`).
4.  **TruePix Data Extraction:** Iterates through each TruePix record found in the index:
    *   Seeks to the `file_offset` of the current TruePix record.
    *   Reads the `R2SONIC_TRUEPIX` data (`tpx`) using `read_R2SONIC_TRUEPIX()`.
    *   **Magnitude Image Generation:**
        *   Allocates an output buffer (`outbuffer`) of `tpx.D1_TotalSamples` size.
        *   For the port magnitude data (`tpx.D1_Data_PortMagnitude`), it converts the magnitude values to an 8-bit logarithmic scale (`2.0 * 20.0 * log10(...)`) and stores them in the `outbuffer` (reversed order).
        *   Writes the `outbuffer` to `_mag.8bit`.
        *   Repeats the process for starboard magnitude data (`tpx.D1_Data_StbdMagnitude`), storing them in `outbuffer` (normal order).
        *   Writes the `outbuffer` to `_mag.8bit`.
    *   **Angle Image Generation:**
        *   For the port angle data (`tpx.D1_Data_PortAngle`), it converts the angle values to an 8-bit scaled representation (`fabs(...) * AngleScalingFactor * 180.0/M_PI * 3.0`) and stores them in `outbuffer` (reversed order).
        *   Writes the `outbuffer` to `_angle.8bit`.
        *   Repeats the process for starboard angle data (`tpx.D1_Data_StbdAngle`), storing them in `outbuffer` (normal order).
        *   Writes the `outbuffer` to `_angle.8bit`.
    *   **Time Series Dump (`-ping`):** If the current `ping` matches `desired_ping`:
        *   Calculates `range` from `rx_sample_rate` and `sound_speed`.
        *   For each sample in the TruePix data, it prints detailed information (sample index, port magnitude, port angle, starboard magnitude, starboard angle, and calculated X/Y coordinates in meters) to `_timeseries.out`.
5.  **Cleanup:** Closes all open files.

## Output Files
*   `<output_prefix>_mag.8bit`: Binary file containing 8-bit magnitude data.
*   `<output_prefix>_angle.8bit`: Binary file containing 8-bit angle data.
*   `<output_prefix>_timeseries.out`: ASCII file with detailed time-series data for a specified ping (if `-ping` is used).
```
```