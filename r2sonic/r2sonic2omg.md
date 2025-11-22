---
layout: default
title: r2sonic2omg
parent: R2Sonic Tools
nav_order: 161
---
# r2sonic2omg

## Description
`r2sonic2omg` is a utility designed to convert R2Sonic multibeam sonar data (`.r2s` files) into the OMG-HDCS (Ocean Mapping Group - Hydrographic Data Conversion System) merged file format. This tool extracts bathymetry, snippet (full time series), and TruePix (beam-formed magnitude and angle time series) data from the `.r2s` files and maps them to the corresponding structures in the OMG-HDCS format.

It allows for optional roll stabilization and provides flags to skip certain data types, making it flexible for different processing workflows. The output merged file is a foundational format for further processing and visualization within the OMG toolkit.

## Usage
```bash
r2sonic2omg -r2s <input.r2s> -omg <omg_file_prefix> [-skip_fts] [-skip_truepix] [-roll_stabilize] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `-r2s <input.r2s>` | **Required.** Path to the input R2Sonic `.r2s` file. |
| `-omg <omg_file_prefix>` | **Required.** Prefix for the output OMG-HDCS files. The tool will generate:
    *   `<omg_file_prefix>.merged`: The main OMG-HDCS merged file.
    *   `<omg_file_prefix>.merged.ss_data`: Snippet side-scan data (if not skipped).
    *   `<omg_file_prefix>.sonar_settings`: Binary file containing R2Sonic packet headers (BTH0, FTS0, TPX0). |
| `-skip_fts` | Skips processing and writing of Full Time Series (FTS) snippet data. |
| `-skip_truepix` | Skips processing and writing of TruePix data. |
| `-roll_stabilize` | Adjusts beam angles by roll stabilization angles prior to calculating preliminary soundings. This does not affect receiver steering angles in the output file. |
| `-v` | Enable verbose output. |

## How It Works

1.  **Initialization:** Parses command-line arguments, setting input/output filenames and various flags (e.g., `skip_fts`, `skip_truepix`, `do_roll_stabilize`).
2.  **File Opening:** Opens the input `.r2s` file for reading. Creates the output OMG-HDCS merged file (`.merged`), snippet data file (`.merged.ss_data`), and a sonar settings file (`.sonar_settings`).
3.  **R2Sonic Indexing:** Calls `build_R2SONIC_INDEX()` (an external function) to create an index of all packet types within the `.r2s` file.
4.  **OMG Summary Header Initialization:**
    *   Reads the first bathy packet to determine `base_time` and `sonar_type`.
    *   Initializes an `OMG_HDCS_summary_header` structure, setting `fileVersion`, `toolType`, `refTime`, `numDepths`, etc.
    *   Writes this summary header to the `.merged` file.
    *   Allocates memory for `OMG_HDCS_beam` structures.
5.  **Packet Traversal Loop:** Iterates through each Bathy packet (`R2SONIC_ID_BTH0`) found in the `.r2s` index:
    *   Seeks to the Bathy packet's file offset and reads the `R2SONIC_BATHY` data (`bathy`).
    *   Finds corresponding FTS (`R2SONIC_ID_SNI0`) and TruePix (`R2SONIC_ID_TPX0`) packets by matching ping numbers.
    *   Reads `R2SONIC_FTS` and `R2SONIC_TRUEPIX` data if not skipped. Handles fragmented FTS packets.
    *   **OMG Profile Header Population:** Populates an `OMG_HDCS_profile_header` structure:
        *   `ping_time` is converted from R2Sonic time.
        *   `numDepths`, `bathy_sample_rate`, `td_sound_speed` are set from `bathy` header.
        *   `profile.vesselRoll` is set if `do_roll_stabilize`.
        *   Offsets to raw R2Sonic headers (BTH0, FTS0, TPX0) are stored in `profile.sonar_settings_offset_*` and written to `.sonar_settings`.
        *   TruePix magnitude and angle data are written to `.merged.ss_data`, and their offsets/scales are stored in the profile header.
    *   **OMG Beam Structure Population:** For each beam in the `bathy` data:
        *   `beams[i].twtt`, `beams[i].range`, `beams[i].Rc_steer` are set.
        *   `beams[i].status` and `beams[i].Q_factor` are derived from R2Sonic `quality` flags.
        *   Preliminary `beams[i].observedDepth` and `beams[i].acrossTrack` are calculated using `range`, `angle`, and optionally `roll_stabilize_angle`.
        *   `beams[i].reflectivity` is set from `bathy.beam[i].intensity` or TruePix data.
        *   If FTS data is available and not skipped:
            *   `beams[i].no_samples`, `beams[i].snippet_first_sample` are set.
            *   `beams[i].centre_no` is calculated from `twtt_corr`.
            *   `beams[i].offset` is set to the current file pointer in `.merged.ss_data`.
            *   Snippet samples are written to `.merged.ss_data`.
    *   **Write to Merged File:** `OMG_HDCS_write_profile()` and `OMG_HDCS_put_raw_beams()` write the populated profile header and beam data to the `.merged` file.
7.  **Cleanup:** Frees allocated memory and closes all open files.

## Output Files
*   `<omg_file_prefix>.merged`: Standard OMG-HDCS merged file.
*   `<omg_file_prefix>.merged.ss_data`: Snippet side-scan data (binary, raw short intensities).
*   `<omg_file_prefix>.sonar_settings`: Binary file containing R2Sonic packet headers (for BTH0, FTS0, TPX0).
```
```