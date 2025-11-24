---
layout: default
title: deHump
parent: OMG Tools
nav_order: 84
---
# deHump

## Description
`deHump` is a utility designed to apply empirical angular corrections to multibeam sonar data, specifically targeting the "hump" effect often observed in older EM1000 data from the Creed, believed to be caused by erroneous beam pointing angle correctors in the EPROM.

The tool can apply corrections using two methods: `angshift` (shifting the beam angle) or `depscale` (scaling the observed depth). It can process either standard OMG-HDCS merged files or USL-HDCS observed depth files.

## Usage
```bash
deHump <mergefile(s)> [-v] (-angshift <value> | -depscale <value>) [-mode <value>] [-hdcs] [-symm]
```

## Arguments

| Option | Description |
|---|---|
| `<mergefile(s)>` | **Required.** One or more paths to OMG-HDCS merged files or USL-HDCS line directories. These files are modified in place. |
| `-v` | Enable verbose output. |

### Correction Methods (Choose one)
| Option | Description |
|---|---|
| `-angshift <value>` | Apply a constant angular shift (in degrees) to the beam angles. |
| `-depscale <value>` | Apply a depth scaling factor to specific beam ranges. | `0.0105` |

### Other Options
| Option | Description |
|---|---|
| `-mode <value>` | Only apply corrections to profiles (pings) with this specific mode value. | `999` (all modes) |
| `-hdcs` | Process USL-HDCS observed depth files instead of OMG-HDCS merged files. |
| `-symm` | (Present in `USAGE` but not implemented) Likely intended for symmetric application of corrections. |
| `-hackfn <filename>` | (Present in `USAGE` but not implemented) Likely intended for an external hack function file. |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file (or USL-HDCS directory).
2.  **Summary Header Reading & File Type Handling:** Reads the summary header and handles both OMG-HDCS and USL-HDCS file formats, mapping USL-HDCS data to OMG structures.
3.  **Correction Parameter Setup:**
    *   **`-angshift` method:** It calculates `angle_corrector[k]` values for each beam `k`. These correctors are based on `ang_shift` and are non-zero only for the innermost and outermost beams, with a smooth transition to zero in between.
    *   **`-depscale` method:** It calculates `dep_shift[k]` values for each beam `k`. These are non-zero (equal to `dep_scale` or a scaled version of it) for the innermost and outermost beams, and zero for central beams, following a pattern based on beam number.
4.  **Profile and Beam Iteration:** For each profile (ping) in the file:
    *   **Mode Filtering:** If `-mode` is specified, it only processes pings whose `profile.mode` matches the `mode_choice`.
    *   Reads the raw beams for the current profile (converting USL-HDCS beams to OMG format if `hdcs_flag` is set).
    *   For each beam `i` that has an `observedDepth` and `reflectivity`:
        *   **Apply `angshift`:**
            *   Calculates `orig_angle` from `orig_depth` and `orig_range`.
            *   Adds `angle_corrector[i]` to `orig_angle` to get `real_angle`.
            *   Recalculates `real_range` and `real_depth` from `real_angle` and `slant_range`.
            *   Updates `beams[i].observedDepth` and `beams[i].acrossTrack` with these `real_depth` and `real_range` values.
        *   **Apply `depscale`:**
            *   Subtracts `beams[i].observedDepth * dep_shift[i]` from `beams[i].observedDepth`.
5.  **In-Place Update:** The modified `beams` (with corrected depths and/or across-track values) are written back to the merged file (or USL-HDCS file) for the current profile.

## Output Files
The input merged files are modified in-place.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
This tool provides empirical corrections for specific sonar artifacts observed in older datasets. The corrections are heuristic and may need careful application. The tool modifies merged files in place, so backups are recommended. It handles both OMG-HDCS and legacy USL-HDCS file formats.