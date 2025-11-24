---
layout: default
title: replaceOMG
parent: OMG Tools
nav_order: 57
---
# replaceOMG

## Description
`replaceOMG` is an emergency toolkit utility designed to selectively replace data fields in a "corrupted" OMG-HDCS merged file with values from an "OK" (good) version of the same file. This is useful for data recovery scenarios where specific parts of a merged file have been inadvertently altered or corrupted by other software, allowing users to restore data without re-processing the entire dataset.

The tool currently supports replacing either motion data (roll, pitch, heave, heading) or beam status flags and some profile-level sonar settings.

## Usage
```bash
replaceOMG <ok_OMG_HDCS_infile> <corrupted_OMG_HDCS_outfile> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<ok_OMG_HDCS_infile>` | **Required.** The path to the "good" OMG-HDCS merged file, which contains the correct data to be copied. |
| `<corrupted_OMG_HDCS_outfile>` | **Required.** The path to the "corrupted" OMG-HDCS merged file, which will be modified in place with data from the `ok_infile`. |
| `-justMotion` | Replaces only the motion-related fields (`vesselHeave`, `vesselPitch`, `vesselRoll`, `vesselHeading`) in the profile header. |
| `-first <ping_num>` | Specifies the starting ping number to process. This functionality is mentioned in the `USAGE` string but is not implemented in the `main` loop, which processes all profiles. |
| `-last <ping_num>` | Specifies the ending ping number to process. This functionality is mentioned in the `USAGE` string but is not implemented in the `main` loop, which processes all profiles. |
| `-v` | Enable verbose output. | |

## How It Works
1.  **File Opening:** Opens the `ok_OMG_HDCS_infile` for reading and the `corrupted_OMG_HDCS_outfile` for reading and writing (in-place modification).
2.  **Summary Header Check:** Reads the summary headers from both files. It verifies that both files have the same `fileVersion` and `numProfiles`, stopping with an error if they do not match.
3.  **Profile and Beam Iteration:** The tool iterates through each profile (ping) from `0` to `summary.numProfiles - 1`:
    *   Reads the profile header from both the `ok_infile` (`profile`) and the `corrupted_outfile` (`prof2`).
    *   **Data Replacement:**
        *   If `-justMotion` is specified, it copies `vesselHeave`, `vesselPitch`, `vesselRoll`, and `vesselHeading` from `profile` to `prof2`.
        *   Otherwise (if `-justMotion` is *not* specified), it copies sonar settings like `power`, `TVG`, `attenuation`, `pulseLength`, `mode`, `status`, and `numDepths` from `profile` to `prof2`. It also reads the raw beams from both files and copies only the `status` field from the `ok_infile`'s beams to the `corrupted_outfile`'s beams.
    *   **Writing Changes:** The modified `prof2` (profile header) and `b2` (beam data) are written back to the `corrupted_OMG_HDCS_outfile` at the corresponding profile index.

## Output Files
The input `corrupted_OMG_HDCS_outfile` is modified in-place.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
`replaceOMG` is an emergency tool for data recovery. It allows for quick fixes by transferring known good data from one file to another, which can save significant reprocessing time. However, users should be extremely cautious when using this tool and ensure that the "OK" file is indeed correct for the intended fields, as it directly modifies binary data. The `-first` and `-last` options are defined in the `USAGE` string but are not implemented in the main processing loop.