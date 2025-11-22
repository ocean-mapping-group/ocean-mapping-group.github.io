--- 
layout: default
title: iosedit
parent: Edit Tools
grand_parent: sidescan
nav_order: 3
---
# iosedit

## Description
`iosedit` is an interactive command-line utility for displaying and attempting to edit header information within an IOS (Institute of Ocean Sciences) GLORIA record file. It provides a basic interface for navigating through records and displaying parsed header fields such as pass number, line number, heading, time, and other IOS-specific details. While it presents an option to change the heading, the functionality to actually write the change back to the file is noted as "not actually implemented" in the source code.

## Usage
```bash
iosedit <filename>
```

## Arguments

| Option | Description |
|---|---|
| `<filename>` | **Required.** The path to the IOS GLORIA file to be edited. |

## Interactive Mode
Upon launching, `iosedit` enters an interactive loop, presenting the user with a menu of options:

*   `r`: **Record number.** Prompts for a specific record number to jump to and display.
*   `+`: **Go forward.** Moves to the next record. Can be followed by a number (e.g., `+5`) to skip multiple records forward.
*   `-`: **Go backward.** Moves to the previous record. Can be followed by a number (e.g., `-3`) to skip multiple records backward.
*   `c`: **Change value.** Allows the user to select a header field to modify. Currently, only `h` (heading) is offered, but its modification is not functional.
*   `e`: **Exit.** Exits the program.

After each operation (except `e`), the tool displays relevant header information for the current record, parsed from the IOS format.

## How It Works
1.  **File Opening:** The tool opens the specified IOS GLORIA file in read-write mode.
2.  **File Length Determination:** It determines the total number of records in the file based on the `sizeof(ios_rec)`.
3.  **Interactive Loop:** It enters a loop, continuously prompting the user for commands:
    *   **Navigation:** Commands like `r`, `+`, `-`, and ` ` (space for next) update the `rec_num` variable, which tracks the current record being viewed.
    *   **Display Record (`show_rec`):** This function reads the IOS record at the current `rec_num` and prints parsed header information, including pass number, line number, time components (year, jday, hour, min, sec), and a calculated full Unix timestamp using `getiostime`.
    *   **Change Values (`change_heading`):** If the `c` command is chosen for heading, it prompts for a new heading. However, the code explicitly states this functionality is not implemented (`printf ("too bad !!!! not actually implemented\n");`), and no write operation occurs for this field.
4.  **`getiostime` Function:** This helper function parses the year, Julian day, hour, minute, and second from the IOS record and calculates a Unix timestamp (seconds since epoch).
5.  **Exit:** The loop terminates when the user enters `e`.
