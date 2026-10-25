---
layout: default
title: iwc_model
parent: Ian Church — Hydrodynamic & 3D Ray-Trace Suite (ianc)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 12
tool_name: iwc_model
source_path: code/ianc/subr/iwc_model.c
category: Ocean Modeling & Hydrographic Utilities (ianc)
input_formats:
- OPeNDAP / THREDDS Catalog URLs
output_formats:
- Predefined C Macros for Operational Ocean Model Endpoints
related_tools:
- modelMerge
- HycomSSP
- modelAnalysis
---

# iwc_model

## Description

`iwc_model` (`code/ianc/subr/iwc_model.c` and `code/ianc/subr/iwc_model.h`) is a header/subroutine configuration module created by Ian Church in January 2016 to centralize OPeNDAP and THREDDS Data Server (TDS) base URLs for the operational hydrodynamic ocean forecast models used across the `ianc` toolset (particularly `modelMerge` and `HycomSSP`).

By defining standardized macro constants for NOAA's Northeast Coastal Ocean Forecast System (`NEGOFS`), the 1/25° Gulf of Mexico HYCOM hourly datasets (`GOM2014`, `GOM2015`), and the Navy Research Laboratory (NRL) CONCORDE model (`NRL_CONCORDE`), `iwc_model.h` documents the remote THREDDS catalog and DODS endpoints queried via the NetCDF-C OPeNDAP client library (`libnetcdf`).

## Public API & Usage

### Header Include

```c
#include "iwc_model.h"
```

### Example C Usage

```c
#include <stdio.h>
#include <netcdf.h>
#include "iwc_model.h"

int main(void) {
    int ncid, status;
    /* Open the 2015 Gulf of Mexico 1/25-degree hourly HYCOM OPeNDAP stream */
    if ((status = nc_open(GOM2015, NC_NOWRITE, &ncid)) != NC_NOERR) {
        printf("Error connecting to HYCOM OPeNDAP server: %d\n", status);
        return 1;
    }
    nc_close(ncid);
    return 0;
}
```

## Defined Macros & Endpoints (`iwc_model.h`)

| Macro Name | Defined Endpoint URL | Model Architecture & Coverage |
| :--- | :--- | :--- |
| `NEGOFS` | `"http://opendap.co-ops.nos.noaa.gov/thredds/catalog/NOAA/NEGOFS/MODELS"` | **NOAA Northeast Coastal Ocean Forecast System**: FVCOM unstructured triangular mesh covering the Gulf of Maine and New England shelf, served by NOAA CO-OPS. |
| `GOM2015` | `"http://tds.hycom.org/thredds/dodsC/GOMl0.04/expt_32.5/2015/hrly"` | **HYCOM Gulf of Mexico 2015 (`GOMl0.04` Expt 32.5)**: 1/25° (`0.04°`) horizontal resolution, 40 vertical coordinate levels, hourly hindcast/forecast output for calendar year 2015. |
| `GOM2014` | `"http://tds.hycom.org/thredds/dodsC/GOMl0.04/expt_32.5/2015/hrly"` | **HYCOM Gulf of Mexico 2014 (`GOMl0.04` Expt 32.5)**: Macro constant for the 1/25° Gulf of Mexico HYCOM experiment (paired in `modelMerge.c` with `.../2014/hrly` for dates after April 1, 2014). |
| `NRL_CONCORDE` | `"http://medusa:8080/thredds/catalog/MedusaThreddsData"` | **NRL CONCORDE Gulf of Mexico Model**: High-resolution Navy Research Laboratory coastal ocean model hosted on the Medusa THREDDS server (internal hostname `medusa` / `10.14.3.54`, external IP `131.95.1.37`). |

## Source File Layout

### `code/ianc/subr/iwc_model.h`
* Defines the include guard (`#ifndef iwc_model`) and the four OPeNDAP/THREDDS URL string literals (`NEGOFS`, `GOM2015`, `GOM2014`, `NRL_CONCORDE`), along with network routing notes for internal vs. external Medusa THREDDS access (`131.95.1.37`).

### `code/ianc/subr/iwc_model.c`
* Includes standard C headers (`<stdlib.h>`, `<stdio.h>`, `<string.h>`, `<math.h>`) and serves as the compilation unit stub for shared model-fetching helper routines in `subr/Makefile`.

## How It Works

1. **OPeNDAP URL Construction**: In `modelMerge` and `HycomSSP`, these base URLs are either passed directly to `nc_open()` (for aggregated single-URL datasets like `GOMl0.04/expt_32.5/2015/hrly` or global HYCOM `GLBv0.08`) or used as prefixes to dynamically format date- and cycle-specific NetCDF file URLs (such as `YYYYMM/nos.negofs.fields.n00X.YYYYMMDD.tHHz.nc` for `NEGOFS` or `nco_rel_concorde_YYYYMMDD00_t0XX.nc` for `NRL_CONCORDE`).
2. **Remote Subsetting via `libnetcdf`**: When `nc_open()` is called with an `http://.../thredds/dodsC/...` URL, `libnetcdf` uses its built-in DAP2/DAP4 client to fetch only the requested hyperslabs (`nc_get_vara_float()`) at the vessel's `(time, depth, lat, lon)` indices rather than downloading multi-gigabyte 4D model files.
