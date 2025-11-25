---
layout: default
title: readADCP_mod
parent: ADCP Tools
nav_order: 12
---

# readADCP_mod

## Description
`readADCP_mod` is a utility for reading and processing RDI ASCII ADCP (Acoustic Doppler Current Profiler) files. It serves a similar purpose to `readADCP` and `readADCP_g`, converting raw ADCP data into a time-series profile saved as a JHC-formatted image file (`.prof`).

This version allows for the visualization of velocity magnitude, azimuth, or backscatter. It supports georeferencing via an external navigation file and can stack (average) data over a set number of ensembles or within geographic bins on a map. The `_mod` suffix suggests it is a modified version, likely with a feature set that is a subset of the main `readADCP` tool.

## Usage
```bash
readADCP_mod -in <infiles> -out <outfile> [OPTIONS]
```

## Key Options

| Option | Description |
|---|---|
| `-in <infilename(s)>` | **Required.** One or more input RDI ASCII ADCP files. |
| `-out <outfile>` | **Required.** The prefix for the output filenames. |
| `-nav <navfile>` | Use an external OMG-HDCS navigation file for positioning. |
| `-use_adcp_nav` | Use the navigation data embedded within the ADCP files. |
| `-map <mapfile.map>` | Georeference and stack the output profiles onto a map grid. |
| `-pixel <size>`| The horizontal pixel size for the output map, if `-map` is used. |
| `-mindepth <m>` / `-maxdepth <m>` | Set the minimum and maximum depth range to process. |
| `-bottom_ref` | Reference depth layers relative to the seafloor instead of the sea surface. |
| `-layers <num>` | Set the number of vertical bins in the output profile. Default is 100. |
| `-draft <m>` | Specify the draft of the ADCP transducer to correct the depth values. |
| `-showMAG` | **(Default)** Display velocity magnitude in the output profile. |
| `-showBS` | Display backscatter intensity. Use with `-BSrange`. |
| `-showAZI` | Display velocity direction (azimuth). |
| `-maxcurrent <m/s>`| Set the maximum current for scaling the output image colors (for magnitude display). |
| `-BSrange <min> <max>`| Set the min/max backscatter values for color scaling. |
| `-ensem_stack <num>` | Average (stack) data over a specified number of ensembles. |
| `-stack_in_map` | When using `-map`, creates a single, averaged profile for all data falling within the map area. |
| `-headbias <deg>` | Apply a constant heading correction in degrees. |
| `-delay <sec>` | Apply a time delay in seconds to the data. |
| `-tidefile <tide.nav>`| Use an external navigation file to provide tidal height corrections. |
| `-phase_zero <Y J H M>`| Defines the reference start time for tidal phase calculations. |
| `-v` | Enable verbose output. |
| `-min_vels_to_av <num>` | Minimum number of depth-averaged velocities required to write an output nav record. |

## How It Works

1.  **Read Data:** The tool reads ADCP data from the specified input files.
2.  **Georeferencing:** It uses either an external (`-nav`) or internal (`-use_adcp_nav`) source for geographic positioning.
3.  **Data Extraction:** It processes each ADCP ensemble and extracts the user-selected data type (Magnitude, Azimuth, or Backscatter) for each depth bin.
4.  **Profile Generation:** The vertical data for each ensemble is binned into a profile. The depth axis can be referenced to the sea surface or the seafloor (`-bottom_ref`).
5.  **Output:** The generated profile is written as a column to the output `.prof` image file, creating a time-series visualization.
6.  **Stacking/Mapping:** If the `-ensem_stack` or `-map` options are used, the tool performs averaging either over time or space before writing the final output.