---
layout: default
title: updateSSheader
parent: OMG Tools
nav_order: 75
---
# updateSSheader

## Description
`updateSSheader` is a utility designed to transfer specific sonar configuration and acquisition parameters from an OMG-HDCS merged file's profile structure to the header of a corresponding GLORIA sidescan (SS) file. This ensures that the sidescan file's header accurately reflects details like transmit power, beam widths, pulse length, and operational mode that were recorded in the original multibeam data.

This tool is useful for synchronizing metadata between related multibeam and sidescan datasets, especially when the sidescan file is generated from the merged data.

## Usage
```bash
updateSSheader <input_omg_file(.merged)> <updated_slrss_file(.ss_usually)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<input_omg_file(.merged)>` | **Required.** The path to the input OMG-HDCS merged file, which is the source of the updated header information. |
| `<updated_slrss_file(.ss_usually)>` | **Required.** The path to the GLORIA sidescan file (`.ss_usually`) whose headers will be updated. This file is modified in place. |
| `-start <ping_num>` | Specifies the starting ping number (inclusive) to process. | All pings |
| `-end <ping_num>` | Specifies the ending ping number (inclusive) to process. | All pings |
| `-v` | Enable verbose output. | |

## How It Works
1.  **File Opening:** Opens the input OMG-HDCS merged file for reading and the GLORIA sidescan file for reading and writing (in-place modification).
2.  **Summary Header Reading:** Reads the summary header from the merged file to determine the total number of profiles.
3.  **Profile Iteration:** Iterates through each profile (ping) in the specified range (from `the_start` to `the_end`):
    *   Reads the `OMG_HDCS_profile_header` from the merged file for the current ping.
    *   Reads the corresponding `gloria_rec` (sidescan record) from the sidescan file for the same ping.
    *   **Header Update:** Copies the following fields from the `OMG_HDCS_profile_header` to the `gloria_rec.header` structure:
        *   `tx_power_reduction`
        *   `rx_beam_width`
        *   `rx_bandwidth`
        *   `tx_pulse_len`
        *   `tx_beam_width`
        *   `absorp_coeff`
        *   `rx_gain_reduction`
        *   `mode`
    *   **Writing Changes:** Writes the modified `gloria_rec` back to the sidescan file at the current ping index.

## Output Files
The input GLORIA sidescan file (`<updated_slrss_file(.ss_usually)>`) is modified in-place.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `jcu_gloria.h`: For GLORIA data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
This tool ensures metadata consistency between multibeam and sidescan datasets, which is important for accurate interpretation and processing. For example, if sidescan imagery is generated from merged data, `updateSSheader` can ensure the sidescan file's header accurately reflects the sonar's operational settings, which might be critical for applying further corrections or for proper display. The tool modifies files in-place, so backups are recommended.