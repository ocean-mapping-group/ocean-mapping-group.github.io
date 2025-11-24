---
layout: default
title: preFlag
parent: OMG Tools
nav_order: 49
---
# preFlag

## Description
`preFlag` is a command-line utility used to pre-process OMG-HDCS merged files by setting status flags on beams and, optionally, performing empirical depth reductions. Its primary use is to identify and mark potentially bad soundings or to apply specific, often ad-hoc, corrections to the data.

The tool can filter beams based on an externally provided specification file (for marking consistently bad beams or applying percentage corrections) or by a maximum incidence angle threshold.

## Usage
```bash
preFlag <mergefile(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<mergefile(s)>` | **Required.** One or more paths to OMG-HDCS merged files to be processed. These files are modified in place. |
| `-v` | Enable verbose output. |
| `-beams <num_beams>` | Specifies the number of beams to consider when using a hackfn file. |
| `-hackfn <filename>` | Specifies a "hack function" file. This file contains `status_set` (0 or 1) and `perc_corr` (percentage correction) values for each beam, which will be applied to the `status` and `processedDepth` fields respectively. |
| `-max_incidence <angle>` | Flags beams whose incidence angle (calculated from across-track and observed depth) exceeds this value (in degrees). Marked beams will have their `status` set to `22`. |
| `-roll_offset <val>` | Specifies a roll offset value (currently not used in the provided code snippet but present in the `USAGE`). |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Summary Header Reading:** Reads the summary header to get basic file information.
3.  **Hack Function File Loading (`-hackfn`):** If `-hackfn` is specified, it reads the "hack function" file, which contains per-beam `status_set` and `perc_corr` values.
4.  **Beam Iteration & Flagging:** For each profile in a merged file, and then for each beam within that profile:
    *   **`NUM_beams` and `-hackfn`:** If `NUM_beams` and a hack function file (`tidename`) are provided:
        *   It checks `status_set[i]`. If `0`, it sets the beam's `status` to `22`.
        *   If `perc_corr[i]` is not -1, it applies this percentage correction to `observedDepth` and stores it in `processedDepth`.
    *   **`-max_incidence`:** If `max_incidence` is specified, it calculates the incidence angle for each beam using its `acrossTrack` and `observedDepth`. If the absolute value of this calculated incidence angle exceeds `max_incidence`, the beam's `status` is set to `22`.
5.  **In-Place Update:** All modifications (setting status flags, adjusting `processedDepth`) are applied directly to the raw beam records within the input merged files.

## Output Files
The input merged files are modified in-place.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.
*   `math.h`: For mathematical functions (used in angle calculations).

## Notes
`preFlag` is useful for applying preliminary quality control or systematic corrections to multibeam data before more intensive processing. The `-hackfn` option provides a mechanism for applying custom, empirical corrections derived from analysis of specific sonar artifacts. As with all in-place modification tools, backups are recommended before processing. The `-roll_offset` option is listed but not implemented in the current code.