---
layout: default
title: JSF Tools
nav_order: 11
has_children: true
---

# JSF Tools

The **JSF (EdgeTech Sonar Data Format)** toolset provides utilities for inspecting and converting EdgeTech Interferometric / Bathymetric Sidescan and Sub-Bottom Profiler `.jsf` files (such as EdgeTech 4600, 6205, and 2205 AUV/UUV payloads) into OMG-HDCS and JCU GLORIA formats.

## Tool Summary

| Tool | Category | Description |
| :--- | :--- | :--- |
| [`jsfTool`](jsfTool.md) | Diagnostics | Scans an EdgeTech `.jsf` file, prints message type inventories, and dumps decoded message structures (`80`, `2020`, `3000`, `3001`, `3002`, `3004`). |
| [`jsf2omg`](jsf2omg.md) | Bathymetry Conversion | Converts EdgeTech JSF Bathymetric (message 3000) and Pressure/Sound Speed (message 3002) records into a 1000-beam binned OMG-HDCS v4 `.merged` file. |
| [`jsf2glo`](jsf2glo.md) | Sidescan & Sub-Bottom | Converts EdgeTech JSF Sonar Data (message 80/82) and Situation (message 2090) records into low-frequency (`.low_ss`), high-frequency (`.hig_ss`), and sub-bottom (`.subb`) JCU GLORIA files (plus optional `.merged` files). |
| [`jsf2nav`](jsf2nav.md) | Navigation Extraction | Extracts JSF Position messages (type 3004) into a binary OMG `jcu_nav_rec` (`.nav`) file. |
| [`jsf2orientation`](jsf2orientation.md) | Attitude Extraction | Extracts JSF Attitude messages (type 3001) into binary OMG-HDCS `.orientation` (roll/pitch/heave) and `.heading` files. |

## Typical JSF Unraveling Workflow

1. **Inspect JSF Message Inventory:**
   ```bash
   jsfTool -contents -in survey_line.jsf
   ```
2. **Convert Interferometric Bathymetry, Attitude, and Navigation:**
   ```bash
   jsf2omg -bin 0.25 -min_qf 0.7 -jsf survey_line.jsf -omg survey_line
   jsf2orientation -jsf survey_line.jsf -orientation survey_line
   jsf2nav -jsf survey_line.jsf -nav survey_line
   ```
3. **Convert Sidescan & Sub-Bottom Traces to GLORIA:**
   ```bash
   jsf2glo -log -in survey_line.jsf -out survey_line
   ```
