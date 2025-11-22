---
layout: default
title: addheader
parent: Merge Tools
grand_parent: sidescan
nav_order: 1
---
# addheader

## Description
`addheader` is a utility designed to manipulate JCU-GLORIA format files. It can operate in two primary modes:
1.  **Add Header:** Adds a JCU-GLORIA header to a raw 1024-byte image file, populating header fields such as altitude, time, ping rate, and pixel size based on user-defined parameters.
2.  **Subtract Header (Extract Image):** Extracts the raw 1024-byte image data from an existing JCU-GLORIA file, effectively removing the header.

## Usage
**Adding a header:**
```bash
addheader imagefile merfile [-ping <rate>] [-pixel_size <size>] [-shallow <depth>] [-deep <depth>]
```
**Subtracting a header (Extracting image data):**
```bash
addheader -sub imagefile merfile
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-sub` | Activates the "subtract header" mode, where the raw image data is extracted from the input GLORIA file. | (None) |
| `-ping <rate>` | Specifies the ping rate (in seconds) to be written into the new GLORIA header. | `30` |
| `-pixel_size <size>` | Specifies the pixel size (in units, e.g., meters) to be written into the new GLORIA header. | `45` |
| `-shallow <depth>` | Specifies the shallowest altitude to be used in calculating header altitude. Used in conjunction with `-deep` to linearly vary altitude across records. | (None) |
| `-deep <depth>` | Specifies the deepest altitude to be used in calculating header altitude. Used in conjunction with `-shallow` to linearly vary altitude across records. | (None) |
| `imagefile` | **Required.** In "add header" mode, this is the input raw 1024-byte image file. In "subtract header" mode, this is the output raw 1024-byte image file. | |
| `merfile` | **Required.** In "add header" mode, this is the output JCU-GLORIA file. In "subtract header" mode, this is the input JCU-GLORIA file. | |

## How It Works
The tool's behavior depends on the presence of the `-sub` flag.

**Mode 1: Add Header (No `-sub` flag)**
1.  **Header Initialization:** A `jcu_all_rec` structure (`header`) is initialized with default or user-specified values for `time`, `centisecs`, `lat`, `lon`, `azi`, `cb_depth`, `cb_offset`, `fishdepth`, `pixel_size`, and `ping_rate`.
2.  **Process Image File:** The tool reads the `imagefile` (raw 1024-byte image data) record by record.
3.  **Dynamic Header Fields:** For each 1024-byte image block:
    *   `header.altitude` is calculated by linearly interpolating between `shallow` and `deep` values based on the record count.
    *   `header.time` is incremented by `ping`.
4.  **Write GLORIA Record:** The populated `header` and the 1024-byte image data from `imagefile` are written sequentially to the `merfile` (JCU-GLORIA format).

**Mode 2: Subtract Header (with `-sub` flag)**
1.  **Process GLORIA File:** The tool reads the `merfile` (JCU-GLORIA format) record by record.
2.  **Extract Image Data:** For each GLORIA record:
    *   It skips the `sizeof(jcu_all_rec)` bytes (the header portion).
    *   It reads the subsequent 1024 bytes (the image data).
    *   The 1024-byte image data is then written to the `imagefile`. A byte-swapping operation (`*(swap_rec + (1023 - i)) = *(raw_rec + sizeof (jcu_all_rec) + i);`) appears to be applied during extraction, reversing the byte order of the image data.
