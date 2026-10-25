---
layout: default
title: safileio
parent: ESRI Shapefile C Library (shapelib-1.3.0a2)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 5
source_path: code/shapelib-1.3.0a2/safileio.c
category: GIS & ESRI Shapefile Library / Tools
input_formats:
- File I/O stream requests from shpopen / dbfopen
output_formats:
- POSIX stdio FILE* or Windows UTF-8 wide-char streams
related_tools:
- shpopen
- dbfopen
- shptree
module_name: safileio
---

# safileio (`safileio.c`)

## Overview

`safileio.c` (`code/shapelib-1.3.0a2/safileio.c`, 289 lines, Revision 1.4) provides the default **Shapelib Abstracted File I/O (`SAHooks`)** implementation based on standard C `stdio` (`fopen`, `fread`, `fwrite`, `fseek`, `ftell`, `fflush`, `fclose`, `remove`, `fprintf(stderr, ...)`, and `atof`), along with optional Windows UTF-8 wide-character (`_wfopen` / `_wremove`) hooks.

Introduced by Frank Warmerdam and Bram de Greve in December 2007–January 2008, `safileio.c` decouples [`shpopen.c`](shpopen.html) and [`dbfopen.c`](dbfopen.html) from direct `stdio` calls. By routing all file operations, error reporting, and floating-point string parsing through the `SAHooks` function-pointer table stored in `SHPInfo` and `DBFInfo`, applications (such as GDAL/OGR or custom virtual file systems) can override file access, support 64-bit offsets, handle UTF-8 filenames on Windows, or replace locale-sensitive `atof()` without modifying core Shapelib code.

---

## Core Data Types & `SAHooks` Structure (`shapefil.h`)

```c
typedef int *SAFile;
typedef unsigned long SAOffset;

typedef struct {
    SAFile     (*FOpen) ( const char *filename, const char *access );
    SAOffset   (*FRead) ( void *p, SAOffset size, SAOffset nmemb, SAFile file );
    SAOffset   (*FWrite)( void *p, SAOffset size, SAOffset nmemb, SAFile file );
    SAOffset   (*FSeek) ( SAFile file, SAOffset offset, int whence );
    SAOffset   (*FTell) ( SAFile file );
    int        (*FFlush)( SAFile file );
    int        (*FClose)( SAFile file );
    int        (*Remove)( const char *filename );

    void       (*Error) ( const char *message );
    double     (*Atof)  ( const char *str );
} SAHooks;
```

---

## Public & Internal Functions in `safileio.c`

| Function | Signature | Description |
| :--- | :--- | :--- |
| `SASetupDefaultHooks` | `void SHPAPI_CALL SASetupDefaultHooks(SAHooks *psHooks)` | Populates `psHooks` with the standard C `stdio` wrapper functions (`SADFOpen`, `SADFRead`, `SADFWrite`, `SADFSeek`, `SADFTell`, `SADFFlush`, `SADFClose`, `SADRemove`), `SADError`, and standard `atof`. Called automatically by `SHPOpen()`, `SHPCreate()`, `DBFOpen()`, and `DBFCreate()`. |
| `SADFOpen` | `SAFile SADFOpen(const char *pszFilename, const char *pszAccess)` | Calls `(SAFile) fopen(pszFilename, pszAccess)`. |
| `SADFRead` | `SAOffset SADFRead(void *p, SAOffset size, SAOffset nmemb, SAFile file)` | Calls `(SAOffset) fread(p, (size_t)size, (size_t)nmemb, (FILE *)file)`. |
| `SADFWrite` | `SAOffset SADFWrite(void *p, SAOffset size, SAOffset nmemb, SAFile file)` | Calls `(SAOffset) fwrite(p, (size_t)size, (size_t)nmemb, (FILE *)file)`. |
| `SADFSeek` | `SAOffset SADFSeek(SAFile file, SAOffset offset, int whence)` | Calls `(SAOffset) fseek((FILE *)file, (long)offset, whence)`. |
| `SADFTell` | `SAOffset SADFTell(SAFile file)` | Calls `(SAOffset) ftell((FILE *)file)`. |
| `SADFFlush` | `int SADFFlush(SAFile file)` | Calls `fflush((FILE *)file)`. |
| `SADFClose` | `int SADFClose(SAFile file)` | Calls `fclose((FILE *)file)`. |
| `SADRemove` | `int SADRemove(const char *filename)` | Calls `remove(filename)` (used by `DBFDeleteField` when replacing temporary files). |
| `SADError` | `void SADError(const char *message)` | Writes error messages to `stderr` via `fprintf(stderr, "%s\n", message)`. |
| `SASetupUtf8Hooks` *(Windows only)* | `void SHPAPI_CALL SASetupUtf8Hooks(SAHooks *psHooks)` | Available when `SHPAPI_UTF8_HOOKS` (`_WIN32`) is defined; binds `FOpen` to `SAUtf8WFOpen` and `Remove` to `SAUtf8WRemove`, converting UTF-8 filenames to `wchar_t` via `Utf8ToWideChar()` (`MultiByteToWideChar(CP_UTF8, ...)`). |

---

## Architectural Fit in OMG

When linking any OMG tool against Shapelib 1.3.0a2 (`shpopen.o` and `dbfopen.o`), `safileio.o` **must** also be linked because `SHPOpen`, `SHPCreate`, `DBFOpen`, and `DBFCreate` call `SASetupDefaultHooks()` defined in `safileio.c`.
