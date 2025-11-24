---
layout: default
title: unrollOMG
parent: OMG Tools
nav_order: 74
---
# unrollOMG

## Description
`unrollOMG` is a versatile utility designed to apply various corrections and adjustments to multibeam sonar data stored in OMG-HDCS merged files. It can rectify issues related to vessel motion (roll, pitch, heave), apply constant offsets, correct for lever arm effects, and even remove specific artifacts like "wobble."

This tool works by recalculating beam depths and positions based on corrected motion data or user-specified offsets, making it a powerful tool for refining bathymetric data quality.

## Usage
```bash
unrollOMG <OMG_HDCS_datafile(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile(s)>` | **Required.** One or more paths to OMG-HDCS merged files. These files are modified in place. |
| `-v` | Enable verbose output. |

### Motion Correction
| Option | Description | Default |
|---|---|
| `-apply_roll` | Apply measured roll data to correct beam positions. | |
| `-roll_offset <val>` | Apply a constant roll offset (in degrees) to the data. Overrides `-apply_roll`. | `0.0` |
| `-flip_roll` | Flips the sign of the measured roll before applying it. | |
| `-roll_scale <val>` | Scale the measured roll value before applying. | `1.0` |
| `-apply_pitch` | Apply measured pitch data to correct beam positions. | |
| `-pitch_offset <val>` | Apply a constant pitch offset (in degrees) to the data. Overrides `-apply_pitch`. | `0.0` |
| `-pitch_rate_scale <val>` | Scale the calculated pitch rate for correction (experimental). | |
| `-flipheave` | Flips the sign of the heave data. | |
| `-negheave` | (Used with `-flipheave`) Applies heave as a positive addition rather than subtraction. | |
| `-leverarm <X Y Z>` | Correct for lever arm offsets (X, Y, Z in meters) between the motion sensor and the sonar head. | |
| `-lag <val>` | Apply a time lag (in seconds) to the measured motion data (for lever arm correction). | `0.0` |

### Depth Adjustments
| Option | Description | Default |
|---|---|
| `-draft <val>` | Specifies the draft (in meters) to use for calculations. | `0.0` |
| `-add_draft <val>` | Adds a constant draft value (in meters) to all depths. | `0.0` |

### Data Filtering & Specific Corrections
| Option | Description | Default |
|---|---|
| `-justport` / `-juststbd` | Apply corrections only to port or starboard beams, respectively. | `FIXBOTH` (both sides) |
| `-modobs` | (For `fileVersion=1`) Modifies `observedDepth` instead of `processedDepth` when applying corrections. | |
| `-remove_wobble` | Removes "wobble" artifacts using a `.roll_wobble` file (requires a previous run of "dewobble"). | |
| `-llshift <lat_offset> <lon_offset>` | Shifts the latitude and longitude offsets in the profile header. | |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Wobble File Loading (`-remove_wobble`):** If specified, it opens a `.roll_wobble` file to read pre-calculated roll correction values.
3.  **Summary Header Reading:** Reads the summary header for basic file information.
4.  **Profile Iteration:** For each profile (ping) in the merged file:
    *   Reads the current profile, and if necessary, the previous and next profiles (for `pitch_rate_scale` and `lag` calculations).
    *   **Wobble Correction (`-remove_wobble`):** Reads the roll offset from the `.roll_wobble` file and applies it to `roll_offset`.
    *   **Latitude/Longitude Shift (`-llshift`):** If specified, directly modifies `profile.vesselLatOffset` and `profile.vesselLongOffset`.
    *   **Induced Heave Calculation (`-leverarm`, `-lag`):** If a lever arm is specified, it calculates `induced_heave` by rotating the lever arm vector with the interpolated vessel attitude (roll, pitch).
    *   **Pitch Rate Calculation (`-pitch_rate_scale`):** Calculates the average pitch rate between adjacent pings.
    *   **Beam Iteration:** For each beam in the current profile (potentially filtered by `-justport` or `-juststbd`):
        *   If the beam has an `observedDepth`:
            *   **Flip Heave (`-flipheave`):** Adjusts `observedDepth` based on the `profile.vesselHeave`.
            *   **Add Draft (`-add_draft`):** Adds a constant draft value to `observedDepth`.
            *   **Pitch Rate Scale (`-pitch_rate_scale`):** Adjusts `observedDepth` based on the calculated pitch rate.
            *   **Lever Arm Induced Heave (`-leverarm`):** Adjusts `observedDepth` based on the calculated `induced_heave`.
            *   **Pitch/Roll Correction (`-apply_pitch`, `-pitch_offset`, `-apply_roll`, `-roll_offset`, `-remove_wobble`):**
                *   These options involve recalculating the beam's depth and across/along-track position based on the original `observedDepth` and `acrossTrack`/`alongTrack` (converted to slant range), and then rotating them by the specified pitch/roll values or offsets.
                *   The corrected values are then written back to `observedDepth` and `acrossTrack`/`alongTrack` (or `processedDepth`/`depthAccuracy` for `fileVersion=1` without `modobs`).
5.  **In-Place Update:** The modified beam records and profile headers are written back to the input merged files.

## Output Files
The input merged files are modified in-place.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
`unrollOMG` is a powerful post-processing tool for refining the accuracy of bathymetric data by correcting for various systematic errors related to vessel motion and sensor installation. The corrections applied can significantly improve the quality of the final DTM. The tool modifies merged files in place, so backups are highly recommended before processing. The `-remove_wobble` option highlights the tool's ability to address specific, complex artifacts.