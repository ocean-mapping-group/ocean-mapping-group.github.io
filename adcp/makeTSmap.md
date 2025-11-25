---
layout: default
title: makeTSmap
parent: ADCP Tools
nav_order: 7
---

# makeTSmap

## Description
`makeTSmap` is a command-line utility designed to generate time-varying temperature and salinity profile maps that are synchronized with an ADCP (Acoustic Doppler Current Profiler) time-series dataset. The tool reads a series of individual temperature and salinity (TS) profiles from ASCII files, each associated with a specific time. It then interpolates this data in both the time and depth domains to create continuous temperature and salinity profiles that correspond to the timestamps of an existing ADCP data stack.

This is particularly useful for preparing environmental data needed for acoustic data processing or for visualizing the evolution of water column properties over time.

## Usage
```bash
makeTSmap [OPTIONS] -guide <prefix> -out <outfilenameprefix> -in <infilename(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-guide <prefix>` | **Required.** Specifies the prefix for the "guide" files, which define the structure of the output. The tool expects two files: `<prefix>.stack_prof` (a JHC file defining the output grid dimensions) and `<prefix>.stack_ASCII` (an ASCII file with timestamps for each trace). | `-guide adcp_data` |
| `-out <outfilenameprefix>` | **Required.** Specifies the prefix for the output profile map files. Two files will be generated: `<outfilenameprefix>.Tprof` (for temperature) and `<outfilenameprefix>.Sprof` (for salinity). | `-out ts_map` |
| `-in <infilename(s)>` | **Required.** One or more input ASCII files, each containing a single TS profile. The file format should start with a header line `YYYY JJJ HH MM` followed by lines of `depth salinity temperature`. | `-in ctd1.txt ctd2.txt` |

## How It Works

1.  **Load Guide Files:** The tool first reads the `.stack_prof` file to get the dimensions (number of time steps and depth bins) and depth range of the target ADCP data stack from its JHC header. It also reads the `.stack_ASCII` file to get the exact timestamp for each time step (trace).
2.  **Load TS Profiles:** It then reads all specified input ASCII files (`-in`). Each file represents a single CTD cast or TS profile at a given time. The tool parses the timestamp and the depth, salinity, and temperature values from each file.
3.  **Depth Interpolation:** For each loaded TS profile, the tool interpolates the temperature and salinity values onto the vertical grid defined by the `.stack_prof` header. This creates a uniformly sampled vertical profile for each input cast.
4.  **Time Interpolation:** The tool iterates through each time step of the target ADCP data (defined by the timestamps in `.stack_ASCII`). For each target timestamp, it finds the two nearest input TS profiles (one before and one after).
5.  **Linear Interpolation and Output:** It performs a linear interpolation between these two profiles to calculate the temperature and salinity profile at the target timestamp. This interpolated profile (or "trace") is then written to the output `.Tprof` and `.Sprof` files.
6.  **File Generation:** This process is repeated for all timestamps, resulting in two JHC-formatted files (`.Tprof` and `.Sprof`) that represent the complete, time-varying temperature and salinity maps synchronized with the ADCP data.

## Input File Format

The input ASCII files for the `-in` argument must follow this format:
*   **Header Line:** `YYYY JJJ HH MM` (Year, Julian Day, Hour, Minute)
*   **Data Lines:** `depth salinity temperature` (space-separated floating-point values)

**Example:**
```
2001 254 14 30
0.5 31.5 12.3
1.0 31.5 12.2
2.0 31.6 12.0
...
```