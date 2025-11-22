---
layout: default
title: joinbeam
parent: Beammap Tools
grand_parent: sidescan
nav_order: 2
---
# joinbeam

## Description
`joinbeam` is a utility that processes a list of JCU GLORIA files. Its primary purpose is to ensure continuity between adjacent files, preventing gaps or discontinuities when these files are later mosaicked. It achieves this by selectively replacing or appending the first record of a subsequent file to the end of the preceding file, based on the time difference between their last and first records, respectively.

## Usage
```bash
joinbeam <file1> <file2> ... <filen>
```

## Arguments

| Option | Description |
|---|---|
| `<file1> <file2> ... <filen>` | **Required.** A list of two or more JCU GLORIA files to be processed sequentially. |

## How It Works
1.  **Sequential Processing:** The tool iterates through the provided list of GLORIA files, processing them in adjacent pairs (e.g., `file1` and `file2`, then `file2` and `file3`, and so on).
2.  **Read Adjacent Records:** For each pair, it reads the last record of the first file and the first record of the second file.
3.  **Calculate Time Difference:** It calculates the time difference (`dtime`) between the `header.time` of the last record of the first file and the first record of the second file.
4.  **Conditional Action:**
    *   **`dtime == 0`:** If the time difference is zero, it means the first record of the second file is temporally identical to the last record of the first. In this case, the tool *replaces* the last record of the first file with the first record of the second file.
    *   **`0 < dtime < TIMETHRESH`:** If the time difference is positive but within a defined threshold (`TIMETHRESH`, set to 180 seconds), it means there's a small temporal gap. The tool *appends* the first record of the second file to the end of the first file.
    *   **Otherwise:** If the time difference is outside these conditions (e.g., negative or exceeding `TIMETHRESH`), a warning is issued, indicating that the times do not match as expected.
5.  **File Management:** After processing a pair, the first file is closed, and the second file becomes the "first file" for the next iteration, ensuring that files are properly linked.
6.  **Loop:** This process continues until all adjacent file pairs in the list have been evaluated.
