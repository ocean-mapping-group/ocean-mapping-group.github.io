---
layout: default
title: get8101BeamPattern
parent: OMG Tools
nav_order: 101
---
# get8101BeamPattern

## Description
`get8101BeamPattern` is a specialized utility designed to model the receive beam pattern (RBP) of SeaBat 8101/8111 multibeam sonars. It does this by analyzing the differences between sidescan trace data and beam-averaged backscatter data. The tool processes merged files, calculates various parameters like grazing angles and ensonified areas, and identifies data points suitable for RBP modeling.

The primary output is an ASCII file (`beampatt`) containing the mean and standard deviation of the intensity differences per beam, which represents the RBP. It can also generate a PGM image (`bp.pgm`) visualizing the differences.

## Usage
```bash
get8101BeamPattern <merged_file(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<merged_file(s)>` | **Required.** One or more paths to input OMG-HDCS merged files (with associated `.ss_data` files). |
| `-v` | Enable verbose output. |
| `-debug_ensonification` | Enable debugging for ensonification calculations. |
| `-debug_swath_geometry` | Enable debugging for swath geometry calculations. |
| `-use_layover` | (Disables check) Uses portions of the swath that are prone to layover. |
| `-use_multiple` | (Disables check) Uses portions of the swath potentially contaminated by multiple reflections. |
| `-use_all_enson` | (Disables check) Uses portions of the swath where ensonified area differs between backscatter sources. |
| `-stbd_only` | Process only starboard beams. |
| `-port_only` | Process only port beams. |
| `-curious <beam_num>` | Displays values found for a specific beam number during processing. |
| `-grazing <method>` | Specifies the grazing angle estimation method:
    *   `1`: Beam geometry only (`-slope` uses neighboring beams for across-track slope).
    *   `2`: (Default) Neighboring beams and swaths.
    *   `3`: Uses a DTM (Digital Terrain Model); requires `-dtm`. | `2` |
| `-slope` | (Used with `-grazing 1`) Estimates grazing angle via beam geometry and uses neighboring beams to account for across-track slope. |
| `-dtm <dtm.r4>` | Specifies a DTM file (in `.r4` format) to use with `-grazing 3`. |
| `-snippet` | Specify that the source of backscatter to compare sidescan to is snippet data. |
| `-ri_theta` | Specify that the source of backscatter to compare sidescan to is RI_theta (beam-averaged) data. |

## How It Works
1.  **Initialization:** Parses command-line arguments to set various flags for debugging, filtering, and grazing angle calculation methods.
2.  **DTM Loading (`-dtm`):** If a DTM is specified, it opens the `.r4` DTM file, reads its header, and loads the DTM data into memory.
3.  **File Iteration:** Loops through each input merged file:
    *   Opens the merged file and its corresponding `.ss_data` file.
    *   Loads sonar parameters from the `.param` file.
    *   Reads the summary header, confirming it's a SeaBat 8101/8111.
    *   **Beam Accumulators:** Dynamically allocates `beam_sum`, `beam_sum_squares`, and `beam_count` arrays for accumulating statistics per beam.
    *   **Profile Iteration:** Loops through each profile (ping) in the merged file:
        *   Reads the current profile header and raw beams.
        *   **Reson Data Reconstruction:** Reconstructs 16-bit raw trace and beam-averaged data from the 8-bit storage.
        *   **Grazing Angle Calculation:** Estimates grazing angles for each beam using the specified `grazing_method` (1, 2, or 3, with DTM lookup if applicable).
        *   **Ensonified Area Calculation:** Calculates ensonified areas for both trace and beam-averaged data.
        *   **Filtering:** Applies various checks (`checkMultiple`, `checkCommonRangeAmbiguity`, `check_ensonified_equality`) to filter out potentially problematic beams (layover, multiple reflections, unequal ensonified areas).
        *   **Backscatter Difference Calculation:** For each valid beam:
            *   Extracts calibrated trace backscatter (`trace_value`) and beam-averaged backscatter (`beam_value`) in logarithmic units (dB).
            *   Calculates the difference `(beam_value - trace_value)`.
            *   If the absolute difference exceeds a `threshold` (20.0 dB), the beam is skipped.
            *   Accumulates the difference into `beam_sum` and `beam_sum_squares`, and increments `beam_count` for the corresponding beam.
4.  **Statistical Output (`beampatt`):** After processing all files:
    *   Calculates the `mean` and `std_dev` of the backscatter differences for each beam that has accumulated data.
    *   Normalizes the `mean` values by subtracting the mean of a specific reference beam (beam 21).
    *   Writes these `mean`, `std_dev`, and `beam_count` values to an ASCII file named `beampatt`.
5.  **Image Output (`bp.pgm`):**
    *   Generates a PGM image visualizing the distribution of `(beam_value - trace_value)` differences.
    *   Scales the image pixels based on the occurrence frequency of differences.
    *   Draws the normalized mean difference curve onto the PGM image.
6.  **Cleanup:** Frees allocated memory and closes files.
```