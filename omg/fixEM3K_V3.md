---
layout: default
title: fixEM3K_V3
parent: OMG Tools
nav_order: 98
---
# fixEM3K_V3

## Description
`fixEM3K_V3` is a specialized utility designed to correct a specific data format issue in early Simrad EM3000 (and EM3002) multibeam sonar data files that were written in version 3 of the OMG-HDCS format. This issue arose because the profile header size was updated to include additional runtime telegram information, but existing files did not reflect this change, leading to incorrect parsing.

This tool essentially "pads" the profile header of affected files and sets a flag (`maxProcDepth` to non-zero) to indicate that the fix has been applied, distinguishing them from uncorrected files.

## Usage
```bash
fixEM3K_V3 <old_V3file> <fixed_V3file> [-v]
```

## Arguments

| Option | Description |
|---|---|
| `<old_V3file>` | **Required.** The path to the input, uncorrected EM3000/EM3002 V3 merged file. |
| `<fixed_V3file>` | **Required.** The path for the output corrected EM3000/EM3002 V3 merged file. |
| `-v` | Enable verbose output. |
| `-first <ping_num>` / `-last <ping_num>` | (Present in `USAGE` but not implemented) These options likely intended to specify a ping range, but `main` processes all profiles. |

## How It Works
1.  **File Opening:** Opens the `old_V3file` for reading and the `fixed_V3file` for writing.
2.  **Summary Header Check:**
    *   Reads the `OMG_HDCS_summary_header` from the `old_V3file`.
    *   It verifies that `summary.fileVersion` is `3` and that `summary.maxProcDepth` is `0` (indicating an uncorrected file). If these conditions are not met, it exits with an error.
    *   Sets `summary.maxProcDepth` to `1` to mark the file as fixed.
3.  **Summary Header Writing:** Writes the modified `summary` header to the `fixed_V3file`.
4.  **Profile and Beam Data Copying:** Iterates through each profile in the input file:
    *   Reads a portion of the profile header (all but the last 24 bytes, which were missing in the old V3 format) into a `bulk_data` buffer.
    *   Writes this `bulk_data` to the `fixed_V3file`.
    *   Writes 24 bytes of `extra_bytes` (initialized to zeros) to the `fixed_V3file`, effectively padding the profile header to its correct size.
    *   Reads the entire block of beam data for the current profile into `bulk_data`.
    *   Writes this beam data to the `fixed_V3file`.
5.  **Output:** A new merged file (`fixed_V3file`) is created with corrected profile header sizes and the `maxProcDepth` flag set.
