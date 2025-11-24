---
layout: default
title: stackOMG
parent: OMG Tools
nav_order: 69
---
# stackOMG

## Description
`stackOMG` is a utility designed to stack and average beam data (depth and across-track offset) from multiple records (pings) within one or more OMG-HDCS merged files. It computes a weighted average of `observedDepth` and `acrossTrack` for each beam number, providing a consolidated view of the seafloor profile.

The tool can process a specific range of pings or iterate through entire files. It can also perform a least-squares fit on the averaged data to determine a best-fit slope and intercept.

## Usage
```bash
stackOMG <OMG_HDCS_datafile(s)> [-mode <value>] [-verbose] [-list]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile(s)>` | **Required.** One or more paths to input OMG-HDCS merged files. If no files are provided on the command line, it prompts for them interactively. |
| `-mode <value>` | Only process pings that match this specific `profile.mode` value. | `999` (process all modes) |
| `-verbose` | Enable verbose output. | |
| `-list` | Instead of generating a `stack.plot` file, it outputs an ASCII listing of averaged depths and offsets to the console or a file (not explicitly specified but implied by `list_flag`). |

## Interactive Mode (if no files specified on command line)
If no filenames are provided on the command line, the tool will:
1.  Prompt for an input OMG file name.
2.  Prompt for `first` and `last` record numbers (pings) to stack.
3.  After processing, ask "another file?", allowing for iterative stacking from multiple sources.

## How It Works
1.  **Initialization:** Initializes arrays to store the sum of depths (`depth`), sum of across-track offsets (`offset`), and count (`count`) for each beam number (up to `MAX_BEAMS_TO_STACK`).
2.  **File and Ping Iteration:**
    *   It iterates through each specified merged file (either from the command line or interactively).
    *   For each file, it reads the summary header.
    *   It then iterates through a specified range of pings (either `first` to `last` if provided, or `0` to `summary.numProfiles` by default).
    *   For each ping, it reads the profile header and raw beams.
    *   **Mode Filtering:** If `-mode` is specified, it only processes pings whose `profile.mode` matches the `mode_choice`.
    *   **Accumulation:** For each valid beam (status `0` and `observedDepth` present), it accumulates:
        *   `depth[j] += (float) beam[j].observedDepth / 1000.0`
        *   `offset[j] += (float) beam[j].acrossTrack / 1000.0`
        *   `count[j]++`
3.  **Averaging:** After processing all selected pings from all files:
    *   For each beam `j`, if `count[j]` is non-zero, it calculates the average depth and across-track offset by dividing the accumulated sums by `count[j]`.
4.  **Least-Squares Fit:** Performs a linear least-squares regression (`do_least_squares`) on the averaged `offset` (X) and `depth` (Y) data to find an `intercept`, `slope`, and `fit` value. This is useful for determining the average slope of the seafloor in the stacked profile.
5.  **Output:**
    *   If `-list` is used, it prints the averaged depths and offsets for each beam to the console.
    *   Otherwise, it creates an output file named `stack.plot` and writes various diagnostic information, including:
        *   Hardcoded parameters (e.g., `15.0 20.0`, `5`).
        *   A depth range derived from `depth[15]`.
        *   For each beam, its averaged `offset`, `depth`, and `count`.
        *   The results of the least-squares fit (`intercept`, `slope`, `fit`).
        *   `leveldepth` (detrended depths based on the least-squares slope) and `leveldepth - depth` (residuals).

## Output Files
*   `stack.plot`: An ASCII file containing averaged beam data and least-squares fit results.
*   Console output if `-list` is used.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
`stackOMG` is useful for generating an average cross-section of the seafloor from multiple pings, which can help to smooth out noise and reveal underlying bathymetric trends. The least-squares fit provides a simple model of the averaged seafloor slope. The interactive mode allows for flexible selection of input files and ping ranges. The tool creates a new file, ensuring the integrity of the original.