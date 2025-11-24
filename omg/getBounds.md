---
layout: default
title: getBounds
parent: OMG Tools
nav_order: 104
---
# getBounds

## Description
`getBounds` is a utility designed to calculate and update the geographic and temporal bounds of OMG-HDCS merged files or GLORIA sidescan files. It iterates through all profiles (pings) in the input file(s), extracts the latitude, longitude, and time for each beam/record, and then determines the minimum and maximum extents.

The calculated bounds are written back to the summary header of the input file, to an auxiliary `.file_bounds` file, and to a `.100ping_bounds` file (which stores bounds for every 100 pings). This tool is crucial for spatial indexing, data management, and ensuring that file headers accurately reflect the data's coverage.

## Usage
```bash
getBounds <datafile(s).{merged,ss}> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<datafile(s).{merged,ss}>` | **Required.** One or more paths to OMG-HDCS merged files or GLORIA sidescan (`.ss`) files. |
| `-v` | Enable verbose output. |
| `-first <ping_num>` | Specifies the starting ping number (inclusive) to process. | All pings |
| `-last <ping_num>` | Specifies the ending ping number (inclusive) to process. | All pings |
| `-dump_soleol` | Dumps the min/max times and file paths to `dump_bounds_soleol.txt` in a format for soleol. |
| `-do_anyway` | (Used with merged files) Forces processing of beams even if their status is bad or `observedDepth` is zero. |

## How It Works
1.  **Initialization:** Initializes global min/max latitude, longitude, and time variables.
2.  **File Iteration:** Loops through each input data file:
    *   **File Opening:** Opens the input file for reading and writing (`r+`) to update its summary header.
    *   **Auxiliary File Creation:** Creates two auxiliary files:
        *   `<filename>.100ping_bounds`: Stores bounds for every 100 pings.
        *   `<filename>.file_bounds`: Stores the global bounds for the current file.
    *   **Summary Reading:** Reads the summary header of the input file. It checks if the file is in OMG-HDCS merged format or attempts to treat it as a GLORIA format if not.
    *   **Ping Iteration:** Loops through each profile (ping) in the file (from `first` to `last`):
        *   **100-Ping Bounds Accumulation:** Every 100 pings, it dumps the accumulated `bounds100` to the `.100ping_bounds` file and resets `bounds100` for the next 100 pings.
        *   **Data Extraction:**
            *   If `merged_format`: Reads the `OMG_HDCS_profile_header` and then all raw beams (`OMG_HDCS_beam`) for the current ping. It extracts `ilat` and `ilon` from `profile.vesselLatOffset`, `profile.vesselLongOffset`, `beams[i].latOffset`, and `beams[i].longOffset`.
            *   If `GLORIA_format`: Reads the `gloria_rec` for the current ping. It extracts `gl_rec.header.time`, `gl_rec.header.lat`, `gl_rec.header.lon`. It also calculates port and starboard swath extents to get the full geographic coverage for the GLORIA record.
        *   **Bounds Update:** Updates the global `bounds` (for the entire file) and `bounds100` (for the current 100-ping block) with the min/max latitude, longitude, and time encountered.
    *   **Final 100-Ping Bounds:** Dumps any remaining `bounds100` to the `.100ping_bounds` file.
    *   **Global Bounds Update:**
        *   Calls `OMG_HDCS_interp_bounds(&bounds, summary)` to normalize the bounds.
        *   If `merged_format`, it updates the `minTime`, `maxTime`, `minLat`, `minLong`, `maxLat`, `maxLong`, and `status` fields in the `summary` header of the input file and writes it back using `OMG_HDCS_dump_summary`.
        *   Writes the final `bounds` for the current file to the `.file_bounds` file.
    *   **Time Duration Output:** Prints the time duration of the file and min/max times to the console.
    *   **Overall Bounds Update:** Updates the global `MinLat`, `MaxLat`, `MinLon`, `MaxLon`, `MinTime`, `MaxTime` across all processed files.
6.  **Overall Bounds Output:** After processing all files, it prints the overall min/max time and geographic bounds across the entire dataset to the console.
7.  **Soleol Dump (`-dump_soleol`):** If specified, dumps the min/max times and file paths to `dump_bounds_soleol.txt`.
8.  **Cleanup:** Closes all open files.

## Output Files
*   The input merged or GLORIA files are modified in-place (updating their summary headers).
*   `<datafile_prefix>.100ping_bounds`: A binary file storing bounds for every 100 pings.
*   `<datafile_prefix>.file_bounds`: A binary file storing the overall geographic and temporal bounds for each file.
*   `dump_bounds_soleol.txt`: An ASCII file containing min/max times and file paths (if `-dump_soleol` is used).

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.

## Notes
This tool is essential for efficient data management, particularly for large datasets where quickly identifying the spatial and temporal coverage of files is important. The `.100ping_bounds` files act as a spatial index, allowing other tools to quickly check if a region of interest overlaps with a data file without reading the entire file. The `dump_soleol` option provides a formatted output for specific scripting or analysis workflows.