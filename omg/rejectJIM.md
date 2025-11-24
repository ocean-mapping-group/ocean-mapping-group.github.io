---
layout: default
title: rejectJIM
parent: OMG Tools
nav_order: 54
---
# rejectJIM

## Description
`rejectJIM` is a utility designed to identify and flag noisy or anomalous beams within OMG-HDCS merged files, primarily focusing on data between specified beam ranges. It applies a statistical filter based on standard deviation to detect outliers, and can also re-initialize beam statuses.

The tool aims to remove spurious soundings (often referred to as "Jim" noise, a common type of spurious noise) that appear in multibeam data, particularly in the inner swath.

## Usage
```bash
rejectJIM <mergefile(s)> [-v] [-newstart] [-sdev <factor>]
```

## Arguments

| Option | Description |
|---|---|
| `<mergefile(s)>` | **Required.** One or more paths to OMG-HDCS merged files to be processed. These files are modified in place. |
| `-v` | Enable verbose output. |
| `-newstart` | Re-initializes the status of all beams to `0` (good) before applying the filter. |
| `-sdev <factor>` | Specifies the standard deviation multiplier to use for outlier detection. Beams whose detrended depth deviates by more than `factor * standard_deviation` from the mean will be flagged. | `1.96` (equivalent to ~95% confidence interval) |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Summary Header Reading:** Reads the summary header for basic file information.
3.  **Profile and Beam Iteration:** For each profile (ping) in the file:
    *   **Beam Status Initialization (`-newstart`):** If `-newstart` is used, all beam statuses are reset to `0` (good) if they have a valid `observedDepth`.
    *   **Least Squares Fit:** It defines two "windows" of beams (hardcoded to `15-25` and `40-45`). It uses the `acrossTrack` and `observedDepth` of valid beams within these windows to perform a least-squares linear regression. This fit estimates the average depth and across-track slope of the seafloor in these relatively "good" regions.
    *   **Detrending:** It then "detrends" the observed depths of beams within a broader range (`finish_first` to `start_second`) by subtracting the effect of the calculated slope.
    *   **Standard Deviation Calculation:** The standard deviation (`sdev`) of these detrended depths (relative to the intercept of the least-squares fit) is calculated, again using beams within the two "good" windows.
    *   **Outlier Detection:** For beams in the "middle" region (hardcoded to `finish_first` to `start_second`), it checks if their detrended depth deviates from the mean (intercept) by more than `sdev_factor * sdev`.
    *   **Flagging:** If a beam is identified as an outlier, its `status` is set to `22` (a common flag for bad soundings in OMG tools).
4.  **In-Place Update:** If any beam's status is modified, the updated raw beam records are written back to the merged file.
5.  **Summary Report:** After processing all profiles in a file, it reports the total number of beams filtered from that file.

## Output Files
The input merged files are modified in-place.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
"Jim" noise is a common artifact in multibeam sonar data, often characterized by spurious detections in the inner swath. This tool applies a statistical filter to detect and remove such outliers, improving the quality of the bathymetric data. The hardcoded beam ranges suggest this tool is optimized for specific sonar configurations or data characteristics. As the tool modifies files in-place, backups are recommended.