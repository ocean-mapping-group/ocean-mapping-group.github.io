---
layout: default
title: edsumm
parent: OMG Tools
nav_order: 95
---
# edsumm

## Description
`edsumm` (Editor Summary) is an interactive utility designed to directly edit the header information of an OMG-HDCS merged data file. It provides a menu-driven interface allowing users to modify various fields within the `OMG_HDCS_summary_header` structure.

This tool is useful for correcting metadata errors, adjusting file parameters, or updating descriptive labels after data acquisition or processing.

## Usage
```bash
edsumm <file> [-verbose] [-addtag]
```

## Arguments

| Option | Description |
|---|---|
| `<file>` | **Required.** The path to the OMG-HDCS merged file whose header is to be edited. |
| `-verbose` | (Present in `USAGE` but not explicitly used in the provided code) Intended to provide more detailed output. |
| `-addtag` | (Present in `USAGE` but not explicitly used in the provided code) Intended to add a tag. |

## Interactive Menu
After launching, `edsumm` will enter an infinite loop, displaying the current header information and presenting a menu of fields that can be modified:

1.  `no records` (`summary.numProfiles`)
2.  `rows` (`JHChead.dy`)
3.  `tlat` (`JHChead.ymax`)
4.  `blat` (`JHChead.ymin`)
5.  `tlon` (`JHChead.xmin`)
6.  `blon` (`JHChead.xmax`)
7.  `xstep` (`JHChead.xstep`)
8.  `ystep` (`JHChead.ystep`)
9.  `datatype` (`JHChead.data_type`)
10. `rgb_bw` (`JHChead.rgb_bw`)
11. `projection` (`JHChead.projection`)
12. `ellipsoid` (`JHChead.ellipsoid`)
13. `proj_merid` (`JHChead.proj_merid`)
14. `sun_elev` (`JHChead.sun_elev`)
15. `sun_azi` (`JHChead.sun_azi`)
16. `sun_exag` (`JHChead.sun_exag`)
17. `view_elev` (`JHChead.view_elev`)
18. `view_azi` (`JHChead.view_azi`)
19. `view_exag` (`JHChead.view_exag`)
20. `min_value` (`JHChead.min_value`)
21. `max_value` (`JHChead.max_value`)
22. `label_1` (`JHChead.label_1`)
23. `label_2` (`JHChead.label_2`)
0.  `nothing` (Exit)

The user enters a number corresponding to the field they wish to edit, then provides the new value. The tool updates the header and redisplays the menu.

## How It Works
1.  **File Opening:** Opens the specified OMG-HDCS merged file for reading and writing (`r+`).
2.  **Interactive Loop:** Enters a `while (!done)` loop:
    *   Reads the current `OMG_HDCS_summary_header` from the file using `OMG_HDCS_read_summary`.
    *   Prints the current header contents to the console using `OMG_HDCS_write_summary` (this function likely prints to stdout, not to the file, despite its name).
    *   Presents a menu of editable fields.
    *   Prompts the user for a `choice`.
    *   **Field Modification:** Based on the user's `choice`:
        *   If `choice == 1`, it prompts for a new `numProfiles` and updates `summary.numProfiles`.
        *   If `choice == 22` or `choice == 23`, it prompts for a new label string and updates `JHChead.label_1` or `JHChead.label_2` respectively.
        *   **Note:** In the provided code, only `choice == 1` and `choice == 22`/`23` are implemented to modify the `summary` or `JHChead` fields. All other choices currently do nothing or only read user input without applying changes to `summary`.
    *   **Write Changes:** If a field is modified, `OMG_HDCS_dump_summary(infile, &summary)` (or `write_JHC_header(infile, JHChead)` for labels) is called to write the updated header back to the file.
3.  **Exit:** The loop continues until the user chooses `0` (nothing/exit).
4.  **Cleanup:** Closes the input file.
