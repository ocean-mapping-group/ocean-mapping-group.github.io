---
layout: default
title: getShifts
parent: Image Tools
nav_order: 24
tool_name: getShifts
source_path: code/image/getShifts.c
category: Image & Raster Processing
input_formats: ["OMG1 8-bit array (JHC_header)"]
output_formats: ["Stdout column shift table (col, min_y, dy - min_shift, max_y - min_y)"]
related_tools: ["subimage", "rotateimage", "pastemos"]
---

# getShifts

## Description
`getShifts` scans every column of an 8-bit `OMG1` (`JHC_header`) raster to locate the uppermost (`min_y`) and lowermost (`max_y`) valid (`!= 255`) pixels in each column, printing a 4-column ASCII shift table to standard output for compacting obliquely oriented strip mosaics.

## CLI Options & Usage
```bash
getShifts -in <infile> > shifts.txt
```
* **`-in <infile>`**: Input 8-bit `OMG1` (`JHC_header`) raster file.

## Algorithm
1. Reads the `JHC_header` (`dx = head.xmax`, `dy = head.ymax`) and loads the 8-bit image buffer.
2. For each column `i = 0 .. dx-1`, scans vertically `j = 0 .. dy-1` to find the first and last row indices (`min_y[i]`, `max_y[i]`) where `pixel != 255`, tracking the global minimum vertical span `min_shift = min(dy - min_y[i] + max_y[i])`.
3. Prints one line per valid column:
   ```text
   col_index   min_y[i]   (dy - min_shift)   (max_y[i] - min_y[i])
   ```
