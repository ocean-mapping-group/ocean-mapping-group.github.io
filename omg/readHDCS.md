---
layout: default
title: readHDCS
parent: OMG Tools
nav_order: 51
---
# readHDCS

## Description
`readHDCS` is a diagnostic command-line utility designed to read and display information from USL-HDCS (University of New Brunswick Ocean Mapping Group - Hydrographic Data Collection System) data files. These files typically store observed and processed depth information along with their temporal indices.

The tool provides a low-level view of the data structures within these files, including summary headers, index blocks, and individual profile and beam data. It's particularly useful for debugging and understanding the internal organization of USL-HDCS datasets.

**Note:** This tool is explicitly noted as "not SWAPIO compliant," meaning it does not handle byte-order differences between systems, which could lead to incorrect data interpretation on systems with different endianness.

## Usage
```bash
readHDCS <USL_HDCS_linedirectory> [-verbose]
```

## Arguments

| Option | Description |
|---|---|
| `<USL_HDCS_linedirectory>` | **Required.** The path to the directory containing the USL-HDCS line data files (e.g., `ObservedDepths`, `ObservedDepthsTmIdx`, `ProcessedDepths`, `ProcessedDepthsTmIdx`). |
| `-verbose` | (Not explicitly used in the provided code but present in `USAGE`) Intended to provide more detailed output. |

## How It Works
1.  **File Opening:** The tool expects a directory path as input and attempts to open several specific files within that directory:
    *   `/ObservedDepths`
    *   `/ObservedDepthsTmIdx`
    *   `/ProcessedDepths`
    *   `/ProcessedDepthsTmIdx`
2.  **Index File Parsing:** It first reads and displays the `USL_HDCS_obs_index_summary` header from the `ObservedDepthsTmIdx` file, showing information like sensor number, file ID, version, and number of blocks. It then iterates through each block, reading and displaying `USL_HDCS_index_block` information, including the number of records per block and time bounds.
3.  **Record Offset Retrieval:** It reads `TmIndex` records to get byte offsets for each profile within the `ObservedDepths` file.
4.  **Observed Depths File Parsing:** It reads the `USL_HDCS_obs_summary_header` from the `ObservedDepths` file, indicating the total number of profiles.
5.  **Profile and Beam Display (Limited):** It then iterates through all profiles in the `ObservedDepths` file:
    *   For each profile, it reads the `USL_HDCS_obs_profile_header` and displays the number of depths and time offset.
    *   It then reads all `USL_HDCS_obs_beam` structures for that profile (though it only prints a commented-out example of beam data).
6.  **Interactive Query (Incomplete):** The code includes an interactive section (labeled `again:`) that prompts the user for a record number and allows navigating `next`, `prev`, or `full` display (though the `OMG_HDCS_display_profile` and `OMG_HDCS_display` functions are commented out or not provided). This interactive part appears incomplete in the provided source.

## Data Structures (from `USL_HDCS_hack.h` - assumed)
The tool relies on definitions from `USL_HDCS_hack.h` (not provided) for structures like `USL_HDCS_proc_summary_header`, `USL_HDCS_obs_profile_header`, etc., which define the format of the USL-HDCS data.
