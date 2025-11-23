# `M3imb2omg.c` - Mesotech M3 IMB/PAQ to OMG Format Converter

This C program is a highly specialized and comprehensive tool designed for the conversion of proprietary Mesotech M3 multibeam sonar data into the standardized Ocean Mapping Group (OMG) data format. It handles data from both IMB (Intensity Measurement Block) files, representing beamformed data, and PMB/PAQ (Profile/Phase Acquisition) data. The program manages the entire conversion pipeline, from parsing M3's native data structures and applying various geophysical corrections to ultimately writing a complete suite of OMG-compatible output files. These output files include merged bathymetry, watercolumn data (both amplitude and phase), navigation, attitude, and sonar parameters, making the Mesotech data fully accessible for broader OMG processing and analysis workflows.

## Key Features and Functions

*   **Command-line Argument Parsing (`main` function):**
    *   Offers an extensive set of command-line options for granular control over the conversion process, ensuring flexibility in data selection and output customization. These include flags for verbosity (`-v`), debugging (`-debug`), and index management (`-force_rebuild_index`).
    *   **Data Selection & Filtering:**
        *   `-ping_start <value>`, `-ping_end <value>`: Specifies a range of ping numbers to process.
        *   `-time_start <Y JD H M S>`, `-time_end <Y JD H M S>`: Defines a time window (Year, Julian Day, Hour, Minute, Second) for filtering data, ensuring only relevant pings are processed.
    *   **Data Handling Options:**
        *   `-dumpTA`: Dumps Transducer Array (TA) data, likely for diagnostics or specialized analysis.
        *   `-dB_range <min_dB> <max_dB>`: Sets the decibel range for packing acoustic intensity values.
        *   `-pack_samp <value>`: Specifies a sample packing factor for watercolumn data, influencing data resolution and file size.
    *   **IMB Stabilization & Motion Compensation:**
        *   `-heading_compensate <value>`, `-pitch_compensate <value>`, `-roll_compensate <value>`: Parameters for applying motion compensation to IMB data, adjusting for sensor orientation.
        *   `-switch_sign_scale <value>`: Allows scaling and sign-switching of motion data, useful for adapting to different sensor conventions.
        *   `-use_external_motion`: Instructs the program to use external motion data instead of internal sensor readings.
    *   **Image/PIE Diagram Generation:**
        *   `-pie`: Activates the generation of PIE (Post-Interp Echosounder) diagrams, which provide visual representations of the watercolumn.
        *   `-interp`, `-look_up`, `-pixel <value>`, `-mindepth <value>`, `-maxdepth <value>`, `-left_across <value>`, `-right_across <value>`: Define parameters specific to PIE generation and general image manipulation (e.g., pixel size, depth/across-track ranges).
    *   **OMG Output & Watercolumn Control:**
        *   `-write_to_OMG`: Enables writing data to the main OMG merged format (`.merged` file).
        *   `-do_snippet`: Activates snippet extraction, writing detailed high-resolution data around bottom detections.
        *   `-write_out_WC`: Controls the writing of watercolumn data to dedicated `.watercol` files.
        *   `-reTrack`: Attempts to re-track missing or unreliable bottom detections by inferring solutions from neighboring beams.
        *   `-trim_WC`, `-trim_WC_by_depth`, `-trim_WC_by_range`: Provides advanced options to trim watercolumn data based on depth or range criteria, removing unwanted acoustic returns (e.g., water surface, water column noise).
        *   `-min_allowed_depth <value>`, `-max_allowed_depth <value>`: Specifies depth limits for watercolumn trimming.
        *   `-head_tilt <value>`, `-head_depth <value>`: Sensor mounting parameters crucial for accurate trimming calculations.
        *   `-unsteered_beamwidth <value>`, `-range_fraction <value>`: Additional parameters for range-based watercolumn trimming.
    *   `-showPhase`: Enables displaying phase data in watercolumn outputs, complementing amplitude information.
    *   `-force_PMB_version <value>`: Forces parsing using a specific PMB version.
    *   **Input/Output Files:**
        *   `-M3imb <filename(s)>`: Specifies one or more input Mesotech M3 proprietary data files.
        *   `-omg <prefix>`: Defines the prefix for all generated OMG output files (e.g., `mydata.merged`, `mydata.nav`, etc.).
*   **File Handling and Indexing:**
    *   Manages the opening and closing of input M3 files and a comprehensive suite of OMG output files.
    *   Utilizes an optional `.index` file to optimize processing. This index stores ping times and byte offsets within the M3 file, allowing for rapid seeking and time-based filtering. The program can use an existing index or rebuild it if `force_rebuild_index` is specified.
*   **M3 Data Parsing:**
    *   Leverages a set of specialized functions (e.g., `parse_M3_Packet_Header`, `parse_M3_PMB_Data_Header`, `parse_M3_Data_Header`, `parse_M3_Packet_Footer`) from the `M3_read.h` library to meticulously extract data from proprietary Mesotech M3 packet structures.
    *   It dynamically identifies different internal M3 data types (e.g., PMB profile solutions `0x1008`, PAQ image data `0x2001`, and IMB image data `0x1002`/`0x2003`) to apply appropriate parsing logic for each data block.
*   **Core Conversion Functions:**
    *   `M3_convert_IMB_to_OMG_WC()`: This function is central to transforming IMB data into an `j_EM_watercolumn` structure. It applies motion compensation based on sensor readings or external data, calculates precise beam pointing angles, and handles sample packing of raw acoustic data (amplitudes) into 8-bit `ts_ampl` arrays within the watercolumn structure.
    *   `M3_convert_PAQ_to_OMG_WC()`: Converts PMB/PAQ data, which can include both amplitude and phase, into `j_EM_watercolumn` structures. It incorporates sensor mounting parameters (`head_tilt`, `head_depth`) and various watercolumn trimming options (`trim_WC_by_range`, `trim_WC_by_depth`) to refine the watercolumn data, including packing of 8-bit amplitude and phase samples.
*   **OMG Output Generation:**
    *   If `write_to_OMG` is enabled, the program meticulously writes data to the main `.merged` file. This includes creating an `OMG_HDCS_summary_header` (customized for M3 data), followed by an `OMG_HDCS_profile_header` for each ping (containing time offsets, sample rates, sound speed, etc.), and `OMG_HDCS_beam` data for each beam (detailing reflectivity, TWTT, range, steering angle, and observed depth). Bottom detection solutions from PMB data are accurately mapped to these `OMG_HDCS_beam` structures.
    *   Dedicated `.nav` and `.orientation` files are generated for navigation and attitude data, respectively. Tx sector information is written to a `.sectors` file. Watercolumn data (amplitude and phase) are written using `j_EM_write_watercolumn` to `.watercol` and `.wc_pha_8bit` files.
*   **`write_out_M3_nav()`:** Formats and writes navigation data (ping time, latitude, longitude) to the `.nav` file in a `jcu_nav_rec` format, with an option to prevent writing redundant navigation records.
*   **`write_out_M3_attitude()`:** Formats and writes attitude data (ping time, roll, pitch, heading, heave) to the `.orientation` file, starting with an `OMG_HDCS_summary_attitude` header.
*   **`fill_in_dumb_depth_across()`:** A helper function that calculates preliminary `observedDepth` and `acrossTrack` values for `OMG_HDCS_beam` structures using simplified geometry based on TWTT, sound speed, and sensor mounting. This is used when precise bottom detections are unavailable.
*   **`attempt_ReTracking()`:** Implements a sophisticated re-tracking algorithm to infer or "fill in" missing or unreliable bottom detections. It extrapolates or interpolates from valid adjacent beams, improving data completeness in areas with sparse or poor detections.
*   **PIE Diagram Generation (`-pie`):** If enabled, the program generates visual PIE (Post-Interp Echosounder) diagrams as image files (`.pie` extension) and accompanying `.txt` metadata files. This involves combining processed watercolumn data into an 8-bit image and writing a `JHC_header` to the image file, along with relevant motion data. The `JasPer` library is integrated for JPEG2000 compression.
*   **Robust Error Handling:** The program employs `error()` for critical failures, `warning()` for non-critical issues, and `usage()` to display correct command-line syntax, enhancing usability and reliability.

## Dependencies

`M3imb2omg.c` is highly dependent on a custom set of libraries and header files, which provide data structures, utility functions, and I/O mechanisms crucial for its operation:

*   `support.h`: General utilities for command-line parsing, error handling, and string manipulation.
*   `OMG_HDCS_jversion.h`: Defines structures and functions for the OMG HDCS format.
*   `j_EM_watercol.h`: Structures and functions for EM-series watercolumn data handling.
*   `stdtime.h`: Time conversion and formatting utilities.
*   `jb_endian.h`: Endian conversion utilities for data portability.
*   `jcu_nav.h`: Navigation data structures and I/O.
*   `M3_read.h`: Critical for M3-specific data structures and parsing functions.
*   `JHC_header`: Used for image header information in PIE generation.
*   `jasper/jasper.h`: For JPEG2000 compression.

## Purpose

`M3imb2omg.c` is an advanced and indispensable component within hydrographic data processing workflows involving Mesotech M3 multibeam sonar data. It plays a pivotal role in:

1.  **Ingesting Proprietary Data:** Enabling the seamless conversion of complex proprietary Mesotech M3 formats into a more accessible and standardized OMG format.
2.  **Comprehensive Data Extraction & Conversion:** Accurately extracting and converting raw acoustic data, alongside critical navigation and attitude information.
3.  **Advanced Correction & Processing:** Applying sophisticated motion compensation, filtering, and watercolumn trimming algorithms based on various geophysical criteria, thereby enhancing data quality and relevance.
4.  **Integrated OMG Output:** Producing a cohesive suite of inter-compatible OMG files, which significantly streamlines subsequent processing, visualization, and analysis by other tools in the broader OMG ecosystem.
5.  **Quality Control & Visualization:** Generating PIE diagrams for quick and effective visual inspection of watercolumn data, which is invaluable for quality assurance and data interpretation.

This program offers essential functionality for managing and processing Mesotech M3 data, making it a powerful utility for scientific research, hydrographic survey applications, and general underwater acoustic data analysis.