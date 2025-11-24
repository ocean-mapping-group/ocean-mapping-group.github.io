---
layout: default
title: DDSsmb_read
parent: M3 Tools
nav_order: 1
---
# DDSsmb_read

## Description
`DDSsmb_read` is a C program designed to convert raw Mesotech DDS (Digital Data Stream) SMB (Sonar Message Block) files, which typically contain raw element sonar data, into the Ocean Mapping Group (OMG) data format. In addition to the primary sonar data, it extracts and processes associated navigation and attitude information, outputting these into separate OMG-compatible files for further processing and analysis within the OMG ecosystem.

## Usage
```bash
DDSsmb_read [OPTIONS] -DDSsmb <filename(s)> -out <prefix>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enables verbose output, providing more detailed status messages during execution. | |
| `-debug` | Activates debug messages, useful for troubleshooting and understanding internal processes. | |
| `-pie` | Flag to indicate the creation of PIE (Post-Interp Echosounder) data. | |
| `-dumpTA` | Flag to dump TA (Transducer Array) data. | |
| `-interp` | Activates interpolation of beams, enhancing data quality. | |
| `-pixel <value>` | Sets the pixel size for processed data. | |
| `-maxdepth <value>` | Defines the maximum depth of interest for filtering or processing. | |
| `-mindepth <value>` | Defines the minimum depth of interest for filtering or processing. | |
| `-left_across <value>` | Specifies the left across-track range. | |
| `-right_across <value>` | Specifies the right across-track range. | |
| `-dB_range <min_dB> <max_dB>` | Sets the decibel range for packing data, likely for intensity values. | |
| `-ping_start <value>` | Specifies a starting ping number for processing. | |
| `-ping_end <value>` | Specifies an ending ping number for processing. | |
| `-time_start <Y JD H M S>` | Defines a start time window (Year, Julian Day, Hour, Minute, Second) to filter data. | |
| `-time_end <Y JD H M S>` | Defines an end time window (Year, Julian Day, Hour, Minute, Second) to filter data. | |
| `-pack_samp <value>` | Sets a packing sample value. | |
| `-DDSsmb <filename(s)>` | **Required.** Specifies one or more input Mesotech DDS SMB raw data files. | `data.smb` |
| `-out <prefix>` | **Required.** Defines the prefix for all generated output files. | `output_survey` |

## Output Files
*   `<prefix>.merged`: Main merged data output.
*   `<prefix>.merged.ss_data`: Sidescan-like data.
*   `<prefix>.merged.16_data`: 16-bit data.
*   `<prefix>.merged.ph_data`: Phase data.
*   `<prefix>.merged.ph16_data`: 16-bit phase data.
*   `<prefix>.orientation`: Attitude data in OMG format.
*   `<prefix>.nav`: Navigation data in OMG format.

## How It Works
1.  **Command-line Argument Parsing:** Provides extensive command-line options to control the conversion process, offering flexibility in data selection and output.
2.  **File Handling and I/O:** Manages the opening of input `.smb` files and a suite of output files, ensuring data can be written in various formats. Iterates through each specified input `.smb` file, reading its content.
3.  **SMB Data Extraction and Parsing:** Uses `jSMB_get_next_tuple_header` (an external function, likely defined in `Mesotech_SMB.h` or a related library) to sequentially parse the input SMB file. This function extracts `SMB_Tuple_Header` (`smb_head`) and `SMB_Tuple_Footer` (`smb_foot`) structures, along with the raw data payload (`tdata`) for each data block. Identifies different types of data telegrams within the SMB stream based on `smb_head.DataType` (e.g., `0x1008` for PMB profile solutions, `0x2001` for 16-bit amplitude and phase images).
4.  **Time-based Filtering:** If a time window is specified via `-time_start` and `-time_end`, the program checks each ping's `ping_time` and skips processing for pings that fall outside this window.
5.  **Output Data Generation:**
    *   **Navigation Output (`write_out_M3_nav`):** This function takes ping time, latitude, and longitude, and formats them into an `jcu_nav_rec` structure, which is then written to the OMG-compatible `.nav` file using `nav_write`. It incorporates a mechanism to prevent writing redundant navigation records if `only_redundant` is set.
    *   **Attitude Output (`write_out_M3_attitude`):** This function extracts roll, pitch, heading, and heave data. It constructs an `OMG_HDCS_summary_attitude` header for the `.orientation` file upon the first record and then writes individual `OMG_HDCS_attitude` records using `OMG_HDCS_write_attitude`.
    *   While other output files (`.merged`, `.merged.ss_data`, etc.) are opened, the specific logic for writing to these files based on the parsed SMB data types is not fully elaborated in the provided code excerpt, implying it resides within the SMB data type parsing blocks.
6.  **Memory Management:** Allocates a large `tdata` buffer (10MB) for reading raw SMB data and ensures it is freed before program exit.
7.  **Error and Usage Reporting:** Utilizes `error()`, `warning()`, and `usage()` functions (presumably from `support.h`) to provide informative messages for critical errors, non-critical issues, and command-line argument misuse, respectively.

## Dependencies
*   `support.h`: Provides general utility functions for command-line parsing (`strtoint`, `strtodbl`), error handling (`error`, `warning`, `check_error`), and string manipulation (`mem_strappend`, `mem_stripext`).
*   `stdtime.h`: Offers functions for converting and formatting time data (`stdtime_from_jul_day`, `stdtime_nicetime`).
*   `OMG_HDCS_jversion.h`: Defines structures and functions specific to the OMG Hydrographic Data Collection System (HDCS) format, including `OMG_HDCS_summary_attitude`, `OMG_HDCS_attitude`, `OMG_HDCS_dump_att_summary`, `OMG_HDCS_write_attitude`, and `OMG_HDCS_fileID_tag`.
*   `jcu_nav.h`: Provides data structures (`jcu_nav_rec`) and functions (`nav_write`) for handling navigation data in a specific format.
*   `Mesotech_SMB.h`: Crucial for defining the structures of Mesotech SMB data (`SMB_Tuple_Header`, `SMB_Tuple_Footer`) and the function `jSMB_get_next_tuple_header` used for parsing these proprietary files.

## Notes
The primary purpose of `DDSsmb_read.c` is to serve as a vital data ingest tool for Mesotech DDS SMB sonar data. By converting this proprietary format into the standardized OMG format, it enables seamless integration of Mesotech data into the broader OMG processing, visualization, and analysis workflows. The program's filtering capabilities (by ping number or time) and flexible output options make it a versatile utility for hydrographic data management and quality control.
