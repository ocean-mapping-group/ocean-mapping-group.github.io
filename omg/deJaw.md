---
layout: default
title: deJaw
parent: OMG Tools
nav_order: 85
---
# deJaw

## Description
`deJaw` is a utility designed to identify and flag specific types of noise artifacts in multibeam sonar data, colloquially referred to as "alligators" or "jaws." These artifacts manifest as sudden, significant changes in the across-track slope of the seafloor from ping to ping. The tool uses a combination of slope analysis and thresholding to detect these anomalies and marks the affected beams as bad.

It can also detect and flag profiles with `vesselHeading` outside the valid 0-360 range.

## Usage
```bash
deJaw <mergefile(s)> [-v] [-badazi] [-port | -stbd]
```

## Arguments

| Option | Description |
|---|---|
| `<mergefile(s)>` | **Required.** One or more paths to OMG-HDCS merged files to be processed. These files are modified in place. |
| `-v` | Enable verbose output. |
| `-badazi` | Flags all beams in a profile if the `profile.vesselHeading` is found to be outside the valid 0-360 degree range. |
| `-port` | Only analyze and correct the port side of the swath. |
| `-stbd` | Only analyze and correct the starboard side of the swath. |
| `-criteria <filename>` | (Present in `USAGE` but not implemented) This option likely suggests an external file for defining slope criteria, but the internal `interping_distance`, `ACROSS_twoslopelimit`, and `ALONG_twoslopelimit` are hardcoded. |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Summary Header Reading:** Reads the summary header for basic file information.
3.  **Profile Iteration (`k` from 1 to `numProfiles - 2`):**
    *   **`badazi` Check:** If `-badazi` is specified, it reads the `profile.vesselHeading` for the current ping. If the heading is outside 0-360, it flags all beams in that ping as `22` (bad).
    *   **"Alligator" Detection (Default):** If `-badazi` is *not* specified:
        *   **Slope Calculation:** It reads the beams from the previous (`before_beams`), current (`beams`), and next (`after_beams`) pings. For each of these sets of beams, it calculates an average across-track slope (`get_slope` function) within the specified side of the swath (`-port`, `-stbd`, or `BOTH`).
        *   **Slope Difference Analysis:** It then calculates the differences in across-track slope between consecutive pings: `before_slope = current_slope - previous_slope` and `after_slope = next_slope - current_slope`.
        *   **Thresholding:** If both `fabs(before_slope)` and `fabs(after_slope)` exceed a predefined `threshold` (hardcoded to `0.25`), it indicates a significant change, marking a potential "alligator" (`got_a_gator` flag is set).
        *   **Flagging Beams:** If an "alligator" is detected (`got_a_gator` is true), it then iterates through each beam `i` in the current ping:
            *   Calculates the along-track slope between `before_beams[i]` and `beams[i]`, and between `beams[i]` and `after_beams[i]`.
            *   If both along-track slopes exceed `ALONG_twoslopelimit` (hardcoded to `5.0`), it flags `beams[i].status` as `22`.
4.  **In-Place Update:** The modified `beams` (with updated `status` flags) are written back to the merged file for the current profile.
5.  **Beam Buffer Update:** Before processing the next profile, the `beams` from the current ping are copied to `before_beams`, and `after_beams` are copied to `beams`, to maintain the sliding window.

## `get_slope` Function
This helper function:
*   Takes an array of `OMG_HDCS_beam` structures.
*   Calculates a linear least-squares fit for depth vs. across-track distance for valid beams within a specified side of the swath (`check_side`).
*   Returns the slope (in degrees) of this fit, representing the average across-track slope of the seafloor.
