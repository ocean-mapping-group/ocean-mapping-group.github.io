---
layout: default
title: paster4
parent: Image Tools
nav_order: 35
tool_name: paster4
source_path: code/image/paster4.c
category: Mosaicking & Patching
input_formats: ["OMG1 32-bit float grids (.r4)"]
output_formats: ["Composite OMG1 32-bit float grid (.r4)"]
related_tools: ["pastemos", "patchArea", "subimage", "decr4"]
---

# paster4

## Description
`paster4` is the 32-bit floating-point (`data_type = 3`, `.r4`) counterpart to [`pastemos`](pastemos.md). It initializes a `cols × rows` floating-point `OMG1` (`JHC_header`) canvas and interactively prompts the user to paste either external `.r4` sub-grids or constant-value rectangular blank patches at arbitrary pixel offsets `(left_x, top_y)`.

## CLI Options & Usage
```bash
paster4 -out <outfile.r4> -rows <nrows> -cols <ncols> [-back <val>]
```
* **`-out <outfile.r4>`**: Output 32-bit float `OMG1` `.r4` file.
* **`-rows <nrows> -cols <ncols>`**: Output canvas height (`ymax`) and width (`xmax`) in cells.
* **`-back <val>`**: Initial background value for the canvas (default: `0.0`; note that `head.back` is set to `255`).

## Interactive Workflow
In an interactive loop until the user declines `Another file? (y/n)`:
1. **`Paste in blank area? (y/n)`**:
   * If `y`: Prompts for `blank value`, `left_x, top_y`, and `width, height`, filling that sub-rectangle with the constant float value.
   * If `n`: Prompts for `Input filename:` (an existing `.r4` `OMG1` file) and `left_x, top_y`, copying the sub-grid into the canvas (adopting the first pasted file's `dx`, `dy`, and `projection` into the output `JHC_header`).
2. Writes the composite `OMG1` `.r4` grid to `<outfile.r4>`.
