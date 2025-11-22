---
layout: default
title: removeAngular
parent: OMG Tools
nav_order: 56
---
# removeAngular

## Description
`removeAngular` is a specialized utility designed to correct for angular variations in backscatter intensity within OMG-HDCS merged files. It first calculates the mean backscatter response for each beam (or beam number, which serves as a crude proxy for grazing angle) across an entire dataset. Then, it uses this average response to flatten the backscatter, aiming to produce a more "angle-independent" backscatter measurement.

The tool can either re-calculate backscatter values (for EM1000/EM100_depth_ss/Seabat9001 systems) or apply a correction to existing reflectivity/calibrated backscatter values.

## Usage
```bash
removeAngular <OMG_HDCS_datafile(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile(s)>` | **Required.** One or more paths to OMG-HDCS merged files to be processed. These files are modified in place. |
| `-v` | Enable verbose output. |
| `-recalc` | Re-calculates `calibratedBackscatter` for each beam based on system-specific algorithms (e.g., EM1000, EM100_depth_ss, Seabat9001). This option often requires associated `.ss_data` files for EM1000. |
| `-use_calib` | Use the `calibratedBackscatter` field instead of `reflectivity` for averaging and correction. |
| `-nocorrect` | Do not apply the correction (only calculates and dumps beam averages if `recalc` is not used). |
| `-draft <val>` | Specifies the draft (in meters) to use in amplitude conversion calculations. | `4.0` |
| `-signal <min_dB> <max_dB>` | Defines a signal range (in dB) for backscatter values (used during recalculation for EM1000). | `120.0` to `180.0` |

## How It Works
1.  **File Processing (Loop 1 - Calculation):** The tool iterates through each provided merged file:
    *   **Summary Reading:** Reads the summary header to determine sonar type.
    *   **Recalculation (`-recalc`):** If specified, it iterates through each profile and beam, recalculating the `calibratedBackscatter` based on the sonar `toolType`. For EM1000, this involves reading raw sidescan traces from an `.ss_data` file and applying a 1994 algorithm considering incidence angle. For other types, it uses `EM_convert_amplitude`.
    *   **Beam Average Accumulation:** If `correct_flag` is enabled, it accumulates the sum of reflectivity or calibrated backscatter values and the count for each beam number (`sum[j]`, `count[j]`) across all pings in all input files.
2.  **Beam Average Output:** After the first loop, if `correct_flag` is enabled, it calculates the average backscatter for each beam number and dumps these averages to a file named `Beam.Averages`.
3.  **File Processing (Loop 2 - Correction):** If `correct_flag` is enabled, the tool re-opens each merged file:
    *   **Overall Average:** It calculates an overall average of the mean beam responses.
    *   **Correction Application:** For each beam in each profile, it calculates a correction factor: `(Overall_Average - Mean_Beam_Response[beam_number])`. This correction is added to the beam's reflectivity or calibrated backscatter.
    *   **Pseudo Angle Independent Backscatter:** The corrected value is stored in the `pseudoAngleIndependentBackscatter` field of the beam structure, and clipped to `0-255`.
4.  **In-Place Update:** The modified beam records (specifically the `pseudoAngleIndependentBackscatter` field) are written back to the input merged files.
