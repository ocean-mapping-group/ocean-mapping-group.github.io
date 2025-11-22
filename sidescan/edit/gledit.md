---
layout: default
title: gledit
parent: Edit Tools
grand_parent: sidescan
nav_order: 1
---
# gledit

## Description
`gledit` is an interactive command-line utility for displaying and editing header information within a JCU GLORIA record file. It provides a simple interface for navigating through records and modifying specific header fields such as altitude, heading, fishdepth, latitude, and longitude.

## Usage
```bash
gledit <filename>
```

## Arguments

| Option | Description |
|---|---|
| `<filename>` | **Required.** The path to the JCU GLORIA file to be edited. |

## Interactive Mode
Upon launching, `gledit` enters an interactive loop, presenting the user with a menu of options:

*   `r`: **Record number.** Prompts for a specific record number to jump to and display.
*   `+`: **Go forward.** Moves to the next record. Can be followed by a number (e.g., `+5`) to skip multiple records forward.
*   `-`: **Go backward.** Moves to the previous record. Can be followed by a number (e.g., `-3`) to skip multiple records backward.
*   `c`: **Change value.** Allows the user to select a header field to modify:
    *   `a`: Altitude
    *   `h`: Heading
    *   `f`: Fishdepth
    *   `l`: Latitude/Longitude
*   `e`: **Exit.** Exits the program.

After each operation (except `e`), the tool displays relevant header information for the current record. When a value is changed, the modification is written back to the GLORIA file.

## How It Works
1.  **File Opening:** The tool opens the specified GLORIA file in read-write mode.
2.  **File Length Determination:** It determines the total number of records in the file.
3.  **Interactive Loop:** It enters a loop, continuously prompting the user for commands:
    *   **Navigation:** Commands like `r`, `+`, `-`, and ` ` (space for next) update the `rec_num` variable, which tracks the current record being viewed or edited.
    *   **Display Record (`show_rec`):** This function reads the GLORIA record at the current `rec_num` and prints its detailed header information to standard output using internal `jcu_write_verbose_head` and `jcu_write_swath_head` functions.
    *   **Change Values (`change_lat_lon`, `change_heading`):** If the `c` command is chosen, it further prompts the user for the specific field to change. New values are read from standard input, converted as necessary (e.g., heading from degrees to radians), and then written back into the `glo_rec` structure.
    *   **Write Record:** After modification, the `jcu_writegloria` function is called to write the updated `glo_rec` back to the file at the current `rec_num`.
4.  **Exit:** The loop terminates when the user enters `e`.
