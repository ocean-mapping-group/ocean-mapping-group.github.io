---
layout: default
title: SYN_scripting
parent: GL Tools
nav_order: 24
---

# SYN_scripting

## Description
`SYN_scripting.c` is a module within the `SYN` project (likely `synSwath`), located in the `gl/` directory. Its core purpose is to provide **scripting capabilities** for the simulation and visualization environment. This module allows users to define and execute sequences of commands, enabling the automation of complex demonstrations, parameter sweeps, and the generation of animated outputs. It fundamentally extends the interactivity and reproducibility of the `glSeis` application. It is not a standalone command-line tool.

The module focuses on:
*   **Script Interpretation**: Reading and parsing commands from external script files.
*   **Automated Control**: Executing these commands to dynamically control simulation parameters, camera views, object properties, and triggering various actions (e.g., calculations, data dumps).
*   **Animation Generation**: Facilitating the creation of animated sequences by systematically varying parameters and capturing frames.

## Functionality

### `void read_in_animation_script(char *name)`
*   **Purpose:** Loads a text file containing a sequence of predefined commands for the simulation.
*   **Action:** Reads each line from the specified script file (`name`). It ignores comments (lines starting with '#') and blank lines. Valid command lines are stored into a global `commandlines` array, and the `no_script_commands` counter is updated. It has a maximum limit of `MAX_SCRIPT_LINES`.

### `void parse_next_script_command(int mode)`
*   **Purpose:** Parses and executes a single command from the currently active script line.
*   **Action:**
    *   Extracts a `keyword` from the command line.
    *   Uses a large `if-else if` block to match the `keyword` against a wide array of predefined simulation commands.
    *   Commands are categorized and dispatched to helper functions or trigger direct actions:
        *   **Single Value Commands**: Modify global float, double, or int variables (e.g., `speed_knots`, `eye_elev`, `plate_scale`, `frequency`, `nominal_depth`, `noise_level`, `pulse_location`, `interp_nodes`, and various `IW` and `SAS` related parameters). Handled by `cmd_single_value()`.
        *   **Single Switch Commands**: Toggle boolean flags (represented by int variables, e.g., `view_beam_pattern`, `view_plate`, `coupling`, `roll_stab`, `use_AR`, `dump_TimeSeries`, `EK_CTD`, `IW_widget`, `SAS_widget`, `use_sub_layers`). Handled by `cmd_single_switch()`.
        *   **Single String Commands**: Set string variables (e.g., `dumpdir` for output directory, `platedumpname`, `tracefilename`). Handled by `cmd_single_string()`.
        *   **Specialized Directives**: These cover a wide range of specific actions within the simulation, such as:
            *   `make_mock_bf`: Generates a mock beamfootprint.
            *   `zero_accum_time`: Resets the accumulated time counter.
            *   `recalc_bp`, `setup_bp`: Recalculates and configures beam patterns.
            *   `illuminate`: Triggers the calculation of incident beam patterns on the DTM.
            *   `draw_all`: Forces a complete redraw of the 3D scene.
            *   `dump_scene`: Captures the current 3D scene and saves it to an RGB image file.
            *   `print_time_series`, `print_angular_response`: Outputs simulation data to files.
            *   `reset_frame_no`: Resets the animation frame counter.
            *   `lookat_...`: Sets various camera look-at points (e.g., `lookat_plate`, `lookat_centre`, `lookat_antenna`, `lookat_middle`, `lookat_bottom`, `lookat_custom`).
            *   `surface_bs`, `surface_phase`, `surface_time`: Sets the display mode for the plate (DTM) visualization.
            *   `plate_edge`, `plate_centre`: Adjusts the positioning of the plate (DTM).
            *   `plot_all_bds`, `plot_wmta_bds`, `plot_peak_bds`, `plot_phas_bds`, `plot_hdbf_bds`: Sets the display mode for bottom detections.
            *   `exit`, `return`: Control the flow of the script and the application.
            *   **SAS/EK/IW Specific Actions**: Directives to trigger specific animation sequences (e.g., `sas_animate`, `ek_animate`, `ek_animateAlong`), or calculations/actions within the SAS, EK, and Internal Wave modules (e.g., `trace_beams`, `calc_ping_spacing`, `IW_dump_surface`, `update_velocline_sublayers`, `calc_SAS_subarray`, `calc_SAS_slr_elev`).
        *   The `mode` parameter (`SCRIPT_CHECK` or `SCRIPT_RUN`) determines if the command is just checked for syntax or actually executed.
        *   Increments `current_command` to advance to the next script line.

### Helper Functions for Command Parsing

*   **`void cmd_single_value(char *line, float *fval, double *dval, int *ival)`**: Parses a command line to extract a keyword and a single numerical value, which is then assigned to a float, double, or int pointer.
*   **`void cmd_single_switch(char *line, int *Switch)`**: Parses a command line to extract a keyword and a qualifier ("on" or "off"), setting the `Switch` integer pointer to 1 or 0 respectively.
*   **`void cmd_single_string(char *line, char *String)`**: Parses a command line to extract a keyword and a string value, copying it into the provided `String` buffer.

### Sequence/Animation Functions (Called by `cmd_sequence()`)

*   **`void cmd_sequence(char *line)`**: Parses a sequence command from the script, identifying the target parameter, start and end values, and number of frames. It then calls the appropriate specialized `sequence_` function.
*   **`void sequence_bp(double *value, int no_frames, double start, double end, int bp_slider)`**: Animates a beam pattern parameter (`value`) over a specified range. It linearly interpolates the parameter over `no_frames`, updating the BP widget slider, recalculating and setting up the beam pattern, optionally calculating incident beam pattern, and redrawing the main scene at each step.
*   **`void animate_bp(double *value, int operation, double factor, int bp_slider)`**: Provides continuous animation of a beam pattern parameter with various operations (multiply, add, oscillate). It runs in a loop until a stop condition is met, updating the parameter, widget, beam pattern, and scene in each iteration.
*   **`void sequence_eye(double *value, int no_frames, double start, double end, int bp_slider)`**: Animates camera (eye) parameters (`eye_azi`, `eye_elev`, `eye_range`) over a range, updating camera position and view in each frame.
*   **`void sequence_vessel(double *value, int no_frames, double start, double end, int bp_slider)`**: Animates vessel attitude parameters (`object_roll`, `object_pitch`, `object_heading`, `object_heave`), updating the vessel's pose and optionally recalculating incident beam patterns.
*   **`void sequence_plate(double *value, int no_frames, double start, double end, int bp_slider)`**: Animates plate (DTM) transformation parameters (`plate_heading`, `plate_roll`, `plate_pitch`, `plate_scale`), updating the DTM's position and orientation.
*   **`void sequence_EchoEnv_ITP_roll(...)`, `sequence_EchoEnv_I_roll(...)`, `sequence_EchoEnv_T_roll(...)`**: Specialized animation sequences designed to sweep through vessel roll angles, re-center the plate, and capture RGB images for Intensity, Time, and Phase views of the echo envelope, and dump binary time series data.
*   **`void ping_away(int noframes)`**: Initiates a continuous simulation loop, stepping through pings or frames. It updates vessel attitude, moves the plate, calculates incident beam patterns, and redraws the scene for each step until `noframes` is reached or `stop_check` is true.

This module fundamentally extends the interactivity and analytical capabilities of `glSeis` by enabling powerful and flexible scripting, allowing users to define, automate, and reproduce complex simulation and visualization scenarios, and to generate detailed animations for in-depth analysis and presentation.