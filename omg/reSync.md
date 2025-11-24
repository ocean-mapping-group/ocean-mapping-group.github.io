---
layout: default
title: reSync
parent: OMG Tools
nav_order: 60
---
# reSync

## Description
`reSync` is a utility designed to re-synchronize sidescan data (specifically `centre_no`, `no_samples`, and `offset` fields) with corresponding depth detections within OMG-HDCS merged files. This tool is particularly useful when the sidescan information has become desynchronized or lost for certain beams, but is still present in adjacent pings.

It identifies sequences of pings where sidescan data is missing for beams that have depth detections, and then attempts to restore this information by copying it from the previous ping's beams. This process can lead to some loss of specific sidescan data if there are no common beams with sidescan.

## Usage
```bash
reSync <mergefile(s)> [-v] [-testonly]
```

## Arguments

| Option | Description |
|---|---|
| `<mergefile(s)>` | **Required.** One or more paths to OMG-HDCS merged files to be processed. These files are modified in place unless `-testonly` is used. |
| `-v` | Enable verbose output. |
| `-testonly` | Runs the synchronization logic but does *not* write any changes back to the merged file. Useful for previewing potential synchronizations. |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Summary Header Reading:** Reads the summary header for basic file information.
3.  **Initial Beam State:** Reads the raw beams from the *first* profile (ping 0) and stores them as `before_beams`.
4.  **Profile Iteration:** For each subsequent profile (ping `k` from 1 to `summary.numProfiles - 1`):
    *   **Detect Desynchronization:** It checks if any beam in the current ping (`beams[i]`) has an `observedDepth` but `no_samples == 0` (indicating missing sidescan data for a detected depth). If such a condition is found, it sets a `dosync` flag.
    *   **Synchronization (`dosync` and not `-testonly`):** If `dosync` is active and not in `testonly` mode:
        *   It iterates through all beams in the current ping.
        *   For each beam `i`, if both `beams[i].observedDepth` (current ping's depth detection) and `before_beams[i].observedDepth` (previous ping's depth detection) are valid, it copies the `centre_no`, `no_samples`, and `offset` (sidescan data pointers) from `before_beams[i]` to `after_beams[i]`.
        *   If `beams[i].observedDepth` is valid but `before_beams[i].observedDepth` is not, the sidescan info for `after_beams[i]` is zeroed out, and a `lost` counter is incremented.
        *   The `after_beams` (with restored sidescan info) are then written back to the current profile `k` in the merged file.
    *   **Update `before_beams`:** Before processing the next ping, the `beams` from the current ping `k` are copied to `before_beams` to be used as a reference for ping `k+1`.
5.  **In-Place Update:** The merged file is modified in place, updating the sidescan data pointers for desynchronized beams.

## Output Files
The input merged files are modified in-place (unless `-testonly` is used).

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
Sidescan data can become desynchronized from bathymetry due to various reasons, including data acquisition issues or processing errors. This tool provides a heuristic approach to recover missing sidescan data pointers by assuming continuity from adjacent pings. This can be critical for generating complete sidescan mosaics. The tool modifies merged files in place, so backups are recommended. The `-testonly` option is useful for evaluating the effect of the synchronization before applying permanent changes.