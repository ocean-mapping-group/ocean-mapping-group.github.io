---
layout: default
title: 8k2omg
parent: Reson Tools
nav_order: 182
---
# 8k2omg

## Description
`8k2omg` is a utility designed to convert older Reson SeaBat 8000 series data (`.81x` files) into the OMG-HDCS (Ocean Mapping Group - Hydrographic Data Conversion System) merged file format. It extracts bathymetry and snippet data from the `.81x` files and maps them to the corresponding structures in the OMG-HDCS format.

This tool provides a bridge for older Reson data to be processed and integrated within the modern OMG toolkit. It handles various aspects of the conversion, including time synchronization, quality flags, and basic sonar calibration parameters.

## Usage
```bash
8k2omg -81x <input_name> -omg <omg_prefix> [-v] [-debug] [-ER]
```

## Arguments

| Option | Description |
|---|---|
| `-81x <input_name>` | **Required.** Path to the input Reson SeaBat 8000 series (`.81x`) file. |
| `-omg <omg_prefix>` | **Required.** Prefix for the output OMG-HDCS files. The tool will generate:
    *   `<omg_prefix>.merged`: The main OMG-HDCS merged file.
    *   `<omg_prefix>.merged.ss_data`: Snippet side-scan data. |
| `-v` | Enable verbose output. |
| `-debug` | Enable debug output. |
| `-ER` | Indicates an Extended Range projector (affects source level calculation). |

## How It Works

1.  **Initialization:** Parses command-line arguments, setting input/output filenames and various flags (e.g., `verbose`, `debug`, `extended_range`). Initializes Reson 8000 series data structures (`RESON_PEEKER`, `RESON_BATHY`, `RESON_SNIPPET`, `SNP1`) and OMG-HDCS structures (`OMG_HDCS_summary_header`, `OMG_HDCS_profile_header`, `OMG_HDCS_beam`).
2.  **File Opening:** Opens the input `.81x` file for reading. Creates the output OMG-HDCS merged file (`.merged`) and snippet data file (`.merged.ss_data`).
3.  **Initial Bathy Record Scan:** Performs a preliminary scan to find the first valid bathymetry record, which is used to initialize the `OMG_HDCS_summary_header` (e.g., `sonar_type`, `base_time`, `refTime`).
4.  **OMG Summary Header Initialization:**
    *   Determines `sonar_type` based on `bathy.sonar_model`.
    *   Initializes an `OMG_HDCS_summary_header` structure, setting `fileVersion`, `toolType`, `refTime`, `numDepths`, etc.
    *   Writes this summary header to the `.merged` file.
    *   Allocates memory for `OMG_HDCS_beam` structures.
5.  **Record Processing Loop:** Rewinds the input `.81x` file and processes it record by record:
    *   **Sync Search:** Calls `seek_next_8K_sync()` (an external function) to find the next Reson 8k synchronization pattern.
    *   **Record Type Identification:** Reads `RESON_PEEKER` to determine the packet type (Bathy or Snippet).
    *   **Data Reading:**
        *   If it's a Bathy record (`RESON_8K_SYNC_PATTERN`), reads `RESON_BATHY` data (`bathy`).
        *   If it's a Snippet record (`SNIPPET_ID_SNP0`), reads `RESON_SNIPPET` data (`snippet`).
    *   **Ping Matching:** Continues until a Bathy record and a Snippet record with matching `ping_number` are found.
    *   **OMG Profile Header Population:** Populates an `OMG_HDCS_profile_header` structure from the `bathy` data:
        *   `timeOffset` is calculated relative to `summary.refTime`.
        *   Sonar settings like `samp_rate`, `power`, `TVG`, `pulseLength`, `rx_gain_reduction`, `tx_power_reduction`, `max_swath_width` are set.
        *   Source level (`profile.params[0].txLevel`) is estimated based on `sonar_type` and `extended_range`.
        *   Projector beam width (`profile.params[0].txBeamAngle`) and projector angle (`profile.params[1].txPulseLength`) are set.
    *   **OMG Beam Structure Population:** For each beam:
        *   `beams[i].range` is set from `bathy.range[i]`.
        *   Preliminary `beams[i].observedDepth` and `beams[i].acrossTrack` are calculated using simplified geometry (angle derived from beam index, slant range from `bathy.range[i]`).
        *   `beams[i].status` and `beams[i].Q_factor` are derived from `bathy.quality[i]`.
        *   `beams[i].calibratedBackscatter` and `beams[i].reflectivity` are derived from `bathy.intensity`.
        *   **Snippet Data Processing:**
            *   `beams[i].centre_no`, `beams[i].no_samples` are derived from `bathy.range[i]` and `snippet` data.
            *   `beams[i].offset` is set to the current file pointer in `outfile_snippets`.
            *   Snippet samples are written to `outfile_snippets`.
            *   `beams[i].reflectivity` is recalculated from the average snippet amplitude.
    *   **Write to Merged File:** `OMG_HDCS_write_profile()` and `OMG_HDCS_put_raw_beams()` write the populated profile header and beam data to the `.merged` file.
6.  **Cleanup:** Closes all open files and frees allocated memory.

## Output Files
*   `<omg_prefix>.merged`: Standard OMG-HDCS merged file.
*   `<omg_prefix>.merged.ss_data`: Snippet side-scan data (binary, raw short intensities).
```
---
layout: default
title: 8k2omg
parent: Reson Tools
nav_order: 182
---
# 8k2omg

## Description
`8k2omg` is a utility designed to convert older Reson SeaBat 8000 series data (`.81x` files) into the OMG-HDCS (Ocean Mapping Group - Hydrographic Data Conversion System) merged file format. It extracts bathymetry and snippet data from the `.81x` files and maps them to the corresponding structures in the OMG-HDCS format.

This tool provides a bridge for older Reson data to be processed and integrated within the modern OMG toolkit. It handles various aspects of the conversion, including time synchronization, quality flags, and basic sonar calibration parameters.

## Usage
```bash
8k2omg -81x <input_name> -omg <omg_prefix> [-v] [-debug] [-ER]
```

## Arguments

| Option | Description |
|---|---|
| `-81x <input_name>` | **Required.** Path to the input Reson SeaBat 8000 series (`.81x`) file. |
| `-omg <omg_prefix>` | **Required.** Prefix for the output OMG-HDCS files. The tool will generate:
    *   `<omg_prefix>.merged`: The main OMG-HDCS merged file.
    *   `<omg_prefix>.merged.ss_data`: Snippet side-scan data. |
| `-v` | Enable verbose output. |
| `-debug` | Enable debug output. |
| `-ER` | Indicates an Extended Range projector (affects source level calculation). |

## How It Works

1.  **Initialization:** Parses command-line arguments, setting input/output filenames and various flags (e.g., `verbose`, `debug`, `extended_range`). Initializes Reson 8000 series data structures (`RESON_PEEKER`, `RESON_BATHY`, `RESON_SNIPPET`, `SNP1`) and OMG-HDCS structures (`OMG_HDCS_summary_header`, `OMG_HDCS_profile_header`, `OMG_HDCS_beam`).
2.  **File Opening:** Opens the input `.81x` file for reading. Creates the output OMG-HDCS merged file (`.merged`) and snippet data file (`.merged.ss_data`).
3.  **Initial Bathy Record Scan:** Performs a preliminary scan to find the first valid bathymetry record, which is used to initialize the `OMG_HDCS_summary_header` (e.g., `sonar_type`, `base_time`, `refTime`).
4.  **OMG Summary Header Initialization:**
    *   Determines `sonar_type` based on `bathy.sonar_model`.
    *   Initializes an `OMG_HDCS_summary_header` structure, setting `fileVersion`, `toolType`, `refTime`, `numDepths`, etc.
    *   Writes this summary header to the `.merged` file.
    *   Allocates memory for `OMG_HDCS_beam` structures.
5.  **Record Processing Loop:** Rewinds the input `.81x` file and processes it record by record:
    *   **Sync Search:** Calls `seek_next_8K_sync()` (an external function) to find the next Reson 8k synchronization pattern.
    *   **Record Type Identification:** Reads `RESON_PEEKER` to determine the packet type (Bathy or Snippet).
    *   **Data Reading:**
        *   If it's a Bathy record (`RESON_8K_SYNC_PATTERN`), reads `RESON_BATHY` data (`bathy`).
        *   If it's a Snippet record (`SNIPPET_ID_SNP0`), reads `RESON_SNIPPET` data (`snippet`).
    *   **Ping Matching:** Continues until a Bathy record and a Snippet record with matching `ping_number` are found.
    *   **OMG Profile Header Population:** Populates an `OMG_HDCS_profile_header` structure from the `bathy` data:
        *   `timeOffset` is calculated relative to `summary.refTime`.
        *   Sonar settings like `samp_rate`, `power`, `TVG`, `pulseLength`, `rx_gain_reduction`, `tx_power_reduction`, `max_swath_width` are set.
        *   Source level (`profile.params[0].txLevel`) is estimated based on `sonar_type` and `extended_range`.
        *   Projector beam width (`profile.params[0].txBeamAngle`) and projector angle (`profile.params[1].txPulseLength`) are set.
    *   **OMG Beam Structure Population:** For each beam:
        *   `beams[i].range` is set from `bathy.range[i]`.
        *   Preliminary `beams[i].observedDepth` and `beams[i].acrossTrack` are calculated using simplified geometry (angle derived from beam index, slant range from `bathy.range[i]`).
        *   `beams[i].status` and `beams[i].Q_factor` are derived from `bathy.quality[i]`.
        *   `beams[i].calibratedBackscatter` and `beams[i].reflectivity` are derived from `bathy.intensity`.
        *   **Snippet Data Processing:**
            *   `beams[i].centre_no`, `beams[i].no_samples` are derived from `bathy.range[i]` and `snippet` data.
            *   `beams[i].offset` is set to the current file pointer in `outfile_snippets`.
            *   Snippet samples are written to `outfile_snippets`.
            *   `beams[i].reflectivity` is recalculated from the average snippet amplitude.
    *   **Write to Merged File:** `OMG_HDCS_write_profile()` and `OMG_HDCS_put_raw_beams()` write the populated profile header and beam data to the `.merged` file.
6.  **Cleanup:** Closes all open files and frees allocated memory.

## Output Files
*   `<omg_prefix>.merged`: Standard OMG-HDCS merged file.
*   `<omg_prefix>.merged.ss_data`: Snippet side-scan data (binary, raw short intensities).
```
```