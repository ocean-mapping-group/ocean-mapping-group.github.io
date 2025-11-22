---
layout: default
title: xtf2glo
parent: XTF Tools
grand_parent: sidescan
nav_order: 4
---
# xtf2glo

## Description
`xtf2glo` is a utility designed to convert XTF (Extended Triton Format) sidescan data into the JCU GLORIA format. It processes various XTF header types, extracting sonar data (typically high-frequency, low-frequency, and optionally sub-bottom profiles). The tool offers options for logarithmic or linear scaling of intensity values, byte swapping for endianness correction, and side swapping for correct port/starboard orientation. It also extracts and logs any raw serial data found in the XTF stream.

## Usage
```bash
xtf2glo [-havesub] [-swapside] [-swapbyte] [-log] [-addISIStime] [-otherdt] [-min16bitval <value>] [-max16bitval <value>] -in <infile> -out <outfile_prefix>
```

## Arguments

| Option | Description |
|---|---|
| `-havesub` | If specified, the tool will attempt to extract sub-bottom profile data and write it to a separate output file (`.sub_ss`). |
| `-swapside` | If specified, port and starboard sides will be swapped during conversion. |
| `-swapbyte` | If specified, byte swapping will be performed on multi-byte values. This is typically needed when the XTF file's endianness differs from the processing system's. |
| `-log` | Activates logarithmic scaling of intensity values. |
| `-addISIStime` | When extracting raw serial data, adds an ISIS-style timestamp to the beginning of each serial string. |
| `-otherdt` | Uses an alternative method for calculating the raw time sample, potentially for different XTF data types. |
| `-min16bitval <value>` | Specifies the minimum 16-bit value for linear scaling. Used with non-logarithmic scaling. | `0` |
| `-max16bitval <value>` | Specifies the maximum 16-bit value for linear scaling. Used with non-logarithmic scaling. | `65535` |
| `-in <infile>` | **Required.** The input XTF data file. |
| `-out <outfile_prefix>` | **Required.** The prefix for the output JCU GLORIA files. The tool will generate: `<outfile_prefix>.hig_ss` (high-frequency sidescan), `<outfile_prefix>.low_ss` (low-frequency sidescan), and `<outfile_prefix>.serial` (ASCII serial data). If `-havesub` is used, also `<outfile_prefix>.sub_ss`. |

## How It Works
1.  **Initialization and Argument Parsing:** The tool sets up parameters for scaling, byte swapping, and output file prefixes based on command-line arguments. It also initializes `logval` and `loglut` arrays if logarithmic scaling is enabled.
2.  **File Opening:** Opens the input XTF file and creates multiple output files for high-frequency sidescan (`.hig_ss`), low-frequency sidescan (`.low_ss`), raw serial data (`.serial`), and optionally sub-bottom profile (`.sub_ss`).
3.  **Read XTF File Header:** Calls `readXTFheader` (from `xtf_funcs.c`) to read and convert the XTF file header into a structured `XTFFILEHEADER` object.
4.  **Process XTF Data Packets (Main Loop):**
    *   It enters a loop, continuously reading XTF data packets using `readXTFdata` (from `xtf_funcs.c`).
    *   **Packet Type Handling:** A `switch` statement handles different `HeaderType`s:
        *   **`XTF_HEADER_SONAR`:** This is the primary data type for sidescan.
            *   Calls `conv_to_jcuglo` to process the sonar data.
            *   Writes the resulting high-frequency (`higrec`) and low-frequency (`lowrec`) GLORIA records to their respective files.
            *   If `-havesub` is enabled, also writes `subrec`.
        *   **`XTF_HEADER_RAW_SERIAL`:** Calls `strip_out_serial` to extract and process raw ASCII serial data, which is then written to the `.serial` file. If `-addISIStime` is specified, a timestamp is prepended to the serial string.
        *   Other header types (Attitude, Bathy, etc.) are recognized and their counts incremented, but their data is not further processed into GLORIA records in this specific implementation.
    *   **Error Handling:** `readXTFdata` includes logic to skip corrupted records and attempt to resynchronize the file pointer.
5.  **`conv_to_jcuglo` Function:**
    *   Takes the XTF `buffer`, `FileHead`, and pointers to GLORIA records (`higrec`, `lowrec`, `subrec`).
    *   It converts the XTF Ping Header (`cXTFPINGHEADER`) into a structured `XTFPINGHEADER` and then populates the common GLORIA header fields (time, lat, lon, altitude, heading, fishdepth) from this XTF ping header.
    *   It then iterates through each sonar channel specified in `PingHeader.NumChansToFollow`:
        *   Converts the XTF Ping Channel Header (`cXTFPINGCHANHEADER`).
        *   Reads the raw intensity data (`BytesPerSample` can be 1 or 2).
        *   Applies logarithmic (`-log`) or linear scaling to convert raw intensity to 8-bit.
        *   Averages multiple XTF samples into 512 GLORIA pixels (`avfact`).
        *   Assigns the processed 8-bit data to the `stbd_data` or `port_data` arrays of `lowrec` or `higrec` based on `ChanHeader.ChannelNumber` and `swapside`. Sub-bottom data (Channel 4) is placed in `subrec.stbd_data`.
6.  **`strip_out_serial` Function:** Extracts ASCII data from `XTFRAWSERIALHEADER` records.
7.  **Loop Termination:** The main loop continues until the end of the input file or an unrecoverable error occurs.
8.  **File Closing:** All opened files are closed.
