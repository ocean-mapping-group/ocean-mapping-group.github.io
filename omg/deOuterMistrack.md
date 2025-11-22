---
layout: default
title: deOuterMistrack
parent: OMG Tools
nav_order: 87
---
# deOuterMistrack

## Description
`deOuterMistrack` is a utility designed to detect and flag "mistracked" soundings in the outer portions of multibeam sonar swaths, particularly observed in data from systems like EM2040C and EM712. These mistracks manifest as spurious detections beyond the coherent outer edges of the swath.

The tool identifies regions of the outer swath where `Q_factor` (quality factor) is `-128` (indicating no detection) to determine the effective swath edge, and then flags any detected soundings (`!beams[i].status`) beyond this edge.

## Usage
```bash
deOuterMistrack <mergefile(s)> [-v] [-first <ping_num>] [-last <ping_num>]
```

## Arguments

| Option | Description |
|---|---|
| `<mergefile(s)>` | **Required.** One or more paths to OMG-HDCS merged files to be processed. These files are modified in place. |
| `-v` | Enable verbose output. |
| `-first <ping_num>` / `-last <ping_num>` | Specifies the starting and ending ping numbers (inclusive) to process. | All pings |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Summary Header Reading:** Reads the summary header for basic file information.
3.  **Ping Iteration:** Loops through profiles (pings) from `first` to `last` (or all profiles if not specified):
    *   Reads the raw beams for the current ping.
    *   **Determine Swath Edges:**
        *   It defines `outer` as `no_beams / 8`.
        *   `port_edge` starts at `outer` and moves inward until a beam with `Q_factor != -128` is found.
        *   `stbd_edge` starts at `no_beams - outer` and moves outward until a beam with `Q_factor != -128` is found.
        *   These `port_edge` and `stbd_edge` values roughly delineate the coherent edges of the swath.
    *   **Flag Mistracks:**
        *   It then iterates from the determined `port_edge` inward towards the center of the swath. If a beam `i` in this region has `!beams[i].status` (meaning it's currently considered valid) it flags it by setting the 5th bit of its `status` field (`beams[i].status |= 1 << 5;`). This marks it as a mistrack.
        *   Similarly, it iterates from the `stbd_edge` outward and flags valid beams in that region as mistracks.
4.  **In-Place Update:** The modified `beams` (with updated `status` flags for mistracks) are written back to the merged file for the current ping.
