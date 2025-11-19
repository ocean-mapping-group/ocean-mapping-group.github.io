# DelayEditor

## Description
`DelayEditor` is an interactive X-window application used for analyzing, visualizing, and correcting various motion-related issues in multibeam sonar data. It runs through a merged bathymetry file (or HDCS/USL formats) and allows the user to interactively adjust parameters like roll delay, lag, scale factor, and lever arms. It can also apply corrections for heave drift, pitch stabilization, and yaw misalignment for dual-head systems. The tool plots various parameters over time, displays bathymetry and imagery, and provides functions for correlating motion data and performing FFT analysis to identify periodic errors. It can output a corrected merged file or an ASCII plot file.

## Usage
```bash
DelayEditor [OPTIONS] <datafile>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-cont_int <value>` | Contour interval for depth plots. | `0.1` |
| `-qcdump` | Dump a simplified ASCII file for QC purposes (only roll, pitch, heading, heave). | |
| `-reference` | Use a reference surface for analysis (e.g., for residual heave calculations). Can be combined with `-fract_swath_to_use <fraction>` (e.g., `0.8`). | |
| `-justdump` | Process and dump a detailed ASCII plot file without launching the interactive X-window interface. | |
| `-wantimage` | Output an image file (e.g., for signal strength). | |
| `-hdcs` | Process HDCS format data (instead of standard OMG-HDCS merged files). | |
| `-proc` | Use processed depths instead of observed depths. | |
| `-compare_motions` | Compare two motion streams (from `.orientation_1` and `.orientation_2` files based on `<datafile>` basename). | |
| `-norollfilter` | Disable the default 3-ping box car filter on roll. | |
| `-multi` | (Multi-file processing, functionality unclear from source without further context) | |
| `-image` | (Related to imagery display, distinct from `-wantimage`) | |
| `-signal <min> <max>` | Define min and max signal range for display. | `120.0 150.0` |
| `-hilbert <count>` | Number of samples for Hilbert transform used in envelope calculation. | `0.1` |
| `-start <ping_num>` | Start ping number for processing/display. | `400` |
| `-end <ping_num>` | End ping number for processing/display. | `700` |
| `-max_incidence <angle>` | Maximum incidence angle to consider for seabed slope calculations. | `50.0` |
| `-maxheave <value>` | Maximum believable heave value; values exceeding this are treated as zero in heave drift calculation. | `2.0` |
| `-fix` | Enable correction mode. This will modify the input data based on other parameters. If `heave_drift_flag` is set, outputs `.depth_shifts`; otherwise outputs `.fixed`. | |
| `-draft <meters>` | Specifies the draft of the sonar transducer. **Required for corrections.** | `2.50` |
| `-lever_arm <x> <y> <z>` | Specify X, Y, Z lever arm offsets (ahead, right, down) for induced heave correction. | `3.1 2.3 0.7` |
| `-auto_lag` | Automatically estimate lag based on average two-way travel time (TWTT). | |
| `-delay <seconds>` | Apply a time delay to roll data for correlation/correction. | `0.1` |
| `-lag <seconds>` | Apply a time lag for correlation/correction. | `0.1` |
| `-scale <factor>` | Apply a scale factor to roll data. | `1.03` |
| `-add_pitch_stab` | Enable pitch stabilization. | |
| `-stab_zero <angle>` | Incidence angle for zero along-track offset for pitch stabilization. Requires `-add_pitch_stab`. | `53.0` |
| `-heave_drift` | Enable heave drift estimation and correction using a cosine-squared tapered weighted average. Can be combined with `-addtotide` or `-replacetide`. | |
| `-avpings <seconds>` | (Used with `-heave_drift`) Length (in seconds) of the tapered weighted average filter for heave drift estimation. | `160` |
| `-addtotide` | (Used with `-heave_drift`) Add heave drift to existing tide values. | |
| `-replacetide` | (Used with `-heave_drift`) Replace existing tide values with heave drift. | |
| `-ss_gradient <value>` | Apply a sound speed gradient correction. | `2.0` |
| `-sss_error <value>` | Apply a surface sound speed error correction. | `2.0` |
| `-dualhead` | Enable dual-head sonar processing for yaw misalignment. | |
| `-port_yaw_misalign <angle>` | Port yaw misalignment angle (degrees) for dual-head systems. Requires `-dualhead`. | `0.34` |
| `-stbd_yaw_misalign <angle>` | Starboard yaw misalignment angle (degrees) for dual-head systems. Requires `-dualhead`. | `0.34` |
| `-otf <otffilename>` | Load an OTF (Ocean Tide File?) file for processing. | |
| `-hack_current <value>` | Manually set a hack current value. | `0.1` |
| `-current <currentfilename>` | Load a current file for processing. | |
| `<datafile>` | **Required.** The input merged bathymetry file (e.g., `.merged`) or HDCS file. | `survey_data.merged` |