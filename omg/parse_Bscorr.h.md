---
layout: default
title: parse_Bscorr.h
parent: OMG Tools
nav_order: 48
---
# parse_Bscorr.h

## Description
`parse_Bscorr.h` is a header file that defines the data structure and utility macros used by `parse_Bscorr.c` for handling EM710 Bscorr (Backscatter Correction) files.

## Structure
```c
typedef struct EM710_Bscorr
{
  float ****BP_value;                    // 4D array to store Beam Pattern (BP) values
  float  ***sector_source_level;         // 3D array to store sector-specific source levels
  int BP_value_memory_allocated;         // Flag indicating if BP_value memory has been allocated
  int sector_source_level_memory_allocated; // Flag indicating if sector_source_level memory has been allocated
} EM710_Bscorr;
```

### `EM710_Bscorr` Members
*   `BP_value`: A 4D array of floats designed to store the beam pattern values. The dimensions typically correspond to `[mode][swath_number][sector_number][angle_index]`.
*   `sector_source_level`: A 3D array of floats to store the source levels associated with each sector, likely corresponding to `[mode][swath_number][sector_number]`.
*   `BP_value_memory_allocated`: An integer flag (boolean) to track if memory for `BP_value` has been successfully allocated.
*   `sector_source_level_memory_allocated`: An integer flag (boolean) to track if memory for `sector_source_level` has been successfully allocated.

## Macro
```c
#define round(x) ((x)>=0?(long)((x)+0.5):(long)((x)-0.5))
```
*   `round(x)`: A macro to round a floating-point number `x` to the nearest long integer. It handles both positive and negative numbers correctly.

## Purpose
This header file provides the necessary definitions for `parse_Bscorr.c` to:
*   Store parsed beam pattern and source level data in a structured manner.
*   Manage memory allocation for these multi-dimensional arrays.
*   Utilize a rounding function for angle calculations during parsing and interpolation.
