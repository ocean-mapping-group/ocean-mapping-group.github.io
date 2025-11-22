---
layout: default
title: appendSS
parent: Merge Tools
grand_parent: sidescan
nav_order: 2
---
# appendSS

## Description
`appendSS` is a utility designed to append multiple JCU GLORIA sidescan files together into a single output file. It intelligently sorts the input files by their start time, and can filter records based on a specified time window. An optional time shift can also be applied to the records during the appending process. This tool is a re-implementation of `appendAtt` tailored for sidescan data.

## Usage
```bash
appendSS [-v] [-intimeshiftsecs <seconds>] [-start <yr jday hr min>] [-end <yr jday hr min>] [-start_sec <yr jday hr min sec>] [-end_sec <yr jday hr min sec>] [-timeboundsof <mergedfile>] -out <outfile> <infile1> [<infile2> ...]
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-intimeshiftsecs <seconds>` | Shifts the time of all input records by the specified number of seconds. |
| `-start <yr jday hr min>` | Specifies the start time (year, Julian day, hour, minute) for filtering records. Only records after this time will be included. |
| `-end <yr jday hr min>` | Specifies the end time (year, Julian day, hour, minute) for filtering records. Only records before this time will be included. |
| `-start_sec <yr jday hr min sec>` | Similar to `-start`, but includes seconds for finer time control. |
| `-end_sec <yr jday hr min sec>` | Similar to `-end`, but includes seconds for finer time control. |
| `-timeboundsof <mergedfile>` | Reads the time bounds (min and max time) from an existing OMG_HDCS merged file and uses these bounds for filtering. |
| `-out <outfile>` | **Required.** The path to the output JCU GLORIA file where all appended sidescan records will be written. |
| `<infile1> [<infile2> ...]` | **Required.** One or more input JCU GLORIA sidescan files to be appended. |

## How It Works
1.  **Argument Parsing:** The tool parses command-line arguments, including verbose flags, time shift, and time bounding parameters.
2.  **Collect Input File Information:** For each input file provided:
    *   It stores the filename.
    *   It reads the first and last records to determine the start (`att_headers[no_files].time`) and end (`att_headers[no_files].end_time`) times, and the number of records (`att_headers[no_files].no_recs`).
3.  **Time Bounds from Merged File (Optional):** If `-timeboundsof` is used, it reads the summary and profile headers from the specified OMG_HDCS merged file to establish `mintime` and `maxtime` for filtering.
4.  **Sort Input Files:** The `att_headers` array (containing file information) is sorted by the start time of each file using `qsort` and `compare_att_headers`. This ensures that records are appended in chronological order even if input files are provided out of sequence.
5.  **Append Records:**
    *   It iterates through the sorted list of input files.
    *   For each input file:
        *   It reads each record from the file.
        *   The record's time is adjusted by `intimeshiftsecs` if specified.
        *   **Time Filtering:** If `mintime` and `maxtime` bounds are defined (either manually or via `-timeboundsof`), the record is only written to the output file if its adjusted time falls within these bounds.
        *   Valid records are written sequentially to the output file using `jcu_writegloria`. A running count (`attCount`) keeps track of the record number in the output file.
6.  **Output:** A single JCU GLORIA file (`outfile`) containing the time-ordered and optionally filtered sidescan records is created.
