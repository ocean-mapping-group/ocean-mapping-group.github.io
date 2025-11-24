---
layout: default
title: packOMG
parent: OMG Tools
nav_order: 46
---
# packOMG

## Description
`packOMG` is a utility designed to convert an OMG-HDCS merged file from an older "verbose" file format (version 1) to a newer, more "packed" format (version 2). This conversion primarily involves rewriting the file to optimize storage or align with updated data structures.

The tool reads each profile and its associated beams from the input file and writes them to a new output file in the specified packed format.

## Usage
```bash
packOMG <OMG_HDCS_infile> <OMG_HDCS_outfile> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_infile>` | **Required.** The path to the input OMG-HDCS merged file in the verbose format (version 1). |
| `<OMG_HDCS_outfile>` | **Required.** The path for the output OMG-HDCS merged file in the packed format (version 2). |
| `-first <ping_num>` | Specifies the starting ping number to process. This functionality seems to be present in the `USAGE` string but is not implemented in the `main` function's loop, which processes all profiles. |
| `-last <ping_num>` | Specifies the ending ping number to process. This functionality seems to be present in the `USAGE` string but is not implemented in the `main` function's loop, which processes all profiles. |
| `-v` | Enable verbose output. | |

## How It Works
1.  **File Opening:** Opens the input merged file for reading and the output file for writing.
2.  **Version Check & Update:** Reads the summary header from the input file. It verifies that the input file is indeed in version 1 format. It then updates the `fileVersion` field in the summary header to 2 for the output.
3.  **Profile and Beam Copying:** Iterates through each profile in the input file:
    *   Reads the profile header.
    *   Reads all raw beams associated with that profile.
    *   Writes the profile header and the raw beams to the output file.

## Output Files
*   `<OMG_HDCS_outfile>`: A new OMG-HDCS merged file in the packed format (version 2).

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
The conversion from version 1 to version 2 format in OMG-HDCS files is often performed to optimize storage efficiency or to align with updated software requirements. This tool handles the low-level binary restructuring of the file. The `-first` and `-last` options are defined in the usage string but currently inactive, meaning the entire file is always converted. The tool creates a new file, ensuring the original remains untouched.