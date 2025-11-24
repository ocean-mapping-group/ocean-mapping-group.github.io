---
layout: default
title: glSeis
parent: GLSEIS Tools
nav_order: 1
---
# glSeis

## Description
`glSeis` is an interactive OpenGL-based application designed for the visualization of seismic and EM watercolumn data. it can display watercolumn profiles, often in conjunction with a loaded Digital Terrain Model (DTM) or "plate" for context. Users can configure scan settings, ping rates, and window sizes, making it suitable for analyzing sonar behavior and seismic returns in a 3D environment.

## Usage
```bash
glSeis [OPTIONS]
```
As an interactive application, command-line options primarily configure the initial state or input data for the visualization.

## Arguments

### Data Loading
| Option | Description |
|---|---|
| `-emWC <filename>` | Load EM watercolumn data. This argument expects a merged file (e.g., `whatever.merged`), and it constructs the watercolumn filename by changing the suffix to `.watercol`. |
| `-plate <filename>` | Load a Digital Terrain Model (DTM) or "plate" file. This typically expects three associated files with suffixes `.r4` (bathymetry), `.BT` (color/texture), and `.sun` (intensity). |

### Scan & Sonar Settings
| Option | Description |
|---|---|
| `-first_ping_of_cycle <ping_number>` | Specify the starting ping number for a watercolumn data cycle. |
| `-no_pings_in_cycle <count>` | Define the number of pings in a complete cycle of watercolumn data. |
| `-ping_rate <rate>` | Set the ping rate of the sonar in Hz. |
| `-scan_settings <deg_per_sec_x10> <upper_deg_x10> <lower_deg_x10>` | Configure the scanning parameters. |

### Rendering & Display
| Option | Description | Default / Example |
|---|---|---|
| `-vert_exag <value>` | Set the vertical exaggeration factor for the terrain display. | |
| `-winsize <width> <height>` | Set the explicit width and height of the main application window. | |

### Behavioral Flags
| Option | Description |
|---|---|
| `-v` | Enable verbose output, printing detailed information to the console during operation. | |

## How It Works
`glSeis` initializes an OpenGL environment for 3D visualization. It loads watercolumn and/or DTM data based on command-line parameters. The application then renders these datasets, allowing users to interact with the 3D scene (e.g., rotate, zoom) to explore the data. Sonar scan settings (ping rate, scan cycle) are used to simulate and display the acoustic data dynamically within the 3D context.

## Output Files
The tool primarily produces interactive graphical output to an OpenGL window. No standard output files are generated for batch processing.

## Dependencies
*   OpenGL libraries for 3D rendering.
*   X-Window System libraries for GUI.
*   Internal libraries for file parsing (e.g., for EM watercolumn, DTMs).

## Notes
`glSeis` is an interactive visualization tool. Most of its functionality is accessed through its graphical user interface. Command-line arguments primarily serve to configure its initial state or load specific data for display.