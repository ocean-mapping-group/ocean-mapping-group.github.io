---
layout: default
title: modelMerge
parent: Ian Church (ianc) Tools
nav_order: 8
tool_name: modelMerge
source_path: code/ianc/modelMerge.c
category: Ocean Modeling & Hydrographic Utilities (ianc)
input_formats: ["OPeNDAP / NetCDF Ocean Models (NEGOFS, GOM HYCOM, NRL CONCORDE)", "OMG Binary Navigation (.nav)", "CARIS SVP (.svp)"]
output_formats: ["CARIS SVP v2 (.svp)", "CARIS Tide (.tid)", "ASCII Model Grid / Elements (.xyz)"]
related_tools: ["HycomSSP", "modelAnalysis", "iwc_model", "iwc_support", "iwc_water"]
---

# modelMerge

## Description

`modelMerge` connects directly to operational oceanographic forecast and hindcast servers over OPeNDAP/THREDDS to extract synthetic CARIS sound velocity profiles (`.svp`), tidal elevation files (`.tid`), and model grid/element geometries (`.xyz`) along a vessel's navigation track or across a specified time window. Created by Ian Church in February 2015 (and updated in January 2016 for CHC 2016 research on dynamic ocean model uncertainty), `modelMerge` unifies three distinct hydrodynamic model architectures under a single command-line interface:

1. **NOAA NEGOFS (`-NEGOFS`)**: Unstructured-grid FVCOM Northeast Coastal Ocean Forecast System hosted on NOAA CO-OPS OPeNDAP servers (`http://opendap.co-ops.nos.noaa.gov/thredds/dodsC/NOAA/NEGOFS/MODELS/...`).
2. **Gulf of Mexico HYCOM (`-GOM_HYCOM_2014`, `-GOM_HYCOM_2015`)**: Structured 1/25° (`0.04°`) hourly Gulf of Mexico HYCOM regional models (`http://tds.hycom.org/thredds/dodsC/GOMl0.04/expt_32.5/...`).
3. **NRL CONCORDE (`-GOM_NRL_CONCORDE`)**: Navy Research Laboratory (NRL) Gulf of Mexico CONCORDE model served via THREDDS (`MedusaThreddsData`).

Like `HycomSSP`, `modelMerge` can also ingest in-situ CARIS `.svp` casts (`-svp`) and apply only the temporal sound-speed anomalies predicted by the operational model onto the observed casts (`-outSVP`, `-svpDiff`).

## Usage

```bash
modelMerge (-NEGOFS | -GOM_HYCOM_2014 | -GOM_HYCOM_2015 | -GOM_NRL_CONCORDE) \
           [input_options] [dynamics_options] [output_options]
```

### Example Commands

Extract synthetic CARIS `.svp` and `.tid` files along an OMG binary `.nav` track from the 2015 Gulf of Mexico 1/25° HYCOM model:

```bash
modelMerge -GOM_HYCOM_2015 -in survey_track.nav \
           -outSVP gom_synthetic.svp -outTide gom_tide.tid -z0 0.25
```

Query NOAA NEGOFS over a fixed time window and location, sampling every 30 seconds:

```bash
modelMerge -NEGOFS -start 2015 02 27 12:00:00 -end 2015 02 27 16:00:00 \
           -samp 30 -lat 44.852 -lon -66.951 -outSVP negofs.svp -outTide negofs.tid
```

Export the NEGOFS unstructured triangular mesh elements or node depths to an ASCII file:

```bash
modelMerge -NEGOFS -in survey_track.nav -depthOut negofs_grid.xyz -ele
```

## CLI Arguments and Options

Exactly one model selection flag must be provided (`modelFlag == 1`).

| Flag / Argument | Parameters | Description |
| :--- | :--- | :--- |
| `-NEGOFS` | None | Selects the NOAA NEGOFS (FVCOM unstructured grid) operational model via OPeNDAP. |
| `-GOM_HYCOM_2014` | None | Selects the 2014 hourly 1/25° Gulf of Mexico HYCOM dataset (`GOMl0.04/expt_32.5/2014/hrly`). Valid for dates after April 1, 2014. |
| `-GOM_HYCOM_2015` | None | Selects the 2015 hourly 1/25° Gulf of Mexico HYCOM dataset (`GOMl0.04/expt_32.5/2015/hrly`). |
| `-GOM_NRL_CONCORDE` | None | Selects the NRL CONCORDE Gulf of Mexico model via Medusa THREDDS (`nco_rel_concorde_*`). |
| `-in` | `<infile.nav>` | Input Option 2: Reads vessel track coordinates `(lat, lon)` and timestamps from an OMG binary `.nav` file. |
| `-start` | `<YYYY> <MM> <DD> <HH:MM:SS>` | Input Option 1: Start UTC date and time for fixed-location extraction. |
| `-end` | `<YYYY> <MM> <DD> <HH:MM:SS>` | Input Option 1: End UTC date and time for fixed-location extraction. |
| `-samp` | `<seconds>` | Sampling interval in seconds when generating query timestamps from `-start`/`-end` or `-svp` (default: `10`). |
| `-lat` | `<degrees>` | Latitude in decimal degrees for fixed-location extraction or fallback for `.svp` files without coordinates. |
| `-lon` | `<degrees>` | Longitude in decimal degrees (automatically shifted by `+360` for `NEGOFS` and `GOM_NRL_CONCORDE` when negative). |
| `-svp` | `<svp_file1> [...]` | Loads observed CARIS `.svp` casts and adds the temporal model sound-speed change `(SSP_model(t) - SSP_model(t0))` to the observed baseline profile. |
| `-svpDiff` | `<error.file>` | Outputs the difference between the evolving model sound speed and the baseline cast (`[SVP_VERSION_2]` format). |
| `-depthOut` | `<file.xyz>` | Outputs the model grid coordinates and variables (`lat,lon,depth` for NEGOFS; `lat,lon,ssh,sal,temp` for GOM HYCOM; `lat,lon` for NRL CONCORDE). |
| `-ele` | None | Modifies `-depthOut` (for `-NEGOFS`) to output triangular mesh element connectivity (`nv`) formatted as an OMG contour file. |
| `-tstep` | None | Outputs model grid data at every model time step to numbered `<depthOut>` files (omit file extension on `-depthOut`). |
| `-outSVP` | `<outfile.svp>` | Writes the extracted or dynamically updated sound speed profiles to a CARIS `[SVP_VERSION_2]` file. |
| `-outTide` | `<outfile.tid>` | Writes the extracted sea surface height / tidal elevation time series to a CARIS `.tid` file. |
| `-z0` | `<meters>` | Applies a constant vertical datum offset (in meters) to all tidal elevations written to `-outTide` (default: `0.0`). |

## File Formats

### Input Formats
* **OPeNDAP / NetCDF Streams**:
  * **GOM HYCOM**: Dimensions `Depth`, `Latitude`, `Longitude`, `MT`; variables `temperature`, `salinity`, `ssh`.
  * **NEGOFS**: Dynamically constructs hourly NetCDF URLs (`.../YYYYMM/nos.negofs.fields.n00X.YYYYMMDD.tHHz.nc`) with dimensions `node`, `nele`, `siglay`, `siglev`, `time` and variables `lat`, `lon`, `h`, `zeta`, `temp`, `salinity`, `nv`, `siglay`, `siglev`.
  * **NRL CONCORDE**: Dynamically constructs 3-hourly NetCDF URLs (`nco_rel_concorde_YYYYMMDD00_t0XX.nc`) with dimensions `depth`, `lat`, `lon`, `time` and variables `water_temp`, `salinity`, `sound_speed`, `surf_el` (scaled by `scale_factor` and `add_offset`).
* **OMG Binary Navigation (`.nav`)** and **CARIS SVP (`.svp`)**.

### Output Formats
* **CARIS SVP v2 (`.svp`)**: Multi-section `[SVP_VERSION_2]` file containing `<depth> <sound_speed>` pairs whenever the water-column profile changes (`isDiffFlag`).
* **CARIS Tide (`.tid`)**: Header `--------` followed by `YYYY/MM/DD HH:MM:SS <tide_m>` records.
* **Model Grid ASCII (`.xyz`)**: CSV/space-delimited node coordinates or element polygons (`-ele`).

## How It Works

1. **Trajectory / Time-Series Initialization**: `modelMerge` populates `navLat`, `navLon`, and `navTime` from `-in <navfile>`, `-start`/`-end` at `-samp` intervals, or the time span between the first and last `-svp` casts.
2. **Model-Specific OPeNDAP Fetching & Temporal Interpolation**:
   * **GOM HYCOM**: Converts each query timestamp into hours since the model epoch (`2014-04-01` or `2015-01-01`), brackets the timestamp between `GOMHour1` and `GOMHour2`, finds the closest grid node (`closeDist()`), fetches vertical slices of `temperature`, `salinity`, and `ssh` via `nc_get_vara_float()`, and performs inverse-time-difference weighted interpolation between the two bracketing hours.
   * **NEGOFS & NRL CONCORDE**: Computes the forecast cycle date and hour (`nItNum`, `nTail`) bracketing each query timestamp, opens the two consecutive remote NetCDF files (`ncid`, `ncid2`), locates the nearest wet node, and interpolates temperature, salinity, and sea surface height across the two time steps.
3. **Sound Speed Computation & Dynamic SVP Updating**: At each depth/sigma layer, pressure is computed via `depth2press()` and sound speed is evaluated using `ChenMillero()`. When `-svp` is enabled, the model's sound speed change relative to the time of the most recent in-situ SVP cast is added to the observed cast profile and written to `-outSVP` and `-svpDiff`.
