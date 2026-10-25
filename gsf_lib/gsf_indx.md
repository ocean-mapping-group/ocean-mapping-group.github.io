---
layout: default
title: gsf_indx
parent: Embedded GSF C Library (gsf_lib)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 4
tool_name: gsf_indx
source_path: code/gsf_lib/gsf_indx.c
category: GSF Library Module
input_formats:
- .gsf
- .ndx
output_formats:
- .ndx
related_tools:
- gsf
- gsf_dec
- gsf_enc
- gsf_info
---

# gsf_indx (`gsf_indx.c` / `gsf_indx.h`)

## Overview
`gsf_indx.c` implements direct-access file indexing for `libgsf`. When a `.gsf` file is opened in `GSF_READONLY_INDEX` or `GSF_UPDATE_INDEX` mode, `gsf_indx.c` either loads an existing companion `.ndx` index file (verifying that the stored `.gsf` file size matches the current file size on disk) or scans the `.gsf` file to build a new `.ndx` file mapping every record type and 1-based record number to its exact byte offset and timestamp.

## Key Indexing Functions

| Function | Purpose |
| :--- | :--- |
| `gsfOpenIndex` | Opens or creates the companion `.ndx` file for a `.gsf` file; automatically calls `gsfCreateIndexFile()` if the `.ndx` file does not exist or `gsfAppendIndexFile()` if the `.gsf` file has grown since indexing. |
| `gsfCreateIndexFile` | Scans the entire `.gsf` file from start to finish, writing per-record-type temporary files in `$GSFTMPDIR` (or `/tmp`), then concatenates them into a single `.ndx` file with an `INDX-v02.00` header and endianness swap tag. |
| `gsfAppendIndexFile` | Seeks to the end of the previously indexed byte offset in an enlarged `.gsf` file and appends newly added records to the `.ndx` index tables. |
| `gsfCloseIndex` | Frees in-memory index lookup tables and closes the `.ndx` file descriptor. |
| `gsf_register_progress_callback` | Registers a user callback function (`GSF_PROGRESS_CALLBACK`) invoked during index creation to report completion percentage. |
