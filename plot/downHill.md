---
layout: default
title: downHill
parent: Plot Tools
nav_order: 126
---
# downHill

## Description
`downHill` is a utility designed to model and generate synthetic beam footprint files (`.bf_file`) for various multibeam sonar systems (e.g., EM300, SeaBeam Classic, RESON 8101, ELAC Mk II, FSWP20, ISIS, TOWSS). It simulates how sonar beams intersect a sloping seafloor, producing across-track and along-track distances for each beam at increasing depths.

This tool is useful for understanding sonar coverage, designing survey parameters, and generating ground truth data for beam footprint analysis, especially in areas with varying bathymetry. It can model different beam spacing types (equiangular or equidistant) and account for across-track slope.

## Usage
```bash
downHill (-em3000 | -fswp20 | -isis | -towss | -elacII_120 | -elacII_150 | -reson_8101 | -em300 | -sb_classic) -outfile <bf_file> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `(-em3000 | -fswp20 | -isis | -towss | -elacII_120 | -elacII_150 | -reson_8101 | -em300 | -sb_classic)` | **Required.** Specifies the sonar model for which to generate the beam footprint. |
| `-outfile <bf_file>` | **Required.** Path for the output beam footprint file. |
| `-infile <param_file>` | (Optional) Path to an input parameter file. |
| `-reprate <val>` | Repetition rate (ping interval) in seconds. |
| `-fixed_sector <val>` | Forces a fixed angular sector width. |
| `-distance_to_go <val>` | Total along-track distance to simulate. | `1000.0` |
| `-desired_swath <val>` | Desired across-track swath width. | `2000.0` |
| `-across_slope <val>` | Specifies the across-track slope in degrees. | `0.0` |
| `-depthrange <start_depth> <stop_depth>` | Specifies the starting and stopping depths for the simulation. | `250.0` to `3000.0` |
| `-ssp <val>` | Surface sound speed. | `1500.0` |
| `-sect_vary` | (Not fully implemented) Intended to vary the angular sector. |
| `-canyon` | (Not fully implemented) Intended to simulate a canyon-like bathymetry. |

## How It Works
1.  **Initialization:** Parses command-line arguments to set the sonar `model`, output filename, and various simulation parameters (e.g., `Start_Depth`, `Stop_Depth`, `across_slope`, `Desired_Swath`).
2.  **Sonar Model Configuration:** Based on the chosen sonar `model`, it populates a `BeamFoot` structure (`bf`) with sonar-specific characteristics:
    *   `toolType`, `operatingMode`, `shot_interval`, `spacing_type`, `nobeams`, `nopings`, `interleave`, `ping_offset`.
    *   `beamangle`, `beamheight`, `beamwidth`, `offset_dirn` for each beam.
3.  **Simulation Loop:** It simulates the sonar moving along-track, increasing `along_dist` in steps determined by `ping_interval`. In each step:
    *   **Depth Calculation:** Determines the current `Depth` based on `Start_Depth`, `Stop_Depth`, `along_dist`, and `across_slope` (if `canyon` or `sect_vary` are used, more complex depth profiles are simulated).
    *   **Beam Footprint Calculation:** For each beam `i` defined by the sonar model:
        *   It determines `full_angle` (the beam's angular position).
        *   Calls `depth_intersect()` to calculate the `actual_depth` at which the beam intersects the seafloor, considering the current `Depth` (nadir depth) and `across_slope`.
        *   Calculates `across_dist` from the `actual_depth` and `full_angle`.
        *   Writes `along_dist` and `across_dist` to the output file.
    *   **Ping Interval Update:** Calculates the `ping_interval` based on the deepest point of the simulated swath to ensure adequate along-track coverage.
4.  **Helper Function `depth_intersect()`:** This function calculates the depth at which a beam, at a given `angle`, intersects a seafloor with a specified `nadirdepth` and `across_slope`. It uses basic trigonometry to account for the slope.
5.  **Output:** The output file (`bf_file`) contains pairs of `along_dist` and `across_dist` values for each beam at each simulated ping interval, representing the synthetic beam footprint.
```