---
layout: default
title: readGenericADCP
parent: ADCP Tools
nav_order: 13
tool_name: readGenericADCP
source_path: code/adcp/readGenericADCP.c
category: adcp
input_formats:
  - jcu_nav Navigation (.nav / .decXX.nav)
  - JHC 32-bit Float Velocity Arrays (.N.r4, .E.r4, .D.r4)
output_formats:
  - jcu_nav Depth-Averaged ADCP Vectors (.nav)
related_tools:
  - mapGenericADCP
  - combineMultiADCP
  - calc_ellipse2
---

# readGenericADCP

## Description
`readGenericADCP` is a command-line utility designed to process generic or Kongsberg Simrad EC150 pre-processed ADCP (Acoustic Doppler Current Profiler) datasets. It calculates a single depth-averaged horizontal current vector (`velocity` and `azi`) for each ADCP ensemble within a specified depth window (`-mindepth` to `-maxdepth`) and writes a new `jcu_nav` `.nav` file ready for multi-cycle tidal analysis in [`combineMultiADCP`](combineMultiADCP.md) or [`calc_ellipse2`](calc_ellipse2.md).

The tool expects each input `.nav` file (e.g., `survey1.dec10.nav`) to be accompanied by three JHC 32-bit floating-point arrays (`survey1.dec10.N.r4`, `survey1.dec10.E.r4`, and `survey1.dec10.D.r4`) representing the vertical profiles of North, East, and Downward velocity components.

> [!IMPORTANT]
> On the command line, `-out <outfile>` **must** be specified before `-in <infile(s)>`, because `-in` consumes all remaining positional arguments.

## Usage
```bash
readGenericADCP [OPTIONS] -out <outfile> -in <infile(s)>
```

## Arguments

| Option | Description |
|---|---|
| `-out <outfile>` | **Required (must precede `-in`).** Output `jcu_nav` `.nav` file containing the depth-averaged current vectors. |
| `-in <infile(s)>`| **Required.** One or more input navigation files (e.g., `survey1.dec3.nav`). The tool automatically opens the companion `.N.r4`, `.E.r4`, and `.D.r4` files. |
| `-mindepth <meters>` | Minimum depth for the vertical averaging window (default `0.0` m). |
| `-maxdepth <meters>`| Maximum depth for the vertical averaging window (default `100.0` m). |
| `-time_start <Y J H M S>`| Start time filter (Year, Julian Day, Hour, Minute, Second). |
| `-time_end <Y J H M S>`| End time filter (Year, Julian Day, Hour, Minute, Second). |
| `-v` | Enable verbose output. |

## Input File Requirements

For each input navigation file `<prefix>.nav` (or `<prefix>.decXX.nav`), three JHC float-array files (`.r4`) with matching dimensions must exist in the same directory:
*   `<prefix>.N.r4` (North velocity in m/s)
*   `<prefix>.E.r4` (East velocity in m/s)
*   `<prefix>.D.r4` (Downward velocity in m/s)
