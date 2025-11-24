---
layout: default
title: compareTwoSVPs
parent: Ray Tools
nav_order: 165
---
# compareTwoSVPs

## Description
`compareTwoSVPs` is a utility designed to compare the ray tracing results of two different Sound Velocity Profiles (SVPs) or a single SVP under varying conditions (e.g., with bulk sound speed shifts or surface sound speed errors). It calculates the predicted ray paths and associated times/distances for a given "calc_depth" (bottom depth) and then outputs the across-track position and depth for each ray.

This tool is useful for visualizing the impact of SVP uncertainty, sound speed errors, or specific sonar steering mechanisms on the actual bottom detection locations. It can help assess the sensitivity of bathymetric measurements to sound speed variations.

## Usage
```bash
compareTwoSVPs -wc1 <ref_jWC_file> -wc2 <comp_jWC_file(s)> -out <output_file> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `-wc1 <ref_jWC_file>` | **Required.** Path to the reference SVP file in jWC format. |
| `-wc2 <comp_jWC_file(s)>` | **Required.** One or more paths to comparison SVP files in jWC format. |
| `-out <output_file>` | **Required.** Path for the output ASCII file containing across-track position and depth. |
| `-calc_depth <val>` | The bottom depth (meters) at which to compare ray paths. | `30.0` |
| `-draft <val>` | Transducer draft (meters). | `0.0` |
| `-max_angle <val>` | Maximum beam angle to trace (degrees). | `75.0` |
| `-angle_range <max_angle> <angle_step>` | Defines the range and step for tracing beam angles. | `75` (max angle), `1` (step) |
| `-bulk_SV_shift <val>` | Applies a bulk sound velocity shift (m/s) to the comparison SVP(s). | |
| `-frac_depth <val>` | Fraction of the profile depth (`calc_depth`) over which to apply the bulk SV shift. | `1.0` |
| `-equal_opposite` | Applies a surface sound speed error equal and opposite to the bulk shift. | |
| `-surf_SV_shift <val>` | Applies a surface sound speed shift (m/s) to the assumed sound speed for ingoing beam steering. | |
| `-SV_shift_range <start> <end> <step>` | Creates multiple comparison SVPs by ranging `surf_SV_shift` or `bulk_SV_shift`. | |
| `-just_surface` | Applies `SV_shift_range` only to `surf_SV_shift`. | |
| `-roll <val>` | Simulates a constant vessel roll (degrees). | `0.0` |
| `-line` / `-elac` / `-em3000d` / `-isis` / `-em1000` | Specifies the sonar type for steering angle calculations. | `LINE_ARRAY` |
| `-v` | Enable verbose output. | |

## How It Works
1.  **Initialization:** Parses command-line arguments to set input/output filenames, comparison parameters (`calc_depth`, `draft`, `max_angle`, `roll`), and various sound speed shift/sonar type options.
2.  **SVP Loading:**
    *   Loads the reference SVP (`-wc1`) into `wc1` using `jWC_read()` and `jWC_sort_async()`.
    *   Determines `surface_sound_speed` from the reference SVP at the `draft` depth.
    *   If `bulk_SV_shift` and `equal_opposite` are set, it applies the bulk shift to the reference SVP.
    *   Loads each comparison SVP (`-wc2`) into `wc[i]`. If `bulk_SV_shift` is set, it applies the shift to these comparison SVPs.
    *   Performs `jWC_interp_zv()` on all loaded SVPs to create finely layered velocity profiles.
3.  **Ray Tracing & Comparison:**
    *   **Loop through comparison SVPs/shifts:** The main loop iterates through all comparison SVPs (or generated shifts if `-SV_shift_range` is used).
    *   **Loop through angles:** For each comparison SVP/shift, it traces rays for `angle_to_use[i]` from `-max_angle` to `max_angle` with `angle_step`.
        *   **Steering Calculation:** If `surf_SV_shift` is active, it calls `steering()` to calculate `true_steered_angle` and `angle_error`, simulating the effect of surface sound speed error on beam steering.
        *   **Reference Ray Trace:** Performs a ray trace (`raypath()`) through the reference `wc1` using the `actual_angle_to_use` (which may include steering errors) and the `surface_sound_speed + surf_SV_shift`. This calculates the across-track position (`equiv_radial`) and one-way travel time (`time_to_use`) to `calc_depth`.
        *   **Comparison Ray Trace:** Performs another ray trace (`raytrace()`) through the current comparison `wc[j]` using the calculated `time_to_use[j][i]` and the original `angle_to_use[i]`. This determines the `newradial` (across-track) and `newdepth` at which the ray reaches the same `time_to_use`.
        *   The `equiv_radial` and `depth` from the reference ray trace (first part of the main loop) are written to the `outfile`.
        *   The `newradial` and `newdepth` from the comparison ray trace (second part of the main loop) are also written to the `outfile`.
4.  **Cleanup:** Frees allocated memory for `watercolumn` structures and closes the output file.

## Output Files
*   `<output_file>`: An ASCII file containing multiple columns of across-track positions and depths, representing the ray path predictions for the reference and comparison SVPs/shifts.

## Helper Functions
*   `steering(int type, double roll, double angle)`: Calculates the steered angle based on sonar `type`, `roll`, and `angle`. This function is primarily brought in from `svpSonar.c` and models different sonar geometries.
*   `jWC_init()`, `jWC_read()`, `jWC_sort_async()`, `jWC_interp_zv()`, `raypath()`, `raytrace()`, `jWC_free()`: External functions from `j_watercolumn.h` for managing sound velocity profiles and ray tracing.

## Dependencies
*   `support.h`: For general utility functions.
*   `j_watercolumn.h`: For `watercolumn` structures and ray tracing functions.
*   `svpSonar.h`: For sonar steering models.

## Notes
`compareTwoSVPs` is a powerful diagnostic tool for assessing the impact of sound velocity profile variations on multibeam bathymetry. It helps visualize how different SVPs or sound speed errors translate into positional and depth discrepancies on the seafloor. The various options for applying shifts and specifying sonar types make it flexible for simulating different scenarios. The tool creates new output files, preserving the original SVP data.