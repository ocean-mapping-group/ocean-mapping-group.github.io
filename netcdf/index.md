---
layout: default
title: NetCDF & HDF5 Tools (netcdf)
has_children: true
nav_order: 28
category: Oceanographic & Acoustic NetCDF/HDF5 Readers
source_path: code/netcdf/
related_tools: ["hdf5EC150read", "ncCopernicusRead", "ncEC150read", "ncread", "jview"]
---

# NetCDF & HDF5 Tools (`netcdf/`)

## Overview

The `netcdf/` (`code/netcdf/`) directory contains command-line utilities authored by John Hughes Clarke (2021–2025) for extracting, slicing, and converting **NetCDF-4 / HDF5** physical oceanography models (such as **Copernicus Marine Service**, **SSCOFS** Salish Sea, **WCOFS** West Coast Operational Forecast System, and **GRTOFS** Global Real-Time Ocean Forecast System) and **Kongsberg Simrad EC150-3C / ES38-7** split-beam ADCP/echosounder ICES SONAR-netCDF4 files into OMG binary `.r4` floating-point grids, `.nav` navigation files, `.motion` attitude files, and ASCII column tables.

Because modern NetCDF-4 files are built on top of the **HDF5** storage layer—and because Kongsberg EC150-3C ADCP files use HDF5 variable-length (`H5Tvlen_create`) datasets inside hierarchical groups (`/Sonar/Beam_group1/ADCP/...`)—this directory includes both standard Unidata `libnetcdf` readers (`ncCopernicusRead`, `ncEC150read`, `ncread`) and a direct `libhdf5` reader (`hdf5EC150read`).

---

## Tools in `netcdf/`

| Tool | Source File | Primary Role | Input Formats | Output Formats |
| :--- | :--- | :--- | :--- | :--- |
| **[`hdf5EC150read`](hdf5EC150read.md)** | `code/netcdf/hdf5EC150read.c` | Production HDF5 reader for Kongsberg Simrad **EC150-3C** ADCP and **ES38-7** split-beam echosounder `.nc` (SONAR-netCDF4) files; extracts vertically binned North/East/Down current velocity `.r4` sections, quality `.r4`, ES38 power `.r4`, `.nav`, and `.motion`. | `.nc` / `.h5` (Kongsberg EC150 / ES38 SONAR-netCDF4) | `.N.r4`, `.E.r4`, `.D.r4`, `.Q.r4`, `.nav`, `.motion` |
| **[`ncCopernicusRead`](ncCopernicusRead.md)** | `code/netcdf/ncCopernicusRead.c` | Multi-dimensional (1D/2D/3D/4D) NetCDF oceanographic model extractor and slicer for **Copernicus**, **SSCOFS** (FVCOM TIN), **WCOFS**, **GRTOFS**, and UBC Salish Sea models. | `.nc` (1D–4D oceanographic NetCDF models) | `.r4`, `.zvals`, `.time`, `.columns`, `.2D_array`, `.3D_array`, `.4D_array`, `.txt` |
| **[`ncEC150read`](ncEC150read.md)** | `code/netcdf/ncEC150read.c` | Initial `libnetcdf` hierarchical group/subgroup explorer and platform navigation extractor (`<infile>.nav`) for Kongsberg EC150 `.nc` files (superseded by `hdf5EC150read` for VLEN traces). | `.nc` (Kongsberg EC150 SONAR-netCDF4) | `<infile>.nav`, `<outfile>` (OMG1 `.r4` header) |
| **[`ncread`](ncread.md)** | `code/netcdf/ncread.c` | Lightweight NetCDF-4 group, subgroup, dimension, and variable structure inspector. | `.nc` (Any NetCDF / NetCDF-4 file) | Terminal group/variable hierarchy dump |

---

## Architectural Fit in the OMG Ecosystem

1. **Water Column & Acoustic Doppler Current Profiling (`hdf5EC150read`)**:
   - Developed aboard *USNS Heezen* (March 2023) and refined through September 2025 to correlate acoustic water column scattering layers (ES38-7 / EM712 / EM2040) with co-located ADCP 3D current velocity vectors (`N`, `E`, `D`) and echo quality (`Q`) in [`jview`](../JV/jview.md).
2. **4D Hydrodynamic Model Ray-Tracing & Comparison (`ncCopernicusRead`)**:
   - Extracts horizontal depth slices (`-depth_pick`, `-all_depths`) or vertical latitude/longitude cross-sections (`-lat_pick`, `-lon_pick`) of temperature (`thetao`), salinity (`so`), sound speed, or sea surface height (`zos`/`ssh`) from operational ocean models into OMG `.r4` rasters for direct 2D/3D inspection in [`jview`](../JV/jview.md) and synthetic SVP generation.
3. **Build & Library Dependencies (`code/netcdf/makefile`)**:
   - Compiled via `code/netcdf/makefile`, linking against `liblocal.a`, `libsimrad.a`, `libnetcdf` (`-lnetcdf`), and `libhdf5` (`-lhdf5`), with binaries installed to `$LOCALBIN`.

---

## Quick-Start Examples

```bash
# Inspect NetCDF-4 group and variable schema:
ncread -in raw/EC150_line01.nc -out /tmp/nc_schema.out

# Extract binned ADCP North/East/Down/Quality .r4 curtains, .nav, and .motion from EC150 HDF5/NetCDF4 files:
hdf5EC150read -grab_EC150_currents -vbin 2.0 -vstep 1.0 -maxdepth 150.0 \
    -in raw/EC150_*.nc -out grids/EC150_curtain

# Extract a 300 m horizontal temperature slice from a 4D Copernicus NetCDF model:
ncCopernicusRead -varid thetao -depth_pick 300.0 -date_label \
    -in copernicus_ibi.nc -out grids/ibi_300m
```
