---
layout: default
title: testmmap
parent: Grid Tools
tool_name: testmmap
source_path: code/grid/testmmap.c
category: gridding
input_formats: []
output_formats: ["JHC_header (.8bit)"]
related_tools: ["make_blank", "edhead"]
---

# testmmap

## Overview

`testmmap` is a diagnostic test program that creates an 8-bit `JHC_header` raster of specified dimensions (`-xlen` by `-ylen`) and tests POSIX memory-mapped I/O (`mmap`) by writing a vertical 0–255 grayscale ramp across the image buffer.

---

## Syntax & CLI Options

```
testmmap [-colorbar] [-spacing <N>] -xlen <cols> -ylen <rows> -out <outfile>
```

| Flag | Description |
|------|-------------|
| `-xlen <cols>` | Grid width in columns (`header.dx`). |
| `-ylen <rows>` | Grid height in rows (`header.dy`). |
| `-spacing <N>` | Grid spacing parameter (default: `10`). |
| `-colorbar` | Enable colorbar flag. |
| `-out <outfile>` | Output raster filename. |

---

## How It Works

1. Opens `<outfile>` for writing, maps `xlen * ylen` bytes at offset `1024` using `mmap(..., PROT_WRITE | PROT_READ, MAP_SHARED, ...)`, and writes the 1024-byte `OMG1` `JHC_header` with `dx = xlen` and `dy = ylen`.
2. Loops over each row `i = 0..ylen-1`, filling each scanline with `(unsigned char)((255.0 * i) / ylen)` and copying it into the memory-mapped region.

---

## Examples

### Test memory-mapped raster creation for a 500x500 image
```bash
testmmap -xlen 500 -ylen 500 -out ramp_test.8bit
```

---

## Workflow Context

- **Related Tools**: [`make_blank`](make_blank.html), [`edhead`](edhead.html).
