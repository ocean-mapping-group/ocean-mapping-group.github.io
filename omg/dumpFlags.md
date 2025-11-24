---
layout: default
title: dumpFlags
parent: OMG Tools
nav_order: 91
---
# dumpFlags

## Description
`dumpFlags` is a utility designed to extract, store, and apply beam status flags from OMG-HDCS merged files. It can either:
1.  **Dump:** Read the `status` byte for each beam in a merged file and save it to a separate `.flag_bk` file (a custom binary format with a JHC header).
2.  **Load:** Read `status` bytes from a `.flag_bk` file and apply them back to the beams in a merged file.

This tool is useful for backing up cleaning efforts, applying a standard set of flags to new data, or restoring flags after an accidental modification.

## Usage
```bash
dumpFlags <OMG_HDCS_datafile_prefix(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile_prefix(s)>` | **Required.** One or more base names of OMG-HDCS merged files (e.g., `line`). The tool will look for `line.merged` and `line.flag_bk`. |
| `-load` | Reads flags from a `.flag_bk` file and applies them to the corresponding merged file. |
| `-clobber` | (Used with `-load`). When loading flags, it overwrites existing beam statuses in the merged file, even if the new flag is 0 (good). By default, it only applies non-zero (bad) flags. |
| `-dropDup` | (Used when dumping flags). Ignores and does not dump flags for pings that have the same `timeOffset` as the previous ping. |
| `-v` | Enable verbose output. |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file prefix.
2.  **Merged File Opening:** Opens the merged file (`.merged` or `inname[k]`) for reading and writing (`r+`).
3.  **Flag File Opening:** Opens the corresponding `.flag_bk` file for writing (`wb`) if dumping flags, or reading (`rb`) if loading flags.
4.  **Summary Header Reading:** Reads the summary header from the merged file to determine `numProfiles` and `numDepths`.
5.  **Initialization (`-load` mode):** If in `load_flag` mode, it reads the JHC header from the `.flag_bk` file to determine the dimensions of the flag data. It also performs a check to ensure the size of the flag file matches the expected size based on the merged file's number of profiles and beams.
6.  **Profile Iteration:** For each profile (`i` from `start` to `end`):
    *   **Duplicate Ping Handling (`-dropDup`):** If `-dropDup` is specified and the current ping's `timeOffset` is the same as the previous, it skips this ping.
    *   **Beam Data Extraction:** Reads the raw beams for the current profile from the merged file.
    *   **Dumping Flags (default mode, no `-load`):**
        *   Initializes a `flags[]` array (unsigned char) to all zeros.
        *   For each beam `j` with valid `observedDepth`, it copies `beams[j].status` to `flags[j]`.
        *   Writes the `flags[]` array (which contains `summary.numDepths` bytes) to the `.flag_bk` file.
    *   **Loading Flags (`-load` mode):**
        *   Reads `summary.numDepths` bytes from the `.flag_bk` file into the `flags[]` array.
        *   For each beam `j` with valid `observedDepth`:
            *   If `-clobber` is specified, it directly overwrites `beams[j].status` with `flags[j]`.
            *   Otherwise (default `-load`), if `flags[j]` is non-zero (i.e., indicates a bad status), it applies this flag to `beams[j].status`.
        *   Writes the modified `beams` back to the merged file.
7.  **JHC Header for Flag File (when dumping):** If dumping flags, it writes a JHC header to the `.flag_bk` file before writing any flag data.
8.  **Cleanup:** Closes all open files.

## Output Files
*   The input merged file (`.merged`) is modified in-place if `-load` is used.
*   `<OMG_HDCS_datafile_prefix>.flag_bk`: A binary file containing the beam status flags (if not `-load`).

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `array.h`: For `JHC_header` structure.
*   `support.h`: For general utility functions and error handling.

## Notes
This tool is invaluable for managing the results of data cleaning. It allows for flexible application of quality control flags, either for backup/restore purposes or for applying a consistent flagging scheme across multiple datasets. The `--dropDup` option helps to manage specific data acquisition scenarios where duplicate pings might exist.