---
layout: default
title: demo_fernando
parent: OMG Tools
nav_order: 86
---
# demo_fernando

## Description
`demo_fernando` is a simple, interactive demonstration program designed to illustrate how to extract basic elements of an EM1000 multibeam sonar data record from an OMG-HDCS merged file. It allows a user to input a record number (ping number) and then retrieves and displays the corresponding bathymetry (xyz coordinates), sidescan traces, and vessel motion (roll, pitch, heading, heave) for that ping.

This tool primarily serves as a debugging aid or a basic example for developers to understand the structure of EM1000 data within the OMG-HDCS format.

## Usage
```bash
demo_fernando <input_omg_file(.merged)> [-v]
```

## Arguments

| Option | Description |
|---|---|
| `<input_omg_file(.merged)>` | **Required.** The path to the input OMG-HDCS merged file. |
| `-v` | Enable verbose output (not explicitly used in the provided code but present in `USAGE`). |

## Interactive Mode
After launching, the program will continuously prompt the user to "input rec num". The user enters a ping number, and the program displays the requested data.

## How It Works
1.  **File Opening:** Opens the specified OMG-HDCS merged file (`.merged`) and its corresponding sidescan data file (`.ss_data`).
2.  **Interactive Loop:** Enters an infinite loop (`upthere:;` and `goto upthere;`) to allow continuous interactive input.
3.  **Record Number Input:** Prompts the user to enter a `recno` (record number or ping number).
4.  **Data Extraction:** Calls `give_me_traces_and_bathy` (an external function, likely from `Echo_calib.h` or a linked library) with the input files and the provided `recno`. This function populates:
    *   `sstraces`: A 2D array to store sidescan traces (up to 60 beams, 500 samples each).
    *   `xyz`: A 2D array to store bathymetry coordinates (x, y, z) for up to 60 beams.
    *   `roll`, `pitch`, `heading`, `heave`: Variables to store vessel motion data.
5.  **Output to Console:**
    *   Prints the extracted `roll`, `pitch`, `heading`, and `heave` values.
    *   For each of the 60 beams, it prints the `xyz` coordinates.
    *   For each beam's sidescan trace, it iterates through up to 500 samples. If a sample is non-zero, it prints "1" (effectively showing a binary presence of data in the trace).
6.  **Loop Continuation:** After displaying the data for one ping, it jumps back to `upthere:;` to prompt for another record number.

## Data Structures (Assumed)
The tool relies on data structures and functions from `Echo_calib.h` (and `OMG_HDCS_jversion.h`, `support.h`) which are not provided here but are essential for reading the binary data formats.
