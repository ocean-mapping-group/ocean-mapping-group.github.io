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
| `-refl` | Use 8-bit reflectivity values. |
| `-calb` | Use 8-bit calibrated backscatter values (historic). |
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
| Option | Description |
|---|---|
| `-onlymode <mode_ID>` | Process data only for a specific mode ID. |
| `-onlyfreq <frequency_kHz>` | Process data only for a specific center frequency (in kHz). |
| `-by_mode` | Keep beam patterns separated by acquisition mode. |
| `-by_sector` | Keep beam patterns separated by transmit sector (for EM systems). |
| `-edit_sector_edges` | Attempt to edit noisy sector edges. |
| `-only_bandwidth <kHz>` | Process data only for a specific signal bandwidth (in kHz). |
| `-first <ping>` / `-last <ping>` | Process data only within a specific ping range. |
| `-depth_range <min_m> <max_m>` | Only use data with water depth within this range. |
| `-vertical_range <min_deg> <max_deg>` | Only use data with vertical incidence angles within this range. |
| `-relative_range <min_deg> <max_deg>` | Only use data with sonar-relative incidence angles within this range. |
| `-valid_ucDN <low> <high>` | Only use unsigned 8-bit DN values within this range. |
| `-area <file.r4>` / `-mask <file.mask>` / `-maskval <val>` | Only process data within a geographical area defined by an `.r4` grid and optionally filtered by a mask file with a specific value. |
| `-cyclops` | Special handling for EM3000D with one head off. |

### Corrections & Adjustments
| Option | Description |
|---|---|
| `-attenremove` | Remove attenuation from the value in the profile header. |
| `-attengain <val>` | Add attenuation compensation with a new coefficient (dB/km). |
| `-re_atten_ctd <CTD_File(s).svp>` | Apply gain corrections from a provided CTD (SVP) profile (Rodrigo thesis). Multiple CTD files can be provided. |
| `-use_deSRA_deTVG` / `-use_deVRA_deTVG` / `-use_deTVG` | Remove various forms of TVG (Time Varying Gain) or SRA (Sonar Relative Angle) related gains. |
| `-DN_Shift <val>` | Shift DN values (applied negatively). | `0` |
| `-draft <val>` / `-AUV_draft` | Specify draft or use AUV draft calculation (which may ignore WLZ). | Auto-calculated |
| `-ymount <val>` | Override the Y-mount offset. | `0.0` |
| `-lambertian_reference` | Calculate residuals with respect to a Lambertian roll-off model. |
| `-external_ARC_reference <file>` | Calculate residuals with respect to an externally estimated Angle Response Curve (ARC). |
| `-SRbp <file>` | Sonar relative beam pattern to be removed before calculating apparent residuals. |
| `-SR_ignore_within <deg>` | Don't use SR beam pattern within that sonar-relative incidence angle. | `0.0` |

### Output & Debugging
| Option | Description |
|---|---|
| `-out <outname>` | Specify the base name for output files. | `beampatt` |
| `-has_ext` | Indicates that the input file prefix includes the extension. |
| `-log` | Average logarithmic intensities (default is linear). |
| `-dump_ascii_stack` | Dump ASCII stacks of beam patterns. |
| `-do_attrib <interval>` | Dump attribute files (`.AR_attribs`) every `<interval>` pings. |
| `-scatterplot` | Dump data for a scatterplot (`beampatt.scatterplot`). |
| `-grab_centre_params` | Output parameters of the center ping in a small window to `centre_ping.params`. |
| `-v` | Enable verbose output. |

## How It Works
1.  **File Input & Configuration:** Reads merged files, parameter files, and optionally sidescan data, sector definitions, and external angle files. It configures processing based on the multitude of command-line options.
2.  **Angle Calculation:** For each beam in each ping, it calculates various incidence angles (vertical, sonar-relative, grazing) using either measured values from files or geometrical calculations, potentially incorporating motion data and draft.
3.  **Backscatter Extraction & Correction:** Extracts backscatter values from the specified source (raw traces, reflectivity, KMALL parameters). Applies corrections for attenuation, TVG, and other sonar-specific adjustments.
4.  **Beam Pattern Accumulation:**
    *   For each valid beam, its backscatter value is binned according to its incidence angle.
    *   Values are accumulated either linearly or logarithmically, and counts are maintained for averaging.
    *   Data can be separated by mode (`-by_mode`) or by transmit sector (`-by_sector`), allowing for distinct beam patterns for different sonar operating conditions.
5.  **Normalization & Averaging:**
    *   After processing all selected pings, the accumulated backscatter values in each angle bin are averaged.
    *   A "mid-signal" level is calculated (either per mode/sector or globally) for normalization purposes.
    *   Backscatter values are then normalized relative to this mid-signal level, often expressed as a difference in dB.
6.  **Output:**
    *   Outputs a beam pattern file (e.g., `beampatt` or specified by `-out`) in an ASCII format, showing angle, intensity, difference from mid-signal, and count for each bin.
    *   Can optionally generate `beampatt.scatterplot` for visualization, and `.AR_attribs` files containing detailed attributes for stacked intervals.
    *   Can also dump combined multi-sector beam patterns in a format usable by `multiMode2Calib`.
