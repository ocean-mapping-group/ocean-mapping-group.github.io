---
layout: default
title: dbfdump
parent: Shapelib GIS Library & Tools (shapelib-1.3.0a2)
nav_order: 3
tool_name: dbfdump
source_path: code/shapelib-1.3.0a2/dbfdump.c
category: GIS & ESRI Shapefile Library / Tools
input_formats: [".dbf (xBase attribute table)"]
output_formats: ["STDOUT tabular / multiline attribute dump"]
related_tools: ["dbfcreate", "dbfadd", "dbfopen", "shpdump", "shputils"]
---

# dbfdump

## Overview

`dbfdump` (`code/shapelib-1.3.0a2/dbfdump.c`) is a command-line inspection utility authored by Frank Warmerdam that reads an **xBase (`.dbf`)** attribute table and prints its column schema and all records to `stdout` in human-readable tabular, raw, or multi-line format.

When working with ESRI Shapefiles in hydrographic and GIS workflows (such as navigation tracklines exported by [`iNav2SHP`](../nav/iNav2SHP.md) or coastline shapefiles), `dbfdump` allows operators and shell scripts to inspect field names, native xBase column types (`C`, `N`, `F`, `L`, `D`), column widths, decimal precisions, `NULL` attribute flags, and record values directly in the terminal without opening a desktop GIS application.

---

## Usage

```bash
dbfdump [-h] [-r] [-m] <xbase_file.dbf>
```

### Command-Line Options

| Flag | Arguments | Description |
| :--- | :--- | :--- |
| `-h` | *(none)* | **Header Info**: Prints a detailed field descriptor line (`Field <i>: Type=<native>/<DBFFieldType>, Title='<name>', Width=<w>, Decimals=<d>`) for every column before printing records. |
| `-r` | *(none)* | **Raw Field Output**: Prints every attribute value as an unformatted raw string (`DBFReadStringAttribute()`) exactly as stored in the `.dbf` record buffer, bypassing numeric reformatting (`%d` / `%lf`) and `(NULL)` substitution. |
| `-m` | *(none)* | **Multiline Output**: Prints each record as a vertical block (`Record: <iRecord>` followed by one `<Title>: <Value>` line per field) instead of a horizontal space-padded table. |
| `<xbase_file.dbf>` | *(positional)* | **Required.** Path to the input `.dbf` file (opened read-only via `DBFOpen(pszFilename, "rb")`). |

### Exit Codes

| Exit Code | Condition |
| :--- | :--- |
| `0` | All records dumped cleanly and memory (`panWidth`) freed. |
| `1` | Missing filename (`pszFilename == NULL`); prints usage help. |
| `2` | `DBFOpen(pszFilename, "rb")` failed (returned `NULL`). |
| `3` | Table contains zero fields (`DBFGetFieldCount(hDBF) == 0`: `"There are no fields in this table!"`). |

---

## Internal Execution Flow & Formatting Logic

1. **Schema Inspection (`-h`)**:
   - Loops over `0 .. DBFGetFieldCount(hDBF) - 1`, calling `DBFGetNativeFieldType(hDBF, i)` (which returns the raw xBase character code `'C'`, `'N'`, `'F'`, `'L'`, or `'D'`) and `DBFGetFieldInfo(hDBF, i, szTitle, &nWidth, &nDecimals)` (which returns `FTString`, `FTInteger`, `FTDouble`, `FTLogical`, or `FTInvalid`).
2. **Column Width Computation (`!bMultiLine`)**:
   - Allocates `int *panWidth` of length `DBFGetFieldCount(hDBF)`.
   - Sets each column's display width `panWidth[i] = max(strlen(szTitle), nWidth)` so that narrow numeric or flag columns are never narrower than their column title, then prints the aligned title header row (`%-<w>s` for strings, `%<w>s` for numbers).
3. **Record Iteration & Typed Formatting**:
   - Loops `for (iRecord = 0; iRecord < DBFGetRecordCount(hDBF); iRecord++)`:
     - If `!bRaw`:
       - Checks `DBFIsAttributeNULL(hDBF, iRecord, i)`. If true, prints `"(NULL)"` aligned to `nWidth`.
       - Otherwise dispatches on `eType`:
         - `FTString`: `DBFReadStringAttribute()` formatted with `%%-%ds`.
         - `FTInteger`: `DBFReadIntegerAttribute()` formatted with `%%%dd`.
         - `FTDouble`: `DBFReadDoubleAttribute()` formatted with `%%%d.%dlf`.
     - If `bRaw` (`-r`):
       - Calls `DBFReadStringAttribute(hDBF, iRecord, i)` for all field types.

---

## Example Output

```bash
$ dbfdump -h survey_lines.dbf
Field 0: Type=C/String, Title=`LINE_ID', Width=24, Decimals=0
Field 1: Type=N/Integer, Title=`JULIAN_DAY', Width=4, Decimals=0
Field 2: Type=N/Double, Title=`SPEED_KTS', Width=6, Decimals=2
LINE_ID                  JULIAN_DAY SPEED_KTS 
0001_20240409_EM2040           100   8.45     
0002_20240409_EM2040           100 (NULL)     
```
