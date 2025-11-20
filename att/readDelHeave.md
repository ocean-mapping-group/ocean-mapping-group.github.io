---
layout: default
title: readDelHeave
parent: Attitude Tools
nav_order: 9
---
# readDelHeave

## Description
`readDelHeave` is a command-line utility for processing various types of raw heave and attitude data files from different navigation systems (e.g., Applanix POS MV, Seatex Seapath, ISS-60). It converts these raw binary or ASCII inputs into standardized OMG-HDCS (Ocean Mapping Group - Hydrographic Data Cleaning System) attitude `.orientation` files, and sometimes associated navigation (`.nav`) or ASCII files. It primarily focuses on extracting and processing heave, roll, pitch, and heading data, often including delayed heave, for use in other OMG-HDCS tools.

## Usage
```bash
readDelHeave [OPTIONS] -comp <output_basename> <raw_input_file(s)>
```

**Output Files (generated based on input format and options):**
*   `.delayed_heave`: OMG-HDCS attitude file containing delayed heave and real-time heave.
*   `.POS_orient` or `.STX_orient` or `.MCOM_orient`: OMG-HDCS attitude file containing roll, pitch, heading, and heave.
*   `.POS_nav` or `.STX_nav` or `.PMC_nav`: Navigation file (latitude, longitude, altitude).
*   `.POS_aux1_NMEA` / `.POS_prim_NMEA`: ASCII files containing NMEA messages.
*   `.txt`: ASCII output for MCOM data.

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-iss_thv` | Process input files in ISS-60 "thv" ASCII delayed heave format. | |
| `-iss_pmc` | Process input files in ISS-60 "pmc" ASCII POS file format. | |
| `-mcom` | Process input files in F180/185 MCOM binary format. | |
| `-skip_to_sync` | (MCOM specific) Skip bytes at the beginning of the file to align with the first sync byte. | |
| `-filtsamps <samples>` | (MCOM specific) Length of the filter in samples for long period heave. | `1000` |
| `-seapath` | Process input files in Seatex Seapath binary formats (Format 11 or 24). | |
| `-debug` | (Seapath specific) Enable debug output for Seapath processing. | |
| `-downsample <factor>` | (Seapath specific) Downsample the Seapath data (e.g., `4` to drop 100Hz to 25Hz). | `4` |
| `-format <format_id>` | (Seapath specific) Specify the Seapath binary format: `11` or `24` (PFreeHeave). | `11` |
| `-STX_24_Pad <bytes>` | (Seapath Format 24 specific) Specify additional byte padding to format 24 packets. | `2` |
| `-only_YJD <YYYY JJJ>` | (Seapath specific) Process data only for a specific Year and Julian Day. | `2011 131` |
| `-posmv` | Process input files as Applanix POS MV binary Group telegrams (default). | |
| `-year <YYYY>` | (POS MV specific) Specify the year for time calculations. Used if Group 3 telegram is not found. | `2000` |
| `-jday <JJJ>` | (POS MV specific) Specify the Julian Day for time calculations. Used if Group 3 telegram is not found. | `143` |
| `-grp3Date` | (POS MV specific) Use the date derived from the Group 3 telegram for time calculations. | |
| `-grpsum` | (POS MV specific) Print a summary of the processed Group telegrams. | |
| `-msgsum` | (POS MV specific) Print a summary of the processed Message telegrams. | |
| `-delay <seconds>` | Apply a general time delay to processed data. | |
| `-comp <output_basename>` | **Required.** Specifies the base name for the output files. Various output files (e.g., `.delayed_heave`, `.POS_orient`, `.POS_nav`) will be created with this basename. | `my_survey` |
| `<raw_input_file(s)>` | **Required.** One or more raw input data files to be processed. | `posmv_data.bin` |
