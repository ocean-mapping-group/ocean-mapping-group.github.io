---
layout: default
title: mergeSB2K
parent: SB2K Tools
nav_order: 191
---
# mergeSB2K

## Description
`mergeSB2K` is a utility designed to merge SeaBeam 2000 sidescan data (from GLORIA-format files) onto existing OMG-HDCS (`.merged`) bathymetry files. It essentially adds a reference to the corresponding sidescan data within the beam structures of the `.merged` file, allowing other OMG tools to access and display the sidescan imagery alongside the bathymetry.

This tool is useful for integrating sidescan data, which provides valuable information about seabed texture and features, with multibeam bathymetry for a more complete understanding of the seafloor.

## Usage
```bash
mergeSB2K -ss <tidefile> <mergefile(s)> [-v] [-date <year> <month> <day>] [-base_offset <value>]
```

## Arguments

| Option | Description |
|---|---|
| `-ss <tidefile>` | **Required.** Path to the GLORIA-format sidescan file (named `tidefile` due to historical reasons, likely containing time-indexed sidescan records). |
| `<mergefile(s)>` | **Required.** One or more OMG-HDCS `.merged` files to which the sidescan data will be merged. |
| `-v` | Enable verbose output. |
| `-date <year> <month> <day>` | (Optional) Manually set the reference date for the summary header in the `.merged` file. This can be useful if the timestamp in the `.merged` file's header is incorrect or missing. |
| `-base_offset <value>` | (Optional) Sets an integer base offset (in millimeters) to be added to the tide value. Used for tide correction (historical name). |

## How It Works

1.  **Initialization:** Parses command-line arguments to get the sidescan (GLORIA) file path, input merged files, and optional parameters (`verbose_flag`, `year`, `month`, `day`, `base_offset`).
2.  **GLORIA File Opening:** Opens the GLORIA-format sidescan file (`tidefile`) for reading.
3.  **Merged File Processing Loop:**
    *   For each input `.merged` file:
        *   Opens the file in read/write mode (`r+`).
        *   Reads the `OMG_HDCS_summary_header`. If a `-date` is provided, it updates `summary.refTime` in the header and writes it back to the file.
        *   **Profile Iteration:** Iterates through each profile (ping) in the merged file:
            *   Reads the `OMG_HDCS_profile_header`.
            *   Calculates the absolute time (`time`) of the current profile.
            *   **Sidescan Record Search:** Uses `jcu_time_search()` to find the closest matching sidescan record in the GLORIA file based on `time`.
            *   Reads the `gloria_rec` (sidescan record) from the GLORIA file.
            *   **Beam Data Update:** Reads the existing `OMG_HDCS_beam` array for the current profile. It then updates specific fields of beam `61` (hardcoded index) in the `beams` array:
                *   `beams[61].offset`: Set to the file offset of the sidescan data within the GLORIA file.
                *   `beams[61].no_samples`: Set to the number of samples (fixed at `1024`).
                *   `beams[61].centre_no`: Set to the center sample (`512`).
                *   `beams[61].sample_interval`: Set to the pixel size from the GLORIA header (`tide_rec.header.pixel_size`).
            *   Writes the modified `OMG_HDCS_beam` array back to the `.merged` file.
        *   Closes the current `.merged` file.
4.  **Cleanup:** Closes the GLORIA file and exits.

## Output
The input `.merged` files are modified in-place. The `OMG_HDCS_beam` structure for beam `61` (a specific placeholder beam) in each profile is updated with references (offset, sample count, etc.) to the corresponding sidescan data within the GLORIA file.
```
```