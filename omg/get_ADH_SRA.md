---
layout: default
title: get_ADH_SRA
parent: OMG Tools
nav_order: 99
---
# get_ADH_SRA

## Description
`get_ADH_SRA` is a utility designed to calculate and output Sonar Relative Angles (SRA) and Vertically Referenced Angles (VRA) from OMG-HDCS merged files. It provides options to compute these angles using either vessel attitude data (from an `.orientation` file) or through cone-to-cone intersection geometry. The output can be in JHC `.r4` (float grid) format or ASCII text files, for both across-track and along-track components.

This tool is essential for advanced backscatter processing, beam pattern analysis, and calibration, where accurate knowledge of the beam's angle relative to the sonar or the vertical is critical.

## Usage
```bash
get_ADH_SRA <input_omg_file(.merged)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<input_omg_file(.merged)>` | **Required.** One or more paths to input OMG-HDCS merged files. |
| `-only_VRA` | Writes out only Vertically Referenced Angles (VRA). |
| `-only_Across_track` | Writes out only across-track SRA. |
| `-only_Along_track` | Writes out only along-track SRA. |
| `-use_cone_cone_intersection` | Computes SRA using cone-to-cone intersection geometry. |
| `-use_attitudedata` | Computes SRA using attitude data from the `.orientation` file. (This is the default if neither `use_cone_cone_intersection` nor `only_VRA` is specified). |
| `-write_ascii` | Additionally writes ASCII text files for the calculated angles. |
| `-out_ext <extension>` | Optional extension to append to the output filenames (e.g., `.SRA_across_cone.<extension>.r4`). |
| `-v` | Enable verbose output. |

## How It Works
1.  **Initialization:** Parses command-line arguments to set output options (e.g., `only_VRA`, `only_Across_track`, `use_attitudedata`, `write_ascii`).
2.  **File Setup:**
    *   Opens input merged file (`.merged`).
    *   Loads sonar parameters from the `.param` file.
    *   Opens the `.orientation` file (required for attitude-based calculations).
    *   Opens the `.sectors` file (required for multi-sector sonars to get TX sector information).
3.  **Output File Creation:** Based on the chosen options (e.g., `only_Across_track`, `only_Along_track`, `only_VRA`) and computation method (`use_attitudedata` or `use_cone_cone_intersection`), it creates output `.r4` files for storing the calculated SRA/VRA values. If `write_ascii` is specified, it also creates corresponding ASCII text files. JHC headers are written to the `.r4` files.
4.  **Profile Iteration:** Loops through each profile (ping) in the merged file:
    *   Reads the profile header and raw beams.
    *   Calculates `tx_time_for_RBP` (transmit time) from the profile.
    *   Loads transmit sector information (`tx_sectors`) for the current profile.
    *   **Angle Calculation per Beam:** For each beam `j` in the profile:
        *   **`use_attitudedata` Method:** If selected, it calls `get_SRA()` (an external function, likely from `grazing_angle.h`) to calculate SRA components (across-track, along-track, VRA) using attitude data from the `.orientation` file and TX sector information.
        *   **`use_cone_cone_intersection` Method:** If selected, it calls `get_SRA_from_geometry()` (an external function) to calculate SRA components based on the sonar's geometry.
        *   **`only_VRA` Method (without attitude data):** If `only_VRA` is selected and `use_attitudedata` is *not* used, it calls `get_grazing_angles()` to compute VRA (Vertically Referenced Angles) directly from depth and across-track values. It then converts the VRA sign convention.
    *   **Output Writing:** Writes the calculated angle values for each beam to the corresponding `.r4` (and optionally ASCII) output files.
5.  **Cleanup:** Closes all open files.

## Output Files
*   `<input_omg_file_prefix>.SRA_across.r4`: JHC float grid of across-track SRA.
*   `<input_omg_file_prefix>.SRA_along.r4`: JHC float grid of along-track SRA.
*   `<input_omg_file_prefix>.VRA.r4`: JHC float grid of VRA.
*   Corresponding ASCII files (`.SRA_across.txt`, `.SRA_along.txt`, `.VRA.txt`) if `-write_ascii` is used.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `array.h`: For `JHC_header` structure and `.r4` file handling.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.
*   `grazing_angle.h`: For `get_SRA`, `get_grazing_angles` functions.

## Notes
The calculation of Sonar Relative Angles and Vertically Referenced Angles is fundamental for understanding how the sonar beam interacts with the seafloor and for applying correct backscatter compensation. This tool provides various methods for computing these angles, accommodating different data availability (e.g., with or without precise attitude data) and analytical needs. The output `.r4` grids allow for easy visualization and integration with other gridded data.