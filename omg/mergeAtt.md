---
layout: default
title: mergeAtt
parent: OMG Tools
nav_order: 40
---
# mergeAtt

## Description
`mergeAtt` is a crucial utility for integrating asynchronous attitude (roll, pitch, heave, heading) data into OMG-HDCS multibeam merged files. It can also re-apply corrections for surface sound velocity, mechanical pitch, and refraction, as well as re-calculate sonar-relative angles and two-way travel times (TWTTs). This tool is essential for ensuring that the bathymetric data accurately reflects the vessel's motion and environmental conditions at the time of data acquisition.

It supports various scenarios, including merging from multiple attitude sources, applying scaling factors to motion data, and advanced recalculations of beam vectors for precise georeferencing.

## Usage
```bash
mergeAtt <datafile_handle> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<datafile_handle>` | **Required.** The base name of the merged file (e.g., `line.merged`). The tool will automatically look for associated `.orientation`, `.surf_ss`, `.mech_pitch`, and `.param` files. Alternatively, use `-strip_ext` to provide the full filename. |
| `-strip_ext` | Use this if `<datafile_handle>` includes the file extension (e.g., `line.merged`). |

### Attitude Data Sources & Manipulation
| Option | Description |
|---|---|
| `-useorient <1 or 2>` | Specifies which orientation file to use: `0` (default, `.orientation`), `1` (`.orientation_1`), `2` (`.orientation_2`). |
| `-alternate_orient <file>` | Use an alternative orientation file instead of the default or numbered ones. |
| `-other_orient <file>` | Specifies a third orientation file whose delayed heave can be put into the `LongPeriodHeaveCorrection` field. |
| `-delay <sec>` | Apply a time delay (in seconds) to the primary orientation data. | `0.0` |
| `-other_delay <sec>` | Apply a time delay (in seconds) to the `-other_orient` data. | `0.0` |
| `-time_limit <sec>` | Only include orientation data if the inter-orientation time interval is within this limit. | `1.0` |
| `-rollscale <val>` / `-pitchscale <val>` / `-heavescale <val>` | Scale the roll, pitch, or heave values. | `1.0` |
| `-declin <val>` | Modify the heading by a specified magnetic declination. (Use with caution if `mergeNav` also applies declination). | `0.0` |
| `-change_heading` | Applies the merged heading to the profile. | |
| `-invert_heave` | Inverts the heave values. | |
| `-difforient` | Calculates the difference between `_1` and `_2` orientation files and stores it in the profile fields (pre-SE-TimeSeries analysis tool). | |
| `-apply_dheave` | Adjusts depths for the heave difference between `_1` and `_2` orientation files (not recommended). | |
| `-dheave_into_DDC` | Puts the difference of heaves 1 and 2 into the `dynamic_draftCorrection` field. | |
| `-dheavescale <val>` | Scale the difference heave. | `1.0` |

### Surface Sound Speed (SSP) & Mechanical Pitch
| Option | Description |
|---|---|
| `-ssp` | Use the `.surf_ss` file for surface sound speed. | |
| `-mpt` | Use the `.mech_pitch` file for mechanical pitch. | |
| `-dump_ssp` | Dump the surface sound speed values for inspection. | |

### Refraction & Beam Vector Recalculation
| Option | Description |
|---|---|
| `-redoref` | Re-calculates refraction using water column sound velocity profiles. Requires `-wc` option. | |
| `-wc <file(s)>` | Specifies one or more water column (`.wc`) files for refraction recalculation. | |
| `-draft <val>` | Specifies the draft to use for refraction calculations. | `0.0` |
| `-max_interp_depth <val>` | Maximum depth for water column interpolation. | `100.0` |
| `-recalc_beamVec` | Recalculates beam vectors (azimuth and depression) from the intersecting cone geometry, using interpolated attitude and other parameters at the time of receive. | |
| `-skip_atRC` | Skip attitude at receive time calculations (uses attitude at transmit). | |
| `-skip_raytrace` | Skip the raytracing step in the beam vector recalculation (uses simple trigonometry). | |
| `-use_prior_wc` | Use previously interpolated water column data (optimization). | |
| `-old_nonortho` | Use old non-orthogonal cone calculation (for specific sonar types). | |
| `-ortho` | Force orthogonal cone calculation. | |
| `-nonortho` | Force non-orthogonal cone calculation. | |
| `-RP` | Reduce all positions to the Reference Point (RP) of the vessel. | |

### General Options
| Option | Description |
|---|---|
| `-skip <val>` | Skip a number of pings when processing. | `1` |
| `-skip_remerge` | Skip the standard re-merging of attitude. | |
| `-just_testing` | Run in test mode without writing changes to the merged file. | |
| `-v` | Enable verbose output. |
| `-debug_wc` | Enable water column debugging output. |

## How It Works
1.  **File Loading:** Opens the input merged file, its parameter file (`.param`), and relevant attitude/SSP/mechanical pitch files. If `-redoref` is used, it also loads water column sound velocity profiles.
2.  **Time Synchronization:** Reads the time stamps from the merged file pings and the asynchronous attitude data. It interpolates the attitude values to match the exact time of each ping's transmission and optionally, the receive time of each beam.
3.  **Applying Corrections:**
    *   **Attitude:** Corrects roll, pitch, heave, and heading based on the interpolated values and user-defined scaling factors or delays.
    *   **SSP & Mechanical Pitch:** Updates the surface sound speed and mechanical pitch in the profile header if respective files are provided.
    *   **Declination:** Applies magnetic declination to the heading if specified.
4.  **Beam Vector Recalculation (`-recalc_beamVec`):**
    *   This is a core advanced feature. For each beam, it determines the attitude at the exact time of receive.
    *   It then uses a complex `calc_Intersecting_Cone_beam_vector` function (tailored for different sonar types) to re-calculate the beam's precise azimuth and depression angles in 3D space, taking into account mounting angles, sonar steering, and interpolated vessel motion.
    *   It then re-raytraces the beam using these new angles and the (interpolated) sound velocity profile to get corrected depth and across/along-track positions.
5.  **Output:** Writes the updated profile headers (and optionally beam records if depths were re-calculated) back to the merged file.
6.  **Diagnostic Output:** Provides verbose output about the merging process, time discrepancies, and corrected values if `-v` is enabled.
```