# appendAtt

## Description
`appendAtt` is a command-line utility designed to append multiple OMG-HDCS (Ocean Mapping Group - Hydrographic Data Cleaning System) attitude record files into a single output file. It sorts the input files based on the time of their first record. It also supports time-bounding the appended data and applying an optional time shift to the input records.

## Usage
```bash
appendAtt [OPTIONS] -out <output_filename> <input_filename(s)>.orientation
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-intimeshiftsecs <seconds>` | Apply a time shift (in seconds) to the input attitude records before appending. | `86400` |
| `-extrasecs <seconds>` | When using `-timeboundsof`, extend the time bounds by this many seconds (before and after). | `10` |
| `-start <YYYY JJJ HH MM>` | Specify a start time for processing using Year, Julian Day, Hour, and Minute. | `1993 180 16 00` |
| `-end <YYYY JJJ HH MM>` | Specify an end time for processing using Year, Julian Day, Hour, and Minute. | `1993 180 17 00` |
| `-start_sec <YYYY JJJ HH MM SS>` | Specify a start time for processing using Year, Julian Day, Hour, Minute, and Second. | `1993 180 16 12 34` |
| `-end_sec <YYYY JJJ HH MM SS>` | Specify an end time for processing using Year, Julian Day, Hour, Minute, and Second. | `1993 180 17 32 51` |
| `-timeboundsof <merged_filename>` | Use time bounds from an existing merged file (e.g., a multibeam merge file) to constrain the output. | `whatever.merged` |
| `-out <output_filename>` | **Required.** Specifies the name of the output `.orientation` file. | `outfileName.orientation` |
| `<input_filename(s)>.orientation` | **Required.** One or more input OMG-HDCS `.orientation` files to be appended. | `infileName1.orientation infileName2.orientation` |