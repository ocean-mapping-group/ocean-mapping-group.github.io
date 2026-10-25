---
layout: default
title: readADCP_g
parent: Teledyne RDI ADCP Processing (adcp)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 11
tool_name: readADCP_g
source_path: code/adcp/readADCP_g.c
category: adcp
input_formats:
- RDI ASCII ADCP
- jcu_nav (.nav)
- OMG Map (.map)
output_formats:
- JHC 8-bit Profile (.prof / .stack_prof / .map_prof)
- jcu_nav Depth-Averaged Vectors (.nav)
related_tools:
- readADCP
- readADCP_mod
- combineMultiADCP
---

# readADCP_g

## Description
`readADCP_g` is a utility for reading and processing RDI ASCII ADCP (Acoustic Doppler Current Profiler) files. It is a streamlined variant of [`readADCP`](readADCP.html) that converts raw RDI ASCII ADCP ensembles into time-series profile images (`<outfile>.prof`), georeferenced mapsheet curtains (`<outfile>.map_prof`), and depth-averaged current vector files (`<outfile>.nav`), with direct support for `-phase_zero` tidal phase referencing and `-ref_bottom` height-above-bottom binning.

## Usage

```bash
readADCP_g -in <infiles> -out <outfile> [OPTIONS]
```

## Key Options

| Option | Description |
|---|---|
| `-in <infilename(s)>` | **Required.** One or more input RDI ASCII ADCP files. |
| `-out <outfile>` | **Required.** The prefix for the output filenames. |
| `-nav <navfile>` | Use an external `jcu_nav` navigation file for positioning. |
| `-use_adcp_nav` | Use the navigation data embedded within the ADCP files. |
| `-map <mapfile.map>` | Georeference and stack the output profiles onto a map grid. |
| `-pixel <size>`| Horizontal pixel size for the output map when `-map` is used. |
| `-mindepth <m>` / `-maxdepth <m>` | Minimum and maximum depth range to process. |
| `-ref_bottom` | Reference depth layers relative to the seafloor instead of the sea surface. |
| `-layers <num>` | Set the number of vertical bins in the output profile (default `100`). |
| `-draft <m>` | Specify the draft of the ADCP transducer to correct depth values. |
| `-showMAG` | **(Default)** Display velocity magnitude in the output profile. |
| `-showBS` | Display backscatter intensity (use with `-BSrange`). |
| `-showAZI` | Display velocity direction (azimuth). |
| `-maxcurrent <m/s>`| Maximum current for scaling magnitude output image colors. |
| `-BSrange <min> <max>`| Min/max backscatter values for color scaling. |
| `-ensem_stack <num>` | Average (stack) data over a specified number of ensembles. |
| `-stack_in_map` | Average profiles falling within the same map column when `-map` is used. |
| `-headbias <deg>` | Apply a constant heading correction in degrees. |
| `-delay <sec>` | Apply a time delay in seconds to external navigation. |
| `-tidefile <tide.nav>`| Use an external `jcu_nav` file to provide tidal height corrections. |
| `-phase_zero <Y J H M>`| Define the reference start time for M2 tidal phase calculations. |
| `-v` | Enable verbose output. |
