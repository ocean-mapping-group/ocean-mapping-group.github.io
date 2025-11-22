---
layout: default
title: refoCustom
parent: Singlebeam Tools
grand_parent: code
nav_order: 1
---
# refoCustom

## Description
`refoCustom` is a utility designed to reformat custom singlebeam data into the OMG_HDCS (Ocean Mapping Group Hydrographic Data Collection System) format. It currently supports two specific input data types: BCHYDRO and SDG, each with its own parsing and conversion logic. The tool extracts time, position (latitude, longitude, UTM), and depth information from these custom formats and populates the corresponding fields in the OMG_HDCS `summary_header`, `profile_header`, and `beam` structures.

## Usage
```bash
refoCustom [-v] [-BCHydro] [-local_datum <value>] [-SDG] [-showbits] <infile> <outfile>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-v` | Enable verbose output, providing more detailed processing messages. | (None) |
| `-BCHydro` | Specifies that the input file is in the BCHYDRO format (a custom ASCII format). | (Undefined) |
| `-local_datum <value>` | Specifies a local datum value (in meters) to apply a correction to the observed depths. Used with `-BCHydro`. | `0.0` |
| `-SDG` | Specifies that the input file is in the SDG format (a custom binary format). | (Undefined) |
| `-showbits` | Used with `-SDG`, displays a breakdown of the status flags within the SDG records. | (None) |
| `<infile>` | **Required.** The input custom singlebeam data file (either BCHYDRO or SDG format). | |
| `<outfile>` | **Required.** The output OMG_HDCS format file. | |

## How It Works
The tool's operation depends on the specified `data_type` (BCHYDRO or SDG). It initializes an `OMG_HDCS_summary_header` and then processes the input data record by record.

**Common Steps:**
1.  **File Opening:** Opens the input custom singlebeam file for reading and the output OMG_HDCS file for writing.
2.  **OMG_HDCS Summary Header Initialization:** Populates the `summary` header with static information (e.g., `fileID`, `sensorNumber`, `toolType = SingleBeam`) and placeholder values for dynamic fields (`numProfiles`, `minTime`, `maxTime`, etc.).

**Processing BCHYDRO Data (`-BCHydro`):**
1.  **Record Parsing:** Reads the input BCHYDRO file line by line. Each line is an ASCII string containing space-separated fields for Northing, Easting, Depth, and Time.
2.  **Coordinate Conversion:** Converts Northing and Easting to Latitude and Longitude using `utmgeo` (assuming a hardcoded meridian of -125.0 and Northern Hemisphere).
3.  **OMG_HDCS Header Population:**
    *   If it's the first record, it sets `summary.refTime`, `summary.refLat`, and `summary.refLong` based on the first record's data and writes the `summary` header to the output file.
    *   For each record, it populates an `OMG_HDCS_profile_header` (time offset, vessel heading, latitude/longitude offsets).
    *   It populates an `OMG_HDCS_beam` structure with the observed depth (applying `local_datum` correction if specified), along-track, and across-track offsets.
4.  **Write to Output:** Writes the `profile_header` and the `beam` data to the output OMG_HDCS file.

**Processing SDG Data (`-SDG`):**
1.  **Record Reading (`read_SDG` function):** The tool reads SDG records from the input binary file. The `read_SDG` function is responsible for:
    *   Reading `LENGTH_SDG` bytes of raw binary data into a buffer.
    *   Extracting and byte-swapping (using `get_swapped_int`, `get_swapped_short`) various fields like `time`, `raw_y_pos`, `raw_x_pos`, `proc_y_pos`, `proc_x_pos`, `raw_depth`, `proc_depth`, `tidal_corr`, `velo_corr`, `draft_heave_corr`, and `status_flag`.
    *   Calculating `d1970time` (double time since 1970) and converting `proc_y_pos`/`proc_x_pos` to `lat`/`lon`.
    *   Converting `proc_depth` to `real_depth` (in meters).
2.  **OMG_HDCS Header Population:**
    *   If it's the first record, it sets `summary.refTime`, `summary.refLat`, and `summary.refLong` and writes the `summary` header.
    *   For each SDG record, it populates an `OMG_HDCS_profile_header` and an `OMG_HDCS_beam` structure. `profile.tide` is set from `sdgr.tidal_corr`.
    *   `beams[0].status` is populated based on `sdgr.status_flag` (e.g., if a position or depth is bad). The `-showbits` flag provides verbose output of individual status bits.
    *   `beams[0].observedDepth` is set from `sdgr.raw_depth`.
3.  **Write to Output:** Writes the `profile_header` and the `beam` data to the output OMG_HDCS file.

**Finalization:** After processing all records, the tool closes input and output files.
