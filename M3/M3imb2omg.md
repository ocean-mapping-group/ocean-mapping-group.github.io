---
layout: default
title: M3imb2omg
parent: M3 Tools
nav_order: 2
---
# M3imb2omg

## Description
`M3imb2omg` is a highly specialized and comprehensive C program designed for the conversion of proprietary Mesotech M3 multibeam sonar data into the standardized Ocean Mapping Group (OMG) data format. It handles data from both IMB (Intensity Measurement Block) files, representing beamformed data, and PMB/PAQ (Profile/Phase Acquisition) data. The program manages the entire conversion pipeline, from parsing M3's native data structures and applying various geophysical corrections to ultimately writing a complete suite of OMG-compatible output files. These output files include merged bathymetry, watercolumn data (both amplitude and phase), navigation, attitude, and sonar parameters, making the Mesotech data fully accessible for broader OMG processing and analysis workflows.

## Usage
```bash
M3imb2omg [OPTIONS] -M3imb <filename(s)> -omg <prefix>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enables verbose output. | |
| `-debug` | Activates debug messages. | |
| `-force_rebuild_index` | Forces a rebuild of the internal M3 index file. | |
| `-ping_start <value>` | Specifies a starting ping number for processing. | |
| `-ping_end <value>` | Specifies an ending ping number for processing. | |
| `-time_start <Y JD H M S>` | Defines a start time window (Year, Julian Day, Hour, Minute, Second) for filtering data. | |
| `-time_end <Y JD H M S>` | Defines an end time window (Year, Julian Day, Hour, Minute, Second) for filtering data. | |
| `-dumpTA` | Dumps Transducer Array (TA) data. | |
| `-dB_range <min_dB> <max_dB>` | Sets the decibel range for packing acoustic intensity values. | |
| `-pack_samp <value>` | Specifies a sample packing factor for watercolumn data. | |
| `-heading_compensate <value>` | Parameter for applying heading motion compensation to IMB data. | |
| `-pitch_compensate <value>` | Parameter for applying pitch motion compensation to IMB data. | |
| `-roll_compensate <value>` | Parameter for applying roll motion compensation to IMB data. | |
| `-switch_sign_scale <value>` | Allows scaling and sign-switching of motion data. | |
| `-use_external_motion` | Instructs the program to use external motion data instead of internal sensor readings. | |
| `-pie` | Activates the generation of PIE (Post-Interp Echosounder) diagrams. | |
| `-interp` | Interpolate image data. | |
| `-look_up` | Look up PIE data. | |
| `-pixel <value>` | Sets the pixel size for PIE diagrams. | |
| `-mindepth <value>` | Minimum depth for PIE diagram generation. | |
| `-maxdepth <value>` | Maximum depth for PIE diagram generation. | |
| `-left_across <value>` | Left across-track range for PIE diagram. | |
| `-right_across <value>` | Right across-track range for PIE diagram. | |
| `-write_to_OMG` | Enables writing data to the main OMG merged format (`.merged` file). | |
| `-do_snippet` | Activates snippet extraction. | |
| `-write_out_WC` | Controls the writing of watercolumn data to dedicated `.watercol` files. | |
| `-reTrack` | Attempts to re-track missing or unreliable bottom detections. | |
| `-trim_WC` | Enables trimming of watercolumn data. | |
| `-trim_WC_by_depth` | Trims watercolumn data by depth criteria. | |
| `-trim_WC_by_range` | Trims watercolumn data by range criteria. | |
| `-min_allowed_depth <value>` | Minimum allowed depth for watercolumn trimming. | |
| `-max_allowed_depth <value>` | Maximum allowed depth for watercolumn trimming. | |
| `-head_tilt <value>` | Sensor mounting parameter (head tilt). | |
| `-head_depth <value>` | Sensor mounting parameter (head depth). | |
| `-unsteered_beamwidth <value>` | Unsteered beamwidth parameter for range-based watercolumn trimming. | |
| `-range_fraction <value>` | Range fraction parameter for range-based watercolumn trimming. | |
| `-showPhase` | Enables displaying phase data in watercolumn outputs. | |
| `-force_PMB_version <value>` | Forces parsing using a specific PMB version. | |
| `-M3imb <filename(s)>` | **Required.** Specifies one or more input Mesotech M3 proprietary data files. | `data.imb` |
| `-omg <prefix>` | **Required.** Defines the prefix for all generated OMG output files. | `output_survey` |

## Output Files
*   `<prefix>.merged`: Main OMG-HDCS merged file.
*   `<prefix>.nav`: Navigation data.
*   `<prefix>.orientation`: Attitude data.
*   `<prefix>.watercol`: Watercolumn amplitude data.
*   `<prefix>.wc_pha_8bit`: Watercolumn phase data.
*   `<prefix>.sectors`: TX sector information.
*   `<prefix>.pie`: PIE diagram image file (if `-pie` is used).
*   `<prefix>.pie.txt`: PIE diagram metadata file (if `-pie` is used).

## How It Works
1.  **Command-line Argument Parsing:** Offers an extensive set of command-line options for granular control over the conversion process, ensuring flexibility in data selection and output customization.
2.  **File Handling and Indexing:** Manages the opening and closing of input M3 files and a comprehensive suite of OMG output files. Utilizes an optional `.index` file to optimize processing.
3.  **M3 Data Parsing:** Leverages a set of specialized functions (e.g., `parse_M3_Packet_Header`, `parse_M3_PMB_Data_Header`, `parse_M3_Data_Header`, `parse_M3_Packet_Footer`) from the `M3_read.h` library to meticulously extract data from proprietary Mesotech M3 packet structures.
4.  **Core Conversion Functions:**
    *   `M3_convert_IMB_to_OMG_WC()`: Transforms IMB data into an `j_EM_watercolumn` structure. It applies motion compensation, calculates precise beam pointing angles, and handles sample packing of raw acoustic data (amplitudes) into 8-bit `ts_ampl` arrays.
    *   `M3_convert_PAQ_to_OMG_WC()`: Converts PMB/PAQ data into `j_EM_watercolumn` structures, incorporating sensor mounting parameters and various watercolumn trimming options.
5.  **OMG Output Generation:** If `write_to_OMG` is enabled, the program writes data to the main `.merged` file, including `OMG_HDCS_summary_header`, `OMG_HDCS_profile_header`, and `OMG_HDCS_beam` records. Dedicated `.nav` and `.orientation` files are generated for navigation and attitude data.
6.  **`write_out_M3_nav()`:** Formats and writes navigation data (ping time, latitude, longitude) to the `.nav` file.
7.  **`write_out_M3_attitude()`:** Formats and writes attitude data (ping time, roll, pitch, heading, heave) to the `.orientation` file.
8.  **`fill_in_dumb_depth_across()`:** A helper function that calculates preliminary `observedDepth` and `acrossTrack` values for `OMG_HDCS_beam` structures.
9.  **`attempt_ReTracking()`:** Implements a sophisticated re-tracking algorithm to infer or "fill in" missing or unreliable bottom detections.
10. **PIE Diagram Generation (`-pie`):** If enabled, the program generates visual PIE (Post-Interp Echosounder) diagrams as image files (`.pie` extension) and accompanying `.txt` metadata files.
11. **Robust Error Handling:** Employs `error()` for critical failures, `warning()` for non-critical issues, and `usage()` to display correct command-line syntax.

## Dependencies
*   `support.h`: General utilities for command-line parsing, error handling, and string manipulation.
*   `OMG_HDCS_jversion.h`: Defines structures and functions for the OMG HDCS format.
*   `j_EM_watercol.h`: Structures and functions for EM-series watercolumn data handling.
*   `stdtime.h`: Time conversion and formatting utilities.
*   `jb_endian.h`: Endian conversion utilities for data portability.
*   `jcu_nav.h`: Navigation data structures and I/O.
*   `M3_read.h`: Critical for M3-specific data structures and parsing functions.
*   `JHC_header`: Used for image header information in PIE generation.
*   `jasper/jasper.h`: For JPEG2000 compression.

## Notes
`M3imb2omg.c` is an advanced and indispensable component within hydrographic data processing workflows involving Mesotech M3 multibeam sonar data. It plays a pivotal role in ingesting proprietary data, comprehensive data extraction & conversion, advanced correction & processing, integrated OMG output, and quality control & visualization. This program offers essential functionality for managing and processing Mesotech M3 data, making it a powerful utility for scientific research, hydrographic survey applications, and general underwater acoustic data analysis.