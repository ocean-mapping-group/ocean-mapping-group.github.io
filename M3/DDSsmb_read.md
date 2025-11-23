# `DDSsmb_read.c` - Mesotech DDS SMB to OMG Format Converter

This C program is designed to convert raw Mesotech DDS (Digital Data Stream) SMB (Sonar Message Block) files, which typically contain raw element sonar data, into the Ocean Mapping Group (OMG) data format. In addition to the primary sonar data, it extracts and processes associated navigation and attitude information, outputting these into separate OMG-compatible files for further processing and analysis within the OMG ecosystem.

## Key Features and Functions

*   **Command-line Argument Parsing (`main` function):**
    *   Provides extensive command-line options to control the conversion process, offering flexibility in data selection and output:
        *   `-v`: Enables verbose output, providing more detailed status messages during execution.
        *   `-debug`: Activates debug messages, useful for troubleshooting and understanding internal processes.
        *   `-pie`: Flag to indicate the creation of PIE (Post-Interp Echosounder) data, although the specific logic for this isn't fully detailed in the provided extract.
        *   `-dumpTA`: Flag to dump TA (Transducer Array) data, again, specific implementation not shown.
        *   `-interp`: Activates interpolation of beams, enhancing data quality.
        *   `-pixel <value>`: Sets the pixel size for processed data.
        *   `-maxdepth <value>`, `-mindepth <value>`: Defines the depth range of interest for filtering or processing.
        *   `-left_across <value>`, `-right_across <value>`: Specifies the across-track range.
        *   `-dB_range <min_dB> <max_dB>`: Sets the decibel range for packing data, likely for intensity values.
        *   `-ping_start <value>`, `-ping_end <value>`: Specifies a range of ping numbers to process.
        *   `-time_start <Y JD H M S>`, `-time_end <Y JD H M S>`: Defines a time window (Year, Julian Day, Hour, Minute, Second) to filter data.
        *   `-pack_samp <value>`: Sets a packing sample value, purpose not explicitly clear from context.
        *   `-DDSsmb <filename(s)>`: Specifies one or more input Mesotech DDS SMB raw data files.
        *   `-out <prefix>`: Defines the prefix for all generated output files.
*   **File Handling and I/O (`main` function):**
    *   Manages the opening of input `.smb` files and a suite of output files, ensuring data can be written in various formats:
        *   `.merged`: Main merged data output.
        *   `.merged.ss_data`: Sidescan-like data.
        *   `.merged.16_data`: 16-bit data.
        *   `.merged.ph_data`: Phase data.
        *   `.merged.ph16_data`: 16-bit phase data.
        *   `.orientation`: Attitude data in OMG format.
        *   `.nav`: Navigation data in OMG format.
    *   Iterates through each specified input `.smb` file, reading its content.
*   **SMB Data Extraction and Parsing:**
    *   Uses `jSMB_get_next_tuple_header` (an external function, likely defined in `Mesotech_SMB.h` or a related library) to sequentially parse the input SMB file. This function extracts `SMB_Tuple_Header` (`smb_head`) and `SMB_Tuple_Footer` (`smb_foot`) structures, along with the raw data payload (`tdata`) for each data block.
    *   Identifies different types of data telegrams within the SMB stream based on `smb_head.DataType` (e.g., `0x1008` for PMB profile solutions, `0x2001` for 16-bit amplitude and phase images), though the full parsing logic for these types is not shown in the provided excerpt.
*   **Time-based Filtering:** If a time window is specified via `-time_start` and `-time_end`, the program checks each ping's `ping_time` and skips processing for pings that fall outside this window.
*   **Output Data Generation:**
    *   **Navigation Output (`write_out_M3_nav`):** This function takes ping time, latitude, and longitude, and formats them into an `jcu_nav_rec` structure, which is then written to the OMG-compatible `.nav` file using `nav_write`. It incorporates a mechanism to prevent writing redundant navigation records if `only_redundant` is set.
    *   **Attitude Output (`write_out_M3_attitude`):** This function extracts roll, pitch, heading, and heave data. It constructs an `OMG_HDCS_summary_attitude` header for the `.orientation` file upon the first record and then writes individual `OMG_HDCS_attitude` records using `OMG_HDCS_write_attitude`.
    *   While other output files (`.merged`, `.merged.ss_data`, etc.) are opened, the specific logic for writing to these files based on the parsed SMB data types is not fully elaborated in the provided code excerpt, implying it resides within the SMB data type parsing blocks.
*   **Memory Management:** Allocates a large `tdata` buffer (10MB) for reading raw SMB data and ensures it is freed before program exit.
*   **Error and Usage Reporting:** Utilizes `error()`, `warning()`, and `usage()` functions (presumably from `support.h`) to provide informative messages for critical errors, non-critical issues, and command-line argument misuse, respectively.

## Dependencies

`DDSsmb_read.c` relies on a set of internal and potentially external libraries and header files that define data structures, utility functions, and I/O mechanisms crucial for its operation:

*   `support.h`: Provides general utility functions for command-line parsing (`strtoint`, `strtodbl`), error handling (`error`, `warning`, `check_error`), and string manipulation (`mem_strappend`, `mem_stripext`).
*   `stdtime.h`: Offers functions for converting and formatting time data (`stdtime_from_jul_day`, `stdtime_nicetime`).
*   `OMG_HDCS_jversion.h`: Defines structures and functions specific to the OMG Hydrographic Data Collection System (HDCS) format, including `OMG_HDCS_summary_attitude`, `OMG_HDCS_attitude`, `OMG_HDCS_dump_att_summary`, `OMG_HDCS_write_attitude`, and `OMG_HDCS_fileID_tag`.
*   `jcu_nav.h`: Provides data structures (`jcu_nav_rec`) and functions (`nav_write`) for handling navigation data in a specific format.
*   `Mesotech_SMB.h`: Crucial for defining the structures of Mesotech SMB data (`SMB_Tuple_Header`, `SMB_Tuple_Footer`) and the function `jSMB_get_next_tuple_header` used for parsing these proprietary files.

## Purpose

The primary purpose of `DDSsmb_read.c` is to serve as a vital data ingest tool for Mesotech DDS SMB sonar data. By converting this proprietary format into the standardized OMG format, it enables seamless integration of Mesotech data into the broader OMG processing, visualization, and analysis workflows. The program's filtering capabilities (by ping number or time) and flexible output options make it a versatile utility for hydrographic data management and quality control.
