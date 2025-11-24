---
layout: default
title: plotOS500
parent: Ray Tools
nav_order: 167
---
# plotOS500

## Description
`plotOS500` is a utility designed to process and output data from OS500 profilers (likely containing Conductivity, Temperature, Depth - CTD - measurements). It reads raw OS500 "dip" files, extracts time, pressure (depth), temperature, and salinity data, and can output them in various ASCII formats or as 2D array files for further processing.

This tool is crucial for handling raw CTD data, organizing it into usable formats, and optionally preparing it for visualization (e.g., as arrays for plotting profiles over time or depth).

## Usage
```bash
plotOS500 <OS500_prefix> [-bytime | -bydepth] [-fulldate] [-up | -down | -updown] [-array <maxz> <dz>] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `<OS500_prefix>` | **Required.** Prefix for the OS500 data files. The tool expects files like `<OS500_prefix>.dir` (directory file) and `<OS500_prefix>.000` (dip files). |
| `-bytime` | Output data ordered by time. |
| `-bydepth` | Output data ordered by depth. |
| `-fulldate` | Output full date and time for each record. |
| `-up` | Only process "up-casts" (profiler moving upwards). |
| `-down` | Only process "down-casts" (profiler moving downwards). |
| `-updown` | Only process both "up-casts" and "down-casts". |
| `-array <maxz> <dz>` | Output salinity and temperature data as JHC `.r4` array files (`.sal.r4`, `.tmp.r4`).
    *   `maxz`: Maximum depth (z-dimension) for the array.
    *   `dz`: Depth resolution for the array. |
| `-v` | Enable verbose output. | |

## Input File Formats
*   `<OS500_prefix>.dir`: An ASCII directory file listing the OS500 dip segments (block number, length, channel code, time, sample interval, etc.).
*   `<OS500_prefix>.000`, `<OS500_prefix>.001`, etc.: ASCII dip files for each segment, containing `sampnum`, `voltage`, `conductivity`, `temperature`, `pressure`, `salinity`, `sigma`, `soundspeed` for each measurement.

## How It Works
1.  **Initialization:** Parses command-line arguments to set the OS500 prefix, output order (`plot_order`), profile selection (`choice`), and array output parameters (`maxz`, `dz`).
2.  **File Opening:**
    *   Opens the OS500 directory file (`.dir`) for reading.
    *   Opens an ASCII output file (`.out`) for processed time/depth series data.
    *   If `-array` is specified, it opens two JHC `.r4` array files (`.sal.r4`, `.tmp.r4`) and initializes their headers.
3.  **Directory File Processing:** Reads the directory file line by line:
    *   Parses metadata for each block (segment) of OS500 data, including `blockno`, `blocklen`, `chancode`, start time (hour, min, sec, month, day, year), `sampint`, `average`, `hexflags`, `noascii`.
    *   Converts the start date/time into a Unix timestamp (`start_time`).
    *   Constructs the dip file name (e.g., `<OS500_prefix>.000`).
4.  **Dip File Processing:** Opens the corresponding dip file for the current block:
    *   Skips initial header lines.
    *   Reads `sampnum`, `voltage`, `conductivity`, `temperature`, `pressure`, `salinity`, `sigma`, `soundspeed` for each measurement.
    *   Calculates `dtime` (absolute time for each measurement).
    *   **Profile Classification:** Determines if the current profile segment is an "up-cast", "down-cast", "top", or "bottom" profile based on pressure change and `middepth`.
    *   **Output to ASCII (`.out`):** If the profile segment matches the `choice` (e.g., `PROF_UP` if `-up` is set), it writes `dtime`/`pressure`, `temperature`, `salinity` to the `.out` file, either `BYTIME` or `BYDEPTH`.
    *   **Output to Arrays (`-array`):** If `array_flag` is set and the profile matches `choice`:
        *   Initializes `salprof` and `tmpprof` (arrays to store salinity and temperature profile data).
        *   Populates `salprof[idepth]` and `tmpprof[idepth]` with interpolated values based on `pressure[i]` and `dz`.
        *   Writes these profiles to the `.sal.r4` and `.tmp.r4` files, updating the `arrhead.dy` counter.
5.  **Cleanup:** Closes all open files and frees allocated memory.

## Output Files
*   `<OS500_prefix>.out`: ASCII file containing processed time/depth series data (format depends on `-bytime` or `-bydepth`).
*   `<OS500_prefix>.sal.r4`: JHC `.r4` array file containing salinity profiles (if `-array` is used).
*   `<OS500_prefix>.tmp.r4`: JHC `.r4` array file containing temperature profiles (if `-array` is used).

## Dependencies
*   `support.h`: For general utility functions.
*   `array.h`: For `JHC_header` structure.
*   `stdtime.h`: For time conversion functions.

## Notes
`plotOS500` is crucial for processing raw CTD data from OS500 profilers, making it accessible for further oceanographic analysis and visualization. The ability to output data in both ASCII and gridded `.r4` formats provides flexibility for different downstream applications. The classification of up-casts and down-casts ensures that only relevant data segments are processed.