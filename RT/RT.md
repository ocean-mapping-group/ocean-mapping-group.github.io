---
layout: default
title: RT
parent: RT Tools
nav_order: 185
---
# RT

## Description
`RT` (Real-Time) is a comprehensive X-windows application designed for real-time unravelling, processing, and visualization of Simrad multibeam sonar telegrams (like EM100, EM1000, EM3000, EM710, etc.) and other sonar formats (RESON, ELAC). It processes raw sonar data, extracts bathymetry, sidescan imagery, attitude, navigation, and sound velocity data, and then displays them graphically in various interactive windows.

The tool can output processed data to OMG-HDCS (Ocean Mapping Group - Hydrographic Data Conversion System) merged files, along with auxiliary attitude, heading, and sidescan data files. It provides interactive controls for panning, zooming, color mapping, and adjusting display parameters. `RT` is a critical tool for real-time quality control, survey monitoring, and initial data processing of multibeam sonar data.

## Usage
```bash
RT [OPTIONS] [<input_file(s)>]
```

## Arguments

| Option | Description |
|---|---|
| `<input_file(s)>` | (Optional) One or more input raw sonar telegram files. If not provided, it will prompt interactively or use auto-discovery. |

### Sonar Type Selection (Choose one)
| Option | Description |
|---|---|
| `-em100` / `-em120` / `-em300` / `-em1000` / `-em1002` / `-em3000` / `-em3000d` / `-em3002` / `-em3002d` / `-em710` / `-em122` / `-em302` / `-em2040` / `-em12s` / `-em121a` | Specifies the Simrad EM sonar model. |
| `-reson` / `-8101` | Specifies Reson SeaBat 8000 series sonar. |
| `-elac` / `-elac2` | Specifies ELAC BottomChart sonar. |
| `-submex` | Specifies Submetrix processing. (Not fully implemented). |

### File Input/Output
| Option | Description |
|---|---|
| `-background` | Runs in background mode (non-graphical) and logs data without display. |
| `-foreground` | Runs in foreground mode (graphical display). (Default if `-background` not used). |
| `-WRITE` | Enables writing output files (default). |
| `-out <prefix>` | Prefix for output OMG-HDCS files (e.g., `<prefix>.merged`, `<prefix>.orientation`). |
| `-prefix <path>` / `-suffix <suffix>` | Define a prefix/suffix for auto-discovered input filenames. |
| `-line <name>` | Specifies a single input line name (for non-auto mode). |
| `-ascii_dump` | Dumps processed data to ASCII files instead of binary. |
| `-tide <tidefile>` | Binary tide file for tide corrections. |
| `-svtd <svtdfile>` | SVP (Sound Velocity Profile) file for ray tracing (currently unused). |

### Data Processing & Conversion
| Option | Description |
|---|---|
| `-force_swap` / `-LE` / `-BE` | Force byte swapping (Little Endian / Big Endian). Auto-guessed by default. |
| `-recalc_AAZ` | Recalculates AAZ (Attitude-Aided Zenith) for some systems. |
| `-head_roll <val>` / `-head_pitch <val>` / `-head_gyro <val>` | Static offsets for head roll, pitch, gyro. |
| `-tide` / `-base_offset <val>` | Enable tide correction with an optional base offset. |
| `-ignore_clock` | Ignores clock information (for some older formats). |
| `-noLength` | Ignores packet length (for some corrupted files). |
| `-hack_reson_time` | Applies a time hack for Reson data. |
| `-custom_mask <file>` | Custom beam mask file. |
| `-unpack_watercol` | Unpacks watercolumn data. |
| `-compress_watercol <factor>` | Compresses watercolumn data by a factor. |
| `-guess_noWCsample` | Guesses number of watercolumn samples. |
| `-rescale_BSN` | Rescales BSn values (for newer Kongsberg systems). |
| `-fix_wc_time` | Fixes water column time stamping issues. |
| `-scramblenav` | Scrambles navigation (for testing). |
| `-refcoord <lat> <lon>` | Reference coordinate for scrambling navigation. |

### Map & Display Options
| Option | Description |
|---|---|
| `-region <file>` | Defines a geographical region. |
| `-area <file>` | Defines a map sheet area (for background imagery). |
| `-utm <meridian>` | Uses UTM projection with a central meridian. |
| `-flipNE` | Flips Northing/Easting coordinates. |
| `-scale <factor>` | Scales X-windows display. |
| `-pixel_size <val>` | Sets the pixel size for sidescan imagery. |
| `-ssshift <val>` | Shifts sidescan imagery. |
| `-paintss` / `-paintbathy` | Paint sidescan/bathy into the background map. |
| `-SUN` / `-sun_exag <val>` / `-cont_int <val>` | Enables sun illumination with exaggeration and contour interval. |
| `-atdist <val>` | Along-track distance for some displays. |

### Nav Flagging
| Option | Description |
|---|---|
| `-posnav` | Enables POS/MV navigation flagging. |
| `-maxNUMSATS <val>` / `-maxCORRAGE <val>` / `-maxHDOP <val>` | Max satellites/correction age/HDOP for nav flagging. |

### Versioning
| Option | Description |
|---|---|
| `-version1` / `-version2` / `-version3` / `-version4` / `-v1` / `-v2` / `-v3` / `-v4` | Overrides default OMG-HDCS file version. |

### Debugging & Verbosity
| Option | Description |
|---|---|
| `-v` | Enable verbose output. |
| `-quiet` | Suppress verbose output. |
| `-turn_on_verbose <ping_num>` | Turns on verbose output at a specific ping number. |
| `-check` | Enable integrity checks. |
| `-date_check` | Enable date checks. |
| `-debug_nav` | Enable navigation debugging. |
| `-show_skipped` | Shows skipped records. |
| `-carry_on_anyway` | Continues processing even if errors are encountered. |

## Interactive X-Windows Interface

When running in foreground (`-foreground` or default), `RT` provides an interactive X-windows graphical user interface with several panels and buttons:

*   **Main Map Window:** Displays bathymetry and sidescan imagery (if `area_flag` is used). Supports panning, zooming, and location lookup.
*   **Color Map Window:** Displays the color scale for imagery.
*   **EOF Widget:** Indicates End-Of-File.
*   **Text Info Widget:** Displays various text information.
*   **Depth Encoded Window:** Shows depth-encoded representation of the swath.
*   **Sun Encoded Window:** Shows sun-illuminated representation of the swath.
*   **Reflectivity Encoded Window:** Shows reflectivity.
*   **EM1000 Full Sidescan Window:** Displays full sidescan imagery.
*   **Azimuth Speed, Current Vector Window:** Shows navigation vectors.
*   **Ship Speed Through Water Widget:** Displays ship speed.
*   **Tidal Widget:** Displays current tide value.
*   **Backscatter Widget:** Displays backscatter angular response.
*   **Buttons Widget:** Contains interactive buttons for various controls (e.g., `Start Log`, `Stop Log`, `Reset`, `Color Palette`, `Image Type`, `Next File`, `Catchup`, `Beam Masks`, `Line Run`).
*   **Attitude, Beam Mask, Line Running Widgets:** Separate pop-up windows for detailed views and controls related to attitude data, beam masking, and runline parameters.

## How It Works

1.  **Initialization:**
    *   Parses command-line arguments to configure various processing, output, and display options.
    *   Initializes global variables, flags, and data structures (`Simrad_em12`, `OMG_HDCS_jversion`, `RESON_UNB`, `UNB_ELAC`, `RT_unravel`, `RT_ancil_data`, `j_ang_resp`).
    *   Attempts to auto-guess byte order and sonar model from the input file.
    *   Sets up default tool-type specific variables (e.g., `MaxDep`, `Min_DB`, `Max_DB`, `att_flag` configuration).
2.  **File Setup:**
    *   If outputting (`WRITE_flag`), opens necessary output OMG-HDCS files (`.merged`, `.nav`, `.orientation`, `.heading`, `.mech_pitch`, `.surf_ss`, `.watercol`, `.reflect`, `.merged.ss_data`, `.merged.ph_data`, `.sectors`, NMEA files).
    *   If `area_flag` is set, loads background imagery (`.ssmos`, `.dtm`) and their headers.
3.  **X-Windows Setup (if `view_flag`):**
    *   Initializes the X-windows display, creates main and auxiliary windows/widgets, and sets up colormaps.
    *   Initializes `XImage` structures for main map and sidescan display.
4.  **Data Processing Loop (`log_data()` / `log_RESON_data()` / `log_ELAC_data()` / `log_SUBMETRIX_data()`):**
    *   Reads raw sonar telegrams from the input file.
    *   Parses the telegrams based on the detected `RAW_type` (sonar model). This involves reading binary structures, extracting relevant fields (timestamps, navigation, attitude, depths, intensities, snippets, watercolumn data), and converting them into generic internal data structures.
    *   Performs various processing steps:
        *   **Time Synchronization:** Matches navigation and attitude data to depth pings.
        *   **Tide Correction:** Applies tide from a loaded tide file (`calc_tide()`).
        *   **Motion Correction:** Applies roll, pitch, heave, and yaw corrections (some are basic/assumed, others rely on detailed motion sensor data).
        *   **Beam Masking:** Applies user-defined or default beam masks.
        *   **Backscatter Processing:** Calculates backscatter values from raw intensities, applying TVG, spreading, absorption corrections.
        *   **Quality Flagging:** Sets quality flags based on various criteria.
        *   **Geolocation:** Converts sonar beam coordinates to geographic coordinates.
    *   **Data Output:** Writes processed data to OMG-HDCS merged files and auxiliary files.
    *   **Display Update (if `view_flag`):** Updates the X-windows display with new pings, painted bathymetry/sidescan, updated navigation, and attitude plots. Includes functions like `paint_bathy()`, `paint_ampl()`, `paint_ss()`, `update_plot()`.
5.  **Interactive Event Loop (`process_x_events()`):**
    *   If `view_flag` is set, it enters a loop to handle user input (mouse clicks, key presses) for panning, zooming, changing display modes, and interacting with widgets.
    *   Calls various helper functions (`shift_view()`, `zoom_view()`, `check_for_edge()`, `change_mask()`) to respond to user actions.
6.  **Cleanup:** Closes all open files and frees allocated memory.

## Output Files
*   `<outprefix>.merged`: OMG-HDCS merged file.
*   `<outprefix>.nav` / `<outprefix>.nav_N`: Binary navigation file(s).
*   `<outprefix>.orientation` / `<outprefix>.orientation_N`: Binary attitude file(s) for roll, pitch, heave.
*   `<outprefix>.heading`: Binary heading file.
*   `<outprefix>.mech_pitch`: Binary mechanical pitch file.
*   `<outprefix>.surf_ss`: Binary surface sound speed file.
*   `<outprefix>.watercol`: Binary water column data.
*   `<outprefix>.reflect`: Reflectivity data.
*   `<outprefix>.merged.ss_data`: Snippet side-scan data.
*   `<outprefix>.merged.ph_data`: Snippet phase data.
*   `<outprefix>.sectors`: TX sector information.
*   `<outprefix>.nmea`: NMEA data.
*   `Velocity_Log_<date_time>.record`: Velocity log (if `want_velrec`).

## Notes
*   This tool is highly complex due to the wide range of sonar types and processing options it supports.
*   It leverages various external libraries and helper functions for specific tasks like NMEA parsing, projection, and X-windows graphics.
```
```