---
layout: default
title: updateArray
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: updateArray
source_path: code/grid/updateArray.c
category: gridding
input_formats:
- JHC_header (.r4_weights, .r4_weight_depth)
output_formats:
- JHC_header (.r4)
related_tools:
- weigh_grid
- addWG
- combine
---

# updateArray

## Overview

`updateArray` recomputes a final 32-bit floating-point bathymetric grid (`<prefix>.r4`) from its intermediate weighted-gridding accumulator files (`<prefix>.r4_weights` and `<prefix>.r4_weight_depth`) by dividing each cell's accumulated weighted depth sum by its accumulated weight sum (`sum_weight_depth / sum_weight`).

---

## Syntax & CLI Options

```
updateArray <prefix>
```

| Argument | Description |
|----------|-------------|
| `<prefix>` | Grid filename prefix. Reads `<prefix>.r4_weights` and `<prefix>.r4_weight_depth`, and writes `<prefix>.r4`. |

---

## How It Works

1. Opens `<prefix>.r4_weight_depth` and `<prefix>.r4_weights` for reading, and `<prefix>.r4` for writing.
2. Reads the `JHC_header` from `<prefix>.r4_weight_depth` and writes it to `<prefix>.r4`.
3. Streams through all `yno` rows (`xno` floats per row):
   - For each column `k`, if `sum_weight[k] != 0`, computes `final_data[k] = sum_weight_depth[k] / sum_weight[k]`; otherwise assigns `0.0`.
   - Writes the normalized scanline to `<prefix>.r4`.

---

## Examples

### Recompute `.r4` depths after merging or updating accumulator grids

```bash
updateArray sheet01
```

---

## Workflow Context

- **Upstream**: [`weigh_grid`](weigh_grid.html) (when run with `-save_weights`) and [`addWG`](addWG.html) (which combines multiple `.r4_weights` and `.r4_weight_depth` accumulator pairs).
- **Downstream**: `jview`, [`r4to8bit`](r4to8bit.html), [`r4toESRI`](r4toESRI.html).
