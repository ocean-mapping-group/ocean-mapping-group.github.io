---
layout: default
title: xseTool
parent: XSE Tools
nav_order: 2
tool_name: xseTool
source_path: xse/xseTool.c
category: diagnostics
input_formats: [XSE]
output_formats: [ASCII_STDOUT]
related_tools: [xse2omg]
---

# xseTool

## Overview

`xseTool` is a diagnostic command-line utility for inspecting binary `.xse` (eXtended Sensor Exchange) files. It scans every frame in an `.xse` file, tallies the count of each frame ID, prints a formatted summary table at the end of execution, and optionally dumps the detailed contents of specific frame types selected with `-vf <frame_ID>`.

## Usage

```
xseTool (-vf 13) (-v) -in filename.xse
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<filename.xse>` | *required* | Input `.xse` file to inspect. |
| `-vf` | `<frame_ID>` | none | Enable detailed printout for a specific XSE frame ID (e.g., `1` = Navigation, `2` = Sound Velocity, `4` = Ship, `5` = Sidescan, `6` = Multibeam, `13` = SeaBeam). May be specified multiple times. |
| `-v` | none | `0` | Print the frame header (ID, size, timestamp) of every frame encountered. |

## How It Works

1. **Frame Scanning**: `xseTool` iterates through the file using `seek_start_frame()` and `read_frame_header()`.
2. **Selective Decoding & Printing**:
   - **ID 1**: Navigation Frame (`read_navigation_frame` / `print_navigation_frame`)
   - **ID 2**: Sound Velocity Frame (`read_sound_velocity_frame` / `print_sound_velocity_frame`)
   - **ID 4**: Ship Frame (`read_ship_frame` / `print_ship_frame`)
   - **ID 5**: Sidescan Frame (`read_sidescan_frame` / `print_sidescan_frame`)
   - **ID 6**: Multibeam Frame (`read_multibeam_frame` / `print_multibeam_frame`)
   - **ID 13**: SeaBeam Frame (`read_seabeam_frame` / `print_seabeam_frame`)
   - **Other Frame IDs**: Iterates over internal group headers (`read_group_header`) and prints them if `-vf <ID>` was enabled.
3. **Summary Table**: After reaching EOF, prints the `File Contents Summary` table showing `ID`, `Frame Type`, and `Count` for every frame ID present, followed by the total valid frame count.

## Practical Examples

### Print a summary of frame types in an `.xse` file

```bash
xseTool -in survey_001.xse
```

### Dump all Ship (ID 4) and Sound Velocity (ID 2) frames

```bash
xseTool -vf 4 -vf 2 -in survey_001.xse
```
