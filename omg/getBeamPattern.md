---
layout: default
title: getBeamPattern
parent: OMG Tools
nav_order: 103
---
# getBeamPattern

## Description
`getBeamPattern` is a comprehensive utility for deriving the average angular variation in backscatter (the beam pattern) from multibeam sonar data. It supports various sonar types (especially Simrad EM series) and allows for detailed analysis of backscatter data (sidescan traces, reflectivity, calibrated backscatter).

The tool processes merged files, applies numerous corrections, filters data based on user-defined criteria (e.g., depth, angle, geographic area), and outputs the resulting beam pattern. It also includes advanced features for extracting across-track and along-track Sonar Relative Beam Patterns (SRBP).

## Usage
```bash
getBeamPattern <file_prefix> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<file_prefix>` | **Required.** The base name of the merged file (e.g., `line`). The tool will look for `line.merged`, `line.ss_data`, `line.param`, etc. Multiple prefixes can be provided. |

### Input Data & Mode
| Option | Description |
|---|---|
| `-refl` | Use reflectivity values from the merged file. |
| `-calb` | Use calibrated backscatter values (historic). |
| `-log` | Averages logarithmic intensities (default is linear). |
| `-useallss` | Use all sidescan trace data regardless of status flags. |
| `-onlymode <mode_ID>` | Process data only for a specific mode ID. |
| `-by_mode` | Keep beam patterns separated by acquisition mode. |
| `-by_sector` | Keep beam patterns separated by transmit sector (for EM systems). |
| `-only_bandwidth <kHz>` | Process data only for a specific signal bandwidth. |

### Angle Calculation
| Option | Description |
|---|---|
| `-use_real_grazing` | Use pre-calculated grazing angles from an external file (`.GRA` file must be provided). |
| `-read_GRA <ext>` | Reads grazing angles from a `.GRA.<ext>.r4` file. Requires `use_real_grazing`. |
| `-use_depression_angle` | Use depression angle as the reference. |
| `-relative` | Calculate angles relative to the sonar. |
| `-roll_reversed` | Reverse the sign of the roll for angle calculations. |
| `-use_ADH_GRZ <pings> <beams>` | Use ADH's grazing angle calculations based on `pings` along-track and `beams` across-track. |
| `-separate_port_stbd_grazing` | Differentiates port/starboard grazing angles based on steering angle. |

### Corrections & Adjustments
| Option | Description | Default |
|---|---|
| `-attenremove` | Remove attenuation from value in profile header. | |
| `-attengain <val>` | Add attenuation compensation with new coefficient (dB/km). | |
| `-re_atten_ctd <CTD_File(s).svp>` | Apply gain corrections from a CTD profile. | |
| `-use_deSRA_deTVG` / `-use_deVRA_deTVG` / `-use_deTVG` | Remove various forms of TVG or SRA related gains. | |
| `-DN_Shift <val>` | Digital Number (DN) shift. | `0` |
| `-draft <val>` / `-AUV_draft` | Specify draft or use AUV draft calculation. | Auto-calculated |
| `-ymount <val>` | Override the Y-mount offset. | |
| `-lambertian_reference` | Calculate residuals with respect to a Lambertian roll-off model. | |
| `-external_ARC_reference <filenm>` | Calculate residuals with respect to an externally estimated ARC. | |
| `-SRbp <filenm>` | Sonar relative beam pattern to be removed. | |
| `-SR_ignore_within <deg>` | Don't use SR beam pattern within that sonar-relative incidence angle. | `0.0` |

### SRBP Extraction (ADH's functionality)
| Option | Description |
|---|---|
| `-Extract_Across_SRBP` | Extracts across-track sonar relative beam pattern. |
| `-Extract_Along_SRBP` | Extracts along-track sonar relative beam pattern (requires across-track RBP). |
| `-Apply_extracted_Across_SRBP_before_extracting_Along_SRBP <file>` | Apply extracted across-track RBP before extracting along-track RBP. |
| `-Apply_extracted_Across_SRBP_before_extracting_ARC <file>` | Apply extracted across-track RBP before extracting ARC. |
| `-Apply_extracted_Along_SRBP_before_extracting_ARC <file>` | Apply extracted along-track RBP before extracting ARC. |
| `-get_STDVs` | Computes and propagates STDVs of BS data. |
| `-do_Kalman` | Uses Kalman filtering on BS data for RBP extraction. |
| `-do_Median_filter <len>` | Uses Median filtering on BS data, with filter length `len`. |
| `-use_rayleigh` | Use Rayleigh distribution for outlier removal (with `-get_STDVs`). |
| `-use_sigma_level <val>` | Use given sigma value for outlier removal (with `-get_STDVs`). |
| `-write_stats_files` | Writes statistics files for debugging. |
| `-do_polynomial_fit` | Fits a polynomial to the central sector. |
| `-polynomial_fit_dof <val>` | Degree of freedom for polynomial fit (3 or 5). |
| `-polynomial_fit_range_from_CPA <val>` | Range from CPA for polynomial fit. |
| `-use_max_sample_SRA_as_reference_for_stacking` | Uses SRA with maximum sample as stacking reference. |
| `-master_reference_SRA <val>` | Master reference SRA for adjusting across-track RBP. |
| `-master_reference_sector <val>` | Master reference sector for adjusting across-track RBP. |

### Data Filtering & Selection
| Option | Description | Default |
|---|---|
| `-valid_ucDN <low> <high>` | Only use unsigned 8-bit DN values within this range. | |
| `-depth_range <min_m> <max_m>` | Only use data with water depth within this range. | |
| `-vertical_range <min_deg> <max_deg>` | Only use data with vertical incidence angles within this range. | |
| `-relative_range <min_deg> <max_deg>` | Only use data with sonar-relative incidence angles within this range. | |
| `-first <ping_num>` / `-last <ping_num>` | Process data only within a specific ping range. | |
| `-area <file.r4>` / `-mask <file.mask>` | Only process data within a geographic area. | |
| `-cyclops` | Special handling for EM3000D with one head off. | |
| `-fill_bin_gaps` | Fills gaps in angle bins by distributing contribution from wide beams. | |

### Output & Debugging
| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-scatterplot` | Dumps data for a scatterplot (`beampatt.scatterplot`). |
| `-out <outname>` | Specify the base name for output files. | `beampatt` |
| `-has_ext` | Indicates that the input file prefix includes the extension. |

## How It Works
1.  **Input Reading & Configuration:** Reads merged files, parameter files, and optionally sidescan data, sector definitions, CTD profiles, DTMs, and various RBP files. It configures processing based on the multitude of command-line arguments.
2.  **Angle Calculation:** For each beam in each ping, it calculates various incidence angles (vertical, sonar-relative, grazing) using either measured values from files or geometrical calculations, potentially incorporating motion data and draft.
3.  **Backscatter Extraction & Correction:** Extracts backscatter values from the specified source (raw traces, reflectivity). Applies corrections for attenuation, TVG, and sonar-specific artifacts. If SRBP extraction is active, it applies existing RBP corrections.
4.  **Beam Pattern Accumulation:**
    *   For each valid beam, its backscatter value is binned according to its incidence angle.
    *   Values are accumulated either linearly or logarithmically, and counts are maintained for averaging.
    *   Data can be separated by mode (`-by_mode`) or by transmit sector (`-by_sector`), allowing for distinct beam patterns for different sonar operating conditions.
    *   Advanced methods like Kalman or Median filtering can be applied during accumulation.
5.  **SRBP Extraction (ADH's functionality):** If `Extract_Across_SRBP` or `Extract_Along_SRBP` is active, the tool uses sophisticated algorithms to extract across-track and/or along-track SRBPs, including:
    *   Processing intensity data for outlier removal (`-get_STDVs`, `-use_rayleigh`, `-use_sigma_level`).
    *   Polynomial fitting (`-do_polynomial_fit`).
    *   Stacking and averaging SRBP sub-functions.
    *   Referencing to a master SRA and sector.
6.  **Normalization & Averaging:**
    *   After processing all selected pings, the accumulated backscatter values in each angle bin are averaged.
    *   A "mid-signal" level is calculated (either per mode/sector or globally) for normalization purposes.
    *   Backscatter values are then normalized relative to this mid-signal level, often expressed as a difference in dB.
7.  **Output:**
    *   Outputs a beam pattern file (e.g., `beampatt` or specified by `-out`) in an ASCII format, showing angle, intensity, difference from mid-signal, and count for each bin.
    *   Can optionally generate `beampatt.scatterplot` for visualization.
    *   If SRBP extraction is active, it outputs specialized RBP files (e.g., `.across_track_RBP`, `.along_track_RBP`) and debug statistics.
    *   A custom ASCII plotfile for Gnuplot (`ARC_for_plot`) is generated.
8.  **Cleanup:** Frees allocated memory and closes all open files.

## Output Files
*   `<outname>`: An ASCII file containing the derived beam pattern.
*   `<outname>.scatterplot`: An ASCII file for scatterplot visualization (if `-scatterplot` is used).
*   `<outname>.ARC_for_plot`: A custom ASCII plotfile for Gnuplot.
*   Specialized RBP files (e.g., `.across_track_RBP`, `.along_track_RBP`) if SRBP extraction is active.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `array.h`: For `JHC_header` structure.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.
*   `j_generic_beam_pattern.h`: For beam pattern structures and loading/dumping.
*   `j_get_launch_angle.h`: For launch angle calculations.
*   `j_calibration.h`: For calibration functions (e.g., `ADH_calibrate_BS`).

## Notes
`getBeamPattern` is a cornerstone tool for sonar calibration and understanding the acoustic interaction with the seafloor. Its extensive options cater to a wide range of sonar systems and processing scenarios, allowing for both basic angular response analysis and advanced SRBP extraction. Careful selection of filtering and correction parameters is crucial for obtaining accurate and meaningful beam patterns. The tool provides a robust framework for developing and validating backscatter models.