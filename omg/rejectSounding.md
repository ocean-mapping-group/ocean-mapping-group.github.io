---
layout: default
title: rejectSounding
parent: OMG Tools
nav_order: 55
---
# rejectSounding

## Description
`rejectSounding` is a command-line utility used to flag or eliminate multibeam soundings in OMG-HDCS merged files that fall outside specified depth or across-track range thresholds. It provides options to re-initialize beam statuses, mark entire swaths as bad, or even apply a scaling factor to problematic soundings.

This tool is useful for initial data cleaning, removing gross outliers, or isolating data within a particular spatial extent.

## Usage
```bash
rejectSounding <mergefile(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<mergefile(s)>` | **Required.** One or more paths to OMG-HDCS merged files to be processed. These files are modified in place unless `-check` is used. |
| `-v` | Enable verbose output. |
| `-eliminate` | Instead of just flagging, it completely zeros out the data for rejected beams. |
| `-check` | Runs the checks but does *not* write any changes to the file. Useful for previewing potential rejections. |
| `-divide10` | For depths outside the specified range, it divides `observedDepth`, `acrossTrack`, and `alongTrack` by 10 (a specific hack). |
| `-newstart` | Resets the `status` of all valid beams to `0` (good) before applying new rejection criteria. |
| `-whole_swath` | If any beam in a profile is rejected, the `status` of all valid beams in that entire swath will be set to `22`. |
| `-range <max_across_track_m>` | Specifies the maximum absolute across-track distance (in meters) a sounding can have. Beams beyond this range are flagged. | `100000` |
| `-depths <min_depth_m> <max_depth_m>` | Specifies the minimum and maximum water depth (in meters) for valid soundings. Beams outside this range are flagged. | `0` to `100000` |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Summary Header Reading:** Reads the summary header for basic file information.
3.  **Profile and Beam Iteration:** For each profile (ping) in the file, and then for each beam within that profile:
    *   **Status Initialization (`-newstart`):** If `-newstart` is active, the status of each beam is reset to `0` if it has a valid `observedDepth`.
    *   **Range Check:** Compares the absolute `acrossTrack` value (converted to meters) with `maxrange`. If it exceeds `maxrange`, the beam is marked for rejection.
    *   **Depth Check:** Compares the `observedDepth` value (converted to meters) with `mindepth` and `maxdepth`. If it falls outside this range, the beam is marked for rejection.
    *   **Action on Rejection:**
        *   **`-divide10`:** If this option is used and a beam fails the depth check, its `observedDepth`, `acrossTrack`, and `alongTrack` values are divided by 10 (a specific, hardcoded scaling).
        *   **Flagging:** Otherwise, if a beam is marked for rejection and its `status` is not already set, its `status` is set to `22` (a common flag for bad soundings).
        *   **`-eliminate`:** If this option is active, the entire `OMG_HDCS_beam` structure for the rejected beam is zeroed out (effectively removing it).
    *   **`-whole_swath`:** If this option is active and any beam in the current profile has been modified, then all valid beams in that profile will have their `status` set to `22`.
4.  **In-Place Update:** If the `-check` flag is *not* used and any beams were modified or refreshed, the updated raw beam records are written back to the merged file.
