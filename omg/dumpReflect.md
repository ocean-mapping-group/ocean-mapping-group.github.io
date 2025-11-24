---
layout: default
title: dumpReflect
parent: OMG Tools
nav_order: 92
---
# dumpReflect

## Description
`dumpReflect` is a utility designed to extract and process reflectivity or backscatter data from OMG-HDCS merged files. It can dump raw or processed reflectivity values, apply various corrections (e.g., gain adjustments, grazing angle corrections), and generate a 2D map of reflectivity or corrected backscatter.

The tool supports specific processing for EM1000 and similar sonar types, allowing for recalculation of calibrated backscatter, and provides options for mapping and normalization.

## Usage
```bash
dumpReflect <OMG_HDCS_datafile> <dumpfile> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile>` | **Required.** The path to the input OMG-HDCS merged file. |
| `<dumpfile>` | **Required.** The path for the output dump file. The format depends on the options (e.g., JHC `.r4` image or ASCII). |
| `-verbose` | Enable verbose output. |
| `-recalc` | Recalculates `calibratedBackscatter` for EM1000 and similar sonars based on internal algorithms, then uses this for output. |
| `-calib` | Use `calibratedBackscatter` field for processing (if available), otherwise `reflectivity`. |
| `-gainout` | Normalizes the output backscatter values to an average of 128 (for Angle-Independent Backscatter). |
| `-map` | Generates a 2D map (JHC `.r4` image) of reflectivity or corrected backscatter. This requires a `skip` value to determine ping resolution. |
| `-graz <val>` | Applies a user-specified correction for grazing angle, defined as DN per degree. | `0.0` |
| `-skip <val>` | Number of pings to skip when generating a map (for vertical resolution). | `1` |
| `-signal <min_dB> <max_dB>` | Defines a signal range (in dB) for backscatter values (used during recalculation). | `140.0` to `180.0` |
| `-range <start_ping> <end_ping>` | Process pings only within this range (inclusive). | All pings |
| `-dumpmod` | (Present in `USAGE` but not fully implemented in main path) Likely intended to dump modified values. |

## How It Works
1.  **File Opening & Initialization:** Opens the input merged file and the specified output dump file. Initializes global flags and parameters.
2.  **Summary Header Reading:** Reads the summary header from the merged file to determine sonar type and number of profiles.
3.  **Recalculation (`-recalc`):** If specified, it iterates through all beams in all pings, recalculating `calibratedBackscatter` using `EM_convert_amplitude` (for EM100_depth_ss, Seabat9001) or specific EM1000 logic. This updates the `calibratedBackscatter` field in the merged file.
4.  **Accumulate Averages (`-map` or `-gainout`):** If `-map` or `-gainout` is active, it iterates through pings and beams to calculate the average reflectivity/calibrated backscatter per beam number (`sum[j]`) and the count of valid beams (`count[j]`).
5.  **Map Generation (`-map`):** If `-map` is active:
    *   Writes a JHC header to the output dump file (`outname`).
    *   Iterates through pings (skipping with `skip`):
        *   Extracts reflectivity/backscatter for each beam.
        *   Scales and places these values into an `amplitude` array, which is then written to the `.r4` file. This creates a 2D image where one dimension is beam number and the other is ping number.
        *   If `calib_flag` and `dumpraw_flag` are active, it outputs raw calibrated backscatter. Otherwise, it applies a correction based on `sum[j]`.
        *   Also writes auxiliary information (pulse length, power, attenuation, TVG) to `plot.ascii`.
6.  **Gain Normalization (`-gainout`):** If active:
    *   Calculates an overall average energy from central beams (excluding nadir and edges).
    *   Normalizes the `pseudoAngleIndependentBackscatter` values for all beams such that the average energy of the swath becomes 128.
7.  **Output to Merged File:** If `!dumpraw_flag` (meaning modified values are being used and mapped), it updates the `pseudoAngleIndependentBackscatter` field in the merged file (and `reflectivity` for certain sonar types).
8.  **Cleanup:** Closes all open files.

## Output Files
*   `<dumpfile>`: The main output file, which can be a JHC `.r4` image of reflectivity/backscatter map, or ASCII listing depending on options.
*   The input merged file may be modified in-place if `-recalc` or `-gainout` are used.
*   `plot.ascii`: Auxiliary ASCII file with plotting information (if `-map` is used).

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `array.h`: For `JHC_header` structure and `.r4` file handling.
*   `support.h`: For general utility functions and error handling.
*   `Echo_calib.h`: For `EM_convert_amplitude` function (for recalculation).

## Notes
This tool is flexible for debugging, visualizing, and standardizing backscatter data. The `-recalc` option is particularly useful for re-applying or comparing manufacturer-specific backscatter algorithms. The `-map` option provides a quick visual overview of the backscatter patterns across a survey line. The tool's behavior regarding in-place modification or new file creation depends on the chosen options.