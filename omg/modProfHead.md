---
layout: default
title: modProfHead
parent: OMG Tools
nav_order: 41
---
# modProfHead

## Description
`modProfHead` is a command-line utility designed to modify the profile headers of OMG-HDCS merged files. Its primary current functionality is to apply a time shift to the `refTime` in the summary header, effectively shifting the entire dataset in time. The tool is designed to work with 100-second integer time shifts.

While the code contains commented-out sections for other modifications (like adjusting `numDepths` or `processedDepth` values), its active functionality is focused on time shifting.

## Usage
```bash
modProfHead <mergefile(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<mergefile(s)>` | **Required.** One or more paths to OMG-HDCS merged files whose profile headers are to be modified. These files are modified in place. |
| `-time_shift <seconds>` | Shifts the `refTime` in the summary header by the specified number of seconds. Only 100-second integer shifts are supported. |
| `-day_shift <days>` | Shifts the `refTime` in the summary header by the specified number of days. This is converted to a 100-second integer `time_shift`. |
| `-v` | Enable verbose output. | |

## How It Works
1.  **File Processing:** The tool iterates through each specified merged file.
2.  **Summary Header Modification:**
    *   If either `-time_shift` or `-day_shift` is provided, the tool calculates the total time shift in seconds.
    *   It then checks if this shift is an integer multiple of 100 seconds. If not, it will report an error.
    *   The calculated 100-second integer shift is added to the `summary.refTime` field, effectively shifting the reference time for all profiles in the file.
    *   The updated summary header is written back to the file.
3.  **Profile Iteration (Currently Inactive for Time Shift):** If no time shift is requested, the tool iterates through all profiles in the file. While the code includes commented-out sections that could be used to modify individual profile fields (e.g., `numDepths`, `processedDepth`), these are not active in the current version of the tool.
4.  **In-Place Update:** All modifications are applied directly to the input merged files.

## Output Files
The input merged files are modified in-place.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
This tool is specifically designed for adjusting the reference time of merged files. While it currently only supports 100-second integer shifts, the design suggests potential for more flexible modifications to profile headers. As with all in-place modification tools, backups are recommended.