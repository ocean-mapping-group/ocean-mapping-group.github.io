# readADCP

## Description
`readADCP` is a command-line utility designed to read, process, and analyze RDI (RD Instruments) ADCP (Acoustic Doppler Current Profiler) data files, primarily in ASCII format. It offers extensive capabilities for filtering, time-bounding, depth-referencing, and outputting various velocity and backscatter profiles. The tool can integrate external navigation and attitude data, apply tide corrections, and generate output in different formats, including raw profiles and r4 grid files. It's a fundamental tool for oceanographers to extract meaningful current and backscatter information from ADCP raw data.

## Usage
```bash
readADCP [OPTIONS] -out <output_filename> -in <input_filename(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-be_quiet` | Suppress verbose output. | |
| `-mindepth` | Minimum depth for processing. | `0` |
| `-maxdepth` | Maximum depth for processing. | `50` |
| `-layers` | Number of depth layers for output profiles. | `100` |
| `-MAX_allowed_layers_to_interp` | Maximum allowed layers to interpolate. | `5` |
| `-reference_depth` | Subtracts sensor instantaneous depth from this value to provide a stable depth reference. | `172.0` |
| `-bottom_ref` | Interprets `-mindepth` and `-maxdepth` as metres away from the bottom track, not the surface. | |
| `-dtm_ref <terrain.r4>` | Use depth from an `r4` terrain file to trim the trace (e.g., exclude data below the seafloor). | |
| `-use_avbeam_depth` | Trim data below the average beam depth, minus a bin depth. | |
| `-draft` | Specifies the draft of the ADCP sensor. | `1.0` |
| `-export_r4` | Export processed data in `r4` format (a specific grid format). | |
| `-start <YYYY JJJ HH MM>` | Specify a start time for processing using Year, Julian Day, Hour, and Minute. | |
| `-end <YYYY JJJ HH MM>` | Specify an end time for processing using Year, Julian Day, Hour, and Minute. | |
| `-bounds_from <other_file_nav_format>` | Use time bounds from another navigation file to constrain processing. | |
| `-startYMD <YYYY MM DD HH MM>` | Specify a start time for processing using Year, Month, Day, Hour, and Minute. | |
| `-endYMD <YYYY MM DD HH MM>` | Specify an end time for processing using Year, Month, Day, Hour, and Minute. | |
| `-duration_min <XXX>` | Specify a duration in minutes. Requires `-start` or `-startYMD` to be set. | |
| `-onlyuseshipheading <MIN MAX>` | Only process data when the ship's heading is within the specified range (in degrees). | |
| `-showMAG` | Display velocity magnitude (default behavior). | |
| `-vel_scaler` | Scaling factor for velocity values. | `0.001` |
| `-showBS` | Display backscatter data. | |
| `-do_Sv` | Convert backscatter to Volume Backscatter Strength (Sv). Requires `-showBS`. | |
| `-Er_DN_shift` | Shift value for Er_DN correction when calculating Sv. Requires `-do_Sv`. | `5` |
| `-BSrange <MIN MAX>` | Specify the backscatter display range. Requires `-showBS`. | `3000 5000` |
| `-doalltrace` | Process all traces, even past the bottom. Requires `-showBS`. | |
| `-showERR` | Display error velocity. | |
| `-max_err_vel` | Maximum allowable error velocity. | `150` |
| `-allowable_sum_percent_good` | Minimum sum of percent good values required for a bin to be considered valid. | `300` (max possible `400`) |
| `-maximum_believable_magnitude` | Maximum believable velocity magnitude (mm/s). | `10000` |
| `-showAZI` | Display velocity azimuth. | |
| `-headbias` | Apply a heading bias (in degrees). | `-20.0` |
| `-showTAN` | Display tangential velocity component. | |
| `-showRAD` | Display radial velocity component. | |
| `-showVERT` | Display vertical velocity component. | |
| `-plotpositive` | Plot only positive values (when showing velocities). | |
| `-plotnegative` | Plot only negative values (when showing velocities). | |
| `-ensem_stack` | Number of ensembles to stack. | `50` |
| `-stack_in_map` | Stack ensembles into a map. | |
| `-phase_zero <YYYY JJJ HH MM>` | Specify a phase zero time. | |
| `-tidefile <filename>` | Path to a tide file for corrections. | `whatever_RTK.nav` |
| `-ref_level` | Reference level for tide corrections. Requires `-tidefile`. | `-22.0` |
| `-maxcurrent` | Maximum current value. | `2.0` |
| `-min_vels_to_av` | Minimum number of valid velocities required for averaging. | `5` |
| `-delay` | Apply a time delay in seconds. | `3600` |
| `-map <filename>` | Path to a mapsheet file for georeferencing. | `whatever.map` |
| `-pixel` | Pixel size for map output. Defaults to map sheet's pixel size. | `1.0` |
| `-pad_gaps` | Pad gaps in data. | |
| `-nav <navfilename>` | Path to an external navigation file. | |
| `-use_adcp_nav` | Use the ADCP's internal navigation data. | |
| `-att <attfilename>` | Path to an external attitude file (for cases without bottom track heading). | |
| `-orientation <orientfile>` | Path to an orientation file. | |
| `-debug_head` | Debug mode: compares CMG (Course Made Good) and MAGhead (Magnetic Heading). | |
| `-debug_azi` | Debug mode: (not of general use). | |
| `-out <output_filename>` | **Required.** Base name for output files. Various outputs will be generated with extensions (e.g., `.prof`, `.r4`, `.nav`). | |
| `-winADCP` | Process data from Windows ADCP format. | |
| `-dump_RPTZ` | Dump RPTZ (Roll, Pitch, Temperature, Depth) data to an ASCII file. | |
| `-dump_CURR` | Dump current data to an ASCII file (supports user-specified format). | |
| `-dump_BINS` | Dump bin data to an ASCII file. | |
| `-in <input_filename(s)>` | **Required.** One or more input ADCP data files. | |