---
layout: default
title: testbeam
parent: Old Stuff
grand_parent: Beam Tools
nav_order: 10
tool_name: testbeam
source_path: code/sidescan/beam/oldstuff/testbeam
category: Sidescan Beam Pattern Processing
input_formats: ["JCU GLORIA .slr (ps89_353.slr)"]
output_formats: ["Beam-corrected GLORIA file (.trash)", "ASCII beam pattern (pattern4)"]
related_tools: ["glbeam_bypass", "testbeam2", "viewbeam.f"]
---

# testbeam

## Description
`testbeam` is a single-line driver script in `code/sidescan/beam/oldstuff/` used to test the [`glbeam_bypass`](glbeam_bypass.md) (`glbeam2`) empirical beam pattern extraction and removal tool on SOPAC 1989 GLORIA pass `353`.

## Script Contents & Usage
```csh
glbeam2 ~/data/sopac/gloria/ps89_353.slr ~/data/sopac/gloria/ps89_353.trash pattern4
```
* **Arg 1 (`~/data/sopac/gloria/ps89_353.slr`)**: Input slant-range corrected JCU GLORIA sidescan file.
* **Arg 2 (`~/data/sopac/gloria/ps89_353.trash`)**: Output beam-corrected GLORIA sidescan file.
* **Arg 3 (`pattern4`)**: Output 91-bin empirical grazing-angle beam pattern table (`0°–90°`).
