---
layout: default
title: makess
parent: OMG Tools
nav_order: 38
---
# makess

## Description
`makess` is a highly configurable command-line utility for processing raw multibeam sonar data (from various manufacturers like Simrad, ATLAS, RESON, R2Sonic, WASSP, Teledyne MB1) into a sidescan sonar image (GLORIA format). It performs complex transformations, corrections, and normalizations to produce a georeferenced sidescan output, often replacing the built-in sidescan processing of the sonars themselves for greater control and quality.

The tool supports a wide array of options for beam pattern correction, gain adjustment, absorption removal, and handling of various sonar-specific formats and behaviors. It can also output additional diagnostic data like grazing angles and along-track displacements.

## Usage
```bash
makess <input_omg_file(.merged)> <output_sidescan_file(.ss_usually)> [OPTIONS]
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `<input_omg_file(.merged)>` | **Required.** Path to the input OMG-HDCS merged file. | |
| `<output_sidescan_file(.ss_usually)>` | **Required.** Path for the output GLORIA sidescan file. | |

### Sonar Specific Options

**RESON Sonars:**
| Option | Description |
|---|---|
| `-RESON_sidescan` | Use RESON raw sidescan traces. |
| `-RESON_snippet` | Use RESON snippet data. |
| `-RESON_intensity` | Use RESON intensity data. |
| `-RESON_dB_scale <val>` | dB per DN scaling. | `2` |
| `-RESON_dB_shift <val>` | dB shift during calibration. | `0` |
| `-RESON_attenuation <val>` | Attenuation coefficient. | `0` |
| `-RESON_remove_tvg` | Remove TVG applied by the sonar. | |
| `-RESON_skip_pulse` | Skip pulse length correction. | |
| `-RESON_skip_gain` | Skip gain correction. | |
| `-RESON_skip_source_level` | Skip source level correction. | |
| `-RESON_skip_conversion_factor` | Skip conversion factor correction. | |
| `-RESON_kick <val>` | Calibration kickout (1-5). | `0` |
| `-RESON_detvg` | Attempt to de-TVG RESON data. | |
| `-white_holly` | Fix White Holly specific issues. | |

**R2Sonic Sonars:**
| Option | Description |
|---|---|
| `-R2SONIC_truepix` | Use R2Sonic true-pixel backscatter. | |
| `-R2SONIC_snippet` | Use R2Sonic snippet data. | |
| `-R2SONIC_snippet_bp` | Apply RX beam pattern to snippets. | |
| `-R2SONIC_attenuation <val>` | Attenuation coefficient. | `0` |
| `-R2SONIC_skip_all` | Skip all R2Sonic corrections. | |
| `-flatseafloor` | Apply flat seafloor assumption (for R2Sonic truepix). | |

**Teledyne MB1 Sonars:**
| Option | Description |
|---|---|
| `-MB1_skip_all` | Skip all MB1 corrections. | |
| `-MB1_dB_shift <val>` | dB shift during calibration. | `0` |
| `-MB1_attenuation <val>` | Attenuation coefficient. | **Required** |

**WASSP Sonars:**
| Option | Description |
|---|---|
| `-WASSP_skip_all` | Skip all WASSP corrections. | |
| `-WASSP_dB_shift <val>` | dB shift during calibration. | `0` |
| `-WASSP_attenuation <val>` | Attenuation coefficient. | **Required** |

### General Processing Options
| Option | Description | Default |
|---|---|
| `-pixel <size>` | Output sidescan pixel size in meters. | Auto-calculated |
| `-gainup <val>` | Apply a digital gain to the output. | `0` |
| `-DN_Shift <val>` | Digital Number (DN) shift to apply. | `0` |
| `-shift_beam_traces <val>` | Shift beam traces by a given amount. | `0` |
| `-dont_shift_along` | Do not apply along-track shifting. | |
| `-taper <dep_angle>` | Taper the beam pattern response based on depression angle. | |
| `-median` / `-linear` | Apply median or linear filtering (mutually exclusive). | |
| `-replicate_ss <num>` | Replicate each sidescan trace `num` times. | `1` |
| `-hack` | Enable a "hack" for missing sidescan (specific to certain sonar types/data issues). | |
| `-extend_outer_beams` | Extend outer beams to fill gaps. | |
| `-userefl` | Use reflectance values directly. | |
| `-useaibs` | Use AIBS (Angle Independent Backscatter) values. | |
| `-useallss` | Use all sidescan trace data irrespective of flags. | |
| `-dontuseinterp` | Do not use interpolated beam sidescan trace data. | |
| `-normalI <angle>` | Normalize to a specific incidence angle response (in degrees). | `45` |
| `-attenremove` | Remove attenuation applied in real-time. | |
| `-attengain <coeff>` | Apply a new attenuation coefficient. | `0` |
| `-re_atten_ctd <ctd_file>` | Re-calculate attenuation using a CTD file. | |
| `-norm_angles <inner> <outer>` | Custom normalization angles for rolling beam patterns. | `30 70` |
| `-bpscale <factor>` | Apply a scaling factor to the beam pattern. | `1.0` |
| `-AUV_draft` | Ignore WLZ and use pressure depths for draft calculation. | |
| `-draft <val>` | Override calculated draft with a specific value. | Auto-calculated |
| `-yoffset <val>` | Override calculated y-offset with a specific value. | Auto-calculated |
| `-apply_along_bp` | Apply an along-track beam pattern correction. | |
| `-apply_bscal` / `-remove_bscal` / `-flip_bscal` | Apply, remove, or flip beam scaling. | |
| `-show_bscal` / `-show_slapp` / `-show_slapp_orig` / `-show_rxsen` / `-show_sl_rx` | Show various calibration parameters. | |
| `-by_sector` | Process data by sonar sector. | |
| `-only_sector <freq_kHz>` | Process only a specific sonar sector (by center frequency in kHz). | |
| `-multi_sector_bp <file>` | Use a multi-sector beam pattern file. | |
| `-Apply_ACROSS_track_RBP_before_making_ss <file>` | Apply an across-track RBP from a file. | |
| `-SR_ATBP_ignore_within <angle>` | Ignore RBP within a specific sonar-relative incidence angle. | `0` |
| `-Apply_ALONG_track_RBP_before_making_ss <file>` | Apply an along-track RBP from a file. | |
| `-modespec_bp <file> <mode#>` | Use a mode-specific beam pattern file. | |
| `-modeshift <mode#> <DN#>` | Apply a DN shift for a specific mode. | |
| `-pulseshift <pulse_len> <DN#>` | Apply a DN shift for a specific pulse length. | |
| `-beam_sector <file> <neg_bound> <pos_bound>` | Apply beam pattern from file for a given sector range. | |
| `-beam_patt <file>` | Load a custom beam pattern from a file. | |
| `-trace_patt <file>` | Load a custom trace pattern from a file. | |
| `-rolling` | Use rolling beam patterns (requires multiple patterns in the beam pattern file). | |
| `-plusone` | (Used with `-rolling`) Adds an extra rolling pattern. | |
| `-blendBP <file> <inner_angle> <outer_angle>` | Blend beam patterns from a file within specified angles. | |

### Debugging & Output Options
| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-dump_ens` | Dump ensonified area details (R2Sonic). |
| `-debug_grazing` | Enable debugging for grazing angle calculations. |
| `-debug_ensonification` | Enable debugging for ensonification. |
| `-RESON_debug_calib` | Enable debugging for RESON calibration. |
| `-debug_ss` / `-debug_ss2` / `-debug_ss3` | Various levels of sidescan debugging output. |
| `-debug_snippets` | Enable debugging for snippets. |
| `-port_gain <val>` / `-stbd_gain <val>` | Apply specific gain to port/starboard. |
| `-skip_port` / `-skip_stbd` | Skip processing port/starboard sides. |
| `-show_beampatt` | Output the beam pattern. | |
| `-show_colSRA` | Show collinear sonar relative angle. | |
| `-show_atten_shift` / `-show_recalc_atten` | Show attenuation shifts/recalculations. | |
| `-write_grz` | Output a `.grz` file containing grazing angles. | |
| `-write_alongtrack` | Output a `.alt` file containing along-track displacements. | |
| `-dump_beam` / `-dump_range` | Dump beam/range codes. | |

## How It Works
1.  **Read Input & Configuration:** Reads the OMG-HDCS merged file and its associated `.param` and `.sonar_settings` files to determine sonar type and configuration. Parses command-line arguments to set up various processing flags and parameters for sonar type, backscatter source, angle calculation, and corrections.
2.  **Beam Pattern & Corrections Setup:** Loads or generates beam patterns. Applies corrections for gain, TVG, absorption, and sonar-specific artifacts, potentially using external files for detailed corrections.
3.  **Sidescan Generation Loop:** For each ping:
    *   Extracts beam data (depth, across-track, along-track).
    *   Applies configured corrections and transformations (e.g., converting depths to across-track distances, calculating grazing angles).
    *   Resamples the data into a fixed-resolution sidescan trace (512 samples per side).
    *   Applies gain, digital number shifts, tapering, and filtering (median/linear) as specified.
4.  **Output:** Writes the processed sidescan traces to the specified output GLORIA file. Optionally, outputs grazing angles (`.grz`) and along-track displacement (`.alt`) files.

## Output Files
*   `<output_sidescan_file(.ss_usually)>`: The output GLORIA sidescan file.
*   `<output_sidescan_file_prefix>.grz`: File containing grazing angles (if `-write_grz` is used).
*   `<output_sidescan_file_prefix>.alt`: File containing along-track displacements (if `-write_alongtrack` is used).

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.
*   `j_generic_beam_pattern.h`: For beam pattern structures and loading.
*   `j_calibration.h`: For various calibration functions.
*   `grazing_angle.h`: For grazing angle calculation.
*   `ensonification.h`: For ensonification calculations.

## Notes
`makess` provides a highly flexible and powerful framework for generating high-quality sidescan imagery from multibeam sonar data. It allows users to bypass or refine the sonar's internal sidescan processing, providing greater control over the final product. The extensive set of options highlights the complexity and variety of factors that influence quantitative sidescan imagery.