---
layout: default
title: testbeam2
parent: Old Stuff
grand_parent: Beam Tools
nav_order: 11
tool_name: testbeam2
source_path: code/sidescan/beam/oldstuff/testbeam2
category: Sidescan Beam Pattern Processing
input_formats: ["JCU GLORIA .slr (ps89_365.slr)"]
output_formats: ["Beam-corrected GLORIA file (.trash)", "Stdout log (pattern365)"]
related_tools: ["glbeam_bypass", "testbeam", "viewbeam.f"]
---

# testbeam2

## Description
`testbeam2` is a test invocation script in `code/sidescan/beam/oldstuff/` that runs [`glbeam_bypass`](glbeam_bypass.md) (`glbeam2`) on SOPAC 1989 GLORIA pass `365` with pattern file output suppressed (`null`), redirecting standard output diagnostics to `pattern365`.

## Script Contents & Usage
```csh
glbeam2 ~/data/sopac/gloria/ps89_365.slr ~/data/sopac/gloria/ps89_365.trash null > pattern365
```
* **Arg 1 (`~/data/sopac/gloria/ps89_365.slr`)**: Input slant-range corrected GLORIA pass `365`.
* **Arg 2 (`~/data/sopac/gloria/ps89_365.trash`)**: Output beam-corrected GLORIA file.
* **Arg 3 (`null`)**: Skips writing a separate `.beam_pattern` file while capturing stdout beam statistics in `pattern365`.
