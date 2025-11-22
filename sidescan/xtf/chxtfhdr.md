---
layout: default
title: chxtfhdr
parent: XTF Tools
grand_parent: sidescan
nav_order: 2
---
# chxtfhdr

## Description
`chxtfhdr` is a C utility library that provides functions for converting raw XTF (Extended Triton Format) binary header data into more accessible C structures. It's designed to correctly interpret XTF files by handling potential endianness differences (byte swapping) and extracting various header components, including file-level information, ping-specific details, attitude data, and channel-specific parameters. The library also offers functions to print the contents of these converted headers for inspection and debugging.

## Functions

### `void cvtChanInfo(cCHANINFO *buffer, CHANINFO *ChanInfo)`
Converts a raw `cCHANINFO` buffer to a structured `CHANINFO` object, performing byte swaps where necessary.
*   `buffer`: Pointer to the raw `cCHANINFO` data.
*   `ChanInfo`: Pointer to the `CHANINFO` structure to populate.

### `void cvtFileHeader(cXTFFILEHEADER *buffer, XTFFILEHEADER *FileHeader)`
Converts a raw `cXTFFILEHEADER` buffer to a structured `XTFFILEHEADER` object, performing byte swaps.
*   `buffer`: Pointer to the raw `cXTFFILEHEADER` data.
*   `FileHeader`: Pointer to the `XTFFILEHEADER` structure to populate.

### `void printFileHeader(XTFFILEHEADER *FileHeader)`
Prints the contents of an `XTFFILEHEADER` structure to standard output.
*   `FileHeader`: Pointer to the `XTFFILEHEADER` structure to print.

### `void cvtPingHeader(cXTFPINGHEADER *buffer, XTFPINGHEADER *PingHead)`
Converts a raw `cXTFPINGHEADER` buffer to a structured `XTFPINGHEADER` object, performing byte swaps.
*   `buffer`: Pointer to the raw `cXTFPINGHEADER` data.
*   `PingHead`: Pointer to the `XTFPINGHEADER` structure to populate.

### `void cvtAttitudeData(cXTFATTITUDEDATA *buffer, XTFATTITUDEDATA *AtData)`
Converts a raw `cXTFATTITUDEDATA` buffer to a structured `XTFATTITUDEDATA` object, performing byte swaps.
*   `buffer`: Pointer to the raw `cXTFATTITUDEDATA` data.
*   `AtData`: Pointer to the `XTFATTITUDEDATA` structure to populate.

### `void cvtNotesHeader(cXTFNOTESHEADER *buffer, XTFNOTESHEADER *Notes)`
Converts a raw `cXTFNOTESHEADER` buffer to a structured `XTFNOTESHEADER` object, performing byte swaps.
*   `buffer`: Pointer to the raw `cXTFNOTESHEADER` data.
*   `Notes`: Pointer to the `XTFNOTESHEADER` structure to populate.

### `void cvtRawSerialHeader(cXTFRAWSERIALHEADER *buffer, XTFRAWSERIALHEADER *SerialHead)`
Converts a raw `cXTFRAWSERIALHEADER` buffer to a structured `XTFRAWSERIALHEADER` object, performing byte swaps.
*   `buffer`: Pointer to the raw `cXTFRAWSERIALHEADER` data.
*   `SerialHead`: Pointer to the `XTFRAWSERIALHEADER` structure to populate.

### `void cvtPingChanHeader(cXTFPINGCHANHEADER *buffer, XTFPINGCHANHEADER *PingChanHdr)`
Converts a raw `cXTFPINGCHANHEADER` buffer to a structured `XTFPINGCHANHEADER` object, performing byte swaps.
*   `buffer`: Pointer to the raw `cXTFPINGCHANHEADER` data.
*   `PingChanHdr`: Pointer to the `XTFPINGCHANHEADER` structure to populate.

### `void printPingChanHdr(XTFPINGCHANHEADER *PingChanHdr)`
Prints the contents of an `XTFPINGCHANHEADER` structure to standard output.
*   `PingChanHdr`: Pointer to the `XTFPINGCHANHEADER` structure to print.

## How It Works
The `chxtfhdr` library functions utilize the `bytes2func` library for fundamental byte-to-data-type conversions, including endianness handling. Each `cvt*` function takes a pointer to a raw (compact) XTF header structure (prefixed with `c`) and a pointer to a "cooked" (standard) C structure. It then systematically copies individual fields from the raw buffer to the cooked structure, calling the appropriate `bytes2short`, `bytes2int`, `bytes2float`, or `bytes2double` function from `bytes2func` to ensure correct byte ordering and data interpretation. String fields are copied directly. The `print*` functions simply access and print the members of the converted structures.
