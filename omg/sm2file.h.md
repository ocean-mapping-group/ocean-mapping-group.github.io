---
layout: default
title: sm2file.h
parent: OMG Tools
nav_order: 63
---
# sm2file.h

## Description
`sm2file.h` is a header file that defines data structures and function prototypes for interacting with "sm2" binary data files. These files appear to be a custom format for storing records with associated timestamps and other metadata.

The header defines structures for record headers, file headers, and a file block that manages the state of an open sm2 file. It also declares several external functions for opening, reading, writing, and closing sm2 files.

## Macros
| Macro | Description |
|---|---|
| `SM2FILE` | `0` |
| `SM2eof` | `((time)0)` |
| `SM2_OPEN_ERR` | `-10` |
| `SM2_READ_ERR` | `-20` |
| `SM2_WRIT_ERR` | `-30` |
| `SM2_ERRC_MAX` | `5` |
These macros define constants related to the sm2 file format and error codes.

## Data Structures

### `sm2RecHdr` (Standard Record Header)
```c
typedef struct {
    long	rh_size;	/* record size, in bytes */
    time	rh_time;	/* record ps time (hinck) */
    } sm2RecHdr;
#define r__hdr sm2RecHdr
#define sm2TimeStamp sm2RecHdr.rh_time
```
This structure defines the header for individual records within an sm2 file.
*   `rh_size`: The size of the record in bytes.
*   `rh_time`: The timestamp of the record.

### `sm2FileHdr` (Standard File Header Record)
```c
typedef struct {
    long	fh_size;	/* header record size, in bytes */
    char	fh_type[4];	/* file type */
    char	fh_label[64];	/* file label - creator's comment area */
    long	fh_rcnt;	/* record count */
    } sm2FileHdr;
#define f__hdr sm2FileHdr
```
This structure defines the header for the entire sm2 file.
*   `fh_size`: The size of the header record in bytes.
*   `fh_type`: A 4-character string identifying the file type.
*   `fh_label`: A 64-character area for comments or a file label.
*   `fh_rcnt`: The total count of data records in the file.

### `sm2FileBlock` (File Block)
```c
typedef struct {
    int		fb_fd;		/* file descriptor */
    char	fb_name[64];	/* file name */
    int		fb_flags;	/* open flags */
    int		fb_mode;	/* create mode */
    sm2FileHdr *fb_fh;		/* file header */
    int		fb_hsiz;	/* file hdr size */
    int		fb_dsiz;	/* data record size */
    char	fb_type[4];	/* file type */
    int		fb_errc;	/* error count */
    long	fb_pos;		/* file pos */
    address	fb_rec;		/* pointer to data record */
    listCell *	fb_froot;	/* file name list head */
    listCell *	fb_flist;	/* file name list current */
    address	fb_blk1;	/* misc status block pointer */
    address	fb_blk2;	/* misc status block pointer */
    address	fb_blk3;	/* misc status block pointer */
    } sm2FileBlock;
#define f__block sm2FileBlock
#define FileBlock sm2FileBlock
```
This structure manages the state and metadata of an open sm2 file.
*   `fb_fd`: File descriptor.
*   `fb_name`: File name.
*   `fb_flags`: Open flags.
*   `fb_mode`: Creation mode.
*   `fb_fh`: Pointer to the file header.
*   `fb_hsiz`: File header size.
*   `fb_dsiz`: Data record size.
*   `fb_type`: File type.
*   `fb_errc`: Error count.
*   `fb_pos`: Current file position.
*   `fb_rec`: Pointer to the current data record.
*   `fb_froot`, `fb_flist`: Pointers for managing a list of filenames.
*   `fb_blk1`, `fb_blk2`, `fb_blk3`: Miscellaneous status block pointers.

## External Functions
The header declares several external functions (presumably implemented in `libsm2.a` or a similar library) for sm2 file operations:
*   `sm2open()`: General open function.
*   `sm2OpenList()`, `sm2Open()`, `sm2Reopen()`: Functions for opening sm2 files or lists of files.
*   `sm2SprintFileList()`: Function for formatting a file list.
*   `sm2read()`, `sm2Read()`, `sm2Read2()`, `sm2ReadN()`: Functions for reading records from sm2 files.
*   `sm2write()`, `sm2Write()`, `sm2Rewrite()`: Functions for writing or rewriting records to sm2 files.
*   `sm2close()`, `sm2Close()`, `sm2CloseUpdate()`: Functions for closing sm2 files, with an option to update.

## Dependencies
This header relies on `sm2misc.h` and `sm2list.h`, which are not provided here but likely contain definitions for `time`, `address`, and `listCell`.

## Notes
This header file is crucial for any application that needs to interact with the custom "sm2" binary file format, providing the necessary data structures and function declarations to correctly parse and manipulate these files. The use of macros for common structure names (`r__hdr`, `f__hdr`) aims to simplify code readability.