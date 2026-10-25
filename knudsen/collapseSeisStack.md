---
layout: default
title: collapseSeisStack
parent: Knudsen Tools
nav_order: 2
tool_name: collapseSeisStack
source_path: knudsen/collapseSeisStack.c
category: seismic_plotting
input_formats: [JHC_ARRAY, ASCII_PERSPECT]
output_formats: [JHC_ARRAY]
related_tools: [makeSeisPlot, makeSeisPlot_Op]
---

# collapseSeisStack

## Overview

`collapseSeisStack` composites multiple map-projected sub-bottom fence/curtain images (`JHC_header` rasters produced by [`makeSeisPlot`](makeSeisPlot) with `-map`) into a single stacked output image (`-comp`). By default, it reads the companion `<kseisfile>.perspect` file for each input image and performs z-buffer hidden-surface removal so that closer survey lines occlude farther survey lines in 3D perspective views (or performs a simple painter's overwrite when `-simple` is specified).

## Usage

```
collapseSeisStack (-v) (-simple) -comp out_filename kseisfile(s)
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-comp` | `<out_filename>` | *required* | Output composite `JHC_header` image file. |
| `<kseisfile(s)>` | `<file1> [file2 ...]` | *required* | One or more input `JHC_header` sub-bottom curtain images of identical dimensions (`dx` by `dy`). |
| `-simple` | none | `0` | Ignore `.perspect` files and composite non-zero pixels in file order (`Stack_perspect` reset to `0`). |
| `-v` | none | `0` | Enable verbose flag. |

## How It Works

1. **Header & Perspective Weight Loading**: Opens all input files, verifies that `header.dx` and `header.dy` match across every file, and (unless `-simple` is set) reads `<name[j]>.perspect` containing `dy` lines of `row_index perspective_weight` into `this_persp[j]`.
2. **Row-by-Row Z-Buffered Compositing**: Writes the output `JHC_header` and iterates through each column/trace `j = 0 .. header.dy - 1`. For each input file `i` that has non-zero perspective weight at trace `j`, reads the `header.dx`-byte vertical trace `This_trace`. For each vertical sample `k`, if `This_trace[k] != 0` and `this_persp[i][j] > Stack_perspect[k]`, updates `Stack_trace[k] = This_trace[k]` and `Stack_perspect[k] = this_persp[i][j]`.
3. **Output**: Writes each composited `Stack_trace` to the `-comp` output file.

## Practical Examples

### Composite a set of perspective sub-bottom lines using z-buffer occlusion

```bash
collapseSeisStack -comp survey_fence.i1 line01.seis line02.seis line03.seis
```
