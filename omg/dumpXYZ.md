---
layout: default
title: dumpXYZ
parent: OMG Tools
nav_order: 93
---
# dumpXYZ

## Description
`dumpXYZ` is a versatile utility for extracting various types of data from OMG-HDCS merged files and outputting them to an ASCII listing. Its primary function is to dump longitude, latitude, and depth (XYZ) triplets, but it can also output attitude data, backscatter values, and other parameters.

The tool offers extensive filtering capabilities, including by ping/beam ranges, geographical area, or pulse length. It can also project coordinates into different systems (UTM, Mercator pixel coordinates) and apply various corrections.

## Usage
```bash
dumpXYZ <OMG_HDCS_datafile(s)> -out <ASCII_listing_file> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_datafile(s)>` | **Required.** One or more paths to OMG-HDCS merged files. |
| `-out <ASCII_listing_file>` | **Required.** The path for the ASCII output file. |

### Data Type Selection (Choose one)
| Option | Description |
|---|---|
| `-att` | Dumps attitude data (roll, pitch, heading, heave) along with lat, lon, and time. |
| `-BSnBSo` | Dumps BSn-BSo values along with ping data. |
| `-dump_nadir` | Dumps nadir beam depth, across, TWTT, and real TWTT. |
| `-refl` / `-aibs` / `-calb` | Dumps reflectivity, pseudo Angle Independent Backscatter (AIBS), or calibrated backscatter values along with lat/lon. |
| `-mani` | Dumps data in a format specific for Mani (UVic). Includes ping/beam info, motion, lat/lon, depth, across, along, and status. |
| `-dataFrame` | Dumps comprehensive data for a data frame, including motion, beam details, lat/lon, depth, across, along, status, reflectivity, Q-factor, frequency, range, TWTT, and TXSector. |

### Coordinate System & Projection
| Option | Description |
|---|---|
| `-utm` | Output coordinates in UTM (easting/northing). Requires `-merid`. |
| `-merid <val>` | Central meridian for UTM projection. | `-63.0` |
| `-wgs84` / `-nad27` | Ellipsoid to use for UTM projection. | Prompts user if not specified. |
| `-area <map.sheet>` | Only outputs beams within the geographical area defined by the map sheet (`.r4` file). |
| `-pixelcoords` | (Used with `-area`) Outputs pixel coordinates (x, y) on the map sheet instead of lat/lon. |

### Data Filtering
| Option | Description |
|---|---|
| `-start <ping_num>` / `-end <ping_num>` | Process pings only within this range (inclusive). | All pings |
| `-choose_beams <first_b> <last_b>` | Process beams only within this beam number range (inclusive). | All beams |
| `-specific <filename>` | Outputs only specific ping/beam combinations listed in a file (mbriss format: `beamno+127 pingno fixno`). |
| `-timeinterval <secs>` | Outputs navigation labels at a specified time interval (seconds). |
| `-dirty` | (Implies `-useallZ`) Includes beams regardless of their status flags. |
| `-just_pulse_microsec <val>` | Only process pings with `tx_pulse_len` equal to `val`. |
| `-add_dyn_draft_shift` | Adds `profile.longperiod_heaveCorrection` to the observed depth. |

### Corrections & Processing
| Option | Description |
|---|---|
| `-coeffs` | Applies empirical refraction coefficients (from `.ref_coeffs` file). |
| `-tidecor` | Applies tide correction (sets `use_tide_corr_flag`). |
| `-mergeSSS <SSSfile>` | Merges a surface sound speed file (SSS) into the output (format: `ping_num sss_value`). |

### Other Options
| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-dump_multidetect_params` | Dumps additional parameters related to multi-detection. |
| `-nortech` | Specific output format for Nortech (similar to `mani`). |

## How It Works
1.  **Initialization:** Parses command-line arguments to set various flags, ranges, and output formats.
2.  **File Setup:** Opens input merged files, the output ASCII file, and any specified auxiliary files (e.g., area map, SSS file, specific beam list).
3.  **Summary Header Reading:** Reads the summary header from the merged file to initialize global parameters like `Ellipsoid` and `JHChead` for projections.
4.  **Coefficient Loading (`-coeffs`):** If specified, it attempts to read refraction coefficients from a `.ref_coeffs` file and sets them up.
5.  **Ping Iteration:** Loops through each ping (profile) in the merged file (potentially skipping pings with `have100` bounds optimization):
    *   **Profile Data:** Reads the profile header. Extracts time, motion, and transducer position.
    *   **Beam Data:** Reads raw beams for the current ping.
    *   **Filtering:** Filters beams based on `firstbeam`/`lastbeam`, `specific_flag`, and `area_flag`.
    *   **Refraction Correction (`-coeffs`):** If specified, it applies refraction corrections to `lolade[j][2]` (depth) and `lolade[j][3]` (across-track).
    *   **Coordinate Transformation:** Transforms lat/lon to UTM easting/northing if `-utm` is used, or to pixel coordinates if `-pixelcoords` is used with `-area`.
    *   **Output Formatting:** Based on the chosen output flag (`-att`, `-BSnBSo`, `-refl`, `-mani`, `-dataFrame`, etc.), it formats and prints the data to the output ASCII file. This can include:
        *   Time, lat, lon, attitude, and central beam depth.
        *   Specific beam properties (depth, across, along, lat, lon, status, backscatter).
        *   UTM coordinates.
        *   Additional multi-detect parameters.
    *   **Depth Range Tracking:** Keeps track of the shallowest and deepest depths encountered.
6.  **Cleanup:** Closes all open files.
