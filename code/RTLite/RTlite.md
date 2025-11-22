---
layout: default
title: RTlite
parent: RTLite Tools
nav_order: 188
---
# RTlite

## Description
`RTlite` is a command-line utility for processing Simrad multibeam sonar telegrams and writing them to OMG-HDCS (Ocean Mapping Group - Hydrographic Data Conversion System) files. It is a streamlined version of the more comprehensive `RT` tool, designed for batch processing without a graphical interface. `RTlite` can unpack Simrad EM100, EM1000, EM12S/D, EM300/3000/3002/3002D, EM710, EM122, EM302, and EM2040 telegrams.

It handles various aspects of data conversion, including byte order, time synchronization, quality flagging, and the extraction of bathymetry, sidescan, attitude, navigation, and watercolumn data.

## Usage
```bash
RTlite [OPTIONS] [<input_file_options>]
```

## Arguments

### Input/Output File Naming (Choose one style)
*   **Old Style:**
    *   `-prefix <prefix_path>`: Prefix for input filenames (e.g., `raw/JD123/`).
    *   `-suffix <suffix_name>`: Suffix for input filenames (e.g., `_ShipName.all`).
    *   `-line <line_name>`: Specific line name to process (used with prefix/suffix).
    *   `-out <output_handle>`: Prefix for output OMG-HDCS files (e.g., `merged/JD123/`).
*   **New Style:**
    *   `-infile <input_filepath>`: Full path to the input raw sonar file (e.g., `raw/JD123/0001_20120705_205514_Shipname.all`).
    *   `-outprefix <output_filepath_prefix>`: Optional. Full path prefix for output files. If not supplied, outputs will be in the input file's directory.

### Verbosity Options
| Option | Description |
|---|---|
| `-quiet` | Suppress verbose output. |
| `-turn_on_verbose <depth_telegram_num>` | Turn on verbose output after a specific depth telegram number. |

### Positioning Options
| Option | Description |
|---|---|
| `-posnav` | Enable POS/MV navigation flagging. |
| `-maxNUMSATS <num>` | Maximum number of satellites for nav flagging. |
| `-maxCORRAGE <age>` | Maximum correction age for nav flagging. |
| `-maxHDOP <hdop>` | Maximum HDOP for nav flagging. |
| `-scramblenav` | Scramble navigation coordinates (for testing/anonymization). |
| `-refcoord <lat> <lon>` | Reference coordinate for `scramblenav`. |
| `-ignore_not_Y2K` | Ignore non-Y2K compliant dates. |
| `-debug_nav` | Enable navigation debugging. |
| `-navcockup` | Intentionally mess up navigation (for testing). |
| `-flipNE` | Flip Northing/Easting coordinates. |
| `-utm <meridian>` | Use UTM projection with a central meridian. |
| `-auto_write_primary_nav` | Automatically write the primary navigation system to the `.nav` file. |

### Attitude Options
| Option | Description |
|---|---|
| `-2motions` | Process data from two motion sensors. |
| `-declin <value>` | Apply magnetic declination correction. |
| `-auto_write_primary_orientation` | Automatically write the primary orientation system to the `.orientation` file. |

### Seabed Imagery Options
| Option | Description |
|---|---|
| `-suppress_sk` / `-unsuppress_sk` | Suppress/unsuppress skipped records. |
| `-forgotss` | Assume no sidescan telegrams are present. |
| `-oldEM100_ampl` | Use old EM100 amplitude format. |
| `-rescale_BSN` | Rescale BSn and BSo values to preserve 0.1dB resolution. |
| `-store_16bit` | Write merged 16-bit sidescan data (`merged.16_ss_data`). |

### Miscellaneous Options
| Option | Description |
|---|---|
| `-noLength` | Ignore telegram length checks. |
| `-check` | Enable general integrity checks. |
| `-phase` | Store phase information. |
| `-onetype` | Process only one type of telegram. |
| `-depth` / `-reflect` | Output depth/reflectivity data. |
| `-dont_addRP` | Do not add roll/pitch to depth. |
| `-ascii_dump` | Output files in ASCII format instead of binary. |
| `-split_TorInge <id>` | Split data for specific processing (used by Tor Inge). |
| `-upsidedown_depth` | Adjust depth for upside-down transducer. |
| `-backout` | Backout flag. |
| `-pre_QF_telegram` | Pre-Q-Factor telegram flag. |
| `-dump_extra_detects` | Dump extra detection information. |
| `-float_twtt` | Write float TWTT. |

### Input File Format Selection (Auto-detected now, but can be forced)
| Option | Description |
|---|---|
| `-em100` / `-em120` / `-em300` / `-em1000` / `-em1002` / `-em3000` / `-em3000d` / `-em3002` / `-em3002d` / `-em710` / `-em122` / `-em302` / `-em2040` / `-em12s` / `-em121a` | Specify the Simrad sonar model. |
| `-force_swap` / `-LE` / `-BE` | Force byte swapping (Little Endian / Big Endian). |

### Output File Version Options
| Option | Description |
|---|---|
| `-packdown` | Use version 2 output format. |
| `-version1` / `-version2` / `-version3` / `-version4` / `-v1` / `-v2` / `-v3` / `-v4` | Specify the OMG-HDCS file version. |

### Water Column Options
| Option | Description |
|---|---|
| `-unpack_watercol` | Unpack watercolumn data. |
| `-compress_watercol <factor>` | Compress watercolumn data by a given factor. |
| `-fix_wc_time` | Fix watercolumn datagram timestamping issues. |
| `-guess_noWCsample` | Guess the number of watercolumn samples. |
| `-fake_wcd_depths <depth>` | Create fake WCD depths at a specified value. |

## How It Works

1.  **Initialization:**
    *   Parses command-line arguments to configure processing and output options.
    *   Initializes global variables and data structures for various sonar telegrams and OMG-HDCS formats.
    *   Initializes JasPer library for watercolumn compression.
2.  **File Naming and Opening:**
    *   Determines input and output file paths based on `infile`, `outprefix`, `prefix`, `suffix`, and `line` arguments.
    *   Opens the raw input sonar file for reading and all necessary output OMG-HDCS files (`.merged`, `.nav`, `.orientation`, `.heading`, `.height`, `.mech_pitch`, `.surf_ss`, `.watercol`, `.reflect`, `.merged.ss_data`, `.merged.16_ss_data`, `.merged.ph_data`, `.sectors`, `.NMEA`, `.svp`, `.param`, `.modified`).
3.  **Automatic Sonar Detection:**
    *   Automatically detects the sonar model and byte order from the input file if not explicitly specified by command-line arguments.
4.  **Data Processing Loop (`convert_data()`):**
    *   Calls `log_data()` (defined in `RTlite_unravel.c`), which is the core function for reading raw sonar telegrams.
    *   `log_data()`:
        *   Iteratively reads telegrams from the input file.
        *   Identifies telegram type (e.g., NAV, DEPTH, IMAGE, ATTITUDE, SSP, WATERCOLUMN).
        *   Calls specialized unpacker functions (e.g., `get_em3000_nav`, `get_em710_depths`, `get_em3000_watercolumn`) to parse the binary data.
        *   Performs byte-swapping as needed.
        *   Aggregates related data (e.g., depth and image telegrams into a single ping record).
        *   Applies various corrections and flagging (e.g., navigation quality checks, declination).
        *   Populates internal OMG-HDCS data structures (`summary`, `profile`, `beams`).
        *   Writes processed data to the appropriate output files.
5.  **Watercolumn Compression:** If `unpack_watercol` and `compress_watercol` are enabled, compresses watercolumn data using JasPer.
6.  **Cleanup:**
    *   Closes all open files.
    *   Frees dynamically allocated memory.

## Output Files
`RTlite` generates various OMG-HDCS formatted output files, including (but not limited to):
*   `<outprefix>.merged`: Consolidated bathymetry and sidescan.
*   `<outprefix>.nav` / `<outprefix>.nav_N`: Navigation data (multiple files if multiple navigation systems are detected).
*   `<outprefix>.orientation` / `<outprefix>.orientation_N`: Attitude (roll, pitch, heave) data.
*   `<outprefix>.heading`: Heading data.
*   `<outprefix>.height`: Height data.
*   `<outprefix>.mech_pitch`: Mechanical pitch data.
*   `<outprefix>.surf_ss`: Surface sound speed data.
*   `<outprefix>.watercol`: Watercolumn data.
*   `<outprefix>.reflect`: Reflectivity data.
*   `<outprefix>.merged.ss_data`: Sidescan snippet data (8-bit).
*   `<outprefix>.merged.16_ss_data`: Sidescan snippet data (16-bit, if `-store_16bit` is used).
*   `<outprefix>.merged.ph_data`: Sidescan phase data.
*   `<outprefix>.sectors`: Transmit sector information.
*   `<outprefix>.NMEA`: NMEA data.
*   `<outprefix>.svp`: Sound velocity profiles.
*   `<outprefix>.param`: Parameter telegrams.
*   `<outprefix>.modified`: Modified input data (if `-scramblenav`).

## Note
`RTlite` is designed for non-interactive batch processing, making it suitable for automated data conversion workflows. It reuses much of the core data parsing logic from the interactive `RT` tool.
```
```