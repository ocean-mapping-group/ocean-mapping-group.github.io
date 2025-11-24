---
layout: default
title: hackSectors
parent: OMG Tools
nav_order: 34
---
# hackSectors

## Description
`hackSectors` is an empirical correction tool designed to adjust the depths of outer-swath beams in OMG-HDCS merged files. It was developed to address specific depth discrepancies or artifacts, such as those caused by yaw steering, particularly in data from older Simrad EM1000 sonars operating in shallow or medium modes.

The tool applies a user-specified depth adjustment to outer beams, modifying the input merged file(s) in place. It also provides diagnostic output regarding yaw steering.

## Usage
```bash
hackSectors <-depthscale <factor> | -depthoffset <meters>> <mergefile(s)> [-v]
```

## Arguments

### Depth Adjustment Method (Choose one)
| Option | Description |
|---|---|
| `-depthscale <factor>` | Multiplies the `observedDepth` of affected beams by the specified `<factor>` (e.g., `1.005` to increase depth by 0.5%). |
| `-depthoffset <meters>` | Adds a constant depth offset (in meters) to the `observedDepth` of affected beams. |

### Other Options
| Option | Description |
|---|---|
| `<mergefile(s)>` | **Required.** One or more OMG-HDCS merged files to be corrected. The tool modifies these files in place. |
| `-v` | Enable verbose output. |

## How It Works
1.  **File Processing:** The tool iterates through each ping in the merged file.
2.  **Depth Adjustment:** For beams in the outer portions of the swath (typically beyond 40-45 degrees from nadir, based on the `acrossTrack` and `observedDepth` values):
    *   It applies the chosen depth adjustment.
    *   If `-depthscale` is used, the `observedDepth` is multiplied by the specified factor.
    *   If `-depthoffset` is used, the specified offset is added to `observedDepth`.
3.  **Yaw Steering Diagnostics:** For each ping, it performs a least-squares fit on the `acrossTrack` versus `alongTrack` positions of the beams to calculate the effective "Yaw Steering" for diagnostic purposes.
4.  **In-Place Update:** The modified `observedDepth` field of these beams is updated directly within the file.

## Output Files
The input merged files are modified in-place.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
This is an empirical correction tool designed to fix specific artifacts that can appear in multibeam data from certain sonar systems. The corrections are heuristic and should be applied with caution and validated against other data. The tool modifies merged files in place, so backups are recommended. The diagnostic output of yaw steering can help to understand the source of the depth discrepancies.