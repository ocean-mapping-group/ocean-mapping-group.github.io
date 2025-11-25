---
layout: default
title: readADCP_g
parent: ADCP Tools
nav_order: 11
---

# readADCP_g

## Description
`readADCP_g` is a utility for reading and processing RDI ASCII ADCP (Acoustic Doppler Current Profiler) files. It is a slightly simplified or earlier version of the more comprehensive `readADCP` tool. Its primary function is to convert raw ADCP data into a time-series profile, which is saved as a JHC-formatted image file.

The tool can visualize velocity magnitude, azimuth, or backscatter. It supports georeferencing via an external navigation file and can stack (average) data over a set number of ensembles or within geographic bins on a map.

## Usage
```bash
readADCP_g -in <infiles> -out <outfile> [OPTIONS]
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
| `-ref_bottom` | Reference depth layers relative to the seafloor instead of the sea surface. |
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

## How It Works

1.  **Read Data:** The tool reads ADCP data from the specified input files.
2.  **Georeferencing:** If a `-nav` file is provided, it interpolates the navigation data to get a position for each ADCP ensemble. If `-use_adcp_nav` is specified, it uses the GPS data from within the ADCP file.
3.  **Data Extraction:** For each ensemble, it extracts the selected data type (Magnitude, Azimuth, or Backscatter) for each depth bin.
4.  **Profile Generation:** The vertical data for each ensemble is binned into a profile according to the `-layers` and depth range settings. This profile becomes one column in the output time-series image.
5.  **Output:** The generated profile is written to the output file (`<outfile>.prof`). The process is repeated for every ensemble, building the image column by column.
6.  **Stacking/Mapping:** If `-ensem_stack` or `-map` options are used, the tool performs averaging either over time or space before writing the final output.

This tool provides a "lite" version of the functionality found in `readADCP`, focusing on the core task of creating profile images from raw ADCP files.