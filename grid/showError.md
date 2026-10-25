---
layout: default
title: showError
parent: Grid Tools
tool_name: showError
source_path: code/grid/showError.c
category: gridding
input_formats: ["JHC_header (.r4)", "OMG HDCS (.merged)"]
output_formats: ["JHC_header (.8bit)"]
related_tools: ["weigh_grid", "stat_grid", "grid_stats"]
---

# showError

## Overview

`showError` reads the geographic/Mercator dimensions from a reference `.r4` mapsheet and scans one or more OMG HDCS `.merged` multibeam survey files to produce an 8-bit raster (`<out_count.8bit>`) counting the number of **rejected/flagged beams** (`status != 0`) that fall within each grid cell.

---

## Syntax & CLI Options

```
showError [-low <val>] <ref_merc.r4> <out_count.8bit> <merged_files...>
```

| Flag / Argument | Description |
|-----------------|-------------|
| `-low <val>` | Optional minimum value parameter (parsed as float). |
| `<ref_merc.r4>` | Reference `.r4` mapsheet defining the Mercator (`projection == 1`, `ellipsoid == 1`) grid geometry. |
| `<out_count.8bit>` | Output 8-bit raster file recording the per-cell count of flagged/rejected soundings (`0..255`). |
| `<merged_files...>` | One or more OMG HDCS `.merged` multibeam files to scan. |

---

## How It Works

1. **Reference Grid Initialization**:
   - Reads the `JHC_header` from `<ref_merc.r4>` and verifies that it uses a Mercator projection (`projection == 1`) on the WGS84 ellipsoid (`ellipsoid == 1`).
   - Allocates a zero-initialized `Dx * Dy` byte buffer (`bbuf`) and sets `head.data_type = 1` (8-bit unsigned) with `zmin = 0.0` and `zmax = 255.0`.
2. **Flagged Sounding Accumulation**:
   - Loops through every supplied `.merged` file (`get_merged_summary`, `get_merged_Nav`, `read_merged_file`, `unpack_merged_record`).
   - For every ping with valid navigation (`nav_status == 0`) and valid soundings (`beams_ok`), inspects each beam `j`.
   - Whenever a beam is **flagged as rejected** (`beams[j].status != 0`), projects its geographic position to Mercator `(X, Y)` grid indices via `mercat` and increments the corresponding cell (`*(bbuf + Y * Dx + X) += 1`).
3. **Output**:
   - Writes the updated `JHC_header` and 8-bit hit-count array to `<out_count.8bit>`.

---

## Examples

### Generate an 8-bit density map of rejected multibeam soundings across a survey sheet
```bash
showError sheet01.r4 sheet01_rejected_counts.8bit line01.merged line02.merged line03.merged
```

---

## Workflow Context

- **Upstream**: `swathEd` (interactive swath editor that sets beam rejection flags in `.merged` files) and [`weigh_grid`](weigh_grid.html).
- **Downstream**: `jview` (to visualize spatial concentrations of noisy or over-edited beams).
