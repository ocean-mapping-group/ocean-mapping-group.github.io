---
layout: default
title: understand_KM_BS
parent: OMG Tools
nav_order: 73
---
# understand_KM_BS

## Description
`understand_KM_BS` is a diagnostic utility designed to extract and analyze various backscatter (BS) and related data fields from KMALL-format OMG-HDCS merged files. It provides a flexible way to dump specific parameters for each beam in each ping, either to an ASCII file or a custom binary (`.r4`) file, facilitating detailed investigation of the raw and corrected backscatter values.

The tool supports a wide range of parameters, including raw reflectivity, applied corrections (e.g., source level, receiver sensitivity), TVG components, and various derived quantities. It also offers options to manipulate calibration data (remove/flip `BScalibration_dB`) and plot specific trends.

## Usage
```bash
understand_KM_BS <OMG_HDCS_datafile(s)> [OPTIONS] -out <ASCII_listing_file>
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile(s)>` | **Required.** One or more paths to input OMG-HDCS merged files (currently only supports a single input file due to code structure). |
| `-out <ASCII_listing_file>` | **Required.** The path for the output ASCII listing file. A binary dump file (`.dmp`) will also be created with the same prefix. |

### Parameter Selection (Choose one)
| Option | Description |
|---|---|
| `-absco` | Absolute absorption coefficient (dB/km). |
| `-refl1` | Reflectivity 1 (dB, often raw backscatter). |
| `-refl2` | Reflectivity 2 (dB). |
| `-rxsen` | Receiver sensitivity applied (dB). |
| `-slapp` | Source level applied (dB). |
| `-bscal` | Backscatter calibration value (dB). |
| `-tvgdb` | Time-Varying Gain (TVG) in dB. |
| `-angrx` | Beam angle relative to receiver (deg). |
| `-ancor` | Beam angle correction (deg). |
| `-angin` | Beam incidence angle adjustment (deg). |
| `-calbs` | Calibrated backscatter (historic 8-bit, 0.5dB/DN). |
| `-aibss` | Pseudo Angle Independent Backscatter (historic 8-bit, 0.5dB/DN). |
| `-sl-rx` | Sum of source level and receiver sensitivity applied (dB). |
| `-r1-r2` | Difference between reflectivity 1 and reflectivity 2 (dB). |
| `-range` | Slant range (m). |
| `-2alpR` | Two-way acoustic path loss (2αR). |
| `-XlogR` | Custom logarithmic slant range (X * log10(slant_range)), where X is set by `-xlogval`. |
| `-10logR` / `-20logR` / `-30logR` / `-40logR` | Logarithmic slant range with specified multipliers. |
| `-xlogval <val>` | Scaler for `-XlogR` option. | `30.0` |
| `-lambe` | Lambertian model prediction for backscatter. |
| `-setvg` | Simrad TVG component (BTS - Bottom Trace Shift). |
| `-bsn_o` | Simrad BSn-BSo (Backscatter Normal to Seabed Surface, minus original). |
| `-areaV` | Area Volume (calculated from beam widths and slant range). |
| `-sstrc` | Sidescan trace average intensity. |
| `-altrk` | Along-track SRA (Sonar Relative Angle) correction values (reads from `.SRA_along_atit.r4`). |
| `-actrk` | Across-track SRA correction values (reads from `.SRA_across_atit.r4`). |

### Calibration Manipulation
| Option | Description |
|---|---|
| `-remove_bscal` | Removes `BScalibration_dB` from `refl1` or `refl2`. |
| `-flip_bscal` | Flips the sign of `BScalibration_dB` (applies `+2 * BSCAL` to compensate for double sign-flip). |

### Profile-level Parameters (for line plots)
| Option | Description |
|---|---|
| `-scstr` | Steering angle of transmit sectors. |
| `-pitch` | Vessel pitch (deg). |
| `-rollt` | Vessel roll (deg). |
| `-headi` | Vessel heading (deg). |
| `-RPGrange <min> <max>` | Range for values of profile-level parameters. | `-10` to `10` (for pitch/roll/scstr), `0` to `360` (for heading) |

### Filtering & Range Options
| Option | Description |
|---|---|
| `-specific_swath <val>` | Processes data only for a specific swath (0-indexed). |
| `-start <ping_num>` / `-end <ping_num>` | Processes pings only within this range (inclusive). | All pings |

### Other Options
| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-ascii_dmp` | Dumps chosen parameter values to the ASCII output file. |
| `-recalc_NormalIncid` | Re-calculates `owtt_to_normal_incidence_crossover` in Simrad TVG. |
| `-alrxbp <angle> <dB_drop>` | Sets parameters for Along-track Receiver Beam Pattern (alrxbp) calculation (used with `-altrk`). | `10` (angle), `3.0` (dB_drop) |

## Output
*   **`<ASCII_listing_file>` (specified by `-out`):** Contains space-separated values of ping number, beam number, ping time, beam angle, and the chosen parameter for each beam. This is generated only if `-ascii_dmp` is used.
*   **`<ASCII_listing_file>.dmp`:** A binary file (JHC `.r4` float array) containing a 2D grid of the chosen parameter (beam number vs. ping number). This file is always created.

## How It Works
1.  **Initialization & Argument Parsing:** Sets up various flags and parameters based on command-line arguments, including the chosen parameter to dump, ranges, and debugging options.
2.  **File Setup:** Opens the input merged file, its associated `.ss_data` file, and optionally `.sectors`, `.SRA_along_atit.r4`, `.SRA_across_atit.r4` files depending on the chosen parameter.
3.  **Data Processing Loop:** Iterates through each ping (profile) in the merged file:
    *   **Swath Filtering:** If `-specific_swath` is used, it skips pings that do not match the specified swath number.
    *   **Profile-Level Parameters (e.g., Roll, Pitch, Heading, SCSTR):** If one of these is chosen, it extracts the relevant value from the `profile` header and writes it to the output dump file. For `-scstr`, it reads sector steering angles.
    *   **Beam-Level Parameters:** If a beam-level parameter is chosen:
        *   Reads all raw beams for the current ping.
        *   **TVG/BSn-BSo Calculation (`-setvg`, `-bsn_o`):** If chosen, it calculates Simrad TVG parameters (`simrad_TVG`) and then derives `BTS` (Bottom Trace Shift) or `BSn-BSo` (Backscatter Normal to Seabed Surface minus original) using `compute_BTS`.
        *   **Parameter Extraction/Calculation:** For each valid beam, it extracts or calculates the `d_chosen_value` based on the selected parameter option (e.g., `reflectivity1_dB`, `slant_range`, `areaVolume`).
        *   **Calibration Manipulation (`-remove_bscal`, `-flip_bscal`):** Applies transformations to the `BScalibration_dB` if specified.
        *   **Sidescan Trace Average (`-sstrc`):** Reads the raw sidescan trace and calculates its linear average, then converts it to dB.
        *   **Along/Across Track SRA (`-altrk`, `-actrk`):** Reads pre-calculated SRA values from external `.r4` files.
    *   **Output to Dump File:** Writes the extracted/calculated parameter values (either profile-level or beam-level) to the `.dmp` file.
    *   **Output to ASCII File (`-ascii_dmp`):** If specified, it also writes ping number, beam number, ping time, beam angle, and the chosen parameter to the ASCII output file.
4.  **Cleanup:** Closes all open files.
