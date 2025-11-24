---
layout: default
title: make_Optech_prof
parent: Optech Tools
nav_order: 114
---
# make_Optech_prof

## Description
`make_Optech_prof` is a utility designed to extract and process individual Optech LASER Bathymetry waveform traces from OMG-HDCS merged files and their associated `.waveform` files. It primarily focuses on processing a specific waveform type (PMT, GAPD, IR, RAMAN) and outputs the detrended waveform traces to a JHC `.r4` (float grid) file.

The tool allows for filtering by geographic area, specific beam number, or azimuth angle, making it useful for detailed inspection and analysis of individual waveform characteristics.

## Usage
```bash
make_Optech_prof <OMG_HDCS_datafile(s)> -out <outfile> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile(s)>` | **Required.** One or more paths to input OMG-HDCS merged files (with associated `.waveform` files). |
| `-out <outfile>` | **Required.** The path for the output JHC `.r4` (float grid) file containing the detrended waveform traces. |

### Waveform Type Selection (Choose one)
| Option | Description |
|---|---|
| `-pmt` | Process PMT (Photo-Multiplier Tube) waveforms. |
| `-gapd` | Process GAPD (Green Avalanche Photodiode) waveforms. |
| `-ir` | Process IR (Infrared) waveforms. |
| `-raman` | Process RAMAN waveforms. |

### Output/Filtering Options
| Option | Description | Default / Example |
|---|---|---|
| `-nadir_beam` | (Not implemented) Intended to dump nadir beam info only. | |
| `-bottom_pick` | (Not implemented) Intended to paint bottom pick points in the trace. | |
| `-beam <val>` | Only dump the waveform trace for this specific beam number. | `50` |
| `-azimuth_angle <val>` | Only dump the waveform trace for beams with this specific azimuth angle. | |
| `-scan_range <first_scan> <last_scan>` | Process profiles (scans) only within this range. | All scans |
| `-area <filename>` | Only process beams within the geographical area defined by the map sheet (`.r4` file). | |
| `-v` | Enable verbose output. | |
| `-merid <val>` | Central meridian for UTM projection (not directly used by this tool but for related geo-processing). | `-63.0` |

## How It Works
1.  **Initialization:** Parses command-line arguments to set various flags, select the waveform type to process (`wave_to_process`), and define output/filtering parameters.
2.  **File Setup:**
    *   Opens input merged files and corresponding `.waveform` files.
    *   Opens the output JHC `.r4` file (`-out`).
3.  **Output Header:** Writes a blank JHC header to the output `.r4` file initially, which will be updated later with actual dimensions.
4.  **Merged File Iteration:** Loops through each input merged file:
    *   Reads the summary header.
    *   **Scan Iteration:** Loops through scans (profiles) from `first_ping` to `last_ping`:
        *   Reads the profile header and raw beams for the current scan.
        *   **Beam Iteration:** Loops through each beam `k` in the current scan that has an `observedDepth`:
            *   Reads raw waveform traces (`WF_trace`) for all available waveform types from the `.waveform` file at `beams[k].offset`.
            *   Clears and populates a `pm_OP_wave` structure (`ALL_waves[wave_to_process]`) with the selected waveform data.
            *   **Waveform Processing (`pm_Process_Wave`):** Calls `pm_Process_Wave` (an external function) to process the selected waveform. This function calculates various parameters and can perform detrending.
            *   **Trace Detrending:** Creates a `detrend_trace` array and populates it with the detrended waveform.
            *   **Filtering by Beam/Azimuth/Area:** Checks if the current beam matches the specified `-beam` number, `-azimuth_angle`, or falls within the `-area`.
            *   **Output Trace:** If all filters pass, it writes the `detrend_trace` (float array) to the output `.r4` file. It also updates the JHC header in the output file to reflect the added trace and seeks back to update the header dynamically.
5.  **Cleanup:** Closes all open files.

## Output Files
*   `<outfile>`: A JHC `.r4` (float grid) file containing the detrended waveform traces.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `array.h`: For `JHC_header` structure and `.r4` file handling.
*   `support.h`: For general utility functions and error handling.
*   `Optech_waveform.h`: For Optech waveform data structures and processing functions (`pm_Process_Wave`).
*   `j_proj.h`: For coordinate projection functions.

## Notes
`make_Optech_prof` is a specialized tool for detailed analysis of individual waveform characteristics, allowing researchers to study how different waveform types behave and respond to the seafloor. The ability to filter by beam, azimuth, or geographic area allows for very targeted investigations. The tool always outputs to a JHC `.r4` file, making it compatible with other grid processing and visualization tools. The `-nadir_beam` and `-bottom_pick` options are listed but not implemented.