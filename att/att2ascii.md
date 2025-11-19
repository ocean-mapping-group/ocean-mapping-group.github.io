# att2ascii

## Description
`att2ascii` reads multiple OMG-HDCS (Ocean Mapping Group - Hydrographic Data Cleaning System) attitude record files and outputs their contents as an ASCII listing. It supports time-bounding, subsampling, and can extract specific attitude components (heave, pitch, roll, heading) in a navigation format. It can also identify and output peak values for these components.

## Usage
```bash
att2ascii [OPTIONS] -comp <output_filename> <att_filename(s)>.orientation
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-avsamps <samples>` | If used with `-navout`, writes out min and max heave (or other specified attitude components) within the given number of samples to the navigation file. | `600` |
| `-navout` | Output data in navigation format. | |
| `-start_sec <YYYY JJJ HH MM SS>` | Specify a start time for processing using Year, Julian Day, Hour, Minute, and Second. | `1993 180 16 24 35` |
| `-end_sec <YYYY JJJ HH MM SS>` | Specify an end time for processing using Year, Julian Day, Hour, Minute, and Second. | `1993 180 17 12 43` |
| `-timeboundsof <merged_filename>` | Use time bounds from an existing merged file to constrain processing. | `whatever.merged` |
| `-addGPSrolloverwraps <value>` | Adds a delay to account for GPS rollover wraps (e.g., `1` for one 1024-week cycle). | `1` |
| `-skip <value>` | Skip attitude records, effectively subsampling the data. | `10` |
| `-just_peaks` | Output only peak values (max/min) for heave, pitch, roll, and heading. | |
| `-heavediff` | When used with `-navout`, outputs (mechanical pitch - heave) in navformat. | |
| `-delayheave` | When used with `-navout`, outputs mechanical pitch in navformat. | |
| `-realheave` | When used with `-navout`, outputs heave in navformat. | |
| `-pitch` | When used with `-navout`, outputs pitch in navformat. | |
| `-roll` | When used with `-navout`, outputs roll in navformat. | |
| `-heading` | When used with `-navout`, outputs heading in navformat. | |
| `-comp <output_filename>` | **Required.** Specifies the name of the output ASCII file. | `outfile.name` |
| `<att_filename(s)>.orientation` | **Required.** One or more input OMG-HDCS `.orientation` files to be processed. | `attfilename1.orientation attfilename2.orientation` |