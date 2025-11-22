---
layout: default
title: RT_unravel
parent: RT Tools
nav_order: 187
---
# RT_unravel

## Description
`RT_unravel` (Real-Time Unravelling) is a core component of the `RT` toolkit, responsible for interpreting and processing raw sonar telegrams from various multibeam systems (Simrad EM series, RESON, ELAC) and converting them into a standardized internal data format for display and output to OMG-HDCS files. It handles complex tasks like byte-swapping, time synchronization, quality control, and data aggregation from multiple telegram types.

This module is crucial for the `RT` tool's ability to ingest and make sense of proprietary sonar data formats, providing a unified interface for real-time visualization and subsequent post-processing within the OMG toolkit.

## Key Features

*   **Multi-Sonar Support:** Handles a wide range of Simrad EM series (EM100, EM1000, EM12S/D, EM300/3000/3002/3002D, EM710, EM122, EM302, EM2040), RESON (6042, 8101), and ELAC (UNB) data.
*   **Byte Order Handling:** Automatically guesses or allows forcing of byte order (Little Endian/Big Endian) for different sonar systems and platforms.
*   **Telegram Parsing:** Interprets proprietary binary telegram structures, extracting navigation, depth, imagery, attitude, sound velocity, and other ancillary data.
*   **Data Aggregation:** Combines related telegrams (e.g., depth and image) into a single profile for processing.
*   **Real-time Processing:** Performs on-the-fly calculations for time offsets, quality flags, and basic geolocation.
*   **OMG-HDCS Output:** Writes processed data to various OMG-HDCS formats (`.merged`, `.nav`, `.orientation`, `.heading`, `.watercol`, `.reflect`, etc.).

## Functions

### `log_data()`
The main loop for reading and processing Simrad EM series telegrams.
*   **Purpose:** Continuously reads the input file, identifies telegram types, extracts data, and calls specialized functions for each type.
*   **Details:** Handles file I/O, error checking, and manages the overall processing flow. Integrates with X-windows for real-time display updates.

### `swap_2bytes(short value)`
Byte-swaps a 2-byte short integer.
*   **Purpose:** Ensures correct interpretation of data regardless of system endianness.

### `print_date(char *header_string, em12_time *time)`
Prints a formatted date string for debugging.

### `get_1970_time(em12_time *time)`
Converts an `em12_time` structure to a Unix timestamp (double).
*   **Purpose:** Standardizes time for internal calculations. Handles Y2K issues and various date formats.

### `check_numeric(char array[], int n)`
Checks if characters in an array are numeric.

### `get_em300_runtime(char *data)`
Unpacks and processes Simrad EM3000/300/120/1002/3002/710/122/302/2040 Runtime Parameter telegrams.
*   **Purpose:** Extracts sonar configuration and operational parameters. Populates the `runTem300` global structure.

### `get_em3000_generic(char *data)`
Generic unpacker for Simrad EM3000 series telegrams.
*   **Purpose:** Reads common header fields for various telegram types.

### `get_em300_echo_trace(char *data)`
Unpacks and processes Simrad EM3000 Echo Trace telegrams (for watercolumn data).
*   **Purpose:** Extracts individual beam echo traces and populates `WHOLE_ping_WC` structure for watercolumn output.

### `get_em3000_watercolumn(char *data)`
Unpacks and processes Simrad EM3000 Water Column telegrams.
*   **Purpose:** Extracts watercolumn amplitude data for each beam, populating `WHOLE_ping_WC` and handling multi-telegram aggregation.

### `get_em3000_svp(char *data, int type)`
Unpacks and processes Simrad EM3000 Sound Velocity Profile (SSP) telegrams.
*   **Purpose:** Extracts SSP data and writes it to a JHC `.svp` file. Handles both old and new SSP formats.

### `get_em3000_height(char *data)`
Unpacks and processes Simrad EM3000 Height telegrams.
*   **Purpose:** Extracts height information (e.g., GPS antenna height above ellipsoid) and writes it to a JHC `.hgt` file.

### `get_em3000_nav(char *data)`
Unpacks and processes Simrad EM3000 Navigation telegrams.
*   **Purpose:** Extracts navigation data (latitude, longitude, speed, heading, quality) and writes it to a JHC `.nav` file. Supports POS/MV navigation flagging.

### `scramble_nav(em12_nav *nav)`
Scrambles navigation coordinates for testing purposes.

### `write_fix(em12_nav *nav)`
Writes a standard EM12/1000/121A navigation fix to a JHC `.nav` file.

### `prime_array()`
Initializes various arrays.

### `print_array()`
Prints debugging information about the image array.

### `get_em3000_imagery(int TYPE, char *data)`
Unpacks and processes Simrad EM3000 series Imagery telegrams.
*   **Purpose:** Extracts side-scan (amplitude and phase) data for each beam. Populates `image_beams` and `ss_imagery` structures.

### `get_em710_depths(char *data)`
Unpacks and processes Simrad EM710 series Depth telegrams.
*   **Purpose:** Extracts depth, across-track, and along-track data for each beam. Populates `dep7ks` and `new_depth_beams` structures.

### `print8bits(unsigned char anint)`
Debugging function to print binary representation of an 8-bit integer.

### `get_em710_qfactor(char *data)`
Unpacks and processes Simrad EM710 Q-Factor telegrams.

### `get_em710_raw_time_angle(char *data)`
Unpacks and processes Simrad EM710 Raw Time and Angle telegrams.
*   **Purpose:** Extracts raw range and angle data for each beam, used for watercolumn and merged output.

### `get_em710_imagery(char *data)`
Unpacks and processes Simrad EM710 series Imagery telegrams.
*   **Purpose:** Extracts high-resolution side-scan imagery (16-bit) and converts to 8-bit for internal processing.

### `unpack_ss_telegram(int TYPE, char *raw_data)`
Unpacks older Simrad EM1000/EM12/EM121A Sidescan telegrams.
*   **Purpose:** Extracts side-scan data (amplitude and phase) and manages multi-telegram assembly.

### `write_image()`
Writes processed image data to the output file.

### `get_em3000_surf_SS(char *data)`
Unpacks and processes Simrad EM3000 Surface Sound Speed telegrams.
*   **Purpose:** Extracts surface sound speed measurements.

### `get_em3000_mech_tilt(char *data)`
Unpacks and processes Simrad EM3000 Mechanical Tilt telegrams.
*   **Purpose:** Extracts mechanical pitch sensor data.

### `get_em3000_heading(char *data)`
Unpacks and processes Simrad EM3000 Heading telegrams.
*   **Purpose:** Extracts high-rate heading data.

### `get_em3000_attitude(char *data)`
Unpacks and processes Simrad EM3000 Attitude telegrams.
*   **Purpose:** Extracts high-rate roll, pitch, heave, and heading data from motion sensors. Supports dual motion sensors.

### `get_em3000_raw_time_angle_new(char *data)`
Unpacks and processes Simrad EM3000 Raw Time and Angle (new format) telegrams.
*   **Purpose:** Extracts raw range and angle data from newer EM systems.

### `get_em3000_raw_time_angle(char *data)`
Unpacks and processes Simrad EM3000 Raw Time and Angle (old format) telegrams.
*   **Purpose:** Extracts raw range and angle data from older EM systems.

### `get_em3000_depths(char *data)`
Unpacks and processes Simrad EM3000 series Depth telegrams.
*   **Purpose:** Extracts depth, across-track, and along-track data for each beam.

### `merge_em3000()`
Merges processed depth, image, and raw time/angle data from EM3000 series telegrams into a single `merge_profile`.
*   **Purpose:** Consolidates data from different telegrams into a coherent output record. Writes to the `.merged` and `.watercol` files.

### `read_121_raw_data(char *data)`
Unpacks Simrad EM121 Raw Data records.

### `write_depths(char *data)`
Writes older Simrad EM1000/EM12/EM121A depth data to output.

### `merge_both()`
Merges processed depth and image data from older Simrad EM1000/EM12/EM121A telegrams.

### `look_for_EM100_dmy()`
Searches for EM100 date/time information.

### `write_utm_fix(char *data)`
Writes EM100 UTM navigation data.

### `write_em100_reflect(char *data)`
Writes EM100 reflectivity (amplitude) data.

### `write_em100_depths(char *data)`
Writes EM100 depth data.

### `write_param(char *data, int length)`
Writes parameter telegrams to a `.param` file.

### `unpack_svp(char *data)`
Unpacks older Simrad EM Sound Velocity Profile telegrams.

### `log_ELAC_data()`
Main loop for reading and processing ELAC telegrams.

### `write_ELAC_nav(ELAC_nav *E_nav)`
Writes ELAC navigation data.

### `write_ELAC_svp(ELAC_svp *E_svp)`
Writes ELAC sound velocity profile data.

### `write_ELAC_parameter(ELAC_parameter *E_parameter)`
Writes ELAC parameter data.

### `write_ELAC_gen_depths(ELAC_general_data *E_gen_data)`
Writes ELAC general depth data.

### `write_ELAC_depth56(ELAC_depth56 *E_depth)`
Writes ELAC 56-beam depth data.

### `log_SUBMETRIX_data()`
Placeholder for Submetrix data logging.

### `log_RESON_data()`
Main loop for reading and processing RESON telegrams.

### `write_RESON_nav(RESON_NAV *R_nav)`
Writes RESON navigation data.

## Output Files
`RT_unravel` generates various OMG-HDCS formatted output files, including:
*   `<outprefix>.merged`: Consolidated bathymetry and sidescan.
*   `<outprefix>.nav`: Navigation data.
*   `<outprefix>.orientation`: Attitude (roll, pitch, heave).
*   `<outprefix>.heading`: Heading.
*   `<outprefix>.height`: Height data.
*   `<outprefix>.mech_pitch`: Mechanical pitch data.
*   `<outprefix>.surf_ss`: Surface sound speed.
*   `<outprefix>.watercol`: Watercolumn data.
*   `<outprefix>.reflect`: Sidescan amplitude data.
*   `<outprefix>.merged.ss_data`: Sidescan snippet data.
*   `<outprefix>.merged.ph_data`: Sidescan phase data.
*   `<outprefix>.sectors`: TX sector information.
*   `<outprefix>.NMEA`: NMEA data.
*   `<outprefix>.svp`: Sound velocity profiles.
*   `<outprefix>.param`: Parameter telegrams.
```
```