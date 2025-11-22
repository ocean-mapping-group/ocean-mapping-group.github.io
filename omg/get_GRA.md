---
layout: default
title: get_GRA
parent: OMG Tools
nav_order: 100
---
# get_GRA

## Description
`get_GRA` is a utility designed to calculate and output various types of grazing angles (GRA) from OMG-HDCS merged files. It provides several methods for computing grazing angles, ranging from simple across-track/depth ratios to more complex methods involving Digital Terrain Models (DTMs) or surrounding beam/ping information. The calculated grazing angles are written to JHC `.r4` (float grid) files.

This tool is critical for backscatter processing and beam pattern analysis, as accurate grazing angles are fundamental for correcting angular response effects.

## Usage
```bash
get_GRA <input_omg_file(.merged)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<input_omg_file(.merged)>` | **Required.** One or more paths to input OMG-HDCS merged files. |
| `-v` | Enable verbose output. |
| `-refract` | Use refracted raypath to adjust grazing angle (requires a `.depression` file, output from `newMergeAtt`). |
| `-debug_grazing` | Enable debugging for grazing angle calculations. |
| `-out_ext <extension>` | Optional extension to append to the output filenames (e.g., `.GRA_ADH.<extension>.r4`). |

### Grazing Angle Calculation Methods (Choose one or more)
| Option | Description |
|---|---|
| `-grazing_just_across` | Calculates grazing angle using simple across-track/depth ratio. |
| `-grazing_pre_ADH` | Uses neighboring pings/beams to determine slope (a pre-ADH method). |
| `-use_dtm_for_grazing <file.r4>` | Uses a DTM file to lookup grazing angles, averaging with 4 adjacent nodes. |
| `-use_dtm_for_grazing_ADH <file.r4>` | Uses a DTM file to lookup grazing angles with ADH's Least Squares fit logic applied to 4 adjacent nodes. |
| `-use_ADH_GRZ <num_pings> <num_beams>` | Uses Anand D. Hiroji's (ADH) grazing angle calculations, considering `num_pings` along-track and `num_beams` across-track surrounding beams. |
| `-compute_dep_azi_from_cone_intersections` | Computes beam depression and azimuth angles using cone-to-cone intersection. |
| `-use_DTM_depth_instedof_beam_depth` | Uses DTM depth instead of beam depth for angle calculations. |

### Other Options
| Option | Description |
|---|---|
| `-separate_port_stbd_grazing` | (Present in `USAGE` but not implemented in code) Intended to differentiate grazing angles for port and starboard. |

## How It Works
1.  **Initialization:** Parses command-line arguments to set various flags for GRA calculation methods and output extensions.
2.  **File Setup:**
    *   Opens input merged file (`.merged`).
    *   Loads sonar parameters from the `.param` file.
    *   Opens `.depression` file if `-refract` is specified.
    *   Opens DTM files (`-use_dtm_for_grazing`, `-use_dtm_for_grazing_ADH`) and loads their data into memory if specified.
3.  **Output File Creation:** Based on the chosen GRA calculation methods, it creates corresponding `.r4` output files (e.g., `.GRA_ADH.r4`, `.GRA_dtm.r4`). A JHC header is written to each `.r4` file.
4.  **Profile Iteration:** Loops through each profile (ping) in the merged file:
    *   Reads the current profile header and raw beams.
    *   **Grazing Angle Calculation:** For each beam, it calls the appropriate external function (e.g., `get_grazing_angles`, `get_full_grazing_angles`, `get_dtm_grazing_angles`, `get_dtm_grazing_angles_ADH`, `get_full_grazing_angles_ADH`) based on the selected command-line option. These functions (likely from `grazing_angle.h` and `grazing_angle.c`) perform the core trigonometric or geometric calculations.
    *   **Output Writing:** Writes the calculated grazing angles for all beams in the current profile to the corresponding `.r4` output files.
5.  **Cleanup:** Closes all open files and frees allocated memory (for DTM data).
