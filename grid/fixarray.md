---
layout: default
title: fixarray
parent: Grid Tools
nav_order: 33
---
---
layout: default
title: fixarray
parent: Grid Tools
nav_order: 33
---
# fixarray

## Description
`fixarray` is a command-line utility for converting legacy JHC grid files into the modern, standardized "OMG1" JHC grid format. The tool reads the header information from an old-format binary array, creates a new standard 1024-byte JHC header, and combines it with the original data into a new, compliant file.

This tool is primarily used for data archeology to ensure backward compatibility with older datasets.

## Usage
```bash
fixarray [-really_old] <-8bit | -float> <badfile> <goodfile>
```

## Arguments

| Option | Description |
|---|---|
| `<badfile>` | **Required.** The path to the input legacy JHC-format grid file. |
| `<goodfile>` | **Required.** The path for the new, corrected, standard-format JHC grid file. |
| `-8bit` | **Required (or `-float`).** Specifies that the data type of the input file is 8-bit character. |
| `-float` | **Required (or `-8bit`).** Specifies that the data type of the input file is 32-bit float. |
| `-really_old` | A flag indicating the input file is from a very old format that is missing the `ystep` (Y pixel size) field in its header. If this is set, the tool assumes `ystep` is equal to `xstep`. |
| `-v` | Enable verbose output. |

## How It Works
1.  **File Opening:** Opens the input legacy grid file (`badfile`) for reading and the new output grid file (`goodfile`) for writing.
2.  **Header Reading (Legacy):** Reads the old-format header from `badfile`. The structure of this old header is assumed to be known (e.g., 20 bytes for integer dimensions and bounds, then 16 bytes for float bounds).
3.  **New Header Creation:** A new `JHC_header` (`good_head`) is initialized with standard values. Relevant information (dimensions, bounds) is transferred from the old header to the `good_head`.
    *   If `-really_old` is specified, `ystep` is explicitly set equal to `xstep`.
    *   `data_type` is set based on `-8bit` or `-float` flags.
4.  **Data Copying:** The tool reads the raw pixel data directly from `badfile` (skipping the old header) and writes it to `goodfile` after the `good_head`. This effectively wraps the old data with a new, compliant header.

## Output Files
*   `<goodfile>`: A new JHC-format grid file with a standard 1024-byte header.

## Dependencies
*   `array.h`: For `JHC_header` structure.
*   `support.h`: For general utility functions and error handling.

## Notes
This tool is specifically designed to handle older, non-standard JHC grid formats and migrate them to the current standard. This ensures that legacy data can be properly read and processed by modern tools that expect the current `JHC_header` structure. Without this tool, older files might be unreadable or misinterpreted.
