---
layout: default
title: refoELAC
parent: ELAC Tools
nav_order: 2
---
# refoELAC

## Description
`refoELAC` is a command-line utility designed to convert raw Honeywell ELAC Bottom Chart FAU (Fast Acquisition Unit) format multibeam data into the OMG-HDCS (Ocean Mapping Group - Hydrographic Data Cleaning System) `.merged` format. It processes the proprietary ELAC data, extracts bathymetry, position, and attitude information, applies a Mercator projection for geographical coordinates, and writes the data into a standard OMG-HDCS merged file, complete with image extensions. It also generates auxiliary files for amplitude and quality histograms.

## Usage
```bash
refoELAC [OPTIONS] <input_FAU_file> <output_merged_file>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output during processing. | |
| `-constant <value>` | Apply a constant offset to the northing values during conversion (used to adjust for specific projection origins). | `0` |
| `-merid <longitude>` | Specifies the central meridian (longitude) for the Mercator projection. | `-69.0` |
| `-proj_lat <latitude>` | Specifies the projection latitude for the Mercator projection. | `45.83333333` |
| `<input_FAU_file>` | **Required.** The input Honeywell ELAC Bottom Chart FAU format data file. | `elac_raw_data.fau` |
| `<output_merged_file>` | **Required.** The base name for the output OMG-HDCS merged file and its associated amplitude and quality histogram files. | `elac_converted.merged` |

## Output Files
*   `<output_merged_file>`: The converted OMG-HDCS `.merged` file.
*   `<output_merged_file>.quality`: An ASCII file containing quality histograms by grazing angle.
*   `<output_merged_file>.amplitudes`: An ASCII file containing amplitude histograms.

## How It Works
1.  **File Opening:** Opens the input FAU file for reading and the output `.merged` and histogram files for writing.
2.  **Projection Setup:** Initializes a Mercator projection based on the provided `-merid` and `-proj_lat` values.
3.  **FAU Data Processing:** Reads the FAU file record by record, parsing proprietary ELAC data structures.
4.  **Data Extraction:** Extracts bathymetry (depth, across-track), position (latitude, longitude), and attitude (roll, pitch, heading) for each ping and beam.
5.  **Coordinate Conversion:** Converts geographic coordinates to projected (Easting, Northing) using the Mercator projection and applies any `-constant` offset.
6.  **OMG-HDCS Header Population:** Populates the `OMG_HDCS_summary_header`, `OMG_HDCS_profile_header`, and `OMG_HDCS_beam` structures with the extracted and converted data.
7.  **Histogram Generation:** Accumulates amplitude and quality values for histograms, which are written to `.amplitudes` and `.quality` files.
8.  **Output:** Writes the populated `profile_header` and `beam` data to the `.merged` file.
9.  **Cleanup:** Closes all open files.

## Notes
This tool is crucial for integrating proprietary ELAC data into the standardized OMG-HDCS format, enabling subsequent processing and analysis with other tools in the OMG ecosystem.