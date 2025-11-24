---
layout: default
title: newGetBP
parent: OMG Tools
nav_order: 44
---
# newGetBP

## Description
`newGetBP` is a tool designed to analyze multibeam sonar data and derive average beam patterns. It processes raw merged files, along with associated sidescan, parameter, and sector files, to calculate backscatter intensity as a function of incidence angle. This information is crucial for calibrating multibeam systems and understanding seabed characteristics.

The tool can handle various input data types (raw sidescan traces, reflectivity, calibrated backscatter, or specific KMALL parameters), apply numerous corrections (e.g., attenuation, TVG, declination), and filter data based on depth, angle, or spatial masks. It supports outputting beam patterns for individual modes/sectors or a collapsed average, and can generate diagnostic scatterplots or detailed attribute files.

## Usage
```bash
newGetBP <file_prefix> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<file_prefix>` | **Required.** The base name of the merged file (e.g., `line`). The tool will look for `line.merged`, `line.ss_data`, `line.param`, etc. Multiple prefixes can be provided. |

### Input Data Type
| Option | Description |
|---|---|
| `-trace` | (Default) Use raw sidescan traces. |
| `-refl` | Use reflectivity values. |
| `-calb` | Use calibrated backscatter values (historic). |
| `-removeBSnBSo` | Remove BSnBSo (backscatter normal to the seabed surface) and TVG (Time-Varying Gain) from `ref_1` or `ref_2` (KMALL). Optionally, `-recalc_NormalIncid` can be used. |
| `-ref_1` | Use KMALL `reflectivity1_dB`. |
| `-ref_2` | Use KMALL `reflectivity2_dB`. |
| `-rxsen` | Use KMALL `receiverSensitivityApplied_dB`. |
| `-txsl` | Use KMALL `sourceLevelApplied_dB`. |
| `-kmtvg` | Use KMALL `TVG_dB`. |
| `-tx+rx` | Use sum of KMALL `sourceLevelApplied_dB` and `receiverSensitivityApplied_dB`. |
| `-ref1-ref2` | Use difference between KMALL `reflectivity1_dB` and `reflectivity2_dB`. |
| `-bscal` | Use KMALL `BScalibration_dB`. |

### Angle Calculation
| Option | Description |
|---|---|
| `-use_real_grazing` | Uses pre-calculated grazing angles from an external file (`.GRA` file must be provided). |
| `-read_GRA <ext>` | Reads grazing angles from a `.GRA.<ext>.r4` file. Requires `use_real_grazing`. |
| `-read_SRA <ext>` | Reads sonar-relative angles from a `.SRA.<ext>.r4` file. |
| `-read_VRA <ext>` | Reads vertically-referenced angles from a `.VRA.<ext>.r4` file. |
| `-use_depression_angle` | Uses depression angle as the reference for beam pattern. |
| `-relative` | Calculate angles relative to the sonar (default is relative to vertical). |
| `-roll_reversed` | Reverse the sign of the roll for angle calculations. |
| `-refract` | Use `.depression` file (from `newMergeAtt`) to consider refraction in grazing angle calculation. |
| `-use_ADH_GRZ <pings> <beams>` | Calculates grazing angle using surrounding `pings` and `beams` (ADH method). |
| `-separate_port_stbd_grazing` | Separates port and starboard grazing angle by looking at the steering angle. |

### Data Filtering & Selection
| Option | Description | Default |
|---|---|
| `-onlymode <mode_ID>` | Process data only for a specific mode ID. | |
| `-onlyfreq <frequency_kHz>` | Process data only for a specific center frequency (in kHz). | |
| `-by_mode` | Keep beam patterns separated by acquisition mode. | |
| `-by_sector` | Keep beam patterns separated by transmit sector (for EM systems). | |
| `-edit_sector_edges` | Attempt to edit noisy sector edges. | |
| `-only_bandwidth <kHz>` | Process data only for a specific signal bandwidth (in kHz). | |
| `-first <ping>` | Process data only from this ping number. | |
| `-last <ping>` | Process data only up to this ping number. | |
| `-depth_range <min_m> <max_m>` | Only use data with water depth within this range. | |
| `-vertical_range <min_deg> <max_deg>` | Only use data with vertical incidence angles within this range. | |
| `-relative_range <min_deg> <max_deg>` | Only use data with sonar-relative incidence angles within this range. | |
| `-valid_ucDN <low> <high>` | Only use unsigned 8-bit DN values within this range. | |
| `-area <file.r4>` / `-mask <file.mask>` | Only process data within a geographic area. | |
| `-cyclops` | Special handling for EM3000D with one head off. | |
| `-fill_bin_gaps` | Fills gaps in angle bins by distributing contribution from wide beams. | |

### Corrections & Adjustments
| Option | Description | Default |
|---|---|---|
| `-attenremove` | Remove attenuation from the value in the profile header. | |
| `-attengain <val>` | Add attenuation compensation with a new coefficient (dB/km). | |
| `-re_atten_ctd <CTD_File(s).svp>` | Apply gain corrections from a provided CTD (SVP) profile (Rodrigo thesis). Multiple CTD files can be provided. | |
| `-use_deSRA_deTVG` / `-use_deVRA_deTVG` / `-use_deTVG` | Remove various forms of TVG (Time Varying Gain) or SRA (Sonar Relative Angle) related gains. | |
| `-DN_Shift <val>` | Shift DN values (applied negatively). | `0` |
| `-draft <val>` / `-AUV_draft` | Specify draft or use AUV draft calculation (which may ignore WLZ). | Auto-calculated |
| `-ymount <val>` | Override the Y-mount offset. | `0.0` |
| `-lambertian_reference` | Calculate residuals with respect to a Lambertian roll-off model. | |
| `-external_ARC_reference <file>` | Calculate residuals with respect to an externally estimated Angle Response Curve (ARC). | |
| `-SRbp <file>` | Sonar relative beam pattern to be removed before calculating apparent residuals. | |
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

### Output & Debugging
| Option | Description |
|---|---|
| `-out <outname>` | Specify the base name for output files. | `beampatt` |
| `-has_ext` | Indicates that the input file prefix includes the extension. | |
| `-log` | Average logarithmic intensities (default is linear). | |
| `-dump_ascii_stack` | Dump ASCII stacks of beam patterns. | |
| `-do_attrib <interval>` | Dump attribute files (`.AR_attribs`) every `<interval>` pings. | |
| `-scatterplot` | Dump data for a scatterplot (`beampatt.scatterplot`). | |
| `-grab_centre_params` | Output parameters of the center ping in a small window to `centre_ping.params`. | |
| `-v` | Enable verbose output. | |

## How It Works
1.  **Input Reading & Configuration:** Reads merged files, parameter files, and optionally sidescan data, sector definitions, and external angle files. It configures processing based on the multitude of command-line arguments.
2.  **Angle Calculation:** For each beam in each ping, it calculates various incidence angles (vertical, sonar-relative, grazing) using either measured values from files or geometrical calculations, potentially incorporating motion data and draft.
3.  **Backscatter Extraction & Correction:** Extracts backscatter values from the specified source (raw traces, reflectivity, KMALL parameters). Applies corrections for attenuation, TVG, and other sonar-specific adjustments. If SRBP extraction is active, it applies existing RBP corrections.
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
*   `<outname>.AR_attribs`: Attribute files (if `-do_attrib` is used).

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `array.h`: For `JHC_header` structure.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.
*   `j_generic_beam_pattern.h`: For beam pattern structures and loading/dumping.
*   `j_get_launch_angle.h`: For launch angle calculations.
*   `j_calibration.h`: For calibration functions (e.g., `ADH_calibrate_BS`).
*   `grazing_angle.h`: For grazing angle calculation.
*   `ensonification.h`: For ensonification calculations.

## Notes
`newGetBP` is a cornerstone tool for sonar calibration and understanding the acoustic interaction with the seafloor. Its extensive options cater to a wide range of sonar systems and processing scenarios, allowing for both basic angular response analysis and advanced SRBP extraction. Careful selection of filtering and correction parameters is crucial for obtaining accurate and meaningful beam patterns. The tool provides a robust framework for developing and validating backscatter models.