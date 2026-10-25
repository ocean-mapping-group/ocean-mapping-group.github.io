---
layout: default
title: ncCopernicusRead
parent: NetCDF & HDF5 Tools (netcdf)
nav_order: 2
tool_name: ncCopernicusRead
source_path: code/netcdf/ncCopernicusRead.c
category: Oceanographic & Acoustic NetCDF/HDF5 Readers
input_formats: [".nc (Copernicus, SSCOFS, WCOFS, GRTOFS, UBC Salish Sea NetCDF)"]
output_formats: [".r4", ".zvals", ".time", ".columns", ".2D_array", ".3D_array", ".4D_array", ".txt"]
related_tools: ["ncread", "hdf5EC150read", "jview", "mergeAtt"]
---

# ncCopernicusRead

## Overview

`ncCopernicusRead` (`code/netcdf/ncCopernicusRead.c`) is a versatile command-line NetCDF-C (`libnetcdf`) inspection, slicing, and raster conversion tool developed by John Hughes Clarke (2021–2025) for extracting 1D, 2D, 3D, and 4D oceanographic model fields into OMG binary `.r4` floating-point grids and ASCII tables.

Originally designed to slice 4D `(time, depth, lat, lon)` rectilinear grids from the **Copernicus Marine Service** (such as potential temperature `thetao`, salinity `so`, current velocities `uo`/`vo`, mixed layer depth, and sea surface height `zos`), `ncCopernicusRead` was progressively extended to handle unstructured triangular irregular network (TIN / FVCOM) and curvilinear operational ocean models including:
- **SSCOFS** (*Salish Sea Coastal Ocean Forecast System* — FVCOM unstructured node/layer grids, epoch `2018-01-01`).
- **WCOFS** (*West Coast Operational Forecast System* — ROMS curvilinear grids, epoch `2016-01-01`).
- **GRTOFS** (*Global Real-Time Ocean Forecast System* — HYCOM grids with `MT` / `Date` timestamps).
- **UBC Salish Sea** structured rectilinear models and 2D bathymetric/terrain NetCDF grids.

---

## Usage

```bash
# 1. Inspect dimensions and variables of a NetCDF file (omit -varid):
ncCopernicusRead -in <model.nc> -out <dummy_prefix>

# 2. Extract a horizontal depth slice (or all depths) from a 4D Copernicus grid:
ncCopernicusRead -varid thetao -depth_pick 300.0 [-date_label] -in <model.nc> -out <out_prefix>
ncCopernicusRead -varid thetao -all_depths -date_label -in <model.nc> -out <out_prefix>

# 3. Extract a vertical cross-section along a fixed latitude or longitude:
ncCopernicusRead -varid thetao -lat_pick 44.0 -date_label -in <model.nc> -out <out_prefix>
ncCopernicusRead -varid thetao -lon_pick 6.5 -date_label -in <model.nc> -out <out_prefix>

# 4. Extract unstructured/curvilinear model layers (SSCOFS, WCOFS, GRTOFS):
ncCopernicusRead -varid temp -isSSCOFS -dumpOne3D -chosenlayer 0 [-dumpr4] -in <sscofs.nc> -out <out_prefix>
```

---

## Command-Line Options

| Flag | Arguments | Description |
| :--- | :--- | :--- |
| `-in` | `<infile.nc>` | **Required.** Input NetCDF file path. |
| `-out` | `<outfile_prefix>` | **Required.** Output filename prefix. |
| `-varid` | `<varname>` | Target NetCDF variable name to extract (e.g., `thetao`, `so`, `zos`). If omitted, `ncCopernicusRead` prints all dimensions (`nc_inq_dim`) and variables (`nc_inq_var`) and exits cleanly. |
| `-depth_pick` | `<depth_m>` | Sets 4D slicing mode to `HORIZONTAL` (`3`) at the first model depth layer $\ge$ `<depth_m>` (`array[1][Depth_Index]`). |
| `-all_depths` | *(none)* | Sets 4D slicing mode to `HORIZONTAL` (`3`) and writes all depth layers sequentially into each time-step `.r4` file, accompanied by a `.zvals` depth-index table. |
| `-lat_pick` | `<lat_deg>` | Sets 4D slicing mode to `VERTICAL_LAT` (`2`), extracting a `(longitude × depth)` vertical section at the nearest latitude index `Lat_Index` (`array[2]`). |
| `-lon_pick` | `<lon_deg>` | Sets 4D slicing mode to `VERTICAL_LON` (`1`), extracting a `(latitude × depth)` vertical section at the nearest longitude index `Lon_Index` (`array[3]`). |
| `-date_label` | *(none)* | Formats output `.r4`, `.zvals`, and `.time` filenames using the decoded timestamp string `YYYY_jdDDD_HH-MM-SS_MMM-DD` (`time_string[kk]`) instead of sequential `.0000` indices. |
| `-dumpAll1D` | *(none)* | Dumps every 1D variable in the NetCDF file to an ASCII `<out>.<varname>` file containing `index value` pairs. |
| `-dumpSpecific1D` | `<var_index>` | Repeatable flag (up to 100 indices) that combines specified 1D variable IDs side-by-side into `<out>.columns` (passing `0` outputs the row index `j`). |
| `-dumpOne2D` | *(none)* | Dumps the 2D variable matching `-varid` to `<out>.2D_array` (as ASCII rows/columns, or as an `OMG1` binary raster if `-dumpr4` is also set). |
| `-dumpOne3D` | *(none)* | Dumps the 3D variable matching `-varid` to `<out>.3D_array` (or `<out>.LayerNode.r4` if `-dumpr4` is set, with `dx = nodes`, `dy = layers`). |
| `-dumpOne4D` | *(none)* | Dumps the 4D variable matching `-varid` at `-chosenlayer` to `<out>.4D_array` (as ASCII `lat lon val` for WCOFS/GRTOFS or as an `OMG1` `.r4` raster if `-dumpr4` is set). |
| `-dumpr4` | *(none)* | Switches `-dumpOne2D`, `-dumpOne3D`, or `-dumpOne4D` output from ASCII text to binary big-endian `OMG1` `.r4` floating-point grid format (`write_JHC_header` + `jswapfloat_fwrite`). |
| `-chosenlayer` | `<layer_idx>` | Required when `-isSSCOFS`, `-isWCOFS`, or `-isGRTOFS` is active; selects the vertical sigma/depth layer index `k` to extract. |
| `-isSSCOFS` | *(none)* | Applies Salish Sea (`SSCOFS`) epoch offset (`2018-01-01` via `stdtime_from_dmy(1,1,2018)`) and node coordinates (`array[5]` lat, `array[4]` lon). |
| `-isWCOFS` | *(none)* | Applies West Coast (`WCOFS`) epoch offset (`2016-01-01` via `stdtime_from_dmy(1,1,2016)`) and 2D curvilinear coordinates (`array[70]` lat, `array[69]` lon). |
| `-isGRTOFS` | *(none)* | Parses HYCOM `Date` (`YYYYMMDD`) and `MT` (days since `1900-12-31`) arrays into Unix 1970 epoch seconds and uses `array[5]`/`array[6]` for lat/lon. |

---

## Internal Processing Architecture & Output Files

1. **Metadata Discovery & 1D Coordinate Loading**:
   - Opens the NetCDF file via `nc_open(..., NC_NOWRITE, &ncid)`, queries total dimensions and variables (`nc_inq`), and loads all 1D coordinate arrays (`time`, `ocean_time`, `Date`, `depth`, `lat`, `lon`) into memory via `nc_get_var_float()`.
   - Converts model time variables into Unix 1970 timestamps (`time1970[j]`) and human-readable labels (`time_string[j]`, `tim2_string[j]`) via `stdtime_nicetime()`.
2. **2D & 3D Rectilinear Grid Export**:
   - For 2D terrain/map variables (`var_ndimsp[i] == 2`), writes `<out>.<varname>.r4` bottom-to-top (`for (idy = JHChead.dy - 1; idy >= 0; idy--)`).
   - For 3D `(time, lat, lon)` map series (e.g., sea surface height `zos`), writes per-timeframe `.r4` rasters (`<out>.<date>.<varid>.r4`), `.time` metadata files, and optional `.0000.txt` XYZ ASCII dumps (excluding `-32767` fill values).
3. **4D `(time, depth, lat, lon)` Sub-Slab Extraction (`nc_get_vara_float`)**:
   - Rather than allocating an entire 4D ocean model in RAM, lines 1168–1356 construct `size_t start[4]` and `size_t count[4]` hyperslab vectors according to `D4_Section` (`VERTICAL_LON`, `VERTICAL_LAT`, or `HORIZONTAL`) and call `nc_get_vara_float()` per time step `kk`.
   - Produces synchronized `<out>.<step>.<varid>.r4`, `<out>.<step>.<varid>.zvals`, and `<out>.<step>.<varid>.time` files ready for 3D curtain and layer inspection in [`jview`](../JV/jview.md).
