---
layout: default
title: Klein Sonar Data Format — SDF (sdf)
parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 10
has_children: true
---

# SDF Tools

The **SDF (Klein Sonar Data Format)** toolset provides utilities for inspecting and converting Klein Sidescan and HydroChart Interferometric Bathymetry `.sdf` files (including Klein 3500, 5000, 5000 V2 / HydroChart 5000, and 5900 series systems) into OMG-HDCS and JCU GLORIA formats.

## Tool Summary

| Tool | Category | Description |
| :--- | :--- | :--- |
| [`sdfTool`](sdfTool.html) | Diagnostics | Scans a Klein `.sdf` file, validates SDF record headers, and reports counts of page versions (`5902`, `5911`, `5910`, `5920`, etc.). |
| [`sdf2omg`](sdf2omg.html) | Bathymetry & Sidescan | Converts Klein HydroChart (`5004`) and Klein 5900 (`5911`, `5902`, `5910`, `5920`, `3501`, `3502`) records into a 1000-beam binned OMG-HDCS v4 `.merged` file, Greensea `.orientation`, and multi-channel JCU GLORIA sidescan/nav files. |
| [`sdf2nav`](sdf2nav.html) | Navigation Extraction | Extracts POS/MV Group 102 navigation records embedded in Klein `.sdf` files into a binary OMG `.nav` file. |
| [`sdf2orientation`](sdf2orientation.html) | Attitude Extraction | Extracts POS/MV Group 102 roll, pitch, heave, and heading records embedded in Klein `.sdf` files into a binary OMG `.orientation` file. |

## Typical SDF Unraveling Workflow

1. **Inspect SDF Record Inventory:**

   ```bash
   sdfTool -v -in line01.sdf
   ```
2. **Convert Bathymetry, Sidescan, Attitude, and Navigation:**

   ```bash
   sdf2omg -bin 0.20 -sdf line01.sdf -omg line01
   sdf2nav -sdf line01.sdf -nav line01
   sdf2orientation -sdf line01.sdf -orientation line01
   ```
