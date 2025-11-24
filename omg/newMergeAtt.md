---
layout: default
title: newMergeAtt
parent: OMG Tools
nav_order: 45
---
# newMergeAtt

## Description
`newMergeAtt` is a powerful and complex utility for processing OMG-HDCS merged multibeam sonar files. Its primary function is to re-raytrace sonar soundings using external sound velocity profiles (SVPs) and precise attitude data, thereby correcting for refraction and motion. It updates the depth, across-track, and along-track values of each beam, ensuring accurate bathymetry.

The tool incorporates advanced features like dynamic SVP selection based on time or distance, detailed motion compensation (including induced heave and crosstalk correction), and a high degree of configurability for sonar parameters and debugging.

## Usage
```bash
newMergeAtt -in <input.merged> -svp svp/*.svp [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `-in <input.merged>` | **Required.** The path to the input OMG-HDCS merged file. This file will be modified in place unless `-test` is used. Multiple input files can be specified. |
| `-svp svp/*.svp` | **Required (unless `-skip_raytrace` or `-just_merge` is used).** Specifies one or more Sound Velocity Profile (SVP) files to be used for raytracing. |
| `-svp_list <file>` | Provides a list file containing paths to SVP files. |

### Raytracing Options
| Option | Description | Default |
|---|---|
| `-wc_bin <val>` | Force watercolumn resampling bin size (in meters). Default is determined by depth range. | Auto-calculated |
| `-skip_raytrace` | Performs an isovelocity raytrace using the velocity in the profile header, skipping full raytracing. | |
| `-velocity <val>` | Specify a constant velocity (m/s) for isovelocity raytrace, overriding the profile header or if absent. | |
| `-just_raytrace` | Trusts depression and azimuth angles as they exist in beam structures and only performs raytracing. | |
| `-cg` | Use the Constant Gradient method for raytracing. | |
| `-check_cast_depth` | Only raytrace soundings shallower than the current cast's maximum depth. | |
| `-quick` | Try the new quicktrace routine. | |
| `-travis` | Use the new sounding reduction algorithm. | |

### Surface Sound Speed Options
| Option | Description |
|---|---|
| `-force_surface_ss` | Force the use of surface sound speed in barrel arrays (e.g., Reson 8101). | |
| `-ignore_surface_ss` | Ignore the use of surface sound speed. | |
| `-repoint <val>` | Repoint beam steering angles using a specified velocity. | |
| `-repoint_from_wc` | Repoint beam steering angles using velocity found in the water column. | |
| `-surf_ss_file` | Force lookup of surface sound speed from a `.surf_ss` file. | |

### Heave Options
| Option | Description |
|---|---|
| `-invert_heave` | Invert the sign of heave data (e.g., for XTF data). | |
| `-ignore_heave` | Do not apply heave correction (does not include induced heave). | |
| `-induce_heave` | Add induced heave based on lever arms between heave sensor and sounder. | |
| `-dont_heave_in_wc` | Do not allow the transducer to heave in the water column during raytrace. | |
| `-migrate_heave` | Migrate heave back to the Reference Point (RP). | |
| `-max_atti_time_gap <sec>` | Maximum time over which to interpolate attitude data. | `1` |
| `-delayed_heave <file>` | Specify an asynchronously logged delayed heave file (must be in `.orientation` format). | |
| `-use_reported_tx_draft` | Use the stored transmit draft instead of WLZ (essential for AUVs). | |

### Vessel Installation Options
| Option | Description |
|---|---|
| `-ignore_param` | Ignore the `.param` file (effectively zeroes all offsets for debugging). | |
| `-alternate_param <file>` | Specify an alternate vessel parameter file. | |
| `-extra_roll <val>` / `-extra_pitch <val>` / `-extra_heading <val>` | Add additional roll, pitch, or heading offsets. | |
| `-extra_x <val>` / `-extra_y <val>` / `-extra_z <val>` | Add additional sonar X, Y, or Z offsets. | |
| `-extra_tx_steer <val>` / `-extra_rx_steer <val>` | Add additional transmit or receiver steering angles. | |
| `-flip_tx_steer` / `-flip_rx_steer` | Flip the sign of transmit or receiver steering angles (e.g., for reverse-mounted sonars). | |
| `-roll_compensated` | Force system to be recognized as roll compensated (beam angles are already vertically referenced). | |

### Orientation Options
| Option | Description | Default |
|---|---|
| `-orientation_delay <sec>` | Apply a time delay to the orientation data. | `0.0` |
| `-no_orientation` | Override error if no `.orientation` file is found (e.g., for single beam data). | |
| `-check_drift` | Use value in `profile.clock_drift_millis` if it exists. | |
| `-alternate_orient <file>` | Specify an alternate orientation file (must be `.orientation` format). | |
| `-uncrosstalk <val>` | Specify a gyro offset to correct for crosstalk between roll and pitch. | `0.0` |

### SVP Selection for Multiple Profiles
| Option | Description |
|---|---|
| `-rules <file>` | Provide a file specifying time-based rules for selecting SVPs. | |
| `-interpolate` | Interpolate between SVPs in time. | |
| `-nearest_in_time` | Select the SVP nearest in time. | |
| `-last_observed` | Select the last observed SVP. | |
| `-next_observed` | Select the next observed SVP. | |
| `-nearest_in_distance` | Select the SVP nearest in distance. | |
| `-converge_to <depth> <velocity>` | Quick and dirty profile extension, sets maximum depth and velocity for SVPs shallower than the specified depth. | |

### Miscellaneous Options
| Option | Description | Default |
|---|---|
| `-just_merge` | Just merge TX orientation onto the merged file, ignoring all other raytracing options. | |
| `-test` | For testing new solution vs. solution already stored in merged file; does NOT write changes. | |
| `-flag` | Flag soundings that have no solution (e.g., first few pings from RESON systems). | |
| `-mask_map <file>` | Map of area of interest; ping positions outside the area are not processed. | |
| `-start_ping <num>` | Specify start/end pings for processing; pings outside this range are not processed. | All pings |
| `-end_ping <num>` | Specify start/end pings for processing; pings outside this range are not processed. | All pings |
| `-dump_depression` | Dump final depression angle and azimuth for every beam (for RESON backscatter calibration). Creates a `.depression` file. | |
| `-OWTT_scaler <val>` | A debug tool to scale the Observed Two-Way Travel Time (OWTT) (typically a power of 2). | `1.0` |
| `-v` | Enable verbose output. | |
| `-debug_wc` | Enable water column debugging output. | |
| `-debug_ping <num>` | Turn on debugging for a given ping number. | |
| `-debug_sounding` | Turn on debugging for sounding geometry calculations. | |
| `-special` | Print all sounding geometry information for testing. | |

## How It Works
1.  **Initialization:** Sets up various parameters from command-line arguments, including SVP file paths, raytracing methods, and debugging flags.
2.  **SVP Loading & Interpolation:** Loads all specified SVP files. If multiple SVPs are provided, it determines the appropriate SVP for each ping based on user-defined rules or interpolation methods (time-based or distance-based).
3.  **Merged File Processing:** Iterates through each ping in the input merged file:
    *   Reads the profile header and all rational beams for the current ping.
    *   For each beam, it calculates the sounding geometry using the selected raytracing method, the interpolated SVP, and corrected attitude (from an `.orientation` file). This involves detailed calculations of the beam path through the water column, accounting for refraction and motion.
    *   Updates the `depth`, `across-track`, and `along-track` fields of each beam with the newly calculated values.
    *   Updates the `vesselHeave`, `vesselPitch`, `vesselRoll`, and `vesselHeading` in the profile header with the merged TX orientation.
4.  **Output:** Writes the updated profile headers (and optionally beam records if depths were re-calculated) back to the merged file.
5.  **Diagnostic Output:** Provides verbose output about the merging process, time discrepancies, and corrected values if `-v` is enabled.

## Output Files
*   The input merged file (`<input.merged>`) is modified in-place (unless `-test` is used).
*   `<input.merged_prefix>.depression`: A binary file containing final depression and azimuth angles for each beam (if `-dump_depression` is used).

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.
*   `j_attitude.h`: For attitude data handling.
*   `j_watercolumn.h`: For water column data handling (if SVP raytracing is used).
*   `j_generic_beam_pattern.h`: For sonar parameter handling.

## Notes
`newMergeAtt` is a foundational tool for achieving high-accuracy multibeam bathymetry by rigorously integrating motion and sound velocity data. Its advanced beam vector recalculation and re-raytracing capabilities are essential for modern multibeam processing workflows. The tool modifies merged files in place, so thorough backups are recommended before processing. The extensive set of options allows for fine-tuning of motion compensation and refraction corrections based on specific survey conditions and sensor configurations. The `travis` algorithm is an experimental sounding reduction technique.