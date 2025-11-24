---
layout: default
title: processSHOALSdepths
parent: Optech Tools
nav_order: 118
---
# processSHOALSdepths

## Description
`processSHOALSdepths` is a specialized utility designed to process Optech SHOALS LASER Bathymetry waveforms and derive various depth types (PIM depth, opaque depth, extinction depth). These derived depths, along with a "depth-to-grid" flag indicating the recommended depth to use, are stored back into the `OMG_HDCS_beam` structure of the merged file.

The tool aims to provide a more refined depth estimate by analyzing the full waveform, accounting for different water column conditions (e.g., clear, turbid, deep water) and the characteristics of PMT (Photo-Multiplier Tube) and GAPD (Green Avalanche Photodiode) channels.

## Usage
```bash
processSHOALSdepths <OMG_HDCS_datafile(s)> [-v] [-area <array.file>] [-scan_range <first> <last>]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile(s)>` | **Required.** One or more paths to input OMG-HDCS merged files (with associated `.waveform` files). These files are modified in place. |
| `-v` | Enable verbose output. |
| `-area <array.file>` | Only process beams within the geographical area defined by the map sheet (`.r4` file). |
| `-scan_range <first_scan> <last_scan>` | Process profiles (scans) only within this range. | All scans |

## How It Works
1.  **Initialization:** Initializes ratio tracking structures (`PMT_ratio`, `GAPD_ratio`), depth structures (`PMT_depths`, `GAPD_depths`), and defines a `PMT_GAPD_depth_diff_ratio`.
2.  **File Opening:** Opens input merged files and corresponding `.waveform` files.
3.  **Summary Header Reading:** Reads the summary header from the merged file.
4.  **Scan Iteration:** Loops through each scan (profile) in the merged file (from `first_scan` to `last_scan`):
    *   Reads the profile header and raw beams.
    *   **Waveform Data Extraction:** For each beam `k` that has `observedDepth`:
        *   Locates the beam's geographic position (lat/lon).
        *   Extracts `ellipsoidal_height` from `beams[k].observedDepth`.
        *   Seeks to the beam's waveform data in the `.waveform` file and reads the raw `WF_trace` for PMT, GAPD, IR, and RAMAN channels.
        *   **Waveform Processing (`pm_Process_Wave`, `classify_Wave`):** Calls `pm_Process_Wave` and `classify_Wave` (external functions) for both PMT and GAPD waveforms. This analyzes the waveform shape to derive parameters like `s_50_bot` (50% bottom start), `s_end_bot` (bottom end), `s_start_sur` (surface start), `s_sink` (sink depth), `s_extinct` (extinction depth), and `valid` (waveform validity flag), and `return_type` (WEAK, DEEP_WATER).
        *   **Land/Water Detection:** Uses the RAMAN waveform's `i_start_sur` to determine if the return is from water or land. Only water returns are processed further.
        *   **Setback Ratio Calculation:** Calculates a dynamic `setback_ratio` for both PMT and GAPD channels using a moving buffer of `BUF_SIZE` values of `s_50_bot / s_end_bot`. This ratio is used in deriving opaque and extinction depths.
        *   **Depth Derivation:** Calculates `pimDepth`, `opaqueDepth`, and `extinctionDepth` for both PMT and GAPD channels based on the processed waveform parameters and the `setback_ratio`. These values are scaled and stored in the `beams[k]` structure. The `PMT_GAPD_depth_diff_ratio` is applied to PMT-derived depths.
        *   **"Depth-to-Grid" Flag:** Determines the optimal depth to use for gridding (`depth_to_grid`) based on the validity and return type of PMT and GAPD waveforms. This flag (`1` to `6` for various depth types, `7` for land return) is stored in `beams[k].prim_depth_conf`.
        *   Updates `beams[k].status` to `0` for valid water returns, and `7` for land returns.
5.  **Write Back:** The modified `beams` and `profile` (with updated depth fields and flags) are written back to the merged file.

## Output Files
The input merged files are modified in-place, with updated `OMG_HDCS_beam` structures containing derived depth types and `prim_depth_conf` flags.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.
*   `Optech_waveform.h`: For Optech waveform data structures and processing functions (`pm_Process_Wave`, `classify_Wave`).

## Notes
`processSHOALSdepths` performs complex waveform analysis to extract more accurate and robust depth estimates than simple first-arrival detection. By considering multiple depth types (PIM, opaque, extinction) and classifying returns (land/water, weak/deep), it significantly enhances the quality and interpretability of SHOALS data. The derived `depth-to-grid` flag provides an automated recommendation for which depth to use in subsequent gridding operations. The tool modifies files in-place, so backups are recommended.