---
layout: default
title: QCdemo
parent: QC Tools
nav_order: 158
---
# QCdemo

## Description
`QCdemo` is an interactive X-windows application designed for quality control (QC) and demonstration of multibeam sonar data processing. It allows users to simulate and visualize the effects of various system parameters and environmental factors on sonar measurements. Users can adjust parameters like attitude scale, time delay, lever arm offsets, sound speed errors, and seabed slope, and instantly see their impact on synthetic depth and attitude error plots.

The tool processes synthetic time-series attitude data, calculates derived attitude and heave errors, and then simulates sonar pings over a seabed model to visualize beam footprints and error propagation.

## Usage
```bash
QCdemo -ts <ascii_attitude_list> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `-ts <ascii_attitude_list>` | **Required.** Path to an ASCII file containing synthetic attitude time-series data (time, roll, pitch, heading, heave). |
| `-v` | Enable verbose output. |
| `-write_out` | Writes synthetic merged data to `synthetic.merged`. |
| `-background` | Runs in background (non-graphical) mode and pings away until a certain along-track distance is covered. |

### Sonar & Stabilization
| Option | Description |
|---|---|
| `-EA` | Equiangular beam mode. |
| `-EDBS` | Equidistant beam mode. |
| `-roll_stab` | Enables roll stabilization. |
| `-pitch_stab` | Enables pitch stabilization. |
| `-beam_hop` | Enables beam hopping. |

### Error & Correction Parameters
| Option | Description | Default / Example |
|---|---|
| `-attitude_scale <val>` | Scales the applied attitude. | `1.0` |
| `-time_delay <val>` | Time delay (in seconds) applied to attitude data. | `0.0` |
| `-yaw_misalign <val>` | Yaw misalignment (in degrees). | `0.0` |
| `-sss_error <val>` | Surface sound speed error (m/s). | `0.0` |
| `-ss_gradient <val>` | Surface sound speed gradient ((m/s)/m). | `0.0` |
| `-sslayer_error <val>` | Layer sound speed error (m/s). | `0.0` |
| `-heave_bw <val>` | Heave bandwidth. | `20.0` |
| `-lever_arm_x <val>` / `-lever_arm_y <val>` / `-lever_arm_z <val>` | Lever arm offsets (meters). | `0.0` |
| `-noise_level <val>` | Noise level for depth measurements (0-10, 0=none, 10=really noisy). | `0.0` |

### Seabed Model
| Option | Description |
|---|---|
| `-oscillate_slope <const> <amp> <period>` | Oscillating seabed slope (degrees), with constant, amplitude, and period (seconds). |
| `-oscillate_dirtn <const> <amp> <period>` | Oscillating seabed slope direction (degrees), with constant, amplitude, and period (seconds). |

## Interactive X-Windows Interface

The application provides several interactive widgets (slider bars and plots) to adjust parameters and visualize results:

*   **Slider Bars (Graphical Controls):**
    *   `Attitude Scaling` (`attitude_scale`)
    *   `Time Delay` (`time_delay`)
    *   `Yaw Misalignment` (`yaw_misalign`)
    *   `Surface Sound Speed Error` (`sss_error`)
    *   `Surface Sound Speed Gradient` (`ss_gradient`)
    *   `Layer Sound Speed Error` (`sslayer_error`)
    *   `Heave Lever Arm X` (`lever_arm_x`)
    *   `Heave Lever Arm Y` (`lever_arm_y`)
    *   `Heave Lever Arm Z` (`lever_arm_z`)
    *   `Seafloor Slope` (`slope`)
    *   `Downhill Direction` (`slope_dirn`)
*   **Plotting Windows:**
    *   **Attitude Series and Errors:** Displays true and apparent roll, pitch, heading, and heave, along with their errors.
    *   **Xtrack -- Ltrack:** Shows a cross-track view of the seabed and errors, including the "depth uncertainty cone".
    *   **Scrolling Displays:** Provides scrolling displays of the seabed with depth coloring and slope visualization.
*   **Buttons:**
    *   `EXIT`: Closes the application.
    *   `Att.`: Toggles visibility of the attitude widget.
    *   `Xtrack`: Toggles visibility of the cross-track widget.
    *   `Raster`: Toggles visibility of the raster widget.
    *   `Go.`: Starts the simulation/pinging.
    *   `Stop.`: Stops the simulation.
    *   `EquiAngu.` / `EquiDist.` / `FFT_Dist.`: Toggles beam mode.
    *   `Roll Stab. ON/OFF`: Toggles roll stabilization.
    *   `Beam Hop ON/OFF`: Toggles beam hopping.

## How It Works
1.  **Initialization:**
    *   Parses command-line arguments to set initial values for various error and simulation parameters.
    *   Reads synthetic attitude time-series data from the `-ts` file into global arrays (`Ttime`, `roll`, `pitch`, `heading`, `heave`, and `orig_*` versions).
    *   Sets up the X-windows display, colormap, and min/max ranges for slider bars and plots.
    *   Creates various interactive widgets (slider bars, buttons, plotting sub-windows).
2.  **Simulation Loop (`ping_away()`):**
    *   If running in non-background mode (`!background`), it enters an event processing loop (`process_x_events()`) to handle user interactions.
    *   If running in background mode (`background`), it continuously simulates pings.
    *   In each ping interval:
        *   Calculates `nadir_depth` based on seabed slope and oscillation.
        *   Calculates `true_roll`, `true_pitch`, `true_heading`, `true_heave` by interpolating from the input time series.
        *   Calculates `appr_roll`, `appr_pitch`, `appr_heading`, `appr_heave` by adding calculated errors (from attitude scale, time delay, yaw misalignment, lever arms) to the true attitude.
        *   **Beam Vector Transformation:** For each beam:
            *   Calculates the beam's pointing angle (`get_pointing_angle()`).
            *   Transforms the beam vector from transducer coordinates to geographical coordinates, accounting for true attitude and lever arms.
            *   Calculates `true_depth` based on the seabed slope model (`get_real_intercept()`).
            *   Applies simulated sound speed errors (`sss_error`, `ss_gradient`, `sslayer_error`) and noise (`noise_level`).
            *   Stores the calculated `across`, `depth`, and `along` values.
        *   Updates the display (`re_draw_box()`) in interactive mode.
3.  **Error Calculation Functions:**
    *   `calc_attitude_errors()`: Calculates `roll_error`, `pitch_error` based on `attitude_scale`, `time_delay`, and `yaw_misalign`.
    *   `calc_heave_errors()`: Calculates `heave_error` based on `time_delay`, `attitude_scale`, and `lever_arm` errors.
    *   `calc_refract_errors()`: (Placeholder)
4.  **Plotting & Display Functions (using `X_extra.h`):**
    *   `re_draw_box()`: Redraws a specific plot window (slider or attitude/depth plot) based on current parameters.
    *   `make_attitude_widget()`, `make_xtr_widget()`, `make_sun_widget()`: Functions to create and configure the various sub-windows.
    *   `prime_slope()`: Initializes `tan_slope`, `cos_slope_dirn`, `rad_slope_dirn`, `tan_forward_slope` based on `slope` and `slope_dirn`.
    *   `re_bound_boxes()`: Recalculates plotting bounds for certain sub-windows based on `nadir_depth` and `percent_range`.

## Output Files
*   The primary output is an interactive X-windows graphical interface.
*   `synthetic.merged`: A synthetic merged file containing simulated multibeam data (if `-write_out` is specified).
*   `history.grid`: (Optional) For dumping grid data.

## Dependencies
*   X-Window System libraries for GUI.
*   Internal libraries for coordinate systems, navigation, and plot drawing.

## Notes
`QCdemo` is an invaluable tool for understanding the impact of various system parameters and environmental factors on multibeam sonar data quality. It allows users to gain intuition about error sources and the effectiveness of different correction strategies. The interactive nature of the tool makes it suitable for both educational purposes and for fine-tuning processing parameters before applying them to real data. The tool relies on a synthetic attitude time-series file for its simulation.