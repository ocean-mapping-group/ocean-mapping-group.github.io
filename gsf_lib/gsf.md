---
layout: default
title: gsf
parent: GSF Library (gsf_lib)
nav_order: 1
tool_name: gsf
source_path: code/gsf_lib/gsf.c
category: GSF Library Module
input_formats: [".gsf", ".ndx"]
output_formats: [".gsf", ".ndx"]
related_tools: ["gsf_dec", "gsf_enc", "gsf_indx", "gsf_info", "omg2gsf", "gsf2omg_7101", "gsftest"]
---

# gsf (`gsf.c` / `gsf.h`)

## Overview
`gsf.c` implements the primary public API for the Generic Sensor Format (`libgsf`) C library. It manages the internal `GSF_FILE_TABLE` for up to `GSF_MAX_OPEN_FILES` simultaneous file descriptors, handles buffered and unbuffered file opening, dispatches sequential and indexed record reads/writes, manages dynamic memory allocation for ping arrays, and translates `KEY=VALUE` processing parameters into structured `gsfMBParams` records.

## Key Public Functions

| Function | Signature / Purpose |
| :--- | :--- |
| `gsfOpen` / `gsfOpenBuffered` | `int gsfOpen(const char *filename, int mode, int *handle)` — Opens a `.gsf` file in `GSF_READONLY`, `GSF_UPDATE`, `GSF_CREATE`, `GSF_APPEND`, `GSF_READONLY_INDEX`, or `GSF_UPDATE_INDEX` mode. |
| `gsfClose` | `int gsfClose(int handle)` — Flushes buffers, closes open `.gsf` and `.ndx` descriptors, and frees internal file table buffers. |
| `gsfRead` | `int gsfRead(int handle, int desired_record, gsfDataID *data_id, gsfRecords *rec, void *stream, int max_size)` — Reads and decodes either the next sequential record (`GSF_NEXT_RECORD`) or a specific indexed record type/number. |
| `gsfWrite` | `int gsfWrite(int handle, gsfDataID *id, gsfRecords *rec)` — Encodes a `gsfRecords` structure into a 4-byte-padded GSF byte stream, optionally computes a checksum, and writes it to disk. |
| `gsfSeek` | `int gsfSeek(int handle, int option)` — Repositions the file pointer (`GSF_REWIND`, `GSF_END_OF_FILE`, `GSF_PREVIOUS_RECORD`). |
| `gsfPutMBParams` / `gsfGetMBParams` | Converts between structured `gsfMBParams` (installation offsets, compensation flags, vertical datum) and `GSF_RECORD_PROCESSING_PARAMETERS` `KEY=VALUE` strings. |
| `gsfLoadScaleFactor` / `gsfGetScaleFactor` | Configures or queries the multiplier, offset, and byte-width (`c_flag`) for compressed swath bathymetry beam array subrecords. |
| `gsfGetSwathBathyBeamWidths` | Returns nominal fore-aft and athwartship beamwidths (in degrees) for supported multibeam sonar `sensor_id` codes. |
| `gsfStringError` / `gsfPrintError` | Returns or prints human-readable descriptions of the global `gsfError` status code. |

## Usage in OMG Tools
OMG tools such as [`omg2gsf`](../gsf/omg2gsf.md), [`gsf2omg_7101`](../gsf/gsf2omg_7101.md), and [`gsftest`](../gsf/gsftest.md) include `"gsf.h"` and call `gsfOpen()`, `gsfLoadScaleFactor()`, `gsfPutMBParams()`, `gsfRead()`, `gsfWrite()`, and `gsfClose()`.
