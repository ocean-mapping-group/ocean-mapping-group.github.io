---
layout: default
title: dbfcreate
parent: ESRI Shapefile C Library (shapelib-1.3.0a2)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 2
tool_name: dbfcreate
source_path: code/shapelib-1.3.0a2/dbfcreate.c
category: GIS & ESRI Shapefile Library / Tools
input_formats:
- CLI field schema definitions (-s, -n)
output_formats:
- .dbf (xBase table)
related_tools:
- dbfadd
- dbfdump
- dbfopen
- shpcreate
---

# dbfcreate

## Overview

`dbfcreate` (`code/shapelib-1.3.0a2/dbfcreate.c`) is a command-line utility authored by Frank Warmerdam for creating a new, empty **xBase (`.dbf`)** attribute table and defining its column schema (field names, data types, character widths, and decimal places) from command-line flags.

Every ESRI Shapefile requires a companion `.dbf` file with the same basename (e.g., `survey_lines.shp`, `survey_lines.shx`, `survey_lines.dbf`) where each geometric entity `i` in the `.shp` file corresponds to record `i` in the `.dbf` file. `dbfcreate` initializes the `.dbf` file via `DBFCreate()` and appends arbitrary sequences of string (`FTString`) and numeric (`FTDouble` / `FTInteger`) column definitions via `DBFAddField()`.

---

## Usage

```bash
dbfcreate <xbase_file.dbf> [[-s <field_name> <width>] [-n <field_name> <width> <decimals>] ...]
```

### Command-Line Options

| Flag | Arguments | Description |
| :--- | :--- | :--- |
| `<xbase_file.dbf>` | *(positional)* | **Required.** Path/basename of the `.dbf` file to create (if the `.dbf` extension is omitted, `DBFCreate()` appends `.dbf` automatically). |
| `-s` | `<field_name> <width>` | Adds an xBase Character/String (`'C'`, `FTString`) column named `<field_name>` (truncated to 10 characters in the 32-byte xBase field descriptor) with maximum string length `<width>` (`1`–`255`). |
| `-n` | `<field_name> <width> <decimals>` | Adds an xBase Numeric (`'N'`, `FTDouble` / `FTInteger`) column named `<field_name>` with total formatted character width `<width>` and `<decimals>` digits after the decimal point (use `<decimals> = 0` for integer columns). |

### Exit Codes

| Exit Code | Condition |
| :--- | :--- |
| `0` | `.dbf` file and field descriptors successfully written and closed. |
| `1` | No filename provided (`argc < 2`); prints usage string. |
| `2` | `DBFCreate(argv[1])` failed (returned `NULL`). |
| `3` | Incomplete or unrecognized command-line option (`Argument incomplete, or unrecognised:<arg>`). |
| `4` | `DBFAddField()` returned `-1` (e.g., invalid field width $\le 0$ or $> 255$). |

---

## Internal Execution Flow & Shapelib API Calls

1. **Table Initialization (`DBFCreate`)**:
   - Calls `hDBF = DBFCreate(argv[1])`, which opens `<basename>.dbf` in `"wb+"` mode, sets the default ANSI language driver (`LDID/87 = 0x57`), and marks `bNoHeader = TRUE` until fields are added.
2. **Sequential Field Definition Loop**:
   - Loops `for (i = 2; i < argc; i++)`:
     - When `strcmp(argv[i], "-s") == 0 && i < argc - 2`:
       Calls `DBFAddField(hDBF, argv[i + 1], FTString, atoi(argv[i + 2]), 0)` and advances `i += 2`.
     - When `strcmp(argv[i], "-n") == 0 && i < argc - 3`:
       Calls `DBFAddField(hDBF, argv[i + 1], FTDouble, atoi(argv[i + 2]), atoi(argv[i + 3]))` and advances `i += 3`. Note that inside `dbfopen.c`, if `nDecimals == 0`, `DBFAddField()` automatically assigns `FTInteger` (for widths $< 10$) or `FTDouble` (for widths $\ge 10$) while storing native xBase type `'N'`.
3. **Header Serialization (`DBFClose`)**:
   - Calls `DBFClose(hDBF)`, which triggers `DBFWriteHeader(hDBF)` to write the 32-byte xBase file header, all 32-byte `XBASE_FLDHDR_SZ` field descriptors, and the `0x0d` header terminator byte.

---

## Example Workflow

```bash
# Create an empty shapefile and matching .dbf table for multibeam survey bounds
shpcreate survey_bounds polygon
dbfcreate survey_bounds.dbf \
    -s SURVEY_ID 20 \
    -n YEAR 4 0 \
    -n JDAY 3 0 \
    -n MIN_DEPTH 8 2 \
    -n MAX_DEPTH 8 2

# Inspect the newly created schema
dbfdump -h survey_bounds.dbf
```

---

## Architectural Fit

`dbfcreate` is the standard CLI schema initializer in `code/shapelib-1.3.0a2/`, paired with [`shpcreate`](shpcreate.html), [`dbfadd`](dbfadd.html), and [`dbfdump`](dbfdump.html) for command-line shapefile generation and inspection.
