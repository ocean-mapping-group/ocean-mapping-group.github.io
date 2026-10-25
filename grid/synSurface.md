---
layout: default
title: synSurface
parent: Grid Tools
tool_name: synSurface
source_path: code/grid/synSurface.c
category: gridding
input_formats: ["JHC_header (.r4)"]
output_formats: ["JHC_header (.r4)"]
related_tools: ["makeSynPing", "make_blank", "edhead"]
---

# synSurface

## Overview

`synSurface` is a minimal utility stub designed to open an existing 32-bit floating-point `.r4` grid (`data_type == 3`), verify and print its `JHC_header` metadata, and prepare a synthetic depth surface for use with `synSwath` / [`makeSynPing`](makeSynPing.html).

---

## Syntax & CLI Options

```
synSurface [-normal <depth>] [-reset] <r4file>
```

| Flag / Argument | Description |
|-----------------|-------------|
| `-normal <depth>` | Nominal depth value in meters (default: `100.0`). |
| `-reset` | Set reset flag. |
| `<r4file>` | Target 32-bit floating-point `.r4` file. |

---

## How It Works

1. Opens `<r4file>` in read/write mode (`"r+"`).
2. Reads and prints the `JHC_header` via `get_print_JHC_header(floatfile, 1)` and verifies `JHChead.data_type == 3`.
3. Seeks to the end of the 1024-byte `JHC_header` and closes the file.

---

## Examples

### Inspect an `.r4` surface header for synthetic swath generation
```bash
synSurface -normal 150.0 test_sheet.r4
```

---

## Workflow Context

- **Related Tools**: [`makeSynPing`](makeSynPing.html), [`make_blank`](make_blank.html).
