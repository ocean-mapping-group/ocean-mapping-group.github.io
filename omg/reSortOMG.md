---
layout: default
title: reSortOMG
parent: OMG Tools
nav_order: 59
---
# reSortOMG

## Description
`reSortOMG` is a utility designed to reorder an OMG-HDCS merged file that has profiles out of chronological or ping number sequence. This can occur due to various reasons during data acquisition or post-processing, especially with systems like KMALL where data packets might not arrive in strict order.

The tool reads the entire merged file, extracts time and ping number information for each profile, sorts this information, and then rewrites the merged file in the correct order.

## Usage
```bash
reSortOMG <input_omg_file(.merged)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<input_omg_file(.merged)>` | **Required.** The path to the input OMG-HDCS merged file. This file will not be modified directly; a new sorted file will be created. |
| `-AUV_draft` | (Not implemented in the provided code, but present in `USAGE`) This option likely has to do with AUV-specific draft calculations or handling but its effect on sorting is not shown. |
| `-v` | Enable verbose output. | |

## How It Works
1.  **Input Reading:** Opens the input merged file for reading.
2.  **Summary Header Reading:** Reads the summary header to get the total number of profiles.
3.  **Index Creation:**
    *   Allocates memory for an array of `pingindex` structures, one for each profile.
    *   Iterates through each profile in the original merged file.
    *   For each profile, it reads the `profile.pingNo` and `profile.timeOffset` and stores them along with the original profile's index (`origpingnum`) into the `pingindex` array.
4.  **Order Check:** During the index creation, it also checks if there are any profiles where `profile.timeOffset` is less than the `last_timeOffset`, indicating out-of-order data.
5.  **Sorting:** If out-of-order profiles are detected (`nobackward > 0`):
    *   It performs a bubble sort (or similar comparison sort) on the `pingindex` array based on the `timeOffset` field. This ensures that the `pingindex` array now contains the original profile numbers in chronological order.
    *   It reports the number of passes and swaps made during the sort to a `.sort.stats` file.
6.  **Output File Creation:**
    *   A new output file is created with the name `input_omg_file.sorted`.
    *   The summary header from the original file is dumped to the new sorted file.
    *   It then iterates through the *sorted* `pingindex` array. For each entry in this array, it reads the corresponding original profile and its raw beams from the input file (using `pI[i].origpingnum`) and writes them to the new `.sorted` file.
7.  **No Sort Scenario:** If no backward time steps are detected, it prints a message indicating that it's not bothering to write out a sorted file.
8.  **Cleanup:** Closes all open files and frees allocated memory.

## Output Files
*   `<input_omg_file_prefix>.sorted`: A new OMG-HDCS merged file with profiles sorted chronologically.
*   `<input_omg_file_prefix>.sort.stats`: An ASCII file containing statistics about the sorting process.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
Sorting merged files chronologically is crucial for ensuring proper processing by other tools that rely on sequential data (e.g., motion compensation, tide correction, or data cleaning algorithms that look at adjacent pings). This tool provides a robust way to correct out-of-order data, particularly from newer data acquisition systems. The tool creates a new file, ensuring the integrity of the original.