---
layout: default
title: Mesotech_SMB
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/Mesotech_SMB.c
category: Sonar Format Parsers & Binary I/O
related_tools:
- DDSsmb_read
module_name: Mesotech_SMB
header_path: code/subr/Mesotech_SMB.h
---

# Mesotech_SMB: Kongsberg Mesotech SM2000 / DDS9001 (.smb) Tuple Stream Parser

## Overview & Purpose
`Mesotech_SMB` (`Mesotech_SMB.c` / `Mesotech_SMB.h`) provides low-level binary synchronization and tuple framing extraction for Kongsberg Mesotech SM2000 and Defence R&D Canada (DRDC) DDS9001 `.smb` sonar data files. Written by John E. Hughes Clarke in March 2019, this module scans raw `.smb` byte streams, hunts for tuple synchronization markers, validates header fields against corruption, verifies matching header and footer payload lengths, and extracts the tuple data payload for downstream decoding.

---

## Key Data Structures & Constants

### Tuple Header & Footer Structures

```c
#define SMB_TUPLE_HEADER_SIZE 16
typedef struct {
    unsigned short Sync;        /* Synchronization word: 32768 (0x8000) */
    unsigned short SourceType;  /* Sensor/source type identifier (valid: 0..200) */
    unsigned short SourceID;    /* Sensor instance ID (valid: 0..1000) */
    unsigned short DataType;    /* Tuple payload type (e.g., 4006 for large sonar records) */
    unsigned int   DataTime;    /* Milliseconds within the day (valid: 0..86,400,000) */
    unsigned short sDataSize1;  /* 16-bit payload size (used when DataType != 4006) */
    unsigned int   iDataSize1;  /* 32-bit payload size (used when DataType == 4006, or promoted from sDataSize1) */
} SMB_Tuple_Header;

#define SMB_TUPLE_FOOTER_SIZE 4
typedef struct {
    unsigned short sDataSize2;  /* 16-bit trailing payload size check */
    unsigned int   iDataSize2;  /* 32-bit trailing payload size check */
} SMB_Tuple_Footer;
```

---

## Public Functions & Signatures

### `int jSMB_get_next_tuple_header(FILE *file, SMB_Tuple_Header *head, SMB_Tuple_Footer *foot, char *data)`
Locates, validates, and reads the next complete SMB tuple record from `file`.

#### Parameters
* `file`: Open `FILE *` stream positioned within an `.smb` binary file.
* `head`: Pointer to an `SMB_Tuple_Header` struct populated with the tuple metadata.
* `foot`: Pointer to an `SMB_Tuple_Footer` struct populated with the trailing size verification field.
* `data`: Caller-allocated buffer into which the tuple body (`head->iDataSize1` bytes) is read.

#### Algorithmic Workflow
1. **Sync Hunting (`hunt_for_sync`):** Reads 2 bytes at a time, sliding a 1-byte window forward until the 16-bit `Sync` word equals `32768` (`0x8000` in little-endian byte order).
2. **Header Parsing:** Rewinds 2 bytes to the start of the sync marker and reads `Sync`, `SourceType`, `SourceID`, `DataType`, and `DataTime`.
3. **Variable-Width Size Handling:**
   * If `head->DataType == 4006` (large acoustic/beamforming tuple), reads a 32-bit integer `iDataSize1` (4 bytes).
   * For all other `DataType` values, reads a 16-bit unsigned short `sDataSize1` (2 bytes) and assigns `head->iDataSize1 = head->sDataSize1`.
4. **Sanity & Corruption Checks:** Validates that:
   * `0 <= SourceType <= 200`
   * `0 <= SourceID <= 1000`
   * `0 <= DataType <= 10000`
   * `0 <= DataTime <= 86400000` (milliseconds in 24 hours)
   If any check fails, the header is treated as a false sync match; the file pointer advances 2 bytes past `where_we_start` and jumps back to `hunt_for_sync`.
5. **Footer Verification & Payload Read:** Seeks forward by `head->iDataSize1` bytes to read the footer size (`iDataSize2` or `sDataSize2`). If `foot->iDataSize2 == head->iDataSize1`, rewinds to the start of the payload, reads `head->iDataSize1` bytes into `data`, and advances past the footer ready for the next call.
* **Returns:** `1` upon reading a tuple header.

---

## How It Fits Into the OMG Architecture
`Mesotech_SMB` serves as the low-level transport/framing layer for `.smb` sonar logs. It is used directly by `code/M3/DDSsmb_read.c` (`DDSsmb_read`), which decodes the extracted tuple payloads (`data`) into OMG HDCS bathymetry and water-column structures.
