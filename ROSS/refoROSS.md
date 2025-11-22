---
layout: default
title: refoROSS
parent: ROSS Tools
nav_order: 184
---
# refoROSS

## Description
`refoROSS` is a utility designed to convert HYPACK-formatted ROSS data (from systems like ROSS profilers or SeaBat 9001) into the OMG-HDCS (Ocean Mapping Group - Hydrographic Data Conversion System) merged file format. It parses ASCII data containing bathymetry, navigation, heading (GYR), and heave/roll/pitch (HCP) records, and then maps them to the corresponding OMG-HDCS structures.

This tool is essential for integrating ROSS data into the OMG processing pipeline, enabling further analysis and visualization with other OMG tools. It can also output a simplified "spitout" file for basic review.

## Usage
```bash
refoROSS <infile> <outfile_prefix> [-9001] [-leapyear] [-spitout <azifile>] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `<infile>` | **Required.** Path to the input HYPACK-formatted ROSS data file. |
| `<outfile_prefix>` | **Required.** Prefix for the output OMG-HDCS files. The tool will generate:
    *   `<outfile_prefix>.merged`: The main OMG-HDCS merged file.
    *   `<outfile_prefix>.nav`: Binary navigation file.
    *   `<outfile_prefix>.gyro`: Binary gyro (heading) attitude file.
    *   `<outfile_prefix>.orientation`: Binary heave/roll/pitch attitude file.
    *   `<outfile_prefix>.fix`: Binary fix data. |
| `-9001` | Specifies that the input data is from a SeaBat 9001 system (instead of a ROSS profiler). This changes beam configuration. |
| `-leapyear` | Accounts for a leap year when calculating Julian Day. |
| `-spitout <azifile>` | Creates a simplified "spitout" file (`.fix`) and uses an external azimuth file (`azifile`). |
| `-v` | Enable verbose output. |

## How It Works

1.  **Initialization:** Parses command-line arguments, setting input/output filenames and various flags (`sonar_type`, `leap_flag`, `spitout_flag`). Initializes OMG-HDCS structures (`OMG_HDCS_summary_header`, `OMG_HDCS_profile_header`, `OMG_HDCS_beam`, `OMG_HDCS_summary_attitude`, `OMG_HDCS_attitude`).
2.  **File Opening:** Opens the input HYPACK file for reading. Opens output files (`.merged`, `.nav`, `.gyro`, `.orientation`, `.fix`) as needed.
3.  **OMG Summary Header Initialization:** Initializes `summary` (for merged data) with `fileVersion`, `toolType` (ROSS_Profiler or Seabat9001), and `numDepths`.
4.  **Record Processing Loop:** Reads the input HYPACK file line by line:
    *   **Line ID Parsing:** Identifies the record type by a 3-character ID (e.g., "TND", "DEV", "PRD", "GYR", "POS", "RAW", "ECM", "HCP", "SB2", "EC1").
    *   **Timestamp Parsing ("TND" record):** Extracts date and time, converting it to Julian Day and a Unix timestamp (`day_time`).
    *   **Device Parameters ("PRD" record):** Extracts beam across, along, and draft offsets for ROSS profiler.
    *   **Gyro Data ("GYR" record):** Extracts `heading` and calls `dump_GYRO()` to write an `OMG_HDCS_attitude` record to the `.gyro` file.
    *   **Navigation Data ("RAW" record):** Extracts `centre_lat`, `centre_lon`, and creates a `jcu_nav_rec`. Writes it to the `.nav` file.
    *   **Heave/Roll/Pitch Data ("HCP" record):** Extracts `heave`, `roll`, `pitch` and calls `dump_HRP()` to write an `OMG_HDCS_attitude` record to the `.orientation` file.
    *   **ROSS Swath Data ("ECM" record):** Extracts `depth` and `nobeams` and calls `dump_ROSS_swath()` to write a profile of `across`, `along`, `depth` data to the `.merged` file.
    *   **SeaBat 9001 Swath Data ("SB2" record):** Extracts `soundvel`, `range`, `codes` and calls `dump_9001_swath()` to write a profile of `across`, `along`, `depth` data to the `.merged` file.
    *   **Spitout Mode (`-spitout`):** If enabled, it writes a simplified format to the `.fix` file.
5.  **Cleanup:** Closes all open files.

## Helper Functions

### `dump_GYRO()`
Writes heading data to the `.gyro` file.
*   Initializes `gyr_summary` for the first gyro record.
*   Populates `gyr_att` with `heading` and writes it to `gyrfile`.

### `dump_HRP()`
Writes heave, roll, pitch data to the `.orientation` file.
*   Initializes `hrp_summary` for the first HRP record.
*   Populates `hrp_att` with `heave`, `roll`, `pitch` and writes it to `hrpfile`.

### `dump_9001_swath()`
Writes SeaBat 9001 swath data to the `.merged` file.
*   Initializes `summary` for the first swath record.
*   Populates `profile` with time, position, attitude (derived), and various sonar settings.
*   Populates `beams` with calculated `acrossTrack`, `alongTrack`, `observedDepth` based on `range` and `array_angle`.
*   Writes `profile` and `beams` to `depfile`.

### `dump_ROSS_swath()`
Writes ROSS profiler swath data to the `.merged` file.
*   Initializes `summary` for the first swath record.
*   Populates `profile` with time, position, and (empty) attitude data.
*   Populates `beams` with `acrossTrack`, `alongTrack`, `observedDepth` based on extracted data.
*   Writes `profile` and `beams` to `depfile`.

## Output Files
*   `<outfile_prefix>.merged`: OMG-HDCS merged file.
*   `<outfile_prefix>.nav`: Binary navigation file.
*   `<outfile_prefix>.gyro`: Binary gyro (heading) attitude file.
*   `<outfile_prefix>.orientation`: Binary heave/roll/pitch attitude file.
*   `<outfile_prefix>.fix`: Simplified output file (if `-spitout`).
```
```