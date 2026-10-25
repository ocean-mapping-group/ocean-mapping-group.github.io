---
layout: default
title: L-3 / SeaBeam XSE Format (xse)
parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 12
has_children: true
---

# XSE Tools

Tools in the `xse/` directory inspect and convert binary `.xse` (eXtended Sensor Exchange) files produced by L-3 Communications / ELAC Nautik HydroStar and SeaBeam acquisition systems into OMG HDCS formats.

## Tool Summary

| Tool | Source | Description |
| :--- | :--- | :--- |
| [xse2omg](xse2omg) | `xse/xse2omg.c` | Converts XSE multibeam, navigation, attitude, sidescan, ship configuration, and sound velocity frames into `.merged`, `.nav`, `.orientation`, `.ss`, `.param`, and `.svp` files. |
| [xseTool](xseTool) | `xse/xseTool.c` | Diagnostic utility that scans `.xse` files, prints a frame count summary table, and optionally dumps specific frame IDs in detail. |

## Typical Workflow

1. **Inspect XSE frame inventory:** Run `xseTool -in survey.xse` to list the frame types (Navigation, Sound Velocity, Ship, Sidescan, Multibeam, SeaBeam) and counts present in the file.
2. **Convert XSE to OMG HDCS:** Run `xse2omg -in survey.xse -out survey` to extract `.merged`, `.nav`, `.orientation`, `.ss`, `.param`, and `.svp` files.
3. **Merge navigation and heading:** Because XSE stores vessel heading in the 1 Hz navigation frame rather than the high-rate attitude group, run `mergeNav -hdg` and `mergeOrientation` on the resulting `.merged` file.
