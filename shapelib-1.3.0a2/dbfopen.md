---
layout: default
title: dbfopen
parent: Shapelib GIS Library & Tools (shapelib-1.3.0a2)
nav_order: 4
module_name: dbfopen
source_path: code/shapelib-1.3.0a2/dbfopen.c
category: GIS & ESRI Shapefile Library / Tools
input_formats: [".dbf", ".cpg (xBase table & codepage)"]
output_formats: [".dbf", ".cpg"]
related_tools: ["shpopen", "safileio", "dbfcreate", "dbfadd", "dbfdump", "shputils", "iNav2SHP"]
---

# dbfopen (`dbfopen.c`)

## Overview

`dbfopen.c` (`code/shapelib-1.3.0a2/dbfopen.c`, 1,857 lines, Revision 1.83) is the core C library implementation of the **Shapelib xBase (`.dbf`) Attribute Table API**, authored by Frank Warmerdam with codepage (`.cpg` / `LDID`) enhancements by Bram de Greve.

In ESRI Shapefiles, feature attributes are stored in a dBase III+ / xBase binary table (`.dbf`) where the 0-based record index `iShape` matches the 0-based shape index in the `.shp` and `.shx` files. `dbfopen.c` implements complete read/write/update access to `.dbf` headers, field descriptors, typed attributes (`FTString`, `FTInteger`, `FTDouble`, `FTLogical`), `NULL` values, record deletion flags, dynamic schema modifications (`DBFAddField` even on populated tables, `DBFDeleteField`), and codepage discovery (`DBFGetCodePage`).

---

## Core Data Structures (`shapefil.h`)

### `DBFInfo` / `DBFHandle`

```c
typedef struct
{
    SAHooks     sHooks;                 /* Abstracted file I/O and error hooks */
    SAFile      fp;                     /* Underlying .dbf file handle */
    int         nRecords;               /* Total number of records in table */
    int         nRecordLength;          /* Byte length of one record (sum of field widths + 1 delete byte) */
    int         nHeaderLength;          /* Byte offset to first record (32 + 32*nFields + 1) */
    int         nFields;                /* Number of columns */
    int         *panFieldOffset;        /* Byte offset of each field within a record */
    int         *panFieldSize;          /* Character width of each field (1..255) */
    int         *panFieldDecimals;      /* Decimal precision of numeric fields */
    char        *pachFieldType;         /* Native xBase type char ('C', 'N', 'F', 'L', 'D') */
    char        *pszHeader;             /* Raw 32*nFields byte array of field descriptors */
    int         nCurrentRecord;         /* Currently cached record index (-1 if none) */
    int         bCurrentRecordModified; /* Dirty flag for cached record */
    char        *pszCurrentRecord;      /* 1-record cache buffer (nRecordLength bytes) */
    int         nWorkFieldLength;       /* Size of pszWorkField string buffer */
    char        *pszWorkField;          /* Dynamic string return buffer for DBFReadAttribute */
    int         bNoHeader;              /* TRUE if header has not yet been written to disk */
    int         bUpdated;               /* TRUE if file metadata needs header update on close */
    double      dfDoubleField;          /* Thread-safe per-handle double return slot */
    int         iLanguageDriver;        /* Header byte 29 LDID code (default 0x57 = ANSI) */
    char        *pszCodePage;           /* Resolved codepage string (e.g. "LDID/87" or .cpg content) */
} DBFInfo;
typedef DBFInfo * DBFHandle;
```

### `DBFFieldType` Enumeration

| Enum Constant | Native xBase Code | Description |
| :--- | :--- | :--- |
| `FTString` | `'C'`, `'D'` | Character string or 8-byte `YYYYMMDD` Date string (whitespace trimmed if `TRIM_DBF_WHITESPACE` is defined). |
| `FTInteger` | `'N'`, `'F'` | Numeric field with `nDecimals == 0` and `nWidth < 10` (fits in 32-bit `int`). |
| `FTDouble` | `'N'`, `'F'` | Floating-point numeric field (`nDecimals > 0`) or wide integer (`nWidth >= 10`). |
| `FTLogical` | `'L'` | 1-byte logical/boolean field (`'T'`, `'t'`, `'Y'`, `'y'` vs `'F'`, `'f'`, `'N'`, `'n'`, `'?'`). |
| `FTInvalid` | *(other)* | Unrecognized or unsupported column type. |

---

## Public API Reference

### File Lifecycle & Codepage Functions
- `DBFOpen(const char *pszDBFFile, const char *pszAccess)` / `DBFOpenLL(..., SAHooks *psHooks)`: Opens an existing `.dbf` (and optional `.cpg`) file in `"rb"` or `"r+b"` mode, automatically stripping `.shp`/`.shx` extensions and trying both `.dbf` and `.DBF`.
- `DBFCreate(const char *pszDBFFile)` / `DBFCreateEx(..., const char *pszCodePage)` / `DBFCreateLL(...)`: Creates a new `.dbf` file (default codepage `"LDID/87"`, `0x57` ANSI) and writes an accompanying `.cpg` file if `pszCodePage` cannot be encoded as a single `LDID/<num>` byte.
- `DBFCloneEmpty(DBFHandle psDBF, const char *pszFilename)`: Creates a new `.dbf` file with the exact same field definitions and header layout as `psDBF`, but with zero records.
- `DBFUpdateHeader(DBFHandle hDBF)`: Flushes the active record cache (`DBFFlushRecord`) and updates the 32-bit little-endian record count at bytes `4..7` of the 32-byte `.dbf` header.
- `DBFClose(DBFHandle hDBF)`: Flushes any modified record and header, closes `fp`, and frees all heap buffers in `DBFInfo`.
- `DBFGetCodePage(DBFHandle psDBF)`: Returns `psDBF->pszCodePage`.

### Schema Inquiry & Manipulation Functions
- `DBFGetFieldCount(DBFHandle psDBF)` / `DBFGetRecordCount(DBFHandle psDBF)`: Returns `nFields` or `nRecords`.
- `DBFAddField(DBFHandle hDBF, const char *pszFieldName, DBFFieldType eType, int nWidth, int nDecimals)` / `DBFAddNativeFieldType(...)`: Appends a new column definition (up to 10-character uppercase name, width `1..255`). Supports adding fields even after records have already been written by expanding `pszCurrentRecord` and shifting existing records in-place on disk!
- `DBFDeleteField(DBFHandle hDBF, int iField)`: Removes column `iField`, compacts all existing records on disk, and updates field offsets.
- `DBFGetFieldInfo(DBFHandle psDBF, int iField, char *pszFieldName, int *pnWidth, int *pnDecimals)`: Retrieves the `DBFFieldType`, 11-byte null-terminated field name, width, and decimals for column `iField`.
- `DBFGetFieldIndex(DBFHandle psDBF, const char *pszFieldName)`: Case-insensitive lookup returning the 0-based column index (`-1` if not found).
- `DBFGetNativeFieldType(DBFHandle hDBF, int iField)`: Returns the raw xBase type character (`'C'`, `'N'`, `'F'`, `'L'`, `'D'`).

### Record & Attribute Read/Write Functions
- **Reading**: `DBFReadIntegerAttribute()`, `DBFReadDoubleAttribute()`, `DBFReadStringAttribute()`, `DBFReadLogicalAttribute()`, `DBFIsAttributeNULL()`, `DBFReadTuple()`.
- **Writing**: `DBFWriteIntegerAttribute()`, `DBFWriteDoubleAttribute()`, `DBFWriteStringAttribute()`, `DBFWriteLogicalAttribute()`, `DBFWriteNULLAttribute()`, `DBFWriteAttributeDirectly()`, `DBFWriteTuple()`.
- **Deletion Flags**: `DBFIsRecordDeleted(psDBF, iShape)` checks if byte `0` of record `iShape` is `'*'`; `DBFMarkRecordDeleted(psDBF, iShape, bIsDeleted)` sets byte `0` to `'*'` (deleted) or `' '` (active).

---

## Architectural Fit in OMG

`dbfopen.o` is compiled in `code/shapelib-1.3.0a2/` and linked with `shpopen.o` and `safileio.o` into OMG GIS exporters such as [`iNav2SHP`](../nav/iNav2SHP.md), which writes survey line metadata (`LINE_NAME`, timestamps, ping counts) into `.dbf` tables alongside `.shp` tracklines.
