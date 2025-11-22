---
layout: default
title: openISIS
parent: SUB2K Tools
grand_parent: code
nav_order: 4
---
# openISIS

## Description
`openISIS` is a utility designed to parse ISIS Submetrix 2000 data files and convert the extracted information into OMG_HDCS (Ocean Mapping Group Hydrographic Data Collection System) format. It processes various ISIS Generic Block (GBH) data types, including ping times, control status, raw sidescan imagery, PRANG (Phase Range, which likely corresponds to phase-derived bathymetry), and attitude data (roll, pitch, heading, vertical displacement, depth, missed times). The tool combines this information to produce both JCU GLORIA records (for sidescan and derived products like fish depth and total depth) and structured OMG_HDCS files.

## Usage
```bash
openISIS [-v] [-dump] [-omg] [-skip <value>] -out <outfile_prefix> <rawISISfiles(s)>
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output, providing more detailed processing messages. |
| `-dump` | Enables debugging output for PRANG data to a `.dump` file. |
| `-omg` | Activates output to OMG_HDCS merged format files (in addition to JCU GLORIA files). |
| `-skip <value>` | Specifies a skip value (in records) when searching for the next ping start. | `1` |
| `-out <outfile_prefix>` | **Required.** Specifies a prefix for the output files. The tool will generate: `<prefix>.nav` (JCU NAV), `<prefix>.the_ss` (JCU GLORIA), `<prefix>.raw_ss` (JCU GLORIA), `<prefix>.merged.phase` (PRANG data), `<prefix>.merged.trace` (raw sidescan traces), `<prefix>.zfish` (JCU GLORIA fish depth), `<prefix>.ztot` (JCU GLORIA total depth), and `<prefix>.dump` (PRANG debug if `-dump` is used). If `-omg` is used, also `<prefix>.omg.merged`. |
| `<rawISISfiles(s)>` | **Required.** One or more input raw ISIS data files. |

## How It Works
1.  **Initialization:** The tool initializes global variables for processing, including arrays for attitude data, sidescan parameters, and ISIS Generic Block structures. It also defines `ISIS_angbin` structures for managing grazing angle bins.
2.  **File Opening:** Opens various output files (`.nav`, `.raw_ss`, `.the_ss`, `.phase`, `.trace`, `.zfish`, `.ztot`, `.dump`, and optionally `.omg.merged`).
3.  **Assign Angle Bins (`assign_angle_bins`):** Defines a set of 100 angle bins (50 for positive, 50 for negative across-track angles) by calculating their `centre_angle`, `inner_angle`, and `outer_angle`.
4.  **Process ISIS Files:** The tool iterates through each input `rawISISfile`:
    *   **Search for Ping Start (`search_for_ping_start`):** Scans the file to locate the beginning of the next valid ISIS ping block (marked by `GT_PING_BEGIN`).
    *   **Generic Block Processing Loop:** Reads ISIS Generic Blocks (GBH and GBlock) sequentially until a `GT_LINE_END` block is encountered.
        *   **`GT_DATA_PING_TIME`:** Updates `ping_time`.
        *   **`GT_DATA_TRANSMIT_PERIOD`, `GT_DATA_PING_LENGTH`, `GT_DATA_PING_PERIOD`:** Extracts and stores these values.
        *   **`GT_DATA_CONTROL_STATUS`:** Determines if the current data is for the port or starboard side.
        *   **`GT_ANALOGUE_SIDESCAN` / `GT_ANALOGUE_RAW`:** Extracts raw sidescan intensity data into `ss_trace`.
        *   **`GT_PRANG`:** Extracts phase range data (`the_prangs`).
        *   **`GT_DATA_ROLL`, `GT_DATA_PITCH`, `GT_DATA_HEADING`, `GT_DATA_VERT_DISP`, `GT_DATA_DEPTH`, `GT_DATA_MIS_TIMES`:** Extracts corresponding attitude and sensor data into arrays indexed by side.
        *   **`GT_FIX_LAT_LONG`:** Extracts latitude and longitude, populates a `jcu_nav_rec` structure, and writes it to the `.nav` file.
        *   **`GT_PING_END`:** This is a crucial block where data accumulated during the ping is processed:
            *   **`fill_out_ss_header`:** Populates a `gloria_rec` header with time, position, attitude, and calculated pixel sizes.
            *   **`sort_out_sidescan` (for Port/Stbd):** Processes the raw 16-bit sidescan `ss_trace` data:
                *   Performs a simple bottom pick to find a `port_pick` or `stbd_pick` (leading edge of return).
                *   Converts the 16-bit data to 8-bit using a square root scaling (`(unsigned char)(sqrt((double)ss_trace[type][i] + 32768.0))`).
                *   Downsamples the data (averages 6 samples) into 512-pixel GLORIA format.
                *   Writes the processed 8-bit traces to `.trace` file.
            *   **`sort_out_prangs`:** Processes PRANG data to derive bathymetry:
                *   Determines `phase_start_time` from PRANG.
                *   Calculates `angle`, `range`, `across`, and `depth` from PRANG data.
                *   Corrects angle for `data_roll`.
                *   Validates PRANG data based on `ss_trace` threshold, `phase_start_time`, and `PAST_REVERB`.
                *   Populates `ibeams` (ISIS_intermed_struct) with summed range, amplitude, and count for each angle bin.
                *   Fills `raw_prof` and `cln_prof` (GLORIA-like depth images).
            *   **`write_out_swath`:** If `omg_flag` is set and `side` is STBD (indicating a complete swath):
                *   Populates `OMG_HDCS_profile_header` and `OMG_HDCS_beam` structures using the processed attitude, position, and `ibeams` data.
                *   Writes these structures to the `.omg.merged` file.
                *   Writes the 8-bit sidescan data to `.raw_ss` and `.the_ss` files.
                *   Writes the depth profiles to `.zfish` and `.ztot` files.
5.  **Loop Termination:** Continues until `GT_LINE_END` block for the current file or EOF is reached.
6.  **File Closing:** All opened files are closed.
