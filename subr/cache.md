---
layout: default
title: cache
parent: Core Shared Libraries (subr)
module_name: cache
source_path: code/subr/cache.c
header_path: code/subr/cache.h
category: Memory & Disk Caching Utilities
related_tools:
  - mos2
  - rasterCoords
  - s2_reader
---

# cache: Block-Based Least-Recently-Used (LRU) Disk Array Cache

## Overview & Purpose
`cache` (`cache.c` / `cache.h`) implements a block-oriented, Least-Recently-Used (LRU) virtual memory disk cache for reading and writing large 2D byte arrays (such as sidescan sonar mosaics and satellite imagery) pixel-by-pixel without triggering operating-system page thrashing or exhausting physical RAM. Originally written by Guy Carpenter at James Cook University of North Queensland (JCUNQ) in February 1990 for the OMG sidescan mosaicking suite and integrated with `JHC_header` arrays by John Hughes Clarke in December 1991, it divides an on-disk image file (including an arbitrary header offset) into fixed 1,024-byte blocks and maintains up to 1,500 active blocks in memory using a doubly linked LRU list.

---

## Key Constants & Data Structures

### Cache Sizing Constants
```c
#define CACHE_MAXBLOCKS 1500   /* Maximum number of 1 KB blocks held in memory (~1.5 MB per cache) */
#define CACHE_BLOCKSIZE 1024   /* Size of each cached file block in bytes */
```

### `cache` Structure
```c
typedef struct cache {
    int    x0, y0;        /* Pixel coordinate origin offset (default 0, 0 at lower-left) */
    int    dx, dy;        /* Array dimensions in pixels (width, height) */
    FILE  *file;          /* Backing disk file stream */
    int    blocks;        /* Total number of whole & partial 1024-byte blocks in file */
    char **index;         /* Array of pointers to in-memory block buffers (NULL if not resident) */
    int   *lrufwd;        /* Forward links for doubly linked LRU block chain */
    int   *lruback;       /* Backward links for doubly linked LRU block chain */
    int    lru;           /* Block index of the Least Recently Used resident block */
    int    mru;           /* Block index of the Most Recently Used resident block */
    int    lastblock;     /* Block index of the final (partial) block */
    int    lastblocksize; /* Byte size of the final partial block */
    int    avail;         /* Number of free memory block slots remaining (starts at CACHE_MAXBLOCKS) */
    int    header;        /* Byte length of file header preceding pixel (0,0) (e.g., sizeof(JHC_header)) */
} cache;
```

---

## Public Functions & Signatures

### Lifecycle & Origin Management
* `cache *cache_open(FILE *file, int header, int dx, int dy)`
  Initializes a `cache` descriptor for an open `FILE *file` with `header` leading bytes and dimensions `dx` $\times$ `dy` pixels. Computes the total block count `(dx * dy + header + CACHE_BLOCKSIZE - 1) / CACHE_BLOCKSIZE`, allocates the `index`, `lrufwd`, and `lruback` tables, and sets `avail = CACHE_MAXBLOCKS`.
* `void cache_setorigin(cache *c, int x0, int y0)`
  Sets the logical coordinate offset `(x0, y0)` subtracted from all subsequent `cache_read` and `cache_write` pixel coordinates.
* `void cache_flush(cache *c)`
  Writes all currently resident blocks in `c->index` back to `c->file` via `cache_writeback()`.
* `void cache_flush_clear(cache *c)`
  Flushes all resident blocks to disk, frees their heap buffers, resets `c->avail`, and clears the LRU chain (`lru = mru = -1`).
* `void cache_close(cache *c)`
  Calls `cache_flush_clear(c)`, closes `c->file`, and frees `c->index`, `c->lrufwd`, `c->lruback`, and `c`.

### Pixel-Level Read & Write Operations
* `void cache_write(cache *c, int x, int y, char z)`
  Checks if `(x, y)` lies within `[x0..x0+dx-1, y0..y0+dy-1]` (`cache_inrange`). Computes the linear byte offset `length = (x - x0) + (y - y0) * dx + header`, resolves the block index `b = length / 1024` and intra-block offset `d = length % 1024` (`cache_block`), loads block `b` into memory via `cache_load(c, b)`, and writes byte `z` at `p[d]`.
* `char cache_read(cache *c, int x, int y)`
  Validates range via `cache_inrange`, resolves `(b, d)` via `cache_block`, loads block `b` via `cache_load(c, b)`, and returns byte `p[d]` (or `0` if out of bounds).

### Internal Block & LRU Chain Management
* `char *cache_load(cache *c, int b)`
  Returns `c->index[b]` immediately if block `b` is already resident in memory. Otherwise, if `c->avail > 0`, allocates a new 1,024-byte buffer; if `c->avail == 0`, evicts the oldest block (`cache_drop(c)`), writes it to disk (`cache_writeback`), and reuses its buffer. Appends `b` to the MRU end of the LRU chain (`cache_addtolru`), seeks to `b * 1024` (`cache_seek`), and reads the block from disk.
* `char *cache_writeback(cache *c, int b)`
  Seeks to block `b` on disk, writes the buffer (`lastblocksize` bytes for the final block, `1024` bytes otherwise), clears `c->index[b] = 0`, and returns the buffer pointer for reuse or freeing.
* `int cache_drop(cache *c)`, `void cache_promote(cache *c, int b)`, `void cache_addtolru(cache *c, int b)`, `void dump_lru(cache *c)`
  Doubly linked list primitives maintaining the LRU/MRU block ordering.

---

## How It Fits Into the OMG Architecture
`cache` is used by the OMG sidescan mosaicking tools (`code/newmos/mos2.c` and `code/newmos/rasterCoords.c`) as well as `code/sdf/curray/s2_reader.c` to allow arbitrary along-track and across-track sidescan ray-tracing writes into large output mosaic rasters on disk.
