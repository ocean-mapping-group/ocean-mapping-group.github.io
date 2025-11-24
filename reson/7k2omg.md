---
layout: default
title: 7k2omg
parent: Reson Tools
nav_order: 177
---
# 7k2omg

## Description
`7k2omg` is a utility designed to convert Reson 7k (`.s7k`) data files into the OMG-HDCS (Ocean Mapping Group - Hydrographic Data Conversion System) merged file format. This tool extracts bathymetry, sonar settings, snippet, and watercolumn data from `.s7k` files and maps them to the corresponding structures in the OMG-HDCS format.

It supports both old and new 7k bathymetry and snippet packet types, handles various Reson sonar models, and provides options for ignoring specific data types, forcing old packet usage, and dealing with dual-head sonar systems. The output merged file is a foundational format for further processing and visualization within the OMG toolkit.

## Usage
```bash
7k2omg -s7k <input_name> -omg <omg_file_prefix> [-sonar <type>] [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `-s7k <input_name>` | **Required.** Path to the input Reson 7k `.s7k` file. |
| `-omg <omg_file_prefix>` | **Required.** Prefix for the output OMG-HDCS files. The tool will generate:
    *   `<omg_file_prefix>.merged`: The main OMG-HDCS merged file.
    *   `<omg_file_prefix>.merged.ss_data`: Snippet side-scan data (if not ignored).
    *   `<omg_file_prefix>.sonar_settings`: Binary file containing 7k Sonar Settings and Remote Control Settings.
    *   `<omg_file_prefix>.watercol`: Watercolumn data (if not ignored). |
| `-sonar [7125|7111|7101|7150|7160|20 (for T20P)]` | Specifies the Reson sonar model. |
| `-v` | Enable verbose output. | |
| `-debug` | Enable debug output. | |
| `-ignore_flags` | Ignores quality flags, treating all beams as valid. | |
| `-ignore_snippets` | Skips processing and writing of snippet data. | |
| `-ignore_watercolumn` | Skips processing and writing of watercolumn data. | |
| `-dual_head` | Stores the system identifier in the profile mode field, useful for dual-head systems. | |
| `-force_old_bathy` | Forces the use of old bathymetry packets (7006) even if new ones (7027) are present. | |
| `-force_old_snippets` | Forces the use of old snippet packets (7008) even if new ones (7028) are present. | |

## How It Works

1.  **Initialization:** Parses command-line arguments, setting input/output filenames and various flags (e.g., `ignore_snippets`, `force_old_bathy`, `dual_head`). Initializes Reson 7k data structures and `j_EM_watercolumn`.
2.  **7k Indexing:** Calls `build_Reson_7K_Index()` (an external function) to create an index of all packet types within the `.s7k` file.
3.  **File Opening:** Opens the input `.s7k` file for reading. Creates the output OMG-HDCS merged file (`.merged`), snippet data file (`.merged.ss_data`), sonar settings file (`.sonar_settings`), and watercolumn file (`.watercol`).
4.  **OMG Summary Header Initialization:**
    *   Determines `bathy_id` (7006 or 7027) and `snippets_id` (7008 or 7028) based on available packets and `force_old_*` flags.
    *   Reads the first bathy packet to determine `base_time`.
    *   Initializes an `OMG_HDCS_summary_header` structure, setting `fileVersion`, `toolType` (from `-sonar` option), `refTime`, `numDepths`, etc.
    *   Writes this summary header to the `.merged` file.
    *   Allocates memory for `OMG_HDCS_beam` structures.
5.  **Ping Traversal Loop:** Iterates through each Bathy packet (ping) found in the `.s7k` index:
    *   Reads the Bathy packet (`7006` or `7027`) and extracts `ping_time`.
    *   Searches the index for corresponding `7000_Sonar_Settings`, `7503_Remote_Control_Settings`, `7004_Beam_Geometry`, and snippet/watercolumn records based on `ping_time`.
    *   Reads these associated records.
    *   **OMG Profile Header Population:** Populates an `OMG_HDCS_profile_header` structure:
        *   `ping_number`, `multi_ping_sequence`, `num_beams` are set from bathy data.
        *   `td_sound_speed` is set from sonar settings or bathy.
        *   Various offsets to raw 7k packet headers are stored in the profile header and written to `.sonar_settings`.
        *   Snippet sample descriptors are stored in the profile header.
        *   `profile.mode` is set to `drf.system_enumerator` if `dual_head`.
    *   **OMG Beam Structure Population:** For each beam (`j`) within the current ping:
        *   Extracts `beam_index`.
        *   `beams[beam_index].Tx_steer`, `beams[beam_index].twtt`, `beams[beam_index].range`, `beams[beam_index].Rc_steer`, `beams[beam_index].beam_depress_angle` are set from bathy and beam geometry data.
        *   `beams[beam_index].status` and `beams[beam_index].Q_factor` are derived from quality flags, respecting `ignore_flags`.
        *   `beams[beam_index].reflectivity` is set from signal strength or calculated from snippets.
        *   Preliminary `beams[beam_index].observedDepth` and `beams[beam_index].acrossTrack` are calculated.
        *   If snippet data is available:
            *   `beams[beam_index].centre_no`, `beams[beam_index].no_samples`, `beams[beam_index].offset`, `beams[beam_index].snippet_first_sample`, `beams[beam_index].snippet_last_sample` are set.
            *   Snippet samples are written to `.merged.ss_data`.
    *   **Watercolumn Data (`-watercolumn`):** If watercolumn data is present and not ignored:
        *   Calls `convert_7K_watercolumn()` to convert 7k watercolumn data to OMG format.
        *   Calls `j_EM_write_watercolumn()` to write the OMG watercolumn data to `.watercol`.
    *   **Write to Merged File:** `OMG_HDCS_write_profile()` and `OMG_HDCS_put_raw_beams()` write the populated profile header and beam data to the `.merged` file.
    *   Increments `num_bathy_recs`.
6.  **Cleanup:** Frees allocated memory and closes all open files.

## Output Files
*   `<omg_file_prefix>.merged`: Standard OMG-HDCS merged file.
*   `<omg_file_prefix>.merged.ss_data`: Snippet side-scan data (binary, raw short intensities).
*   `<omg_file_prefix>.sonar_settings`: Binary file containing 7k Sonar Settings and Remote Control Settings.
*   `<omg_file_prefix>.watercol`: Watercolumn data (binary).

## Dependencies
*   `Reson_7K_parser.h`: For Reson 7k data structures and parsing functions.
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `j_EM_watercol.h`: For water column data structures.
*   `support.h`: For general utility functions and error handling.

## Notes
`7k2omg` is a critical tool for integrating Reson 7k raw data into the standard OMG-HDCS processing workflow. It handles the complex translation from Reson's proprietary binary format to the structured OMG-HDCS format, extracting and organizing bathymetry, sonar settings, snippet, and watercolumn data. The various options for handling packet types and data sources provide flexibility for different processing needs. The tool creates new files without modifying the original `.s7k` input.