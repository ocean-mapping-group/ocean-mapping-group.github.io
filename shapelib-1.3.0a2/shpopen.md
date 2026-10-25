---
layout: default
title: shpopen
parent: ESRI Shapefile C Library (shapelib-1.3.0a2)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 9
source_path: code/shapelib-1.3.0a2/shpopen.c
category: GIS & ESRI Shapefile Library / Tools
input_formats:
- .shp
- .shx (ESRI Shapefile geometry & index)
output_formats:
- .shp
- .shx
related_tools:
- dbfopen
- shptree
- safileio
- shpcreate
- shpadd
- shpdump
- shprewind
- iNav2SHP
module_name: shpopen
---

# shpopen (`shpopen.c`)

## Overview

`shpopen.c` (`code/shapelib-1.3.0a2/shpopen.c`, 2,369 lines, Revision 1.59) is the core C library implementation of the **Shapelib ESRI Shapefile (`.shp` / `.shx`) Geometry Read/Write API**, authored by Frank Warmerdam.

An ESRI Shapefile consists of a variable-length binary geometry file (`.shp`, with big-endian record headers and little-endian IEEE-754 double coordinates) paired with a fixed-record-length index file (`.shx`, containing a 100-byte header followed by 8-byte big-endian `[offset_in_16bit_words, content_length_in_16bit_words]` entries for each shape). `shpopen.c` automatically detects host CPU endianness (`bBigEndian`), performs all required big/little-endian word swapping (`SwapWord`), manages `.shx` offset tables (`panRecOffset`, `panRecSize`), computes 4D `(X, Y, Z, M)` bounding envelopes (`SHPComputeExtents`), validates/rewinds polygon ring orientations (`SHPRewindObject`), and reads/writes all 14 ESRI shape types (`SHPT_NULL` through `SHPT_MULTIPATCH`).

---

## Core Data Structures (`shapefil.h`)

### `SHPInfo` / `SHPHandle`

```c
typedef struct
{
    SAHooks       sHooks;          /* File I/O and error hook table (safileio.c) */
    SAFile        fpSHP;           /* Open .shp file handle */
    SAFile        fpSHX;           /* Open .shx file handle (closed after load in read-only mode) */
    int           nShapeType;      /* Layer shape type (SHPT_*) */
    int           nFileSize;       /* Current .shp file size in bytes */
    int           nRecords;        /* Number of shapes in layer */
    int           nMaxRecords;     /* Allocated capacity of panRecOffset / panRecSize */
    int           *panRecOffset;   /* Byte offset of each shape in .shp (from .shx) */
    int           *panRecSize;     /* Content byte size of each shape in .shp (from .shx) */
    double        adBoundsMin[4];  /* Layer-wide [Xmin, Ymin, Zmin, Mmin] */
    double        adBoundsMax[4];  /* Layer-wide [Xmax, Ymax, Zmax, Mmax] */
    int           bUpdated;        /* Dirty flag triggering SHPWriteHeader() on close */
    unsigned char *pabyRec;        /* Per-handle scratch record I/O buffer */
    int           nBufSize;        /* Current byte size of pabyRec */
} SHPInfo;
typedef SHPInfo * SHPHandle;
```

### `SHPObject` (In-Memory Geometry Feature)

```c
typedef struct
{
    int     nSHPType;        /* Shape type (SHPT_POINT, SHPT_ARC, SHPT_POLYGON, etc.) */
    int     nShapeId;        /* 0-based shape index (-1 for newly created/unassigned) */
    int     nParts;          /* Number of rings/parts (0 for Point/MultiPoint) */
    int     *panPartStart;   /* Starting vertex index of each part [0..nParts-1] */
    int     *panPartType;    /* Part type (SHPP_RING, SHPP_OUTERRING, etc. for MultiPatch) */
    int     nVertices;       /* Total number of vertices */
    double  *padfX;          /* X coordinate array [nVertices] */
    double  *padfY;          /* Y coordinate array [nVertices] */
    double  *padfZ;          /* Z coordinate array [nVertices] (0.0 if 2D) */
    double  *padfM;          /* Measure array [nVertices] (0.0 if unused) */
    double  dfXMin, dfYMin, dfZMin, dfMMin;
    double  dfXMax, dfYMax, dfZMax, dfMMax;
    int     bMeasureIsUsed;  /* TRUE if M values are present and > -1e38 */
} SHPObject;
```

---

## Public API Reference

| Function | Signature / Description |
| :--- | :--- |
| `SHPOpen` / `SHPOpenLL` | `SHPHandle SHPOpen(const char *pszShapeFile, const char *pszAccess)`: Opens `<basename>.shp` and `<basename>.shx` (`"rb"` or `"r+b"`), reads the 100-byte header and `.shx` offset table into `panRecOffset`/`panRecSize`, and closes `fpSHX` immediately if opened read-only. |
| `SHPCreate` / `SHPCreateLL` | `SHPHandle SHPCreate(const char *pszShapeFile, int nShapeType)`: Creates a new `.shp` and `.shx` file pair with initial 100-byte headers, then reopens them via `SHPOpenLL(..., "r+b", psHooks)`. |
| `SHPGetInfo` | `void SHPGetInfo(SHPHandle hSHP, int *pnEntities, int *pnShapeType, double *padfMinBound, double *padfMaxBound)`: Queries any non-`NULL` output pointers for shape count, shape type, and 4D bounds. |
| `SHPCreateObject` | `SHPObject *SHPCreateObject(int nSHPType, int nShapeId, int nParts, const int *panPartStart, const int *panPartType, int nVertices, const double *padfX, const double *padfY, const double *padfZ, const double *padfM)`: Allocates and populates a full `SHPObject` and computes its bounding box via `SHPComputeExtents()`. |
| `SHPCreateSimpleObject` | `SHPObject *SHPCreateSimpleObject(int nSHPType, int nVertices, const double *padfX, const double *padfY, const double *padfZ)`: Convenience wrapper around `SHPCreateObject()` for single-part shapes without measures. |
| `SHPComputeExtents` | `void SHPComputeExtents(SHPObject *psObject)`: Recomputes `dfXMin..dfMMax` from `padfX..padfM`. |
| `SHPWriteObject` | `int SHPWriteObject(SHPHandle hSHP, int iShape, SHPObject *psObject)`: Serializes `psObject` to `.shp`, updates `.shx` offset/size arrays (`iShape == -1` appends; `iShape >= 0` overwrites or extends file), updates global layer bounds, and returns the written `iShape` ID. |
| `SHPReadObject` | `SHPObject *SHPReadObject(SHPHandle hSHP, int hEntity)`: Seeks to `panRecOffset[hEntity]` in `.shp`, decodes the geometry record into a newly allocated `SHPObject`, and returns it. |
| `SHPRewindObject` | `int SHPRewindObject(SHPHandle hSHP, SHPObject *psObject)`: Checks polygon ring winding order (point-in-polygon test + signed area check: outer rings clockwise, inner holes counter-clockwise), reverses offending rings in-place, and returns the count of altered rings. |
| `SHPDestroyObject` | `void SHPDestroyObject(SHPObject *psObject)`: Frees a `SHPObject` and all its coordinate/part arrays. |
| `SHPWriteHeader` / `SHPClose` | `SHPWriteHeader()` writes updated 100-byte headers and the entire `.shx` index array to disk; `SHPClose()` calls `SHPWriteHeader()` if `bUpdated` is true and frees `SHPInfo`. |
| `SHPTypeName` / `SHPPartTypeName` | Returns human-readable strings for `SHPT_*` (e.g., `"PolygonZ"`) and `SHPP_*` (e.g., `"OuterRing"`). |

---

## Architectural Fit in OMG

`shpopen.o` is compiled in `code/shapelib-1.3.0a2/` and linked into OMG navigation and GIS tools (such as [`iNav2SHP`](../nav/iNav2SHP.html)) to export multibeam vessel tracklines directly as `SHPT_ARC` shapefiles.
