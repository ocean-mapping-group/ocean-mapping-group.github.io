---
layout: default
title: extractNodeProf
parent: Grid Tools
nav_order: 26
---
# extractNodeProf

## Description
`extractNodeProf` is a specialized data extraction utility designed to pull vertical profiles of oceanographic parameters from 3D model output, specifically the SalishSeaCast model. The tool identifies all model nodes that fall within a user-defined geographic area (a mapsheet) and, for each of those nodes, extracts the complete vertical profile (salinity, temperature, sound velocity, and U/V/W current components) for one or more model time steps.

This tool is essential for creating subsets of large-scale model data for regional analysis or for comparison with field observations.

## Usage
```bash
extractNodeProf -mapsheet <area.r4> -outprefix <prefix> -custom_Salish <lat.r4> <lon.r4> <mask> <bathy.r4> -param3D <model_time_file(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-mapsheet <area.r4>` | **Required.** A JHC grid file (e.g., `.r4` or `.8bit`) that defines the geographic boundaries of the area from which to extract node profiles. | `-mapsheet study_area.r4` |
| `-outprefix <prefix>` | **Required.** A prefix that will be used for all output files. | `-outprefix my_extraction` |
| `-custom_Salish <lat> <lon> <mask> <bathy>` | **Required.** Specifies the four critical geometry files that define the SalishSeaCast model grid: <br> 1. `lat.r4`: A grid of node latitudes. <br> 2. `lon.r4`: A grid of node longitudes. <br> 3. `mask.r4`: A grid defining valid water cells. <br> 4. `bathy.r4`: A grid of the model's bathymetry. | `-custom_Salish SalishSea_lat.r4 SalishSea_lon.r4 SalishSea_mask.r4 SalishSea_bathy.r4` |
| `-param3D <model_time_file(s)>` | **Required.** One or more `.time` files from the SalishSeaCast output. The tool uses the prefix and path of each `.time` file to locate the corresponding parameter files (e.g., `.salinity.r4`, `.temperature.r4`, etc.) for that specific time step. | `-param3D model/20241119/salishsea.t00z.temperature.time` |
| `-v` | Enable verbose output during processing. | |

## Output Files
For each input file specified with `-param3D`, the tool generates a set of three files, using the date string from the input file:

1.  **`<outprefix>.<datestr>.node`**: An ASCII file listing the geographic coordinates (`latitude longitude`) and grid index of every model node found within the mapsheet area.
2.  **`<outprefix>.<datestr>.curr`**: A JCU-format navigation file containing the **surface** current vectors (magnitude and azimuth) for each node. This file can be used for vector plotting.
3.  **`<outprefix>.<datestr>.prof`**: A detailed ASCII file containing the full vertical profile data for each node. For each node, it lists the data for every depth layer, including depth, salinity, temperature, sound speed, and the u, v, and w velocity components.
