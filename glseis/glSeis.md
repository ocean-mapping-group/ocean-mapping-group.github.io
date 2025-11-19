# glSeis

## Description
`glSeis` is an interactive OpenGL-based application designed for the visualization of seismic and EM watercolumn data. it can display watercolumn profiles, often in conjunction with a loaded Digital Terrain Model (DTM) or "plate" for context. Users can configure scan settings, ping rates, and window sizes, making it suitable for analyzing sonar behavior and seismic returns in a 3D environment.

## Usage
```bash
glSeis [OPTIONS]
```
As an interactive application, command-line options primarily configure the initial state or input data for the visualization.

## Key Command-Line Options

### Data Loading
*   `-emWC <filename>`: Load EM watercolumn data. This argument expects a merged file (e.g., `whatever.merged`), and it constructs the watercolumn filename by changing the suffix to `.watercol`.
*   `-plate <filename>`: Load a Digital Terrain Model (DTM) or "plate" file. This typically expects three associated files with suffixes `.r4` (bathymetry), `.BT` (color/texture), and `.sun` (intensity).

### Scan & Sonar Settings
*   `-first_ping_of_cycle <ping_number>`: Specify the starting ping number for a watercolumn data cycle.
*   `-no_pings_in_cycle <count>`: Define the number of pings in a complete cycle of watercolumn data.
*   `-ping_rate <rate>`: Set the ping rate of the sonar in Hz.
*   `-scan_settings <deg_per_sec_x10> <upper_deg_x10> <lower_deg_x10>`: Configure the scanning parameters.
    *   `<deg_per_sec_x10>`: Scan rate in tenths of degrees per second.
    *   `<upper_deg_x10>`: Upper scan limit in tenths of degrees.
    *   `<lower_deg_x10>`: Lower scan limit in tenths of degrees.

### Rendering & Display
*   `-vert_exag <value>`: Set the vertical exaggeration factor for the terrain display.
*   `-winsize <width> <height>`: Set the explicit width and height of the main application window.

### Behavioral Flags
*   `-v`: Enable verbose output, printing detailed information to the console during operation.