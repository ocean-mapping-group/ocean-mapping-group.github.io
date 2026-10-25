---
layout: default
title: dehypack
parent: Hypack Tools (hypack)
nav_order: 1
tool_name: dehypack
source_path: code/hypack/dehypack.c
category: Raw Data Unraveling & Format Conversion
input_formats: ["HYPACK binary-framed sonar file"]
output_formats: ["Unframed raw sonar binary file"]
related_tools: ["hypack2omg", "RTlite", "read_kmall"]
---

# dehypack

## Overview

`dehypack` (`code/hypack/dehypack.c`) is a binary stream unwrapping utility that strips 4-byte little-endian packet length headers inserted by **HYPACK** when logging raw manufacturer sonar streams to disk.

When HYPACK logs native binary sonar datagrams (such as Reson SeaBat, Kongsberg/Simrad, or Edgetech binary packets) into a raw container file, it prepends each variable-length packet with a 4-byte unsigned little-endian integer (`unsigned int offset`) specifying the byte length of the payload that immediately follows. Native manufacturer unpackers (such as `RTlite` or Reson XTF/S7K readers) expect contiguous raw datagrams without HYPACK's 4-byte framing prefix. `dehypack` iterates through the framed file, reads each 4-byte length prefix via `fread_LE_int()`, copies the exact payload block (`offset` bytes) to the output file using a dynamically growing `OMG_Buffer`, and discards the framing bytes.

---

## Usage

```bash
dehypack [-v] [-debug] -in <input_name> -out <output_name>
```

### Command-Line Options

| Flag | Arguments | Description |
| :--- | :--- | :--- |
| `-in` | `<input_name>` | **Required.** Path to the HYPACK-framed binary input file. |
| `-out` | `<output_name>` | **Required.** Path to the unwrapped binary output file. Must not be identical to `<input_name>` (enforced by an anti-clobber check). |
| `-v` | *(none)* | Increments verbosity counter (`verbose++`). |
| `-debug` | *(none)* | Increments debug level (`debug++`). |

---

## Internal Data Structures & Unwrapping Algorithm

`dehypack` relies on the dynamic buffer management API from `omg_buffer.h` (`liblocal.a`) and little-endian byte-swapping I/O from `support.h`:

| Variable / Struct | Type | Role |
| :--- | :--- | :--- |
| `inbuffer` | `OMG_Buffer` | Dynamically sized byte buffer initialized via `init_OMG_Buffer(&inbuffer)`, expanded on demand via `grow_OMG_Buffer(&inbuffer, offset)`, and freed via `free_OMG_Buffer(&inbuffer)`. |
| `offset` | `unsigned int` | 32-bit little-endian payload size (in bytes) read at the start of each HYPACK frame via `fread_LE_int(&offset, 4, 1, infile)`. |
| `file_position` | `unsigned int` | Current byte offset in `infile` (`ftell(infile)`) before reading the 4-byte length header. |
| `file_size` | `unsigned int` | Total byte length of `infile` determined at startup via `fseek(infile, 0, SEEK_END)` and `ftell(infile)`. |

### Processing Loop

1. **Anti-Clobber & File Initialization**:
   - Verifies that `inname` and `outname` are both specified and `strcmp(inname, outname) != 0` (`error("Cannot overwrite input file with output file!")`).
   - Measures total `file_size` and rewinds `infile` to byte `0`.
2. **Frame-by-Frame Extraction**:
   - Records `file_position = ftell(infile)`.
   - Reads the 4-byte little-endian frame size: `fread_LE_int(&offset, 4, 1, infile)`.
   - **Truncation Guard**: Checks `if (file_position + offset >= file_size)`. If a corrupt or partial trailing frame would read past EOF, prints `"%ld: Busting out with offset that would've put me off the end of the file (%d)"` and breaks cleanly out of the loop.
   - **Buffer Growth**: If `offset > inbuffer.size_buffer`, calls `grow_OMG_Buffer(&inbuffer, offset)`.
   - **Payload Copy**: Reads `offset` bytes from `infile` into `inbuffer.buffer` and writes `offset` bytes directly to `outfile`.
3. **Completion Summary**:
   - Prints `"Dehypacked <ftell> of <file_size> bytes"` and releases all file handles and heap buffers.

---

## Architectural Fit

In the OMG software suite, `dehypack` serves as a pre-processor whenever raw binary multibeam or sidescan data logged inside HYPACK needs to be passed to native binary decoders (as opposed to ASCII HYSWEEP `.HSX` files, which are unpacked directly by [`hypack2omg`](hypack2omg.md)).
