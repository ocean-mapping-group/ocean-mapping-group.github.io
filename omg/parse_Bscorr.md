---
layout: default
title: parse_Bscorr
parent: OMG Tools
nav_order: 47
---
# parse_Bscorr

## Description
`parse_Bscorr` is a tool designed to read and parse a standard `Bscorr` file (specifically for EM710 sonars) into an OMG beam pattern file format. It also includes functionality for interpolating the beam pattern values for angles between the reported values, ensuring a smooth and complete representation of the angular response.

The primary use case is to convert manufacturer-provided backscatter correction tables into a format compatible with OMG tools for further analysis or application.

## Usage
```bash
parse_Bscorr <file.Bscorr_XXX> [-EM710] [-interpolate <val>] [-out <outname>] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `<file.Bscorr_XXX>` | **Required.** The path to the input `Bscorr` file (e.g., `CalibEM710.txt`). |
| `-EM710` | Specifies that the input `Bscorr` file is in the EM710 format. |
| `-interpolate <val>` | Interpolates the beam pattern values for every `<val>` degree interval. | `1` (implicitly, as it iterates in 1-degree steps after interpolation setup). |
| `-out <outname>` | The base name for the output file(s). | Input filename (without extension). |
| `-v` | Enable verbose output. |

## How It Works
1.  **Input Reading:** Reads the specified `Bscorr` file line by line, ignoring comment lines starting with `#`.
2.  **EM710 Format Parsing:** If `-EM710` is specified, it parses the file according to the EM710 `Bscorr` format, which typically includes:
    *   Depth Mode, Swath Number, Number of Sectors per Swath.
    *   Source Level (SL) for each sector.
    *   Number of angle-vs-BP (Beam Pattern) value pairs for each sector.
    *   Angle and corresponding BP value pairs.
3.  **Data Storage:** The parsed data is stored in a multi-dimensional array structure (`EM710_Bscorr`) indexed by depth mode, swath number, sector number, and angle. Source levels are stored separately.
4.  **Interpolation:**
    *   For each depth mode, swath, and sector combination, it collects the available angle-vs-BP pairs.
    *   It then uses the GSL (GNU Scientific Library) spline interpolation to create a continuous curve from these discrete points.
    *   The interpolated values are then used to fill in the BP values for every 1-degree interval between the observed angles.
5.  **Output Writing:** The processed and interpolated beam pattern data is written to one or more output files.
    *   The output format attempts to mimic the input `Bscorr` file structure, including comments for human readability.
    *   It generates separate files for each depth mode and swath combination (e.g., `.Bscorr_1_0`, `.Bscorr_1_1` for mode 1, single and dual swath 1 respectively).
6.  **Memory Management:** Dynamically allocates and frees memory for the multi-dimensional arrays used to store the beam pattern data.

## Output File Naming Convention
The output files will be named using the `-out` prefix (or the input filename if `-out` is not specified) followed by `.<mode_id>_<swath_number>`. For example, `CalibEM710.Bscorr_1_0`, `CalibEM710.Bscorr_2_1`, etc.

## External Libraries
This tool uses the GNU Scientific Library (GSL) for spline interpolation.
