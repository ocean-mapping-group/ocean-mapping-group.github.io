---
layout: default
title: checkBounds
parent: Steve Tools
grand_parent: code
nav_order: 1
---
# checkBounds

## Description
`checkBounds` is a utility designed to check and process bounding box information from OMG_HDCS (Ocean Mapping Group Hydrographic Data Collection System) merged files. It reads the `OMG_HDCS_summary_header` and optionally `.100ping_bounds` and `.file_bounds` files to derive global minimum/maximum latitude, longitude, and time extents for the survey data. The tool can output these bounds to a binary file and/or an ASCII file. Additionally, it performs a sanity check, comparing the derived bounds against a reference position to identify potential large discrepancies.

## Usage
```bash
checkBounds [-v] [-ascii_out <ascii_outfile>] [-out <outfile>] [-xyzlist <listfile>] [-in <merged_file>]
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output, providing more detailed processing messages and intermediate results. |
| `-ascii_out <ascii_outfile>` | Specifies an output ASCII file to write the global bounds (min/max time, latitude, longitude) for each processed merged file. |
| `-out <outfile>` | Specifies an output binary file to write the global bounds (an array of 6 doubles for min/max time, lat, lon) for each processed merged file. |
| `-xyzlist <listfile>` | Specifies a file containing a list of merged file paths to process. |
| `-in <merged_file>` | Specifies a single merged file to process. (Mutually exclusive with `-xyzlist`). |

## How It Works
1.  **Argument Parsing:** The tool parses command-line arguments to set output file names, verbosity, and to determine whether to process a single merged file or a list of files.
2.  **Input File Handling:**
    *   **Single File Mode (`-in`):** If a single merged file is specified, it opens that file.
    *   **List Mode (`-xyzlist`):** If a list file is provided, it reads the paths of multiple merged files from the list.
3.  **Process Each Merged File:** For each merged file:
    *   **Open Merged File:** Opens the merged file for reading.
    *   **Read Summary Header:** Reads the `OMG_HDCS_summary_header` from the merged file, which contains overall survey parameters including reference latitude/longitude and scale factors for position.
    *   **Read 100-Ping Bounds (Optional):** Attempts to open a `.100ping_bounds` file associated with the merged file. If found, it reads and interpolates these 100-ping bounds (which contain min/max lat/lon/time for every 100 pings) to find the overall min/max extents for the entire file.
    *   **Read Global File Bounds (Optional):** Attempts to open a `.file_bounds` file. If found, it reads the pre-computed global bounds from this file.
    *   **Calculate Global Bounds:** If neither a 100-ping bounds file nor a global file bounds file is found, the tool might rely solely on the summary header or internal logic to determine bounds (though the provided code snippet primarily focuses on using the bounds files if available).
    *   **Output Global Bounds:**
        *   If an `-out` binary file is specified, it writes an array of 6 doubles (mintime, maxtime, minlat, maxlat, minlon, maxlon) to this file.
        *   If an `-ascii_out` file is specified, it appends a line to this file containing the merged filename and its global bounds in a human-readable format.
    *   **Sanity Check:**
        *   It calculates `ref_lat` and `ref_lon` from the `summary` header.
        *   It then computes the distance (in nautical miles) from this reference point to the top-left (`delta_dist_TL`) and bottom-right (`delta_dist_BR`) corners of the derived global bounds.
        *   If either of these distances exceeds `max_delta_dist` (hardcoded to 50 nautical miles), it prints a warning message, suggesting a problem with the bounds data.
4.  **File Closing:** All opened files are closed.
5.  **Test Output (Optional):** If an `-out` file was created and verbose mode is enabled, it re-opens and reads this binary output file to print its contents, verifying the written bounds.
