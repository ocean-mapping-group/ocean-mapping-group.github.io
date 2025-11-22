---
layout: default
title: xtf_funcs
parent: XTF Tools
grand_parent: sidescan
nav_order: 3
---
# xtf_funcs

## Description
`xtf_funcs` is a C utility library providing functions for reading and parsing data from XTF (Extended Triton Format) binary files. It enables the interpretation of XTF file headers and individual data packets (pings), supporting various `HeaderType` identifiers defined within the XTF specification. The library manages file pointers to navigate through the XTF stream and handles scenarios where expected magic numbers or record lengths are invalid, attempting to resynchronize the file read. It leverages `bytes2func.c` for byte-level conversions and `chxtfhdr.c` for structured header conversions.

## Functions

### `void readXTFheader(FILE *inf, XTFFILEHEADER *FileHead)`
Reads the initial XTF file header from the input file stream and converts it into a structured `XTFFILEHEADER` object.
*   `inf`: Pointer to the input `FILE` stream (XTF file).
*   `FileHead`: Pointer to the `XTFFILEHEADER` structure to populate.

### `int FindNextXTFPing(FILE *inf, unsigned char *buffer)`
Searches for the next XTF ping (data packet) by looking for the `0xFACE` magic number within a buffer.
*   `inf`: Pointer to the input `FILE` stream.
*   `buffer`: An `unsigned char` buffer (`BUFFER_SIZE` bytes) where data is read for searching.
*   **Returns:** `0` on success (magic number found), `0xFE0F` if EOF is reached, `0xFFFF` if magic number is not found within the buffer and new data is read.

### `int readXTFdata(FILE *inf, unsigned char *buffer)`
Reads an XTF data packet (ping) from the input file stream into a buffer, handling various `HeaderType`s and potential read errors.
*   `inf`: Pointer to the input `FILE` stream.
*   `buffer`: An `unsigned char` buffer where the entire XTF record will be stored.
*   **Returns:** The `HeaderType` of the read record on success, `0xFE0F` if EOF is reached or a read error occurs, `0xFFFF` if an invalid header is found and an attempt to resynchronize the file pointer is made.

## How It Works
1.  **`readXTFheader`:** This function directly reads `sizeof(cXTFFILEHEADER)` bytes from the input file into a raw `cXTFFILEHEADER` buffer. It then calls `cvtFileHeader` (from `chxtfhdr.c`) to convert this raw buffer into the properly structured and byte-swapped `XTFFILEHEADER`.

2.  **`FindNextXTFPing`:** This function is a low-level search utility. It's used when the expected XTF structure is broken (e.g., an invalid record length or header type). It iteratively scans through the provided `buffer` (or reads new `BUFFER_SIZE` blocks from the file if the magic number isn't found in the current buffer) looking for the `0xFACE` magic number that signifies the start of a valid XTF record. Once found, it repositions the file pointer (`fseek`) to the beginning of the detected XTF record.

3.  **`readXTFdata`:** This is the core function for reading subsequent XTF records after the file header.
    *   It first attempts to read 64 bytes, which is sufficient to determine the `HeaderType` and `NumBytesThisRecord` (total record length).
    *   It uses `bytes2int` to get the `RecLen`, applying byte-swapping if necessary.
    *   **Error Handling and Resynchronization:** If `RecLen` is invalid (zero or too large), it assumes a corrupted record, backs up the file pointer by 64 bytes, reads a larger `BUFFER_SIZE` block, and calls `FindNextXTFPing` to try and locate the next valid `0xFACE` magic number. This mechanism helps to recover from corrupted XTF streams.
    *   **Full Record Read:** If `RecLen` is valid, it reads the remaining `RecLen - 64` bytes of the record into the buffer.
    *   **Return Header Type:** It returns the `HeaderType` of the successfully read record, allowing the caller to then interpret the contents of the `buffer` based on that type.
