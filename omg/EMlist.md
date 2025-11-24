---
layout: default
title: EMlist
parent: OMG Tools
nav_order: 96
---
# EMlist

## Description
`EMlist` is a low-level utility designed to parse and list the contents of raw Simrad EM multibeam telegrams (specifically EM1000 data). It reads a binary input file containing these telegrams, identifies different types of telegrams (e.g., Navigation, Depth, Sidescan), and then attempts to unpack and display key information from them.

This tool is primarily for debugging, reverse-engineering, or in-depth analysis of raw Simrad EM data streams, providing insights into the binary structure and content of the acquisition files.

## Usage
```bash
EMlist -in <infile> -out <outfile> [-v] [-recno <val>]
```

## Arguments

| Option | Description |
|---|---|
| `-in <infile>` | **Required.** The path to the input binary file containing raw Simrad EM telegrams. |
| `-out <outfile>` | **Required.** The path for the output ASCII file where extracted data will be written. |
| `-v` | Enable verbose output. |
| `-recno <val>` | (Present in `USAGE` but not implemented) This option likely suggests a record number, but its functionality is not seen in `main`. |

## How It Works
1.  **File Opening:** Opens the input binary file for reading (`-in`) and the output ASCII file for writing (`-out`).
2.  **Telegram Parsing Loop:** Reads the input file byte by byte:
    *   **STX Detection:** It searches for the Start-of-Text (STX) byte (`0x02`). Any bytes encountered before an STX are skipped.
    *   **Telegram ID:** Once an STX is found, it reads the next byte, which is the Telegram ID.
    *   **Telegram Handling (`handle_telegram`):** Based on the Telegram ID, it calls a specific handler function:
        *   `0x93`: Calls `unpack_NAV()` for Navigation telegrams.
        *   `0x97`: Calls `unpack_DEPTH()` for EM1000 Depth telegrams.
        *   `0xCA`: Prints "YO got a SIDESCAN telegram" (no dedicated unpacker implemented).
        *   Other IDs: Prints "NOT recognised".
    *   **ETX and Checksum:** After unpacking a telegram, it expects an End-of-Text (ETX) byte (`0x03`) and a 2-byte checksum. It calculates a simple sum of the telegram's bytes and compares it to the read checksum.
3.  **Telegram Unpacking Functions:**
    *   **`unpack_NAV()` (Telegram ID `0x93`):**
        *   Reads 90 bytes into an `em1000_nav` structure.
        *   Prints "would unpack nav here" (no actual unpacking code implemented beyond basic checksum).
    *   **`unpack_DEPTH()` (Telegram ID `0x97`):**
        *   Reads 692 bytes into an `em1000_depth` structure.
        *   Extracts `gyro` and `roll` values (applying `swap_short` for endianness).
        *   Loops through 60 beam structures within `em1000_depth`:
            *   Extracts `depth` for each beam (applying `swap_short`).
            *   Prints the beam depth (scaled by 50.0) to the output file.
            *   **Note:** The depths are currently outputted as a single line for each depth telegram.
4.  **`swap_short()`:** A helper function to byte-swap a `short` integer, handling endianness differences.

## Output Files
*   `<outfile>`: An ASCII file containing extracted information from recognized Simrad EM telegrams.

## Dependencies
*   `support.h`: For general utility functions.
*   `jb_endian.h`: For byte swapping.

## Notes
This tool is a low-level diagnostic utility. It has limited unpacking capabilities for specific EM1000 telegram types and primarily provides raw dumps. It's useful for understanding the binary structure of these telegrams and for debugging issues with raw acquisition files. The `recno` argument is present in the usage but not implemented in the current code.