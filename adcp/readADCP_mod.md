---
layout: default
title: readADCP_mod
parent: Teledyne RDI ADCP Processing (adcp)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 12
tool_name: readADCP_mod
source_path: code/adcp/readADCP_mod.c
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
- readADCP_g
- combineMultiADCP
---

# readADCP_mod

## Description
`readADCP_mod` is a modified variant of [`readADCP`](readADCP.html) and [`readADCP_g`](readADCP_g.html) for reading and processing RDI ASCII ADCP (Acoustic Doppler Current Profiler) files into 8-bit JHC vertical profile images (`.prof`), mapsheet sections (`.map_prof`), and depth-averaged `jcu_nav` current vector files (`.nav`). It introduces the `-min_vels_to_av` threshold to ensure depth-averaged current records are only written when a minimum number of valid vertical bins are present in the ensemble.

## Usage

```bash
readADCP_mod -in <infiles> -out <outfile> [OPTIONS]
```

## Key Options

| Option | Description |
|---|---|
| `-in <infilename(s)>` | **Required.** One or more input RDI ASCII ADCP files. |
| `-out <outfile>` | **Required.** Prefix for the output filenames. |
| `-nav <navfile>` | Use an external `jcu_nav` navigation file for positioning. |
| `-use_adcp_nav` | Use the navigation data embedded within the ADCP files. |
| `-map <mapfile.map>` | Georeference and stack the output profiles onto a map grid. |
| `-pixel <size>`| Horizontal pixel size for the output map, if `-map` is used. |
| `-mindepth <m>` / `-maxdepth <m>` | Set the minimum and maximum depth range to process. |
| `-bottom_ref` | Reference depth layers relative to the seafloor instead of the sea surface. |
| `-layers <num>` | Set the number of vertical bins in the output profile (default `100`). |
| `-draft <m>` | Specify the draft of the ADCP transducer to correct the depth values. |
| `-showMAG` | **(Default)** Display velocity magnitude in the output profile. |
| `-showBS` | Display backscatter intensity (use with `-BSrange`). |
| `-showAZI` | Display velocity direction (azimuth). |
| `-maxcurrent <m/s>`| Set the maximum current for scaling the output image colors. |
| `-BSrange <min> <max>`| Set the min/max backscatter values for color scaling. |
| `-ensem_stack <num>` | Average (stack) data over a specified number of ensembles. |
| `-stack_in_map` | Average all ensembles falling into the same map bin when `-map` is used. |
| `-headbias <deg>` | Apply a constant heading correction in degrees. |
| `-delay <sec>` | Apply a time delay in seconds to external navigation. |
| `-tidefile <tide.nav>`| Use an external `jcu_nav` file to provide tidal height corrections. |
| `-phase_zero <Y J H M>`| Define the reference start time for M2 tidal phase calculations. |
| `-min_vels_to_av <num>` | Minimum number of valid vertical velocity bins required to output a depth-averaged `.nav` record. |
| `-v` | Enable verbose output. |
