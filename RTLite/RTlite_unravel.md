---
layout: default
title: RTlite_unravel
parent: RTLite Tools
nav_order: 189
---
# RTlite_unravel

## Description
`RTlite_unravel.c` is the core processing module for the `RTlite` utility. Adapted from the more comprehensive `RT` tool, it is responsible for the low-level parsing, interpretation, and processing of raw Simrad multibeam sonar telegrams. It supports a wide range of Simrad EM series systems (EM100, EM1000, EM12S/D, EM300/3000/3002/3002D, EM710, EM122, EM302, EM2040).

The module extracts various data types including navigation, bathymetry, sidescan imagery, attitude, sound velocity profiles, and watercolumn data. It handles byte-swapping, time synchronization, quality control, and the aggregation of data from multiple telegrams into a unified OMG-HDCS (Ocean Mapping Group - Hydrographic Data Conversion System) format for output.

## Key Features

*   **Extensive Sonar Support:** Handles binary telegrams from numerous Simrad EM multibeam echosounder models.
*   **Byte Order Management:** Automatically detects and applies byte-swapping as required by the system's architecture and data format.
*   **Telegram-Specific Parsing:** Contains dedicated functions for parsing different types of Simrad telegrams (e.g., `EM3000_NAV_CODE`, `EM710_DEPTH_CODE`, `EM3000_WATERCOLUMN_CODE`).
*   **Data Aggregation & Merging:** Combines related data from various telegrams (e.g., depth, image, raw time/angle) into a single, comprehensive `OMG_HDCS_profile_header` and `OMG_HDCS_beam` array. This is critical for generating the `.merged` output file.
*   **Time Synchronization:** Extracts and normalizes timestamps from telegrams, using them to synchronize data streams and establish a reference time for output files.
*   **Quality Control & Flagging:** Applies basic quality checks and propagates quality flags from the raw data into the output format.
*   **Specialized Data Handling:** Includes logic for handling watercolumn data (unpacking and optional compression), sound velocity profiles, attitude data from multiple motion sensors, and NMEA strings.

## Functions

### `convert_data()`
The main entry point for processing. It orchestrates file parsing, sonar detection, and calls specific telegram handlers.
*   **Purpose:** Reads the input raw file byte by byte, identifies telegram boundaries, and dispatches data to appropriate parsing functions.
*   **Details:** Manages file pointers, tracks telegram counts, and calls `check_for_eof()` to handle end-of-file conditions for actively logging files.

### `swap_2bytes(short value)`
Performs byte-swapping on a 2-byte short integer if `DOSWAP` is enabled.

### `print_date(char *header_string, em12_time *time)`
(Primarily for debugging) Prints a formatted date and time from an `em12_time` structure.

### `get_1970_time(em12_time *time)`
Converts an `em12_time` structure to a double-precision Unix timestamp.
*   **Purpose:** Standardizes time representation across various telegram formats. Includes logic for Y2K compatibility.

### `check_numeric(char array[], int n)`
(For debugging/validation) Checks if characters in an array are numeric.

### `get_em300_runtime(char *data)`
Parses the `EM3000_RUNTIME_PARAMETER_CODE` telegram.
*   **Purpose:** Extracts sonar operational parameters (e.g., mode, filter ID, depths, pulse length, beam widths, gain settings) and populates the `runTem300` global structure.

### `get_em3000_generic(char *data)`
Parses generic header information common to many `EM3000` series telegrams.

### `get_em300_echo_trace(char *data)`
Parses the `EM3000_ECHOGRAM_CODE` telegram.
*   **Purpose:** Extracts watercolumn echo trace data for individual beams and populates the `WHOLE_ping_WC` structure.

### `get_em3000_watercolumn(char *data)`
Parses the `EM3000_WATERCOLUMN_CODE` telegram.
*   **Purpose:** Extracts comprehensive watercolumn data, including transmit sector information and beam-specific echo traces. Handles multi-datagram pings and dual-head systems.

### `get_em3000_svp(char *data, int type)`
Parses `EM3000_SSP_CODE` and `EM3000_NEW_SSP_CODE` telegrams.
*   **Purpose:** Extracts Sound Velocity Profile (SVP) data and writes it to a `.svp` file.

### `get_em3000_height(char *data)`
Parses the `EM3000_HEIGHT_CODE` telegram.
*   **Purpose:** Extracts height information (e.g., from an RTK GPS) and writes it to a `.hgt` file.

### `get_em3000_nav(char *data)`
Parses the `EM3000_NAV_CODE` telegram.
*   **Purpose:** Extracts navigation data (latitude, longitude, quality, speed, course over ground) and writes it to a `.nav` file. Incorporates NMEA parsing and optional POS/MV quality flagging.

### `scramble_nav(em12_nav *nav)`
(For debugging/testing) Scrambles navigation coordinates.

### `write_fix(em12_nav *nav)`
Writes an `EM12_NAV_CODE` telegram's navigation data to the `.nav` file.

### `prime_array()`
Initializes arrays for sidescan processing.

### `print_array()`
(For debugging) Prints formatted contents of the image array.

### `get_em3000_imagery(int TYPE, char *data)`
Parses `EM3000_IMAGE_CODE` telegrams.
*   **Purpose:** Extracts sidescan imagery data (amplitude/phase) and populates `image_beams` and `ss_imagery` arrays. Handles multi-datagram pings for dual-head systems.

### `get_em710_depths(char *data)`
Parses `EM710_DEPTH_CODE` telegrams.
*   **Purpose:** Extracts bathymetric data (depth, across-track, along-track, quality) for EM710/EM122/EM302/EM2040 systems.

### `print8bits(unsigned char anint)`
(For debugging) Prints the binary representation of an 8-bit integer.

### `get_em710_extra_parameters(char *data)`
Parses `EM710_EXTRA_PARAMETERS_CODE` telegrams.
*   **Purpose:** Used to extract extra parameters, specifically for BScorr files (from SIS 4.1+).

### `get_em710_extra_detects(char *data)`
Parses `EM710_EXTRA_DETECT_CODE` telegrams.
*   **Purpose:** Extracts detailed extra detection information and writes it to an `.merged.extra` file.

### `get_em710_qfactor(char *data)`
Parses `EM710_QFACTOR_CODE` telegrams.
*   **Purpose:** Extracts quality factor information per beam.

### `get_em710_raw_time_angle(char *data)`
Parses `EM710_RAW_TANG_CODE` telegrams.
*   **Purpose:** Extracts raw time and angle (range and beam steering angles) per beam for EM710/EM122/EM302/EM2040 systems.

### `get_em710_imagery(char *data)`
Parses `EM710_IMAGE_CODE` telegrams.
*   **Purpose:** Extracts high-resolution sidescan imagery (16-bit) for EM710/EM122/EM302/EM2040 systems, converting to 8-bit for internal use.

### `unpack_ss_telegram(int TYPE, char *raw_data)`
Parses older `EM1000/EM12/EM121A` sidescan telegrams.

### `write_image()`
Writes processed image data (sidescan) to the output file.

### `get_em3000_surf_SS(char *data)`
Parses the `EM3000_SURF_SS_CODE` telegram.
*   **Purpose:** Extracts surface sound speed measurements.

### `get_em3000_mech_tilt(char *data)`
Parses the `EM3000_MECH_TILT_CODE` telegram.
*   **Purpose:** Extracts mechanical pitch sensor data.

### `get_em3000_heading(char *data)`
Parses the `EM3000_HEADING_CODE` telegram.
*   **Purpose:** Extracts high-rate heading data.

### `get_emXXX_network_attitude(char *data)`
Parses generic network attitude telegrams (e.g., `EM710_NET_ATT_CODE`).
*   **Purpose:** Extracts attitude (roll, pitch, heave, heading) and potentially velocity data from external motion sensors (e.g., Seatex, POS/MV AAC Group 102).

### `get_em3000_attitude(char *data)`
Parses the `EM3000_ATTITUDE_CODE` telegram.
*   **Purpose:** Extracts high-rate motion sensor data (roll, pitch, heave, heading). Supports dual motion sensors.

### `get_em3000_raw_time_angle_new(char *data)`
Parses `EM3000_RAW_TANG_NEW_CODE` telegrams (newer format).
*   **Purpose:** Extracts raw range and angle data.

### `get_em3000_raw_time_angle(char *data)`
Parses `EM3000_RAW_TANG_CODE` telegrams (older format).
*   **Purpose:** Extracts raw range and angle data.

### `get_em3000_depths(char *data)`
Parses `EM3000_DEPTH_CODE` telegrams.
*   **Purpose:** Extracts bathymetric data (depth, across-track, along-track, quality) for EM3000 series systems.

### `merge_em3000()`
Merges processed depth, image, and raw time/angle data from `EM3000` series telegrams.
*   **Purpose:** Consolidates data from different telegrams into a coherent `OMG_HDCS_profile_header` and `OMG_HDCS_beam` array for output to the `.merged` and `.watercol` files. Handles dual-head systems and watercolumn compression.

### `read_121_raw_data(char *data)`
Parses `EM121A_RAW_DATA_REC_CODE` telegrams.

### `write_depths(char *data)`
Writes older `EM1000/EM12/EM121A` depth data.

### `merge_both()`
Merges processed depth and image data from older `EM1000/EM12/EM121A` telegrams into a single `OMG_HDCS` profile.

### `look_for_EM100_dmy()`
Specialized function to look for date/time information in EM100 START telegrams.

### `write_utm_fix(char *data)`
Writes EM100 UTM navigation data.

### `write_em100_reflect(char *data)`
Writes EM100 reflectivity (amplitude) data.

### `write_em100_depths(char *data)`
Writes EM100 depth data.

### `write_param(char *data, int length)`
Writes parameter telegrams to a `.param` file.

### `unpack_svp(char *data)`
Parses older `EM_SVP` telegrams (Sound Velocity Profile).

### `get_telegram_length()`
Helper function to extract the length of a Simrad telegram.

### `get_and_check_telegram(char *data, int nobytes)`
Reads and performs a checksum verification on a telegram.

### `look_for_etx()`
Helper function to locate the End-Of-Telegram (ETX) marker.

### `check_valid_em_datagram(em3000_generic *tele)`
Performs basic validation on EM3000-series telegram headers.

### `write_out_sectors()`
Writes transmit sector information to the `.sectors` file.

### `prepare_output_files()`
Sets up and opens all necessary output files for `RTlite`.

### `check_for_eof()`
Checks for end-of-file conditions and handles file re-opening for actively logged data.

## Output Files
`RTlite_unravel` is responsible for writing the bulk of `RTlite`'s output. The specific files written depend on the input data and command-line options, but generally include:
*   `<outprefix>.merged`: Consolidated bathymetry and sidescan.
*   `<outprefix>.nav` / `<outprefix>.nav_N`: Navigation data.
*   `<outprefix>.orientation` / `<outprefix>.orientation_N`: Attitude (roll, pitch, heave) data.
*   `<outprefix>.heading`: Heading data.
*   `<outprefix>.height`: Height data.
*   `<outprefix>.mech_pitch`: Mechanical pitch data.
*   `<outprefix>.surf_ss`: Surface sound speed.
*   `<outprefix>.watercol`: Watercolumn data.
*   `<outprefix>.reflect`: Sidescan amplitude data (8-bit).
*   `<outprefix>.merged.16_ss_data`: Sidescan amplitude data (16-bit, if `-store_16bit`).
*   `<outprefix>.merged.ph_data`: Sidescan phase data.
*   `<outprefix>.sectors`: Transmit sector information.
*   `<outprefix>.NMEA`: NMEA data.
*   `<outprefix>.svp`: Sound velocity profiles.
*   `<outprefix>.param`: Parameter telegrams.
*   `<outprefix>.modified`: Modified input data (if `-scramblenav`).
*   `<outprefix>.Bscorr`: Backscatter correction files (if `EM710_EXTRA_PARAMETERS_CODE` is parsed).
*   `<outprefix>.merged.extra`: Extra detections (if `EM710_EXTRA_DETECT_CODE` is parsed).
```
```