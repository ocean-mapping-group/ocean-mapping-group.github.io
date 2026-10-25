---
layout: default
title: dbfadd
parent: ESRI Shapefile C Library (shapelib-1.3.0a2)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 1
tool_name: dbfadd
source_path: code/shapelib-1.3.0a2/dbfadd.c
category: GIS & ESRI Shapefile Library / Tools
input_formats:
- .dbf (xBase table)
output_formats:
- .dbf (xBase table with appended record)
related_tools:
- dbfcreate
- dbfdump
- dbfopen
- shpadd
- shpcreate
---

# dbfadd

## Overview

`dbfadd` (`code/shapelib-1.3.0a2/dbfadd.c`) is a command-line utility authored by Frank Warmerdam for appending a single attribute record (row) to an existing **xBase (`.dbf`)** database table associated with an ESRI Shapefile.

When building shapefiles from shell scripts or batch hydrographic workflows, [`dbfcreate`](dbfcreate.html) is first used to define the attribute schema (`.dbf`), [`shpcreate`](shpcreate.html) creates the geometry files (`.shp`/`.shx`), and then each feature is added by calling [`shpadd`](shpadd.html) (to append the geometry) together with `dbfadd` (to append the corresponding attribute row at index `iRecord = DBFGetRecordCount(hDBF)`).

---

## Usage

```bash
dbfadd <xbase_file.dbf> <field_value_1> [field_value_2 ...]
```

### Positional Arguments

| Argument | Description |
| :--- | :--- |
| `<xbase_file.dbf>` | Path to an existing `.dbf` file (opened in `"r+b"` read/write binary mode via `DBFOpen()`). |
| `<field_value_1> ...` | Exact number of field values matching `DBFGetFieldCount(hDBF)`. Passing an empty string `""` for any field writes an xBase `NULL` attribute via `DBFWriteNULLAttribute()`. |

### Exit Codes

| Exit Code | Condition |
| :--- | :--- |
| `0` | Record successfully appended and flushed via `DBFClose(hDBF)`. |
| `1` | Fewer than 2 arguments supplied (`argc < 3`); prints `dbfadd xbase_file field_values`. |
| `2` | `DBFOpen(argv[1], "r+b")` returned `NULL` (file missing or permission denied). |
| `3` | Argument count mismatch: `DBFGetFieldCount(hDBF) != argc - 2` (`Got <argc-2> fields, but require <nFields>`). |

---

## Internal Execution Flow & Shapelib API Calls

1. **Database Open & Schema Validation**:
   - Calls `hDBF = DBFOpen(argv[1], "r+b")`.
   - Verifies that the number of command-line value arguments (`argc - 2`) equals the number of columns in the `.dbf` table (`DBFGetFieldCount(hDBF)`).
   - Queries the next zero-based record index at the end of the file: `iRecord = DBFGetRecordCount(hDBF)`.
2. **Type-Aware Attribute Writing Loop**:
   - Iterates `for (i = 0; i < DBFGetFieldCount(hDBF); i++)` over each column `i` and corresponding CLI argument `argv[i + 2]`:
     - **NULL Value (`strcmp(argv[i + 2], "") == 0`)**: Calls `DBFWriteNULLAttribute(hDBF, iRecord, i)` to fill the raw xBase field with spaces/asterisks indicating a null value.
     - **String Field (`DBFGetFieldInfo(hDBF, i, NULL, NULL, NULL) == FTString`)**: Calls `DBFWriteStringAttribute(hDBF, iRecord, i, argv[i + 2])`.
     - **Numeric Field (`FTInteger` or `FTDouble`)**: Parses the argument with `atof(argv[i + 2])` and calls `DBFWriteDoubleAttribute(hDBF, iRecord, i, atof(argv[i + 2]))` (which formats both integer and floating-point xBase `N`/`F` fields according to the column's width and decimal precision).
3. **Header Update & Flush**:
   - Calls `DBFClose(hDBF)` to flush the modified record buffer and update the 32-bit record count in the `.dbf` file header.

---

## Example Workflow

```bash
# 1. Create a survey line attribute table with LineID (String), JD (Integer), and Speed (Double)
dbfcreate survey_lines.dbf -s LINE_ID 24 -n JULIAN_DAY 4 0 -n SPEED_KTS 6 2

# 2. Append two survey line records (second record has NULL speed)
dbfadd survey_lines.dbf "0001_20240409_EM2040" 100 8.45
dbfadd survey_lines.dbf "0002_20240409_EM2040" 100 ""
```

---

## Architectural Fit

In the OMG software suite, `dbfadd` is built alongside the Shapelib library in `code/shapelib-1.3.0a2/` and used by shell scripts and regression tests (`stream1.sh`) to populate `.dbf` attribute tables for survey trackline shapefiles.
