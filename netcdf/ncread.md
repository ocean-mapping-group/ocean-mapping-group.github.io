---
layout: default
title: ncread
parent: NetCDF & HDF5 Ocean/Sonar Readers (netcdf)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 4
tool_name: ncread
source_path: code/netcdf/ncread.c
category: Oceanographic & Acoustic NetCDF/HDF5 Readers
input_formats:
- .nc (NetCDF-3 / NetCDF-4)
output_formats:
- STDOUT NetCDF schema dump
related_tools:
- ncCopernicusRead
- ncEC150read
- hdf5EC150read
---

# ncread

## Overview

`ncread` (`code/netcdf/ncread.c`) is a lightweight NetCDF-3 / NetCDF-4 structure and group discovery utility written by John Hughes Clarke (updated March 2023) for inspecting the root dimensions, variables, attributes, top-level groups, and second-level subgroups of any `.nc` file using the Unidata `libnetcdf` C API.

Before running [`ncCopernicusRead`](ncCopernicusRead.html) (which requires knowing the exact `-varid` string and dimension ordering of a 2D/3D/4D ocean model) or [`hdf5EC150read`](hdf5EC150read.html) (which requires knowing which `/Sonar/Beam_group<X>` groups exist), `ncread` provides a fast, zero-configuration summary of the NetCDF file's internal schema.

---

## Usage

```bash
ncread -in <infile.nc> -out <outfile>
```

### Command-Line Options

| Flag | Arguments | Description |
| :--- | :--- | :--- |
| `-in` | `<infile.nc>` | **Required.** Path to the input NetCDF (`.nc`) file to inspect. |
| `-out` | `<outfile>` | **Required.** Path to an output file opened and closed upon completion (required by the CLI argument check in `ncread.c`, line 69). |

---

## Internal Inspection Workflow (`libnetcdf` API Calls)

`ncread` executes a structured two-level metadata walk across the NetCDF file:

1. **Root (`CORE`) File Inquiry**:
   - Opens `<infile.nc>` read-only via `nc_open(inname, NC_NOWRITE, &ncid)`.
   - Calls `nc_inq(ncid, &ndims, &nvars, &natts, &unlimdimid)` and prints the root counts of dimensions (`ndims`), variables (`nvars`), global attributes (`natts`), and the unlimited dimension ID (`unlimdimid`).
2. **Top-Level Group Enumeration (`nc_inq_grps`)**:
   - Calls `nc_inq_grps(ncid, &ngrps, ncids)` to retrieve up to 1,000 child group IDs (`ncids[1000]`) and prints each group's internal NetCDF ID.
3. **Per-Group & Subgroup Discovery Loop**:
   - For each top-level group `k` (`this_ncid = ncids[k]`):
     - Queries and prints the full hierarchical group path (`grpname`) and length (`grpnamelen`) via `nc_inq_grpname_full(this_ncid, &grpnamelen, grpname)`.
     - Queries child subgroups via `nc_inq_grps(this_ncid, &nsubgrps, ncsubids)`. For each subgroup `kk`, prints its full path (`nc_inq_grpname_full`) and its `ndims`, `nvars`, `natts`, and `unlimdimid` (`nc_inq`).
     - Queries the top-level group's own `ndims`, `nvars`, `natts`, and `unlimdimid` via `nc_inq(this_ncid, ...)`.
     - Iterates over `0 .. ndims-1` calling `nc_inq_dim(this_ncid, i, dimname[i], &dimlength[i])` to print each dimension's index, name, and length.
     - Iterates over `0 .. nvars-1` calling `nc_inq_var(this_ncid, i, varname[i], &vartype[i], &var_ndimsp[i], var_ndimids[i], &var_nattsp[i])` to print each variable's index, name, NetCDF data type (`nc_type`), rank (`ndim`), and list of dimension IDs.

---

## Example Terminal Output

```text
 core ncid 65536
 CORE 
ndims    : 0
nvars    : 0
natts    : 12
unlimdimid  : -1
 # groups 4
 group 0 - id # 65537
 ...
 ***************************** group name /Sonar  len 6 
 # subgroups 2
 subgroup 0 - id # 65541
 ***************************** sub group name /Sonar/Beam_group1  len 18 
ndims: 2 nvar: 19 natts 3 unlimdimid -1
```

---

## Architectural Fit

Within `code/netcdf/`, `ncread` is the baseline schema exploration utility that complements the specialized extractors [`ncCopernicusRead`](ncCopernicusRead.html), [`ncEC150read`](ncEC150read.html), and [`hdf5EC150read`](hdf5EC150read.html).
