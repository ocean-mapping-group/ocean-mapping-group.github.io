# synSwath

## Description
`synSwath` is an interactive OpenGL-based simulation and visualization tool for multibeam sonar systems. It allows users to simulate various aspects of multibeam operations, including beam pattern generation, bottom detection algorithms, sound propagation effects, and the interaction of sonar pulses with a simulated seafloor. It supports 3D visualization, real-time animation, and can load custom terrain models, beam patterns, and motion data. The tool is designed for demonstrating and understanding complex sonar physics and data acquisition principles.

## Usage
```bash
synSwath [OPTIONS]
```
Many options refer to files that configure the simulation (e.g., for beam patterns, terrain, or motion data) rather than direct input/output for batch processing.

## Key Command-Line Options

### Simulation & Data Loading
*   `-bp <filename>`: Load a beam pattern file.
*   `-lbl <filename>`: Load a Long Baseline (LBL) file.
*   `-currents <filename(s)>`: Load current profile data (multiple files can be specified).
*   `-dg <filename>`: Load a distorted grid file.
*   `-mru <filename>`: Load MRU (Motion Reference Unit) data for motion simulation.
*   `-TCtraj <filename(s)>`: Load a Transducer-Coupled trajectory file (multiple files can be specified).
*   `-Hphone <filename(s)>`: Load hydrophone data (multiple files can be specified), often used with `-TCtraj`.
*   `-RealData <filename(s)>`: Load real data files (multiple files can be specified).
*   `-navSect <filename(s)>`: Load navigation section data (multiple files can be specified).
*   `-adcpSect <filename(s)>`: Load ADCP section data (multiple files can be specified).
*   `-modelEpoch <filename(s)>`: Load model epoch data (multiple files can be specified).
*   `-plate <filename>`: Load a terrain plate file. This typically expects three associated files with suffixes `.r4` (bathymetry), `.BT` (color/texture), and `.sun` (intensity).
*   `-ts <filename>`: Load a time series file for animation.

### Rendering & Display
*   `-mini`: Use a reduced window size (e.g., 725x725 pixels) for the OpenGL display.
*   `-gldisp <display_name>`: Specify the OpenGL display server (e.g., `:0.0`).
*   `-lowres`: Enable low-resolution rendering for faster performance.
*   `-tr_and_rc`: Display both transmit and receive beam patterns.
*   `-rc`: Display only the receive beam pattern.
*   `-tr`: Display only the transmit beam pattern.
*   `-nolight`: Disable OpenGL lighting effects in the 3D view.
*   `-maxsize <value>` / `-plate_scale <value>`: Set the maximum dimension or scaling factor for the loaded terrain plate.
*   `-level <value>`: Apply a vertical shift to the terrain model.
*   `-vert_exag <value>`: Set the vertical exaggeration factor for the terrain display.
*   `-plate_yshift <value>`: Shift the terrain plate along the Y-axis.
*   `-plate_xshift <value>`: Shift the terrain plate along the X-axis.
*   `-plate_azi <value>`: Set the rotation (heading) of the terrain plate in degrees.
*   `-mindB <value>`: Set the minimum viewable power in dB for intensity displays.
*   `-winsize <width> <height>`: Set the explicit width and height of the main application window.
*   `-rpy <roll> <pitch> <yaw>`: Set the initial roll, pitch, and yaw (heading) for the simulated object/vehicle in degrees.
*   `-angle_skip <value>`: Set a skip factor for angular rendering steps, affecting visual detail and performance.
*   `-SUN`: Enable a specific "SUN" display mode (details may vary with internal implementation).

### Behavioral & Toggle Flags
*   `-v`: Enable verbose output, printing detailed information to the console during operation.
*   `-jevent`: Enable JEVENT debug mode, likely for internal event handling diagnostics.
*   `-sunny_plate`: Enable a specific rendering mode for the plate, possibly related to sun illumination simulation.
*   `-separate_beams`: Process or display individual beams separately, as opposed to a combined swath.
*   `-force_steer`: Force a specific pitch steer angle for beam pattern calculations.
*   `-adcp`: Activate ADCP (Acoustic Doppler Current Profiler) related simulation or display features.
*   `-mru`: Activate MRU (Motion Reference Unit) related simulation or display features.
*   `-no_plate_normals`: Disable the calculation and use of surface normals for the terrain plate.
*   `-no_plate_phase`: Disable the use of phase information from the terrain plate.
*   `-rough`: Render the terrain with a "rough" appearance, typically meaning a non-flat surface.
*   `-internal_wave`: Enable the simulation and visualization of internal waves.
*   `-slow`: Use a "slow" screen type, possibly for compatibility or debugging.
*   `-background`: Run the simulation in the background (requires a script for headless operation).
*   `-run`: Execute a loaded script for animation or predefined sequences.
*   `-record`: Enable recording of the simulation's visual output (e.g., to image files).
*   `-latent_Rx`: Enable simulation of a "latent receiver" for analyzing transmit/receive latency effects.
*   `-TxRx_latency <seconds>`: Set the transmit/receive latency in seconds when `-latent_Rx` is enabled.
*   `-force_bd_TS_range <min> <max>`: Force a specific minimum and maximum range for bottom detection time series.
*   `-TS_perc <percentage>`: Set the percentage of the Time Series (TS) to plot in a 2D beam pattern subplot.
*   `-force_mean_depth <depth>`: Override the automatically calculated mean depth for plate registration with a specified value.
*   `-nominal_depth <depth>`: Set the nominal depth, influencing scaling factors for various displayed objects and motions.