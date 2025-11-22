---
layout: default
title: test_tvg_effect
parent: Mock Tools
grand_parent: sidescan
nav_order: 15
---
# test_tvg_effect

## Description
`test_tvg_effect` is a utility designed to visualize the effect of Time-Varying Gain (TVG) on different seafloor depths as a function of range and grazing angle. It generates a 2D plot, represented as a JHC image format "table" file, which illustrates how the TVG-applied gain (in dB) changes under various depth and grazing angle conditions. This helps in understanding the compensation mechanism of the TVG function.

## Usage
```bash
test_tvg_effect [-table <tablename>] [-full]
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-table <tablename>` | Specifies the prefix for the output table file. The output file will have a `.table` extension. | `table` |
| `-full` | This flag is present but its functionality is not apparent in the provided source code. It might be a placeholder for future or debugging features. | (None) |

## How It Works
1.  **TVG Calculation:** The tool first computes a TVG curve using `tvg_shading_loss` for a ping rate of 20. This curve provides TVG values for different ranges.
2.  **Table Initialization:**
    *   A `JHC_header` (`table_head`) is set up for the output image, defining its dimensions (`dx`, `dy`) and coordinate ranges (x-axis for grazing angle, y-axis for dB gain).
    *   A 2D array `table_pointer[241][241+32]` is initialized with a default background value (16).
3.  **Iteration over Depth and Grazing Angle:**
    *   The tool iterates through various simulated grazing angles (`j` from 1 to 88 degrees).
    *   For each grazing angle, it iterates through a range of simulated seafloor depths (`i` from 500 to 3000 meters, in steps of 500 meters).
4.  **Gain Calculation:**
    *   For each combination of simulated depth and grazing angle, it calculates an `index` into the TVG array. This index represents the corresponding range.
    *   It also calculates an `index_base` for a fixed reference depth (e.g., 3000m).
    *   It retrieves the TVG gain (in dB) at `index` and `index_base` from the `tvg` array.
    *   The `gain` is then calculated as the difference between the baseline gain and the current gain (`baseline - gain`). This represents the change in TVG compensation.
5.  **Populate Table:**
    *   The calculated `gain` (converted to an 8-bit offset `gain_offset`) and the current grazing angle (`j`, converted to `angle_offset`) are used as coordinates into the `table_pointer` array.
    *   A specific pixel value (5) is written into `table_pointer[gain_offset][angle_offset]`, creating a visual representation of the TVG effect.
6.  **Output:** After calculations, the `table_head` and the populated `table_pointer` array are written to the output file (`.table`), which is a JHC image format file.
