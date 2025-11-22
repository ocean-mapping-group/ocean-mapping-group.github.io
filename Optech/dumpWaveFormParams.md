---
layout: default
title: dumpWaveFormParams
parent: Optech Tools
nav_order: 111
---
# dumpWaveFormParams

## Description
`dumpWaveFormParams` is a utility designed to extract and analyze waveform parameters from Optech SHOALS LASER Bathymetry data, which is stored in OMG-HDCS merged files and associated `.waveform` files. It processes waveforms to derive various parameters (e.g., depths, widths, slopes, K-values) and outputs them as ASCII longitude, latitude, and parameter triplets.

The tool supports different waveform types (PMT, GAPD, IR, RAMAN) and offers numerous options for filtering, parameter selection, and specialized output formats.

## Usage
```bash
dumpWaveFormParams <OMG_HDCS_datafile(s)> -out <ASCII_listing_file> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile(s)>` | **Required.** One or more paths to input OMG-HDCS merged files (with associated `.waveform` files). |
| `-out <ASCII_listing_file>` | **Required.** The path for the ASCII output file. |

### Waveform Type Selection (Choose one)
| Option | Description |
|---|---|
| `-pmt` | Process PMT (Photo-Multiplier Tube) waveforms. |
| `-gapd` | Process GAPD (Green Avalanche Photodiode) waveforms. |
| `-ir` | Process IR (Infrared) waveforms. |
| `-raman` | Process RAMAN waveforms (used primarily for land/water returns if `-no_land` is used). |

### Parameter Output Selection (Choose one or more)
| Option | Description |
|---|---|
| `-nadir_beam` | Output nadir beam info only (depths, widths, slopes, K-values). |
| `-height_only` | Output only `i_top_bot_d` (a depth/height parameter). |
| `-width_only` | Output only `width_bot` (waveform width). |
| `-k_only` | Output only the K-value (a water column turbidity parameter). |
| `-lin_height` | Output linear height (`height_lin`). |
| `-top_bot_only` | Output only `i_top_bot` (top-of-bottom value). |
| `-setback` | Output a ratio related to the waveform setback. |
| `-depths` | Output various depths (pimDepth_PMT/GAPD, opaqueDepth_PMT/GAPD, extinctionDepth_PMT/GAPD) based on wave type. |
| `-depth_ratio` | Output depth difference ratio between GAPD and PMT depths. |
| `-opaque` / `-extinct` | Output opaque or extinction depths. |
| `-pim` | Output `pimDepth` (Pim's depth). |
| `-returntype` | Output a classification of return type (WEAK, DEEP_WATER). |
| `-D_E_method` | Use Dijkstra and Elstons' (2004) method for reflectance. |
| `-combo` | Output a combination of depths (uses `pimDepth`, `opaqueDepth`, `extinctionDepth`). |
| `-pseudo_reflectance` | Output pseudo-reflectance `R` (related to `i_top_bot` and depth). |
| `-hdk` | Output `i_top_bot_d`, depth-121, and `K * -1.0`. |

### Filtering & Range Options
| Option | Description |
|---|---|
| `-valid_only` | Only output data that `pm_Process_Wave` marks as valid (not `9`). |
| `-check_flag` | Only output data that `pm_Process_Wave` marks as valid (`9`). |
| `-no_land` | Only process water returns (filters out land returns based on RAMAN waveform processing). |
| `-surface_only` | Only output surface return information. |
| `-area <filename>` | Only process beams within the geographical area defined by the map sheet (`.r4` file). |
| `-scan_range <first_scan> <last_scan>` | Process profiles (scans) only within this range. | All scans |
| `-trace <depth>` | Dumps ASCII trace data for waveforms at a specific depth. |

### Other Options
| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-merid <val>` | Central meridian for UTM projection (not directly used by this tool but often needed for related geo-processing). | `-63.0` |
| `-antoine` | Option to dump ASCII trace data in a specific format for Antoine. |
| `-k_prof` | Output `K * -1.0` vs. `depth - 121` for nadir beam. |

## How It Works
1.  **Initialization:** Parses command-line arguments to set various flags, select the waveform type to process, and define output parameters.
2.  **File Setup:** Opens input merged files, corresponding `.waveform` files, and the output ASCII file (`-out`).
3.  **Summary Header Reading:** Reads the summary header from the merged file.
4.  **Scan Iteration:** Loops through each scan (profile) in the merged file (from `first_scan` to `last_scan`):
    *   Reads the profile header and raw beams.
    *   **Waveform Data Extraction:** For each beam `k` that has `observedDepth`:
        *   Locates the beam's geographic position (lat/lon).
        *   Retrieves `depth` from `beams[k].observedDepth`.
        *   Seeks to the beam's waveform data in the `.waveform` file using `beams[k].offset` and reads the raw `WF_trace` for all available waveform types (PMT, GAPD, IR, RAMAN).
        *   **Waveform Processing (`pm_Process_Wave`):** Calls `pm_Process_Wave` (an external function) to process the selected waveform (`wave_to_process`) and also the RAMAN waveform (if `-no_land` is active). This function populates the `ALL_waves` structure with derived parameters like `i_top_bot`, `K`, `width_bot`, `valid`, `return_type`, etc.
        *   **Land/Water Filtering (`-no_land`):** If `-no_land` is active, it checks if `ALL_waves[PM_WAVE_RAMAN].i_start_sur > 55`. If this condition is met (indicating a water return), it proceeds to output.
        *   **Output Formatting:** Based on the chosen output parameter flags (`-nadir_beam`, `-height_only`, `-k_only`, etc.), it formats and prints the derived waveform parameters (along with lat/lon and depth) to the output ASCII file. This can include raw trace data if `-trace` or `-antoine` is used.
5.  **Cleanup:** Closes all open files.
```