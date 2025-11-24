---
layout: default
title: shiftSStraces
parent: OMG Tools
nav_order: 61
---
# shiftSStraces

## Description
`shiftSStraces` is a utility designed to perform a bulk shift operation on the sidescan trace information (specifically `no_samples`, `centre_no`, and `offset`) within OMG-HDCS merged files. This tool can be used to re-align sidescan data across beams, effectively "shifting" the trace content from one beam to another within the same ping.

This could be useful for specific debugging scenarios, correcting acquisition errors where sidescan samples are misregistered relative to their intended beam, or artistic manipulation.

## Usage
```bash
shiftSStraces <OMG_HDCS_datafile(s)> -shift <value> [-v]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile(s)>` | **Required.** One or more paths to OMG-HDCS merged files to be processed. These files are modified in place. |
| `-shift <value>` | **Required.** The integer value by which to shift the sidescan traces.
    *   **Positive value:** Shifts trace information from earlier beams to later beams. The first `value` beams will have their sidescan information zeroed out.
    *   **Negative value:** Shifts trace information from later beams to earlier beams. The last `abs(value)` beams will have their sidescan information zeroed out. |
| `-v` | Enable verbose output. | |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Summary Header Reading:** Reads the summary header for basic file information.
3.  **Profile and Beam Iteration:** For each profile (ping) in the file:
    *   **Read Beams:** Reads the raw beams for the current profile and stores a copy in `orig_beams`.
    *   **Apply Shift (`toshift > 0` - positive shift):**
        *   The `no_samples`, `centre_no`, and `offset` fields of the first `toshift` beams are set to `0` (effectively clearing their sidescan content).
        *   For subsequent beams (from `toshift` to `no_beams - 1`), their sidescan information is copied from the `orig_beams` array, but offset by `toshift`. For example, `beams[j]` gets data from `orig_beams[j - toshift]`.
    *   **Apply Shift (`toshift < 0` - negative shift):**
        *   The `no_samples`, `centre_no`, and `offset` fields of the last `abs(toshift)` beams are set to `0`.
        *   For earlier beams (from `0` to `no_beams - abs(toshift) - 1`), their sidescan information is copied from `orig_beams`, offset by `abs(toshift)`. For example, `beams[j]` gets data from `orig_beams[j + abs(toshift)]`.
    *   **Write Beams:** The modified `beams` array (with shifted sidescan information) is written back to the current profile in the merged file.

## Output Files
The input merged files are modified in-place with the shifted sidescan trace information.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
This tool performs a very specific data manipulation. It directly modifies the pointers and metadata for sidescan traces within the merged file. It should be used with caution and primarily for specific debugging or data recovery scenarios, as improper use could lead to data corruption. Backups are highly recommended before processing.