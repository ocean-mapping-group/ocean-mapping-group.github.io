---
layout: default
title: DTMreject
parent: Grid Tools
nav_order: 22
---
---
layout: default
title: DTMreject
parent: Grid Tools
nav_order: 22
---
# DTMreject

## Description
`DTMreject` is a quality control utility for automated cleaning of multibeam sonar data. It processes one or more OMG-HDCS merged files and compares the depth of each individual beam against a reference Digital Terrain Model (DTM) grid. If a beam's depth differs from the interpolated depth of the reference DTM by more than a user-specified threshold, the beam's status is flagged as invalid within the merged file.

This tool is essential for identifying and rejecting flyers or systematic biases in survey lines by comparing them against a trusted, previously established surface.

## Usage
```bash
DTMreject -area <reference_dtm.r4> -away <threshold_meters> [OPTIONS] <merged_file(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-area <reference_dtm.r4>` | **Required.** Specifies the path to the JHC-format 32-bit floating-point (`.r4`) grid file to be used as the reference DTM. | `-area master_surface.r4` |
| `-away <threshold_meters>` | **Required.** Sets the maximum allowable difference (in meters) between a beam's measured depth and the corresponding depth from the reference DTM. If the absolute difference `|DTM_depth - beam_depth|` exceeds this value, the beam is flagged. | `-away 2.5` |
| `<merged_file(s)>` | **Required.** One or more OMG-HDCS merged files to be processed. The tool modifies these files in place. | `line_001.merged line_002.merged` |
| `-just_show` | Performs a "dry run". The tool will identify and report the beams it would reject but will not make any actual modifications to the input merged files. | |
| `-from_scratch` | Before running the comparison, this option resets the status of all beams in the file to 0. This is useful for ensuring a fresh flagging pass, removing any flags set by previous processing steps. | |
| `-tide` | If specified, the tool applies the tide correction value found in each profile's header to the beam's observed depth before comparing it to the DTM. | |
| `-list_changes` | If specified, creates an ASCII file for each input merged file, named `<merged_filename_prefix>.DTM_reject_changes`, which contains a list of all rejected beams (lat, lon, depth, beam number). | |
| `-v` | Enable verbose output during processing. | |

## How It Works
1.  **File Opening:** Opens the reference DTM (`-area`) and the input merged files.
2.  **Header Reading:** Reads the `JHC_header` from the DTM file.
3.  **DTM Loading:** Loads the DTM data into memory.
4.  **Merged File Processing:** Iterates through each input merged file:
    *   Reads the `OMG_HDCS_summary_header`.
    *   If `-from_scratch` is set, it resets the status of all beams to `0` (good).
    *   **Profile and Beam Iteration:** Iterates through each profile (ping) and each beam within that profile:
        *   Calculates the beam's geographic position (latitude, longitude).
        *   Projects the geographic position to pixel coordinates on the DTM.
        *   Interpolates the DTM to get the `reference_depth` at the beam's location.
        *   Retrieves the beam's `observed_depth` (applying tide correction if `-tide` is set).
        *   Calculates the absolute difference `|reference_depth - observed_depth|`.
        *   If the difference exceeds `threshold_meters`:
            *   If `-just_show` is set, reports the rejection without modifying the file.
            *   Otherwise, flags the beam's `status` as `22` (rejected by DTM).
            *   If `-list_changes` is set, writes the beam's details to a `.DTM_reject_changes` file.
    *   **In-Place Update:** If not `-just_show`, the modified beam statuses are written back to the merged file.

## Output Files
*   The input merged files are modified in-place (unless `-just_show` is used).
*   `<merged_filename_prefix>.DTM_reject_changes`: An ASCII file listing rejected beams (if `-list_changes` is used).

## Dependencies
*   `array.h`: For `JHC_header` structure and DTM data handling.
*   `support.h`: For general utility functions and error handling.
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `j_proj.h`: For coordinate projection functions.

## Notes
This tool provides an automated and objective method for quality control of multibeam data against a trusted reference surface. It is particularly useful for identifying systematic errors, calibration issues, or residual noise that might manifest as consistent deviations from the DTM.
