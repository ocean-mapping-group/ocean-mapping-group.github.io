---
layout: default
title: svpSonar
parent: Ray Tools
nav_order: 171
---
# svpSonar

## Description
`svpSonar` is a utility designed to model the distortion of sonar beams resulting from errors in the assumed sound velocity at the transducer. It simulates various multibeam sonar geometries (line arrays, paired inclined arrays, curved faces) and calculates how an error in the surface sound velocity affects the true steering angle, apparent across-track position, and depth of a beam.

This tool is critical for understanding the sensitivity of multibeam systems to sound velocity profile inaccuracies and for quantifying potential depth and position errors. It generates output data that can be plotted to visualize these distortions.

## Usage
```bash
svpSonar (-elac | -em1000 | -line | -em3000d | -isis | -custom <LUT_file>) -out <output_file> [-actual <val>] [-speed_range <min> <max> <step>] [-angle_range <min> <max> <step>]
```

## Arguments

| Option | Description |
|---|---|
| `(-elac | -em1000 | -line | -em3000d | -isis)` | **Required.** Specifies the sonar array geometry type:
    *   `-line`: Horizontal line array.
    *   `-elac`: Paired 30 deg inclined line arrays.
    *   `-em3000d`: Paired 45 deg inclined line arrays.
    *   `-isis`: Paired 60 deg inclined line arrays.
    *   `-em1000`: EM1000-like array. |
| `-custom <LUT_file>` | Uses a custom lookup table file (`.Time_LUT`, `.ACROSS_LUT`) for ray tracing (currently commented out). |
| `-out <output_file>` | **Required.** Path for the output ASCII file containing the distortion data. |
| `-actual <val>` | Actual sound speed (m/s) at the transducer. | `1500.0` (assumed) |
| `-assumed <val>` | Assumed sound speed (m/s) for beam steering. | `1500.0` (default) |
| `-speed_range <min_error> <max_error> <step_error>` | Defines a range of sound speed errors (m/s) to simulate.
    *   `min_error`: Minimum sound speed error.
    *   `max_error`: Maximum sound speed error.
    *   `step_error`: Step size for the sound speed error. | `-5.0 5.0 0.5` |
| `-angle_range <min_angle> <max_angle> <step_angle>` | Defines the range of beam angles (degrees) to simulate.
    *   `min_angle`: Minimum beam angle.
    *   `max_angle`: Maximum beam angle.
    *   `step_angle`: Step size for the beam angle. | `-75.0 75.0 1.0` |
| `-roll <val>` | Simulates a constant vessel roll (radians, converted internally). | `0.0` |
| `-v` | Enable verbose output. |

## How It Works

1.  **Initialization:** Parses command-line arguments, setting the sonar `type`, sound speed parameters (`actual_speed`, `assumed_speed`, `min_speed_error`, `max_speed_error`, `error_step`), and angle range (`min_angle`, `max_angle`, `angle_step`).
2.  **Output File Setup:** Creates the specified output ASCII file (`-out`). Writes header information to the file including the number of speed error steps, default Y ranges, and number of angle steps.
3.  **Speed Error Loop:** Iterates through `speed_error` values from `min_speed_error` to `max_speed_error` with `error_step`:
    *   Calculates `actual_speed` by adding `speed_error` to `assumed_speed`.
    *   Writes `actual_speed` and `assumed_speed` to the output file.
    *   **Angle Loop:** Iterates through `angle` values (in radians) from `min_angle` to `max_angle` with `angle_step`:
        *   **Steering Calculation:** Calls `steering()` to calculate `steered_angle` (the angle the sonar system thinks the beam is steered to), taking into account the `type` of sonar and a simulated `roll`.
        *   **True Steering Angle:** Calculates `true_steered_angle` using Snell's Law, accounting for the `actual_speed` and `assumed_speed`.
        *   **Angle Error:** Calculates `angle_error` as the difference between `true_steered_angle` and `steered_angle`.
        *   **Actual Angle:** Calculates `actual_angle` by adding `angle_error` to the original `angle`.
        *   **Position Calculation:**
            *   Assumes a `true_slant_range` of 1.0.
            *   Calculates `apparent_across` and `apparent_depth` based on `actual_angle`.
            *   Calculates `true_across` (based on `angle`).
            *   Calculates `across_error` as `true_across - apparent_across`.
        *   **Output Data:** Writes all calculated values (angles, across-track, depth, and errors) to the output file.
4.  **`steering(int type, double roll, double angle)` Function:**
    *   Calculates the effective steered angle based on the sonar array geometry (`type`) and applied `roll`.
    *   Different sonar types have different relationships between the physical beam angle, roll, and the final steered angle (e.g., simple sum for line array, or offsetting by fixed angles for inclined paired arrays).
5.  **Cleanup:** Closes the output file.

## Output File Format (ASCII)
The output file (`-out`) contains multiple lines of data. For each `speed_error` step, it first prints `actual_speed` and `assumed_speed`, followed by a series of lines (one for each `angle` step) containing:
`angle actual_angle steered_angle angle_error apparent_across apparent_depth true_across across_error`
(All angles are in degrees, converted from radians for output).
```
```
---
layout: default
title: svpSonar
parent: Ray Tools
nav_order: 171
---
# svpSonar

## Description
`svpSonar` is a utility designed to model the distortion of sonar beams resulting from errors in the assumed sound velocity at the transducer. It simulates various multibeam sonar geometries (line arrays, paired inclined arrays, curved faces) and calculates how an error in the surface sound velocity affects the true steering angle, apparent across-track position, and depth of a beam.

This tool is critical for understanding the sensitivity of multibeam systems to sound velocity profile inaccuracies and for quantifying potential depth and position errors. It generates output data that can be plotted to visualize these distortions.

## Usage
```bash
svpSonar (-elac | -em1000 | -line | -em3000d | -isis | -custom <LUT_file>) -out <output_file> [-actual <val>] [-speed_range <min> <max> <step>] [-angle_range <min> <max> <step>]
```

## Arguments

| Option | Description |
|---|---|
| `(-elac | -em1000 | -line | -em3000d | -isis)` | **Required.** Specifies the sonar array geometry type:
    *   `-line`: Horizontal line array.
    *   `-elac`: Paired 30 deg inclined line arrays.
    *   `-em3000d`: Paired 45 deg inclined line arrays.
    *   `-isis`: Paired 60 deg inclined line arrays.
    *   `-em1000`: EM1000-like array. |
| `-custom <LUT_file>` | Uses a custom lookup table file (`.Time_LUT`, `.ACROSS_LUT`) for ray tracing (currently commented out). |
| `-out <output_file>` | **Required.** Path for the output ASCII file containing the distortion data. |
| `-actual <val>` | Actual sound speed (m/s) at the transducer. | `1500.0` (assumed) |
| `-assumed <val>` | Assumed sound speed (m/s) for beam steering. | `1500.0` (default) |
| `-speed_range <min_error> <max_error> <step_error>` | Defines a range of sound speed errors (m/s) to simulate.
    *   `min_error`: Minimum sound speed error.
    *   `max_error`: Maximum sound speed error.
    *   `step_error`: Step size for the sound speed error. | `-5.0 5.0 0.5` |
| `-angle_range <min_angle> <max_angle> <step_angle>` | Defines the range of beam angles (degrees) to simulate.
    *   `min_angle`: Minimum beam angle.
    *   `max_angle`: Maximum beam angle.
    *   `step_angle`: Step size for the beam angle. | `-75.0 75.0 1.0` |
| `-roll <val>` | Simulates a constant vessel roll (radians, converted internally). | `0.0` |
| `-v` | Enable verbose output. |

## How It Works

1.  **Initialization:** Parses command-line arguments, setting the sonar `type`, sound speed parameters (`actual_speed`, `assumed_speed`, `min_speed_error`, `max_speed_error`, `error_step`), and angle range (`min_angle`, `max_angle`, `angle_step`).
2.  **Output File Setup:** Creates the specified output ASCII file (`-out`). Writes header information to the file including the number of speed error steps, default Y ranges, and number of angle steps.
3.  **Speed Error Loop:** Iterates through `speed_error` values from `min_speed_error` to `max_speed_error` with `error_step`:
    *   Calculates `actual_speed` by adding `speed_error` to `assumed_speed`.
    *   Writes `actual_speed` and `assumed_speed` to the output file.
    *   **Angle Loop:** Iterates through `angle` values (in radians) from `min_angle` to `max_angle` with `angle_step`:
        *   **Steering Calculation:** Calls `steering()` to calculate `steered_angle` (the angle the sonar system thinks the beam is steered to), taking into account the `type` of sonar and a simulated `roll`.
        *   **True Steering Angle:** Calculates `true_steered_angle` using Snell's Law, accounting for the `actual_speed` and `assumed_speed`.
        *   **Angle Error:** Calculates `angle_error` as the difference between `true_steered_angle` and `steered_angle`.
        *   **Actual Angle:** Calculates `actual_angle` by adding `angle_error` to the original `angle`.
        *   **Position Calculation:**
            *   Assumes a `true_slant_range` of 1.0.
            *   Calculates `apparent_across` and `apparent_depth` based on `actual_angle`.
            *   Calculates `true_across` (based on `angle`).
            *   Calculates `across_error` as `true_across - apparent_across`.
        *   **Output Data:** Writes all calculated values (angles, across-track, depth, and errors) to the output file.
4.  **`steering(int type, double roll, double angle)` Function:**
    *   Calculates the effective steered angle based on the sonar array geometry (`type`) and applied `roll`.
    *   Different sonar types have different relationships between the physical beam angle, roll, and the final steered angle (e.g., simple sum for line array, or offsetting by fixed angles for inclined paired arrays).
5.  **Cleanup:** Closes the output file.

## Output File Format (ASCII)
The output file (`-out`) contains multiple lines of data. For each `speed_error` step, it first prints `actual_speed` and `assumed_speed`, followed by a series of lines (one for each `angle` step) containing:
`angle actual_angle steered_angle angle_error apparent_across apparent_depth true_across across_error`
(All angles are in degrees, converted from radians for output).
```
---
layout: default
title: svpSonar
parent: Ray Tools
nav_order: 171
---
# svpSonar

## Description
`svpSonar` is a utility designed to model the distortion of sonar beams resulting from errors in the assumed sound velocity at the transducer. It simulates various multibeam sonar geometries (line arrays, paired inclined arrays, curved faces) and calculates how an error in the surface sound velocity affects the true steering angle, apparent across-track position, and depth of a beam.

This tool is critical for understanding the sensitivity of multibeam systems to sound velocity profile inaccuracies and for quantifying potential depth and position errors. It generates output data that can be plotted to visualize these distortions.

## Usage
```bash
svpSonar (-elac | -em1000 | -line | -em3000d | -isis | -custom <LUT_file>) -out <output_file> [-actual <val>] [-speed_range <min> <max> <step>] [-angle_range <min> <max> <step>]
```

## Arguments

| Option | Description |
|---|---|
| `(-elac | -em1000 | -line | -em3000d | -isis)` | **Required.** Specifies the sonar array geometry type:
    *   `-line`: Horizontal line array.
    *   `-elac`: Paired 30 deg inclined line arrays.
    *   `-em3000d`: Paired 45 deg inclined line arrays.
    *   `-isis`: Paired 60 deg inclined line arrays.
    *   `-em1000`: EM1000-like array. |
| `-custom <LUT_file>` | Uses a custom lookup table file (`.Time_LUT`, `.ACROSS_LUT`) for ray tracing (currently commented out). |
| `-out <output_file>` | **Required.** Path for the output ASCII file containing the distortion data. |
| `-actual <val>` | Actual sound speed (m/s) at the transducer. | `1500.0` (assumed) |
| `-assumed <val>` | Assumed sound speed (m/s) for beam steering. | `1500.0` (default) |
| `-speed_range <min_error> <max_error> <step_error>` | Defines a range of sound speed errors (m/s) to simulate.
    *   `min_error`: Minimum sound speed error.
    *   `max_error`: Maximum sound speed error.
    *   `step_error`: Step size for the sound speed error. | `-5.0 5.0 0.5` |
| `-angle_range <min_angle> <max_angle> <step_angle>` | Defines the range of beam angles (degrees) to simulate.
    *   `min_angle`: Minimum beam angle.
    *   `max_angle`: Maximum beam angle.
    *   `step_angle`: Step size for the beam angle. | `-75.0 75.0 1.0` |
| `-roll <val>` | Simulates a constant vessel roll (radians, converted internally). | `0.0` |
| `-v` | Enable verbose output. |

## How It Works

1.  **Initialization:** Parses command-line arguments, setting the sonar `type`, sound speed parameters (`actual_speed`, `assumed_speed`, `min_speed_error`, `max_speed_error`, `error_step`), and angle range (`min_angle`, `max_angle`, `angle_step`).
2.  **Output File Setup:** Creates the specified output ASCII file (`-out`). Writes header information to the file including the number of speed error steps, default Y ranges, and number of angle steps.
3.  **Speed Error Loop:** Iterates through `speed_error` values from `min_speed_error` to `max_speed_error` with `error_step`:
    *   Calculates `actual_speed` by adding `speed_error` to `assumed_speed`.
    *   Writes `actual_speed` and `assumed_speed` to the output file.
    *   **Angle Loop:** Iterates through `angle` values (in radians) from `min_angle` to `max_angle` with `angle_step`:
        *   **Steering Calculation:** Calls `steering()` to calculate `steered_angle` (the angle the sonar system thinks the beam is steered to), taking into account the `type` of sonar and a simulated `roll`.
        *   **True Steering Angle:** Calculates `true_steered_angle` using Snell's Law, accounting for the `actual_speed` and `assumed_speed`.
        *   **Angle Error:** Calculates `angle_error` as the difference between `true_steered_angle` and `steered_angle`.
        *   **Actual Angle:** Calculates `actual_angle` by adding `angle_error` to the original `angle`.
        *   **Position Calculation:**
            *   Assumes a `true_slant_range` of 1.0.
            *   Calculates `apparent_across` and `apparent_depth` based on `actual_angle`.
            *   Calculates `true_across` (based on `angle`).
            *   Calculates `across_error` as `true_across - apparent_across`.
        *   **Output Data:** Writes all calculated values (angles, across-track, depth, and errors) to the output file.
4.  **`steering(int type, double roll, double angle)` Function:**
    *   Calculates the effective steered angle based on the sonar array geometry (`type`) and applied `roll`.
    *   Different sonar types have different relationships between the physical beam angle, roll, and the final steered angle (e.g., simple sum for line array, or offsetting by fixed angles for inclined paired arrays).
5.  **Cleanup:** Closes the output file.

## Output File Format (ASCII)
The output file (`-out`) contains multiple lines of data. For each `speed_error` step, it first prints `actual_speed` and `assumed_speed`, followed by a series of lines (one for each `angle` step) containing:
`angle actual_angle steered_angle angle_error apparent_across apparent_depth true_across across_error`
(All angles are in degrees, converted from radians for output).
```
---
layout: default
title: svpSonar
parent: Ray Tools
nav_order: 171
---
# svpSonar

## Description
`svpSonar` is a utility designed to model the distortion of sonar beams resulting from errors in the assumed sound velocity at the transducer. It simulates various multibeam sonar geometries (line arrays, paired inclined arrays, curved faces) and calculates how an error in the surface sound velocity affects the true steering angle, apparent across-track position, and depth of a beam.

This tool is critical for understanding the sensitivity of multibeam systems to sound velocity profile inaccuracies and for quantifying potential depth and position errors. It generates output data that can be plotted to visualize these distortions.

## Usage
```bash
svpSonar (-elac | -em1000 | -line | -em3000d | -isis | -custom <LUT_file>) -out <output_file> [-actual <val>] [-speed_range <min> <max> <step>] [-angle_range <min> <max> <step>]
```

## Arguments

| Option | Description |
|---|---|
| `(-elac | -em1000 | -line | -em3000d | -isis)` | **Required.** Specifies the sonar array geometry type:
    *   `-line`: Horizontal line array.
    *   `-elac`: Paired 30 deg inclined line arrays.
    *   `-em3000d`: Paired 45 deg inclined line arrays.
    *   `-isis`: Paired 60 deg inclined line arrays.
    *   `-em1000`: EM1000-like array. |
| `-custom <LUT_file>` | Uses a custom lookup table file (`.Time_LUT`, `.ACROSS_LUT`) for ray tracing (currently commented out). |
| `-out <output_file>` | **Required.** Path for the output ASCII file containing the distortion data. |
| `-actual <val>` | Actual sound speed (m/s) at the transducer. | `1500.0` (assumed) |
| `-assumed <val>` | Assumed sound speed (m/s) for beam steering. | `1500.0` (default) |
| `-speed_range <min_error> <max_error> <step_error>` | Defines a range of sound speed errors (m/s) to simulate.
    *   `min_error`: Minimum sound speed error.
    *   `max_error`: Maximum sound speed error.
    *   `step_error`: Step size for the sound speed error. | `-5.0 5.0 0.5` |
| `-angle_range <min_angle> <max_angle> <step_angle>` | Defines the range of beam angles (degrees) to simulate.
    *   `min_angle`: Minimum beam angle.
    *   `max_angle`: Maximum beam angle.
    *   `step_angle`: Step size for the beam angle. | `-75.0 75.0 1.0` |
| `-roll <val>` | Simulates a constant vessel roll (radians, converted internally). | `0.0` |
| `-v` | Enable verbose output. |

## How It Works

1.  **Initialization:** Parses command-line arguments, setting the sonar `type`, sound speed parameters (`actual_speed`, `assumed_speed`, `min_speed_error`, `max_speed_error`, `error_step`), and angle range (`min_angle`, `max_angle`, `angle_step`).
2.  **Output File Setup:** Creates the specified output ASCII file (`-out`). Writes header information to the file including the number of speed error steps, default Y ranges, and number of angle steps.
3.  **Speed Error Loop:** Iterates through `speed_error` values from `min_speed_error` to `max_speed_error` with `error_step`:
    *   Calculates `actual_speed` by adding `speed_error` to `assumed_speed`.
    *   Writes `actual_speed` and `assumed_speed` to the output file.
    *   **Angle Loop:** Iterates through `angle` values (in radians) from `min_angle` to `max_angle` with `angle_step`:
        *   **Steering Calculation:** Calls `steering()` to calculate `steered_angle` (the angle the sonar system thinks the beam is steered to), taking into account the `type` of sonar and a simulated `roll`.
        *   **True Steering Angle:** Calculates `true_steered_angle` using Snell's Law, accounting for the `actual_speed` and `assumed_speed`.
        *   **Angle Error:** Calculates `angle_error` as the difference between `true_steered_angle` and `steered_angle`.
        *   **Actual Angle:** Calculates `actual_angle` by adding `angle_error` to the original `angle`.
        *   **Position Calculation:**
            *   Assumes a `true_slant_range` of 1.0.
            *   Calculates `apparent_across` and `apparent_depth` based on `actual_angle`.
            *   Calculates `true_across` (based on `angle`).
            *   Calculates `across_error` as `true_across - apparent_across`.
        *   **Output Data:** Writes all calculated values (angles, across-track, depth, and errors) to the output file.
4.  **`steering(int type, double roll, double angle)` Function:**
    *   Calculates the effective steered angle based on the sonar array geometry (`type`) and applied `roll`.
    *   Different sonar types have different relationships between the physical beam angle, roll, and the final steered angle (e.g., simple sum for line array, or offsetting by fixed angles for inclined paired arrays).
5.  **Cleanup:** Closes the output file.

## Output File Format (ASCII)
The output file (`-out`) contains multiple lines of data. For each `speed_error` step, it first prints `actual_speed` and `assumed_speed`, followed by a series of lines (one for each `angle` step) containing:
`angle actual_angle steered_angle angle_error apparent_across apparent_depth true_across across_error`
(All angles are in degrees, converted from radians for output).
```
```