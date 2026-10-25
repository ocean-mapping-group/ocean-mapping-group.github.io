---
layout: default
title: makeTSmap
parent: ADCP Tools
nav_order: 7
tool_name: makeTSmap
source_path: code/adcp/makeTSmap.c
category: adcp
input_formats:
  - JHC Stacked Profile (.stack_prof)
  - ASCII Stack Timestamps (.stack_ASCII)
  - ASCII CTD Profiles
output_formats:
  - JHC Temperature Profile Map (.Tprof)
  - JHC Salinity Profile Map (.Sprof)
related_tools:
  - readADCP
---

# makeTSmap

## Description
`makeTSmap` is a command-line utility designed to generate time-varying temperature and salinity profile maps that are synchronized with an ADCP (Acoustic Doppler Current Profiler) time-series dataset. The tool reads a series of individual temperature and salinity (TS) profiles from ASCII CTD files, each associated with a specific timestamp, and interpolates them in both depth and time onto the grid of an existing ADCP ensemble stack (`<prefix>.stack_prof` and `<prefix>.stack_ASCII` produced by [`readADCP`](readADCP.md) `-ensem_stack`).

## Usage
```bash
makeTSmap [OPTIONS] -guide <prefix> -out <outfilenameprefix> -in <infilename(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-guide <prefix>` | **Required.** Prefix for the guide files defining the target output grid (`<prefix>.stack_prof` and `<prefix>.stack_ASCII`). | `-guide adcp_data` |
| `-out <outfilenameprefix>` | **Required.** Prefix for the output JHC profile map files (`<outfilenameprefix>.Tprof` and `<outfilenameprefix>.Sprof`). | `-out ts_map` |
| `-in <infilename(s)>` | **Required.** One or more input ASCII CTD profile files (`YYYY JJJ HH MM` header followed by `depth salinity temperature` lines). | `-in ctd1.txt ctd2.txt` |

## How It Works

1.  **Load Guide Files:** Reads `<prefix>.stack_prof` to obtain the number of time steps (`dx`), depth bins (`dy`), and depth range from its JHC header, and reads `<prefix>.stack_ASCII` to obtain the timestamp of each stacked ensemble.
2.  **Load TS Profiles:** Reads all input ASCII CTD files (`-in`), parsing the cast timestamp (`YYYY JJJ HH MM`) and vertical `depth salinity temperature` triplets.
3.  **Depth Interpolation:** Interpolates each CTD cast onto the vertical depth bins defined by `.stack_prof`.
4.  **Time Interpolation & Output:** For each ensemble timestamp in `.stack_ASCII`, linearly interpolates between the bracketing CTD casts and writes the resulting vertical profiles to `<outfilenameprefix>.Tprof` (temperature) and `<outfilenameprefix>.Sprof` (salinity).

## Input File Format

```text
2001 254 14 30
0.5 31.5 12.3
1.0 31.5 12.2
2.0 31.6 12.0
```
