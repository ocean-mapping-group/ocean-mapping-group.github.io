---
layout: default
title: correctBS
parent: OMG Tools
nav_order: 83
---
# correctBS

## Description
`correctBS` is a specialized utility designed to correct multibeam backscatter (BS) data for various effects, including seabed slope, refracted path, and aspherical spreading. Its primary goal is to produce accurate, true grazing angle-corrected backscatter values, which can then be used to calculate beam pattern residuals and understand transducer roll effects.

The tool uses a Digital Terrain Model (DTM) for true seabed slope, and can incorporate raytracing-derived look-up tables (LUTs) for grazing angle, aspherical spreading, and beam angles. It can also identify shadowed areas and apply a mock backscatter calculation.

## Usage
```bash
correctBS <OMG_HDCS_merged_file(s)> -topo <DTM_file(.r4)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<OMG_HDCS_merged_file(s)>` | **Required.** One or more paths to input OMG-HDCS merged files. These files will be modified in place. |
| `-topo <DTM_file(.r4)>` | **Required.** Specifies the input Digital Terrain Model (DTM) file in `.r4` (float grid) format. Alternatively, `flat` can be used for nadir topography only. |
| `-image <file.merged>` | (Present in `USAGE` but not implemented) Likely intended to specify an input merged file to process. |
| `-water <LUT_prefix>` | Specifies a prefix for raytracing-derived Look-Up Table (LUT) files (e.g., `.grazing_angle`, `.aspherical`, `.beam_angle`). |
| `-mock` | Enable mock backscatter calculation (outputs angle difference). |
| `-maxangle <val>` | Maximum angle for mock backscatter calculation. | `25` |
| `-clip_beam <val>` | Minimum beam angle to map (masking out beam data inside the beam null). | `45.0` |
| `-cast_shadow` | Enable cast shadow detection. |
| `-min <val>` | Minimum dB value for the 8-bit output scale. | `-90.0` |
| `-max <val>` | Maximum dB value for the 8-bit output scale. | `0.0` |
| `-nofocus` | Disable beam focus correction. |
| `-v` | Enable verbose output. |

## How It Works
1.  **Input Reading & Initialization:**
    *   Opens input merged files and the DTM file (`-topo`).
    *   If `-water` is specified, it also opens raytracing-derived LUT files (`.grazing_angle`, `.aspherical`, `.beam_angle`) and loads their data into memory.
    *   Initializes `min_dB`, `max_dB`, `draft`, and other parameters.
2.  **DTM & LUT Loading:**
    *   Reads the DTM from the `.r4` file into a float array (`depths`).
    *   Reads grazing angle, aspherical spreading (focus), and beam angle LUTs into memory if `-water` is used.
    *   Initializes Mercator projection based on DTM header.
3.  **Profile and Beam Iteration:** Loops through each profile (ping) in the merged file and then through each beam within that profile:
    *   **Geographic Positioning:** Locates the beam's geographic position (lat/lon) using `locate_beam`.
    *   **DTM Lookup:** Projects the beam's lat/lon onto the DTM grid (`xpos`, `ypos`) and retrieves the DTM depth (`value`) at that location, along with adjacent depths for slope calculation (`peast`, `psouth`).
    *   **True Grazing Angle Calculation:**
        *   If `flat_flag` is used, assumes a flat seafloor.
        *   Otherwise, it uses `vectangle` (an external function for 3D vector calculation) to determine the `true_grazing_angle` from the DTM, beam elevation, and azimuth.
    *   **Beam Focus & Shadowing:**
        *   Retrieves `beam_focus` from the aspherical LUT if available.
        *   Performs `cast_shadow_flag` checks to identify shadowed areas.
        *   Applies `clip_beam` to mask out data inside the beam null.
    *   **Backscatter Correction/Calculation:**
        *   **Unimageable/Shadowed Areas:** If `true_grazing_angle` is negative (indicating unimageable seafloor or shadow), it assigns a specific color (RED, GREEN, BLUE, YELLOW) to `Beams[j].pseudoAngleIndependentBackscatter`.
        *   **True Backscatter (`!mock_flag`):** If not in mock mode, `Beams[j].pseudoAngleIndependentBackscatter` is set based on `true_grazing_angle` (scaled to 8-bit). `Beams[j].freq` and `Beams[j].sample_interval` are also updated with related parameters (rgraze and insonified area).
        *   **Mock Backscatter (`mock_flag`):** Calculates `angle_diff` (`rgraze - true_grazing_angle`) and scales it to `Beams[j].pseudoAngleIndependentBackscatter`.
        *   **Backscatter Strength (`backscatter_flag`, currently not directly used):** Contains commented-out logic for calculating backscatter strength based on sonar equation components.
4.  **In-Place Modification:** The `pseudoAngleIndependentBackscatter`, `freq`, and `sample_interval` fields of the `Beams` structure are updated in the merged file.

## Output Files
The input merged files are modified in-place.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `array.h`: For `JHC_header` structure and DTM data handling.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.
*   `backscatter.h`: For `vectangle` function.

## Notes
This tool is critical for quantitative backscatter analysis, allowing for the normalization of backscatter values for environmental and geometric effects. The corrected `pseudoAngleIndependentBackscatter` can then be used for seafloor classification and habitat mapping. The use of raytracing-derived LUTs significantly improves the accuracy of grazing angle and spreading loss corrections.