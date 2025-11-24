---
layout: default
title: getAngularResponse
parent: OMG Tools
nav_order: 102
---
# getAngularResponse

## Description
`getAngularResponse` is a comprehensive utility designed to model the angular response of backscatter from various multibeam sonar systems, particularly Reson SeaBat series (81XX, 7125). It analyzes backscatter data (sidescan, beam-averaged, or snippet) as a function of incidence angle, applies numerous corrections and filters, and outputs a calibrated angular response curve.

This tool is crucial for backscatter calibration, quality control, and understanding how different sonar systems interact with the seafloor. It can also generate diagnostic images and export the response curve in a standardized format.

## Usage
```bash
getAngularResponse <merged_file(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<merged_file(s)>` | **Required.** One or more paths to input OMG-HDCS merged files (with associated `.ss_data`, `.orientation`, `.depression`, and `.sonar_settings` files). |

### Backscatter Source (Choose one)
| Option | Description |
|---|---|
| `-sidescan` | Use sidescan trace data. |
| `-ri_theta` | Use beam-averaged data (from R/I theta format). |
| `-snippet` | Use snippet data. |

### Angle Calculation
| Option | Description |
|---|---|
| `-grazing <method>` | Specifies the grazing angle estimation method:
    *   `1`: Beam geometry only (`-slope` improves with across-track slope).
    *   `2`: (Default) Neighboring beams and swaths.
    *   `3`: Uses a DTM; requires `-dtm`. | `2` |
| `-slope` | (Used with `-grazing 1`) Improves grazing angle estimate with local across-track slope. |
| `-use_refract` | (Used with `-grazing 2` or `3`) Uses refracted beam vectors (requires `.depression` file). |
| `-dtm <dtm.r4>` | Specifies a DTM file (in `.r4` format) to use with `-grazing 3`. |
| `-vert_ref` | Uses vertically-referenced incidence angle. |
| `-sonar_relative <TX or RX>` | Uses sonar-relative incidence angle (relative to transducer orientation at TX or RX). |
| `-ignore_topo <val>` | If grazing angle differs from basic flat seafloor assumption by `val` degrees, ignore the data point. |

### Data Filtering
| Option | Description |
|---|---|
| `-max_incidence <val>` | Ignore incidence angles above this value. |
| `-min_count <val>` | Don't output values for angular bins with less than `val` beams contributing. | `10` |
| `-use_layover` | (Disables filter) Use portions of the swath prone to layover. |
| `-use_beyond_multiple` | (Disables filter) Use portions of the swath potentially contaminated by multiple reflections. |
| `-first <ping_num>` / `-last <ping_num>` | Process pings only within this range (inclusive). | All pings |
| `-stbd_only` / `-port_only` | Process only starboard or port beams. |

### Corrections & Adjustments
| Option | Description |
|---|---|
| `-redo_prop <val>` | Apply a new absorption coefficient (`val` dB/km) if current value is unreasonable. |
| `-rx_bp <rx.beampatt>` / `-tx_bp <tx.beampatt>` | Specify receiver/transmitter beam patterns to apply. |
| `-dB_scale <val>` | Scale factor for dB values. | `2` |
| `-dB_shift <val>` | Constant dB shift. | `0.0` |
| `-invert_heave` | Invert heave for ensonification and grazing angle calculations. |
| `-smooth_nadir` | Interpolates over potentially bad nadir data. |
| `-old_cal` | Use old calibration method. |

### Output & Debugging
| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-debug_calib` | Enable calibration debugging. |
| `-debug_grazing` | Enable grazing angle debugging. |
| `-debug_ensonification` | Enable ensonification debugging. |
| `-debug_swath_geometry` | Enable swath geometry debugging. |
| `-touch` | Show touched (processed) areas (used with `-check_calib`). |
| `-curious <angle_val>` | Display values for a specific angle. |
| `-check_calib <val>` | Check calibration. (`1`: standard, `2`: with ensonified area offsets). |
| `-ens_area_offset <val>` / `-ens_area_scale <val>` | Offset/scale for ensonified area. |
| `-rolling <n_pings>` | Dump rolling averages every `n_pings`. |
| `-AR_map <ar_map_file>` | Compile into an Angular Response Map. |

## How It Works
1.  **Initialization:** Parses command-line arguments, sets up flags, and initializes global variables for debugging and processing parameters.
2.  **File Setup:**
    *   Opens input merged files, corresponding `.ss_data` (sidescan) or `.sonar_settings` files, `.orientation`, and `.depression` files.
    *   Opens DTM file if `grazing_method == 3`.
    *   Opens output `angular_response` file and `arc.pgm` image file.
3.  **Beam Pattern Loading:** Loads RX and TX beam patterns if specified by `-rx_bp` or `-tx_bp`.
4.  **Profile Iteration:** Loops through each profile (ping) in the merged file:
    *   Reads `profile` header and raw `beams`.
    *   If a SeaBat 7K system, loads `sonar_settings`.
    *   **Data Acquisition:** Reads sidescan data (raw `IScans`) or beam-averaged data into memory based on `sidescan_flag`, `beam_avg_flag`, or `snippet_flag`.
    *   **Grazing Angle Calculation:** Estimates `grazing_angles` for each beam using the specified `grazing_method`.
    *   **Ensonified Area Calculation:** Calculates `ensonified_areas` for each beam.
    *   **Filtering:** Applies filters to weed out problematic data (e.g., layover, multiples, topography differences).
    *   **Calibration:**
        *   If `sidescan_flag` or `snippet_flag` is active, it calls `calibrate_reson` to process the raw backscatter values, applying various corrections (ensonification, propagation, gain).
        *   If `beam_avg_flag` is active, it calls `rebuildResonBeamIntensities`.
    *   **Statistical Accumulation:** For each valid beam, it calculates the backscatter value (converted to dB if needed) and accumulates it into `ByAngle[index]` (sum of linear backscatter) and `bcount[index]` (count of samples) based on the calculated incidence angle.
    *   **Image Accumulation:** Populates an `image` array for PGM output.
    *   **Rolling Average:** If `rolling` is active, it periodically dumps accumulated statistics to the output file.
5.  **Final Processing & Output:** After processing all files:
    *   Calculates `midsig` (a reference intensity) and normalizes the `ByAngle` values relative to it.
    *   If `smooth_nadir` is active, it interpolates over the nadir region.
    *   Writes the final angular response curve (angle, intensity, difference from `midsig`, and count) to the `angular_response` file.
    *   Generates a PGM image (`arc.pgm`) visualizing the angular response curve.
    *   If `do_ar_map` is active, it compiles and prints an `AR_Map` (Angular Response Map).
6.  **Cleanup:** Frees allocated memory and closes all open files.

## Output Files
*   `angular_response`: An ASCII file containing the calibrated angular response curve.
*   `arc.pgm`: A PGM image visualizing the angular response curve.
*   Auxiliary files (e.g., for rolling averages, `AR_Map`) if specific options are used.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `array.h`: For `JHC_header` structure and `.r4` file handling.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.
*   `grazing_angle.h`: For grazing angle calculation functions.
*   `ensonification.h`: For ensonification area calculations.
*   `Echo_calib.h`: For `calibrate_reson` and `rebuildResonBeamIntensities` functions.
*   `backscatter.h`: For backscatter related functions.

## Notes
`getAngularResponse` is a powerful tool for backscatter calibration and seabed characterization. Its ability to apply various corrections and filters makes it adaptable to different sonar types and environmental conditions. The output angular response curves are fundamental for understanding the acoustic properties of the seafloor and for use in backscatter classification schemes. The `-AR_map` option provides a mechanism for compiling spatially distributed angular response data.