---
layout: default
title: autorejectSoundings
parent: OMG Tools
nav_order: 79
---
---
layout: default
title: autorejectSoundings
parent: OMG Tools
nav_order: 79
---
# autorejectSoundings

## Description
`autorejectSoundings` is a utility for automatically flagging (rejecting) anomalous multibeam soundings within OMG-HDCS merged files. It applies rejection criteria based on across-track and along-track slope discontinuities, as well as the isolation of individual soundings. The tool is designed to work in a batch mode, applying criteria previously identified as effective using interactive tools like `SwathEditor`.

This tool aims to automate the removal of spikes and other noise artifacts from bathymetric data.

## Usage
```bash
autorejectSoundings <mergefile(s)> [-v] [-isolated] [-criteria <filename>]
```

## Arguments

| Option | Description |
|---|---|
| `<mergefile(s)>` | **Required.** One or more paths to OMG-HDCS merged files to be processed. These files are modified in place. |
| `-v` | Enable verbose output. |
| `-isolated` | Flags soundings that are isolated in space (i.e., surrounded by flagged or missing beams). |
| `-criteria <filename>` | Specifies a file containing the numerical criteria for slope-based rejection. The file should contain:
    *   `interping_distance` (double)
    *   `ACROSS_twoslopelimit` (double)
    *   `ALONG_twoslopelimit` (double) |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Criteria Loading (`-criteria`):** If a criteria file is specified, it reads `interping_distance`, `ACROSS_twoslopelimit`, and `ALONG_twoslopelimit` from it. These values define the thresholds for detecting spikes.
3.  **Profile Iteration:** For each profile (`k` from 1 to `summary.numProfiles - 2`, to allow for before and after pings):
    *   Reads the current profile's beams (`beams`), the previous profile's beams (`before_beams`), and the next profile's beams (`after_beams`).
    *   **Slope-Based Rejection (`-criteria`):**
        *   **Across-Track Slopes:** For each beam `i`, it calculates the slope between `beams[i-1]` and `beams[i]`, and between `beams[i]` and `beams[i+1]`. If both these slopes exceed `ACROSS_twoslopelimit` (and are of opposite sign for detecting spikes), `beams[i].status` is set to `22`.
        *   **Along-Track Slopes:** Similarly, for each beam `i`, it calculates the slope between `before_beams[i]` and `beams[i]`, and between `beams[i]` and `after_beams[i]`. If both these slopes exceed `ALONG_twoslopelimit` (and are of the same sign for detecting spikes), `beams[i].status` is set to `22`.
    *   **Isolated Beam Rejection (`-isolated`):**
        *   Checks for isolation in the across-track direction (i.e., if a beam has valid depth but its neighbors are flagged or missing).
        *   Checks for isolation in the along-track direction (i.e., if a beam has valid depth but its corresponding neighbors in the previous and next pings are flagged or missing).
        *   If a beam is deemed isolated, its `status` is set to `22`.
4.  **In-Place Update:** The modified `beams` (with updated `status` flags) are written back to the merged file for the current profile.
5.  **Beam Buffer Update:** Before processing the next profile, the `beams` from the current ping are copied to `before_beams`, and `after_beams` are copied to `beams`, to maintain the sliding window of three pings.

## Output Files
The input merged files are modified in-place.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
This tool is intended for batch processing after initial tuning of rejection criteria using interactive tools. It helps to automatically remove common noise artifacts, improving the overall quality of bathymetric datasets. The specific status flag `22` is typically used to mark automatically rejected soundings.

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Criteria Loading (`-criteria`):** If a criteria file is specified, it reads `interping_distance`, `ACROSS_twoslopelimit`, and `ALONG_twoslopelimit` from it. These values define the thresholds for detecting spikes.
3.  **Profile Iteration:** For each profile (`k` from 1 to `summary.numProfiles - 2`, to allow for before and after pings):
    *   Reads the current profile's beams (`beams`), the previous profile's beams (`before_beams`), and the next profile's beams (`after_beams`).
    *   **Slope-Based Rejection (`-criteria`):**
        *   **Across-Track Slopes:** For each beam `i`, it calculates the slope between `beams[i-1]` and `beams[i]`, and between `beams[i]` and `beams[i+1]`. If both these slopes exceed `ACROSS_twoslopelimit` (and are of opposite sign for detecting spikes), `beams[i].status` is set to `22`.
        *   **Along-Track Slopes:** Similarly, for each beam `i`, it calculates the slope between `before_beams[i]` and `beams[i]`, and between `beams[i]` and `after_beams[i]`. If both these slopes exceed `ALONG_twoslopelimit` (and are of the same sign for detecting spikes), `beams[i].status` is set to `22`.
    *   **Isolated Beam Rejection (`-isolated`):**
        *   Checks for isolation in the across-track direction (i.e., if a beam has valid depth but its neighbors are flagged or missing).
        *   Checks for isolation in the along-track direction (i.e., if a beam has valid depth but its corresponding neighbors in the previous and next pings are flagged or missing).
        *   If a beam is deemed isolated, its `status` is set to `22`.
4.  **In-Place Update:** The modified `beams` (with updated `status` flags) are written back to the merged file for the current profile.
5.  **Beam Buffer Update:** Before processing the next profile, the `beams` from the current ping are copied to `before_beams`, and `after_beams` are copied to `beams`, to maintain the sliding window of three pings.
