---
layout: default
title: makeWC
parent: OMG Tools
nav_order: 39
---
# makeWC

## Description
`makeWC` is a versatile command-line utility for processing multibeam water column (WC) data. It generates various visualizations and extracts information from water column telegrams, such as pie diagrams, vertical profiles, time-angle plots, and horizontal profiles. The tool offers extensive customization for output format, spatial/temporal filtering, motion correction, and mapping.

## Usage
```bash
makeWC <input_omg_file(.merged)> <output_WCprefix> [OPTIONS]
makeWC -out <output_WCprefix> -ins <many.merged's> [OPTIONS]
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `<input_omg_file(.merged)>` | Path to the input OMG-HDCS merged file. When using the first usage syntax, the output filename will be derived from this, typically with a `.watercol` extension. | |
| `<output_WCprefix>` | **Required.** Prefix for the output water column files. | |
| `-ins <many.merged's>` | Allows processing multiple merged files. The files are listed after `-ins` until another option is encountered. | |
| `-out <output_WCprefix>` | Alternative way to specify the output prefix, especially when using `-ins`. | |

### Output Type
| Option | Description | Default |
|---|---|---|
| `-pie` | Generates a "pie diagram" (circular or semi-circular view of the water column). | **Default** |
| `-vert_prof` | Generates a vertical profile of the water column. | |
| `-horiz_prof` | Generates a horizontal profile of the water column. | |
| `-time_angle` | Generates a time-angle plot. | |
| `-out_as_ss` | (Used with `-horiz_prof`) Outputs the horizontal slice in GLORIA sidescan format. | |

### Spatial & Temporal Filtering
| Option | Description |
|---|---|
| `-start <ping_num>` | Process pings within a specific range (inclusive). | All pings |
| `-end <ping_num>` | Process pings within a specific range (inclusive). | All pings |
| `-pixel <size>` | Pixel size for the output image. | `0.5` |
| `-maxdepth <val>` | Maximum depth (in meters) for the water column image. | `100.0` |
| `-mindepth <val>` | Minimum depth (in meters) for the water column image. | `0.0` |
| `-left_across <val>` | Define the left across-track limit for the image (replaces symmetrical aspect). | `+/- maxdepth * aspect / 2.0` |
| `-right_across <val>` | Define the right across-track limit for the image (replaces symmetrical aspect). | `+/- maxdepth * aspect / 2.0` |
| `-aspect <val>` | Aspect ratio for the water column image (depth vs. across-track width). | `2.0` |
| `-image_centre_x <val>` | Defines the X-center of a specific image area. Requires `image_width` and `image_height`. | |
| `-image_centre_z <val>` | Defines the Z-center of a specific image area. Requires `image_width` and `image_height`. | |
| `-image_width <val>` | Defines the width of a specific image area. Requires `image_centre_x` and `image_centre_z`. | |
| `-image_height <val>` | Defines the height of a specific image area. Requires `image_centre_x` and `image_centre_z`. | |
| `-bottom_relative <val>` | Sets `image_centre_z` `val` meters off the bottom detect of the center beam. | |
| `-z_scaler <val>` | Scaling factor for the Z-axis (depth). | `1.0` |
| `-centre_on_sonarY` | If using aspect, aligns the image with the offset Transducer (Tx). | |
| `-centre_ping_beam_LL <lat> <lon>` | Centers the processing on the ping closest to the given Latitude/Longitude. | |
| `-mindist <val>` | (Used with `-centre_ping_beam_LL`) Minimum allowed distance for a beam to be considered "closest". | `5` |
| `-pings_centre <ping_num>` | Centers the processing around a specific ping number. | |
| `-pings_around <val>` | Processes a given number of pings around `pings_centre`. | |
| `-pings_aside <val>` | Processes `+/- val` pings around `pings_centre`. | |
| `-closest_to_time <time_1970> <mode>` | Finds the ping closest to a given 1970 Unix timestamp. `mode`: `0` (absolute), `1` (before), `2` (after). | |
| `-time_start_1970 <time_1970>` | Process data starting from a 1970 Unix timestamp for a given window in seconds. | |
| `-window_sec <val>` | Process data for a given window in seconds, starting from `time_start_1970`. | |
| `-time_start <year> <jday> <hr> <min> <sec>` | Process data within a specific date/time range. | |
| `-time_end <year> <jday> <hr> <min> <sec>` | Process data within a specific date/time range. | |
| `-timeboundsof <merged_file>` | Use time bounds from another merged file. | |
| `-timeboundssubset <frac> <cent>` | Use time bounds from another merged file; optionally specify a fraction and center of that time range. | |
| `-stack <val>` | Stack `val` pings together for averaging (typically for vertical profiles). | `1` |
| `-skip <val>` | Skip `val` pings between processed pings. | `1` |
| `-specif_BW <SECT#> <minBW> <maxBW>` | Restrict the bandwidth of a specific sector. | |
| `-specific_swath <1 or 2>` | Process only a specific swath (for dual-swath systems, though this option may not work for all EM2040 configurations). | |
| `-em2040D_first` / `-em2040D_second` | Process only the first or second of the EM2040 dual-head data. | |
| `-em2040_left` / `-em2040_right` | Process only the left or right side of the EM2040 data. | |
| `-shift_logic <val>` | Logic for shifting processing in EM2040D (0-3 valid). | `0` |

### Corrections & Enhancements
| Option | Description | Default |
|---|---|---|
| `-add_heave` / `-other_heave` | Apply heave correction. `-other_heave` may use an alternative heave source. | |
| `-the_draft <val>` | Override the draft value. | Auto-calculated |
| `-add_roll_pitch` / `-hull <hull_vector_file>` / `-hull_offset_to_sonar <x> <y> <z>` | Embed motion data (roll, pitch) and/or visualize a hull shape using a vector file and offset. | |
| `-embed_motion` | Embed motion data into the output (primarily for vertical profiles). | |
| `-fix_pointing` | Apply corrections for beam pointing angles. | |
| `-suppress_SRA_range <min> <max>` | Suppress data within a specified Sonar Relative Angle range. | |
| `-hori_tilt <m_per_ping> <ref_ping>` | Apply a horizontal tilt correction, shifting depth per ping relative to a specified reference ping. | |
| `-dophase` | Process phase data (only for kmall files if phase data is present). | |
| `-WC_wrap_8bit <val>` | 8-bit wrap value for water column intensity. | `-40` |
| `-add_DN_per_km <val>` | Add a Digital Number (DN) shift per kilometer. | `0.0` |
| `-add_sector_gains <file>` | Apply custom sector gains from an ASCII file. | |
| `-add_BT <val>` | Add bottom track information to the output image. `0` (off), `1` (on for pie), `2` (on for vertical profile). | `0` |
| `-before_1st_arrival` | Consider data before the first arrival for BT (experimental). | |
| `-beyond_DN_drop <val>` | Define the DN drop threshold for bottom detection. | `60` |

### Output Formatting
| Option | Description |
|---|---|
| `-pgm` | Output in PGM (Portable Graymap) format. | |
| `-ppm` | Output in PPM (Portable Pixmap) format. (If BT is requested, it will map them as a color). | |
| `-str_result <min_DN> <max_DN>` | Stretch the resulting pixel values to a min/max DN range. | `0 255` |
| `-show_thresh` | Show threshold for pixel values. | |
| `-dump_sector_info` | Dump information about sonar sectors. | |
| `-preserve_ping_no` | Preserve the original ping numbers in the output. | |
| `-add_graticule <pixels>` | Adds a graticule (grid lines) at 1m intervals (for pie diagrams). | |
| `-add_grid <pixels>` / `-gridcol <val>` | Add a grid to the output image with specified pixel spacing and color. | |
| `-add_sequence` | Add sequence numbers (for pie diagrams). | |
| `-outXY_forIVS <freq>` | Output XY coordinates for IVS Fledermaus curtain file at specified frequency (how often you want a geofix). | |
| `-test_compress <val>` | Test water column data compression with a given factor (does not affect raw data). | `1` |
| `-force_maxTA <val>` | Force a maximum time-angle value. | |
| `-do_time_highlights` / `-highlight_halfwidth <val>` / `-check_RxCycle` | Highlight specific time intervals in the output; `check_RxCycle` highlights Rx cycle boundaries. | |

### Mapping
| Option | Description |
|---|---|
| `-map <Box.header0>` | Map the water column data onto an existing map grid defined by `Box.header0`. | |
| `-Xpixel <val>` | Pixel size for the X-dimension in the mapped output. | Uses `maphead.xstep` |
| `-limitmapX <min> <max>` / `-limitmapY <min> <max>` | Limit the mapped output to specific X or Y pixel ranges. | |
| `-orthomap` / `-alongmap` | Map the water column along (default) or orthogonal to the track. | `alongmap` |
| `-lr_flip` / `-no_flip` | Flip the left/right orientation of the map. | `no_flip` |
| `-fill_map_gap` | Fill gaps in the mapped output. | |

## How It Works
1.  **Input Processing:** Reads one or more OMG-HDCS merged files and associated water column (`.watercol` or `.WC_Phase1`), and parameter (`.param`) files. It can also integrate sector information (`.sectors`) and custom sector gains.
2.  **Configuration:** Interprets a vast array of command-line options to configure the type of output, spatial and temporal filters, motion corrections, and visual enhancements.
3.  **Water Column Data Extraction:** For each selected ping, it reads the water column data. Depending on the chosen output type, it transforms this data:
    *   **Pie Diagram:** Projects the water column into a circular view around the sonar.
    *   **Vertical Profile:** Creates a 2D image where one axis is depth and the other is time/ping number.
    *   **Horizontal Profile:** Creates a 2D image where one axis is across-track distance and the other is time/ping number.
    *   **Time-Angle Plot:** (Not fully implemented in the provided source)
4.  **Corrections & Enhancements:** Applies various corrections such as heave, roll/pitch compensation, horizontal tilt, and adjusts intensity values based on gains or attenuation. It can also integrate bottom track data and hull outlines.
5.  **Output Generation:** Generates the output image in JHC's custom image format (or PGM/PPM if specified) and can optionally write auxiliary files like XY coordinates for external mapping software (e.g., IVS Fledermaus), grazing angles, or along-track displacements.
6.  **Mapping:** If the `-map` option is used, it projects the water column data onto a geographical grid defined by a `Box.header0` file, producing a georeferenced image.
7.  **Time-Series Analysis:** For time-series outputs, it can highlight specific events or features based on time windows or RX cycle boundaries.

## Output Files
*   `<output_WCprefix>.pie`: Water column pie diagram (JHC image format or PGM/PPM).
*   `<output_WCprefix>.vert_prof`: Vertical water column profile (JHC image format or PGM/PPM).
*   `<output_WCprefix>.horiz_prof`: Horizontal water column profile (JHC image format or PGM/PPM).
*   `<output_WCprefix>.time_angle`: Time-angle water column plot (JHC image format or PGM/PPM).
*   Auxiliary files such as XY coordinates for IVS Fledermaus (`.ivs`) if `-outXY_forIVS` is used.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `j_EM_watercol.h`: For water column data structures and functions.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.
*   `j_generic_beam_pattern.h`: For beam pattern structures and functions.

## Notes
`makeWC` is a powerful and flexible tool for visualizing and analyzing water column data, providing insights into acoustic scattering, bottom detection reliability, and features within the water column. Its extensive customization options allow users to tailor the output to specific research questions or visualization needs. The tool supports both interactive and batch processing workflows.