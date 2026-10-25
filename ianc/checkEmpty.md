---
layout: default
title: checkEmpty
parent: Ian Church — Hydrodynamic & 3D Ray-Trace Suite (ianc)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 6
tool_name: checkEmpty
source_path: code/ianc/checkEmpty.c
category: Ocean Modeling & Hydrographic Utilities (ianc)
input_formats:
- OMG R4 Grid (.r4)
- OMG 8-Bit Grid (.8bit / .mos)
- OMG 16-Bit Short Grid
output_formats:
- ASCII Status (Empty / NotEmpty) and Shell Exit Code
related_tools:
- calcArea
---

# checkEmpty

## Description

`checkEmpty` is a fast shell-scripting utility that inspects an OMG/JHC raster grid file (`.r4`, `.8bit`, `.mos`, or 16-bit integer grid) to determine whether it contains any valid (non-zero, non-background) data pixels. As soon as it encounters the first valid data cell after the 1024-byte header, it prints `NotEmpty` and exits immediately with status code `1`; if the entire grid contains only no-data values (`0` or `255` for 8-bit), it prints `Empty` and exits with status code `0`.

Because it short-circuits on the very first non-empty pixel and returns distinct exit codes (`0` = Empty, `1` = NotEmpty, `2` = File open error, `3` = Missing argument), `checkEmpty` is designed for batch processing pipelines to quickly prune empty map sheets or tile outputs.

## Usage

```bash
checkEmpty <infile>
```

### Example Commands

Check whether a gridded bathymetry tile contains any data:

```bash
checkEmpty tile_042.r4
```

Use `checkEmpty` in a bash loop to move empty `.r4` or `.mos` files into an `empty/` directory:

```bash
for f in *.r4; do
    if checkEmpty "$f" > /dev/null; then
        mv "$f" empty/
    fi
done
```

## CLI Arguments and Options

| Flag / Argument | Parameters | Description |
| :--- | :--- | :--- |
| `<infile>` | `<path>` | **Required.** Path to an OMG raster file (`.r4`, `.8bit`, `.mos`, or 16-bit short grid). |

### Exit Codes

| Exit Code | Standard Output | Meaning |
| :--- | :--- | :--- |
| `0` | `Empty` | All grid cells in the file are empty/background (`0`, or `255` for 8-bit files). |
| `1` | `NotEmpty` | At least one grid cell contains valid data (`!= 0` and `!= 255`). |
| `2` | `Error opening <file>` | The specified input file could not be opened in `"rb+"` mode. |
| `3` | `Must provide input file (.r4 or .8bit or .mos)` | No input filename was supplied on the command line (`argc == 1`). |

## File Formats

### Input Format: OMG Raster Grid (`.r4`, `.8bit`, `.mos`)
* **Byte Offset `64` (`data_type`)**: `checkEmpty` seeks directly to byte offset `64` (`fseek(infile, 64, SEEK_SET)`) and reads 1 byte (`unsigned char data`) corresponding to the `data_type` field in the 1024-byte OMG `JHC_header`:
  * `data == 1`: 8-bit unsigned integer (`unsigned char`, 1 byte per pixel). Values `0` and `255` are treated as empty/no-data.
  * `data == 2`: 16-bit signed integer (`short`, 2 bytes per pixel). Value `0` is treated as empty.
  * `data == 3`: 32-bit IEEE floating-point (`float`, 4 bytes per pixel, `.r4`). Value `0.0f` is treated as empty.
* **Byte Offset `1024` (Data Payload)**: Binary array of pixels starting immediately after the 1024-byte header (`fseek(infile, 1024, SEEK_SET)`).

## How It Works

1. **File Open & Data Type Detection**: `checkEmpty` opens the first command-line argument in `"rb+"` mode. It seeks to byte `64` of the header and reads a single `unsigned char` (`data`) to identify whether pixel values are `unsigned char` (`1`), `short` (`2`), or `float` (`3`).
2. **Fast Data Scan**: The file pointer is rewound and positioned at byte `1024` (start of the raster array). Inside a `while (!feof(infile))` loop:
   * It reads one element of size `sizeof(unsigned char)`, `sizeof(short)`, or `sizeof(float)` according to `data`.
   * If `var == 255` (the 8-bit no-data sentinel), the loop continues to the next pixel.
   * If `var != 0 || varS != 0 || varF != 0`, the program immediately prints `NotEmpty\n` and returns `1` without scanning the remainder of the file.
3. **Completion**: If `feof(infile)` is reached without encountering any non-zero (and non-`255`) pixel, the program prints `Empty\n`, closes the file, and returns `0`.
