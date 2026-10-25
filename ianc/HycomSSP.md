---
layout: default
title: HycomSSP
parent: Ian Church (ianc) Tools
nav_order: 2
tool_name: HycomSSP
source_path: code/ianc/HycomSSP.c
category: Ocean Modeling & Hydrographic Utilities (ianc)
input_formats: ["OPeNDAP / NetCDF HYCOM Grid", "OMG Binary Navigation (.nav)", "CARIS SVP (.svp)"]
output_formats: ["CARIS SVP v2 (.svp)", "CARIS Tide (.tid)", "OMG Binary Navigation (.nav)", "Ocean Data View (.txt)", "CSV Surface Velocity (.txt)"]
related_tools: ["modelMerge", "modelAnalysis", "oceanReader", "iwc_support", "iwc_water"]
---

# HycomSSP

## Description

`HycomSSP` extracts synthetic sound velocity profiles (SVPs), tidal / sea-surface height (SSH) time series, and surface current magnitudes from operational HYCOM (Hybrid Coordinate Ocean Model) NetCDF/OPeNDAP servers (such as `GLBv0.08`). Written by Ian Church in March 2018, the tool queries remote or local 4D NetCDF datasets (`time`, `depth`, `lat`, `lon`) along a vessel navigation track (`.nav`), a synthetic time window at a fixed coordinate (`-start`/`-end`/`-lat`/`-lon`), or the spatiotemporal span of observed CARIS `.svp` casts.

Using the Chen-Millero sound speed equation (`ChenMillero()` from `soundspeed.h`) and depth-to-pressure conversion (`depth2press()`), `HycomSSP` computes full water-column sound speed profiles from HYCOM `water_temp` and `salinity` fields. It also supports hybrid model-observation assimilation (`-svp`), where temporal ocean dynamics from the HYCOM model relative to a baseline cast time are superimposed onto an observed in-situ SVP cast to produce dynamically updated CARIS V2 `.svp` files.

## Usage

```bash
HycomSSP -modelPath <opendap_url_or_nc> [input_options] [model_dynamics_options] [output_options]
```

### Example Commands

Extract synthetic CARIS `.svp` and `.tid` files along an OMG binary navigation track from a HYCOM OPeNDAP endpoint, searching nearby wet nodes if a coastal node is dry:

```bash
HycomSSP -modelPath http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_57.7 \
         -use_nearest -in survey_track.nav \
         -outSVP hycom_track.svp -outTide hycom_tide.tid -z0 0.35
```

Extract profiles at a fixed mooring location over a time range at 60-second intervals and export to Ocean Data View (ODV) format:

```bash
HycomSSP -modelPath http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_57.7 \
         -start 2015 02 27 12:00:00 -end 2015 02 27 18:00:00 -samp 60 \
         -lat 30.456 -lon -89.247 -odv mooring_odv.txt -outVel max_vel.txt
```

Apply HYCOM temporal sound-speed anomalies to observed CARIS SVP casts and record the profile differences:

```bash
HycomSSP -modelPath http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_57.7 \
         -in survey_track.nav -svp cast01.svp cast02.svp \
         -outSVP dynamic_casts.svp -svpDiff model_obs_diff.svp
```

## CLI Arguments and Options

| Flag / Argument | Parameters | Description |
| :--- | :--- | :--- |
| `-modelPath` | `<url_or_path>` | NetCDF file path or OPeNDAP URL for the HYCOM dataset (e.g., `http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_57.7`). |
| `-in` | `<infile.nav>` | Input Option 1: Read timestamps and `(lat, lon)` coordinates from an OMG binary navigation file. |
| `-start` | `<YYYY> <MM> <DD> <HH:MM:SS>` | Input Option 2: Start UTC date and time for fixed-point time-series extraction. |
| `-end` | `<YYYY> <MM> <DD> <HH:MM:SS>` | Input Option 2: End UTC date and time for fixed-point time-series extraction. |
| `-samp` | `<seconds>` | Sampling interval in seconds when generating synthetic time steps from `-start`/`-end` or `-svp` (default: `10`). |
| `-lat` | `<degrees>` | Input latitude in decimal degrees for fixed-point extraction or fallback when `-svp` files lack coordinates. |
| `-lon` | `<degrees>` | Input longitude in decimal degrees (automatically converted to `0`–`360` east longitude if negative). |
| `-use_nearest` | None | If the closest HYCOM grid node returns fill values (`-30000`) for temperature, salinity, or SSH, iteratively searches up to the 100th closest node (`closeXFloat()`) to find valid wet water-column data. |
| `-old` | None | Sets legacy model flag (`oldFlag`). |
| `-svp` | `<svp_file1> [...]` | Loads one or more observed CARIS `.svp` files via `load_watercolumns()` and applies only the temporal model delta `(SSP_model(t) - SSP_model(t0))` onto the observed baseline cast `SSP_obs(t0)`. |
| `-svpDiff` | `<error.file>` | Writes a CARIS `[SVP_VERSION_2]` file containing the sound speed difference `SSP_model(t) - SSP_obs(t0)` at each model depth. Requires `-svp`. |
| `-outSVP` | `<outfile.svp>` | Outputs synthetic or dynamically adjusted sound velocity profiles in CARIS `[SVP_VERSION_2]` format. |
| `-outTide` | `<outfile.tid>` | Outputs sea-surface elevation (`surf_el * 0.001 + z0`) in CARIS tide format (`YYYY/MM/DD HH:MM:SS <tide>`). |
| `-z0` | `<meters>` | Vertical datum shift in meters added to the HYCOM sea surface height when writing `-outTide` (default: `0.0`). |
| `-outSSH` | `<outfile.nav>` | Writes an OMG binary `.nav` file where each record's `azi` field stores the HYCOM sea-surface height (`surf_el * 0.001` meters). |
| `-outVel` | `<outfile.txt>` | Appends the location and maximum surface current speed (`sqrt(u^2 + v^2) * 0.001` m/s at depth index `0`) as CSV (`lat,lon,maxVel`) to `<outfile.txt>`. |
| `-odv` | `<output.txt>` | Writes extracted depth profiles of temperature, salinity, and sound speed in tab-delimited Ocean Data View (ODV) spreadsheet format. |

## File Formats

### Input Formats
* **HYCOM NetCDF / OPeNDAP Dataset**: Must contain dimensions `depth`, `lat`, `lon`, and `time` (in hours since `2000-01-01 00:00:00`), and variables `depth`, `lat`, `lon`, `time`, `water_temp`, `salinity`, `surf_el`, `water_u`, and `water_v`. Packed integer/short values use scale factor `0.001` with `+20` offset for `water_temp` and `salinity`, `0.001` for `surf_el`, `water_u`, and `water_v`, and `-30000` as the missing/dry fill value.
* **OMG Binary Navigation (`.nav`)**: Read via `nav_read()` to supply query timestamps and track coordinates.
* **CARIS SVP (`.svp`)**: Read via `load_watercolumns()` (`j_watercolumn.h`) and sorted chronologically with `qsort(..., watercolumn_compare)`.

### Output Formats
* **CARIS SVP Version 2 (`-outSVP`, `-svpDiff`)**: ASCII file starting with `[SVP_VERSION_2]` and filename header, followed by `Section YYYY-DDD HH:MM:SS DD:MM:SS DD:MM:SS` headers and tab-separated `<depth> <sound_speed>` pairs filtered to `[1400, 1600]` m/s.
* **CARIS Tide (`-outTide`)**: ASCII file beginning with `--------` followed by `YYYY/MM/DD HH:MM:SS <elevation_m>` lines.
* **Ocean Data View (`-odv`)**: Tab-separated spreadsheet with columns `Cruise`, `Station`, `mon/day/yr`, `hh:mm`, `Longitude [degrees_east]`, `Latitude [degrees_north]`, `Bot. Depth [m]`, `DEPTH [m]`, `QF`, `TEMPERATURE [°C]`, `QF`, `SALINITY [PSS-78]`, `QF`, `SOUNDSPEED [m/s]`, `QF`.

## How It Works

1. **Spatiotemporal Query Construction**: `HycomSSP` builds three parallel arrays (`navLat`, `navLon`, `navTime`) from either the input `.nav` file, the `-start`/`-end` window divided by `-samp`, or the time span between the first and last input `-svp` casts. Negative longitudes are normalized to `[0, 360]`.
2. **Resilient NetCDF / OPeNDAP Connection**: The program opens `-modelPath` with `nc_open()` and queries dimension lengths and variable IDs. Because remote OPeNDAP requests can drop over long runs, any NetCDF read failure increments `errorCount` and jumps to `startRead:` to re-establish the connection (up to 1,000 retries).
3. **Grid Indexing and Nearest-Wet-Node Search**: For each query timestamp, UTC epoch seconds are converted into hours since `2000-01-01 00:00:00` (`GOMHour1`). Whenever the model hour advances, `closeFloat()` locates the nearest `time`, `lat`, and `lon` indices. If `-use_nearest` is enabled and the nearest grid cell contains `-30000` (land/missing), `closeXFloat()` steps outward through the `j`-th closest indices (`j = 0..99`) until valid water-column data are found.
4. **Thermodynamic Sound Speed & Model-Dynamics Blending**: At each valid depth layer `j`, temperature and salinity are unpacked (`val * 0.001 + 20`), pressure is computed via `depth2press(DepthGOM[j], LatGOM[indexLat])`, and sound speed is evaluated with `ChenMillero()`. If `-svp` is active, the first query after each cast's timestamp records the baseline observed profile `wSSPGOMProfBase` (via `closeValue()`) and baseline model profile `wSSPGOMModelBase`; subsequent time steps output `wSSPGOMProfBase[j] + (wSSPGOMProf[j] - wSSPGOMModelBase[j])`.
