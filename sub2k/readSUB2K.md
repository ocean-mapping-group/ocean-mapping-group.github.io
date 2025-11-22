---
layout: default
title: readSUB2K
parent: SUB2K Tools
grand_parent: code
nav_order: 5
---
# readSUB2K

## Description
`readSUB2K` is a comprehensive utility designed for processing Submetrix 2000 sonar data, typically from ISIS `.sxr` or `.sxi` files, and converting it into the OMG_HDCS (Ocean Mapping Group Hydrographic Data Collection System) format. This tool performs extensive processing, including:
*   **Sidescan Intensity Scaling:** Linear, square root, logarithmic, or TVG-based scaling of 16-bit intensity data to 8-bit.
*   **Data Quality Filtering:** Based on amplitude thresholds, minimum binned beams, and maximum variance.
*   **Pre-filtering Nadir Beams:** Applies a median filter to nadir beams to improve quality.
*   **Coverage Control:** Limits maximum across-track coverage by specifying either a maximum distance or a multiple of water depth.
*   **Phase-to-Angle Conversion:** Supports different methods (SEA, Vernier, old UNB) for converting phase information into seafloor angles.
*   **Attitude Data Integration:** Handles various MRU (Motion Reference Unit) types (TSS, F180).
*   **Environmental Corrections:** Accounts for magnetic declination, draft, and sound velocity.
*   **Output Formats:** Can output to the traditional single-sided `ISIS_Submetrix` format or a newer double-sided `SEA_SwathPlus` format.

This tool is central to the processing and conversion of Submetrix 2000 data within the OMG toolkit.

## Usage
```bash
readSUB2K [-v] [-debug] [-linss | -sqrtss | -tvgss] [-linrange <min16> <max16>] [-qua_thresh <value>] [-amp_perc_thresh <value>] [-athresh <value>] [-nobelow <value>] [-oftotal <value>] [-firstsam <value>] [-min_binned <value>] [-max_variance <value>] [-max_coverage_metres <value>] [-max_coverage_multiple <value>] [-angle_sss_ratio_multiplier <value>] [-prefilt_nadir_on | -prefilt_nadir <beams> <half_width> <median_frac_depth>] [-ssv_port <value>] [-tss] [-f180] [-mcom] [-ssv <value>] [-method <value>] [-newType] [-declin <value>] [-draft <value>] [-merid <value>] -out <outfile_prefix> <rawISISfile(s)>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-v` | Enable verbose output. | (None) |
| `-debug` | Enable debug mode, printing extensive intermediate values. | (None) |
| `-linss` | Apply linear scaling for sidescan intensity. | (None, mutually exclusive) |
| `-sqrtss` | Apply square root scaling for sidescan intensity. | (None, mutually exclusive) |
| `-tvgss` | Apply TVG-based scaling for sidescan intensity. | (None, mutually exclusive) |
| `-linrange <min16> <max16>` | Specifies the 16-bit input range for linear scaling (`Min16`, `Max16`). | `0 65535` |
| `-qua_thresh <value>` | Quality threshold for phase solutions. | `8` |
| `-amp_perc_thresh <value>` | Amplitude percentage threshold for filtering. | `25` |
| `-athresh <value>` | Amplitude threshold for first arrival picking. | `16` |
| `-nobelow <value>` | Minimum number of samples to be below `athresh` to accept a first arrival. | `10` |
| `-oftotal <value>` | Percentage of samples that must be above `athresh` within a window. | `20` |
| `-firstsam <value>` | First sample to consider for first arrival picking. | `20` |
| `-min_binned <value>` | Minimum number of beams to be binned for a valid solution. | `2` |
| `-max_variance <value>` | Maximum variance for beam solutions. | `2.5` |
| `-max_coverage_metres <value>` | Maximum across-track coverage in meters. | `100` |
| `-max_coverage_multiple <value>` | Maximum across-track coverage as a multiple of water depth. | `12` |
| `-angle_sss_ratio_multiplier <value>` | Multiplier for angle-based sidescan ratio. | `1.05` |
| `-prefilt_nadir_on` | Enable nadir pre-filtering with default settings (75 beams from nadir, 5 half-width, 0.005 median fraction). | (None) |
| `-prefilt_nadir <beams> <half_width> <median_frac_depth>` | Enable nadir pre-filtering with custom parameters. | (None) |
| `-ssv_port <value>` | Specifies which auxiliary input (AUX1 or AUX2, mapped to 1 or 2) contains the port sound speed. | `2` |
| `-tss` | Specify TSS MRU type for attitude data. | `Default` |
| `-f180` | Specify F180 MRU type for attitude data. | (None) |
| `-mcom` | Specify F180 MCOM MRU type for attitude data. | (None) |
| `-ssv <value>` | Set the default surface sound speed to use until a valid sound speed is found in the data. | `1490` |
| `-method <value>` | Selects the phase-to-angle conversion method: `1` (old UNB), `2` (Vernier), or `3` (SEA). | `3` |
| `-newType` | Outputs to the new double-sided `SEA_SwathPlus` toolType in OMG_HDCS. Default is single-sided `ISIS_Submetrix`. | (None) |
| `-declin <value>` | Magnetic declination in degrees. | `0.0` |
| `-draft <value>` | Sensor draft in meters. | `0.0` |
| `-merid <value>` | Central meridian for coordinate conversion. Only needed if input nav is not LAT/LON. | `-69.0` |
| `-out <outfile_prefix>` | **Required.** Prefix for the output OMG_HDCS merged file and associated JCU GLORIA files. | |
| `<rawISISfile(s)>` | **Required.** One or more input raw ISIS data files (`.sxr` or `.sxi`). | |

## How It Works
`readSUB2K` performs a multi-stage process to extract, quality control, and convert Submetrix 2000 data:

1.  **Initialization and Configuration:**
    *   Initializes numerous global variables, lookup tables (`IQ_LUT`, etc.), and alignment parameters.
    *   Parses command-line arguments to set processing flags and parameters.
    *   Determines the input file type (`.sxr` or `.sxi`) based on a magic number.
2.  **File Handling:** Opens the raw ISIS input file and creates multiple output files (an OMG_HDCS merged file, and associated JCU GLORIA files for raw sidescan, depth, etc.).
3.  **Process ISIS Blocks:** The tool iterates through the raw ISIS input file, identifying and processing ISIS Generic Blocks (GBH):
    *   **Ping Start:** Locates `GT_PING_BEGIN` blocks to delineate individual pings.
    *   **Data Extraction:** Extracts various data types from corresponding GBH blocks:
        *   **Attitude:** Roll, pitch, heading, vertical displacement.
        *   **Navigation:** Latitude, longitude, time.
        *   **Raw Sonar Data:** Raw 16-bit sidescan intensity (I and Q data).
        *   **PRANG:** Phase Range data (for phase-based bathymetry).
        *   **Other Sensors:** Depth, sound velocity, temperature, pressure, etc.
    *   **Quality Control & Filtering:** Applies various quality control checks and filters based on configured thresholds for amplitude, variance, and coverage. This includes:
        *   **Phase Confidence:** Filters PRANG solutions based on `qua_thresh`.
        *   **Amplitude Threshold:** Filters based on `amp_perc_thresh`, `athresh`, `nobelow`, `oftotal`, `firstsam`.
        *   **Nadir Pre-filtering (`-prefilt_nadir`):** Applies a median filter to nadir beams to smooth out noise.
        *   **Outlier Rejection:** Rejects beams based on `max_variance` and `max_coverage`.
    *   **Phase-to-Angle Conversion:** Uses the configured `method` (1, 2, or 3) to convert PRANG (phase difference) data into precise seafloor incident angles and corresponding across-track positions. This involves complex calculations using IQ data, array geometry, and sound velocity.
    *   **Sidescan Intensity Processing:**
        *   Applies the chosen intensity scaling (`-linss`, `-sqrtss`, `-tvgss`, or logarithmic) to convert raw 16-bit sidescan data to 8-bit.
        *   Generates separate sidescan image files (e.g., JCU GLORIA format) for these processed intensities.
    *   **OMG_HDCS Output:** For each processed ping, it constructs and writes the `OMG_HDCS_summary_header`, `OMG_HDCS_profile_header`, and `OMG_HDCS_beam` structures to the output merged file. The `profile_header` contains navigation and attitude, while `beam` structures contain individual beam solutions (depth, across-track, along-track, quality flags, etc.).
4.  **Closing Files:** All opened input and output files are closed upon completion.
