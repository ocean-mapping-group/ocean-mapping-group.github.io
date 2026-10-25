---
layout: default
title: ncEC150read
parent: NetCDF & HDF5 Ocean/Sonar Readers (netcdf)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 3
tool_name: ncEC150read
source_path: code/netcdf/ncEC150read.c
category: Oceanographic & Acoustic NetCDF/HDF5 Readers
input_formats:
- .nc (Kongsberg Simrad EC150-3C SONAR-netCDF4)
output_formats:
- <infile>.nav
- <outfile> (OMG1 .r4 header)
related_tools:
- hdf5EC150read
- ncread
- ncCopernicusRead
---

# ncEC150read

## Overview

`ncEC150read` (`code/netcdf/ncEC150read.c`) is an exploratory NetCDF-4 (`libnetcdf`) reader written by John Hughes Clarke aboard *USNS Heezen* in March 2023 to inspect the hierarchical group structure of **Kongsberg Simrad EC150-3C** ADCP / echosounder `.nc` (ICES SONAR-netCDF4 convention) files and extract vessel platform navigation into OMG `.nav` files.

As documented in the source header comment (`code/netcdf/ncEC150read.c`, lines 6–9), `ncEC150read` was the initial `libnetcdf`-based prototype before development switched to [`hdf5EC150read`](hdf5EC150read.html) (`libhdf5`) due to `libnetcdf` limitations when reading deeply nested variable-length (`NC_VLEN`) user-defined per-ping velocity and backscatter records. However, `ncEC150read` remains a valuable diagnostic tool because it recursively traverses and prints 3 levels of NetCDF-4 groups (`CORE` $\rightarrow$ `GROUP` $\rightarrow$ `SUBGROUP` $\rightarrow$ `SUBSUBGROUP`), reports NetCDF user/VLEN type definitions (`nc_inq_type`, `nc_inq_vlen`), and extracts 1D platform trajectory arrays (`latitude`, `longitude`, `roll`, `pitch`, `heading`) from the `/Platform` group into `<infile>.nav`.

---

## Usage

```bash
ncEC150read [-varid <variable_name>] -in <file1.nc> [file2.nc ...] -out <outfile>
```

### Command-Line Options

| Flag | Arguments | Description |
| :--- | :--- | :--- |
| `-in` | `<file1.nc> [file2.nc ...]` | **Required.** One or more input Kongsberg EC150 `.nc` files (up to `MAXNOFILES = 10000`). Reads consecutive file arguments until the next `-` option flag. |
| `-out` | `<outfile>` | **Required.** Output filename where an `OMG1` `JHC_header` stub is written at program completion. |
| `-varid` | `<variable_name>` | Optional variable name (e.g., `current_velocity_geographical_east`) to probe inside `SUBSUBGROUP`s via `nc_get_vara_float()`. |

---

## Internal Data Structures & Group Traversal

### `Platform` Structure (`ncEC150read.c`, lines 29–42)

```c
typedef struct
{
  int novals;
  double *latitude;
  double *longitude;
  double *vertical_offset;
  float *distance;
  float *heading;
  float *pitch;
  float *roll;
  float *speed_ground;
  float *speed_relative;
} Platform;
```

### 3-Level Recursive NetCDF-4 Group Inspection

For each input file `inname[ii]`, `ncEC150read` opens `<inname[ii]>.nav` and walks the NetCDF-4 hierarchy using `nc_inq_grps()` and `nc_inq_grpname_full()`:

1. **Root (`CORE`) Level**:
   - Queries root `ndims`, `nvars`, `natts`, `unlimdimid` (`nc_inq`) and top-level group IDs (`ncids[0..ngrps-1]`).
2. **Level 1 (`GROUP`, e.g., `/Environment`, `/Platform`, `/Sonar`, `/Top_level`)**:
   - Prints all group dimensions (`nc_inq_dim`) and variables (`nc_inq_var`).
   - Whenever variables named `"latitude"`, `"longitude"`, `"roll"`, `"pitch"`, or `"heading"` are encountered, allocates heap arrays in `platform` and reads them via `nc_get_var_double()` / `nc_get_var_float()`.
   - Writes `jcu_nav_rec` records to `<inname[ii]>.nav` via `nav_write()`.
3. **Level 2 (`SUBGROUP`, e.g., `/Sonar/Beam_group1`)**:
   - Calls `nc_inq_grps(ncids[k], &nsubgrps, ncsubids)` and prints all subgroup dimensions and variables.
4. **Level 3 (`SUBSUBGROUP`, e.g., `/Sonar/Beam_group1/ADCP`)**:
   - Calls `nc_inq_grps(ncsubids[kk], &nsubsubgrps, ncsubsubids)`, lists all variables and dimensions, and queries the underlying NetCDF type size and VLEN base type via `nc_inq_type()` and `nc_inq_vlen()`.

---

## Architectural Fit

Use `ncEC150read` (or [`ncread`](ncread.html)) when inspecting the NetCDF-4 group tree and VLEN type signatures of new SONAR-netCDF4 files; use [`hdf5EC150read`](hdf5EC150read.html) for production extraction of EC150 ADCP velocity curtains (`.N.r4`, `.E.r4`, `.D.r4`, `.Q.r4`), `.nav`, and `.motion` files.
