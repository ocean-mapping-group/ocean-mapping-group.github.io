---
layout: default
title: readSWA
parent: SUB2K Tools
grand_parent: code
nav_order: 7
---
# readSWA

## Description
`readSWA` is a utility designed to process Submetrix SWA (Swath Acoustics) format data files. It can output the extracted information in two primary formats:
*   **ASCII output:** Latitude, longitude, and depth (and optionally across-track distance) for each beam.
*   **OMG_HDCS format:** Converts the SWA data into the structured OMG_HDCS (Ocean Mapping Group Hydrographic Data Collection System) format, specifically as `ISIS_SWA` toolType.

The tool handles various components of SWA data, including position, time, attitude (heading, roll, pitch, transducer depth, tide), and multibeam depth soundings, to integrate them into standardized formats for further hydrographic analysis.

## Usage
```bash
readSWA [-v] [-omg | -ascii [-across]] [-azishift <degrees>] [-out <outfile_prefix>] <swafile(s)>
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output, providing more detailed processing messages. |
| `-omg` | Output in OMG_HDCS merged format. |
| `-ascii` | Output in ASCII format (latitude, longitude, depth). This is the default if neither `-omg` nor `-ascii` is specified. |
| `-across` | Used with `-ascii`, outputs an additional column for across-track distance. |
| `-azishift <degrees>` | Apply an azimuth shift (in degrees) to correct for vessel heading. | `0.0` |
| `-out <outfile_prefix>` | **Required.** Specifies a prefix for the output files. The tool will generate: `<prefix>.merged` (if `-omg`), `<prefix>.ascii` or `<prefix>.ascii_across` (if `-ascii`), and `<prefix>.nav` (JCU NAV). |
| `<swafile(s)>` | **Required.** One or more input raw SWA data files. |

## How It Works
1.  **Initialization:** The tool initializes global variables for processing, including structures for OMG_HDCS data (`summary`, `profile`, `beams`), JCU NAV data (`nav_rec`), and various scaling factors. It also sets up coordinate projection (WGS84 ellipsoid).
2.  **File Opening:** Opens the input SWA file(s) and creates multiple output files based on the chosen output format:
    *   `tidefile`: `.merged` (for OMG_HDCS) or `.ascii` (for ASCII).
    *   `navfile`: `.nav` (for JCU NAV format).
3.  **Process SWA Files:** The tool iterates through each input `swafile`:
    *   **Line-by-Line Parsing:** It reads the SWA file line by line, identifying specific keywords and extracting data.
    *   **Header Information Extraction:** It parses header lines to extract scaling factors for depth, amplitude, horizontal range, roll, pitch, heading, transducer depth, and tide.
    *   **Ping-Specific Data:** It processes lines containing ping data, extracting:
        *   **Position:** UTM coordinates (`ping_east`, `ping_north`) which are converted to `ping_lat`, `ping_lon` using `utmgeo`.
        *   **Time:** Hour, minute, second, day, month, year are parsed and converted to `ping_time` (Unix timestamp).
        *   **Attitude:** Heading, roll, pitch, transducer depth, and tide are extracted.
        *   **Multibeam Soundings:** `depth_rec` structures are read, containing `x_offset`, `y_offset`, `weight`, and `depth` for individual beams.
4.  **Data Transformation:**
    *   **Azimuth Shift (`-azishift`):** Applies a rotation to the across-track offsets (`deast`, `dnorth`) based on `azishift`.
    *   **JCU NAV Output:** Each ping's position and time are written to the `.nav` file as a `jcu_nav_rec`.
    *   **ASCII Output (`-ascii`):** For each valid beam, latitude, longitude, and depth (and optionally across-track distance) are written to the ASCII output file (`.ascii` or `.ascii_across`).
    *   **OMG_HDCS Output (`-omg`):**
        *   **`prime_summary_data`:** For the first ping, the `OMG_HDCS_summary_header` is populated with `refTime`, `refLat`, `refLong` and written to the `.merged` file.
        *   **`prime_profile_data`:** An `OMG_HDCS_profile_header` is populated with ping-specific data (time offset, vessel position/attitude, tide).
        *   **`write_out_swath`:** For each beam, an `OMG_HDCS_beam` structure is populated with observed depth, across-track, along-track, and quality information.
        *   These `profile_header` and `beam` data are then written to the `.merged` file.
5.  **Loop:** This process continues until the end of the input SWA file(s).
6.  **File Closing:** All opened files are closed upon completion.
