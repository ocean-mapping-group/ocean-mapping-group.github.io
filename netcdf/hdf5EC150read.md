---
layout: default
title: hdf5EC150read
parent: NetCDF & HDF5 Tools (netcdf)
nav_order: 1
tool_name: hdf5EC150read
source_path: code/netcdf/hdf5EC150read.c
category: Oceanographic & Acoustic NetCDF/HDF5 Readers
input_formats: [".nc", ".h5 (Kongsberg Simrad EC150-3C / ES38-7 SONAR-netCDF4)"]
output_formats: [".N.r4", ".E.r4", ".D.r4", ".Q.r4", ".nav", ".motion"]
related_tools: ["ncEC150read", "ncCopernicusRead", "ncread", "jview"]
---

# hdf5EC150read

## Overview

`hdf5EC150read` (`code/netcdf/hdf5EC150read.c`) is a specialized HDF5 acoustic and current-profiling unpacker written by John Hughes Clarke (initiated aboard *USNS Heezen* in March 2023 and updated through September–October 2025) to extract **Kongsberg Simrad EC150-3C** combined split-beam echosounder / ADCP and **ES38-7** wideband transceiver datasets from ICES SONAR-netCDF4 (`.nc`) files.

Because Kongsberg's SONAR-netCDF4 implementation stores per-ping ADCP velocity profiles and wideband complex backscatter traces as **HDF5 Variable-Length (`hvl_t` / `H5Tvlen_create`)** arrays inside nested HDF5 groups (`/Sonar/Beam_group1/ADCP/...`), standard NetCDF-C array calls in [`ncEC150read`](ncEC150read.md) could not directly unpack them. `hdf5EC150read` uses the native `libhdf5` API (`H5Fopen`, `H5Ovisit`, `H5Dopen`, `H5Tvlen_create`, `H5Dread`) to read multi-file survey lines, convert Windows NT 1601 nanosecond timestamps to Unix epoch seconds, write per-file `.nav` and `.motion` files, vertically resample/bin raw or time-averaged ADCP currents, trim sidelobe bottom echoes, and append the resulting profiles across multiple input files into continuous OMG `.r4` floating-point curtain grids (`.N.r4`, `.E.r4`, `.D.r4`, `.Q.r4`).

---

## Usage

```bash
hdf5EC150read [OPTIONS] -in <file1.nc> [file2.nc ...] -out <outfile_prefix>
```

### Command-Line Options

| Flag | Arguments | Description |
| :--- | :--- | :--- |
| `-in` | `<file1.nc> [file2.nc ...]` | **Required.** One or more input SONAR-netCDF4 / HDF5 files (up to `MAXNOFILES = 10000`). Reads all consecutive arguments until the next `-` flag. |
| `-out` | `<outfile_prefix>` | **Required.** Output prefix for the concatenated `.N.r4`, `.E.r4`, `.D.r4`, and `.Q.r4` OMG1 raster curtain files. |
| `-grab_EC150_currents` | *(none)* | Extracts 3D geographical current velocities (North, East, Down), echo quality, and error velocity from `/Sonar/Beam_group<X>/ADCP`, vertically bins them, trims below the seafloor slant range, and writes `.N.r4`, `.E.r4`, `.D.r4`, and `.Q.r4`. |
| `-averages` | *(none)* | When used with `-grab_EC150_currents`, reads ensemble-averaged currents from `/ADCP/Mean_current/current_velocity_geographical_{north,east,down}` instead of instantaneous single-ping currents. |
| `-beamgroup` | `<int>` | Selects which `/Sonar/Beam_group<X>` group to read (default `1`). Automatically probes `/Sonar/Beam_group0` through `19` via `H5Gopen2()` and reports which groups exist and contain an `/ADCP` subgroup. |
| `-vbin` | `<float>` | Vertical averaging window height in meters (default `4.0` m; usage example `2.0` m). |
| `-vstep` | `<float>` | Vertical output grid step interval in meters (default `2.0` m; usage example `1.0` m). Total vertical bins = `maxdepth / vstep` (must not exceed `MAXBINS = 2000`). |
| `-maxdepth` | `<float>` | Maximum water depth in meters for vertical binning (default `200.0` m; usage example `150.0` m). |
| `-grab_ES38_trace` | *(none)* | Extracts complex quadrature (`backscatter_i`, `backscatter_r`) 3D VLEN traces from `/Sonar/WBT 400798-15 ES38-7_ES`, computes log power $10 \log_{10}(\sqrt{I^2 + R^2})$, and writes beams 0, 1, and 2 into `.N.r4`, `.E.r4`, and `.D.r4`. |
| `-varid` | `<string>` | Optional variable identifier string (`cvarid`). |
| `-v` | *(none)* | Enables verbose per-ping trace length, range, and binned velocity diagnostic output. |

---

## Key Data Structures & Compile-Time Limits

```c
#define MAXPINGS    3000
#define MAXTRACELEN 15000
#define MAXBINS     2000
#define MAXBEAMS    4
```

The global `Ping_Cycle ping_cycle` structure (`code/netcdf/hdf5EC150read.c`, lines 53–129) holds:
- **Navigation & Attitude (from `/Sonar/Beam_group<X>`)**:
  - `ping_time[MAXPINGS]` (Windows NT 1601 time in nanoseconds; converted via `dtime / 1e9 - 11644473600LL` to Unix 1970 epoch seconds), `latitude`, `longitude`, `vertical`, `heading`, `pitch`, `roll`.
- **Transducer & Echosounder Metadata**:
  - `sample_interval`, `sample_time_offset`, `detect_bott_range`, `sound_speed`, `water_temp`.
- **ADCP Parameters & VLEN Velocity Arrays (from `/Sonar/Beam_group<X>/ADCP`)**:
  - `bin_length`, `vert_samp_intvl`, `depth_first_sam_cen`, `slant_range_to_bottom[MAXPINGS][4]`, `transmit_duration_nominal_sub_pulse`, `transmit_lag_interval_sub_pulse`.
  - `curr_vel_tracelengths[MAXPINGS]`, `curr_vel_geo_N[MAXPINGS][MAXTRACELEN]`, `curr_vel_geo_E`, `curr_vel_geo_D`, `quality[MAXPINGS][MAXTRACELEN]` (`0`–`100`), `error_velocity[MAXPINGS][MAXTRACELEN]`.
- **Resampled Vertical Curtain Buffers**:
  - `bin_count[MAXPINGS][MAXBINS]`, `bin_av_geo_N`, `bin_av_geo_E`, `bin_av_geo_D`, `bin_av_Quali`.

---

## Internal Helper Functions

| Function | Signature / Purpose |
| :--- | :--- |
| `visit_obj()` | Callback passed to `H5Ovisit()` that enumerates and prints every `H5O_TYPE_DATASET` path in the HDF5 file. |
| `grab_HDF5_1D_double_data()` / `float` / `int` / `longint` | Opens a 1D dataset at `mem_strappend(gname, dname)` and reads `H5T_NATIVE_DOUBLE`, `FLOAT`, `INT`, or `ULONG` into `ping_cycle`. |
| `grab_HDF5_2D_vlen_data()` / `grab_HDF5_2D_Ivlen_data()` | Reads 2D variable-length (`hvl_t`) float or integer per-ping profile arrays using `H5Tvlen_create()` and copies each trace (`rdata[i].len`) into `ping_cycle`. |
| `grab_HDF5_3D_vlen_data()` | Reads 3D variable-length (`hvl_t`) split-beam arrays (`[beam][ping]`) for `-grab_ES38_trace`. |
| `dump_Nav()` | Writes `<infile>.nav` (`jcu_nav_rec` records with Windows-NT-to-Unix converted timestamps and bottom-track depth). |
| `dump_Motion()` | Writes `<infile>.motion` (`OMG_HDCS_summary_attitude` Version 3 and `OMG_HDCS_attitude` roll/pitch/heading records). |

---

## Vertical Binning & Seafloor Sidelobe Trimming

When `-grab_EC150_currents` is active:
1. Each valid (non-`NaN`) sample $k$ at depth $z_k = k \cdot \text{vert\_samp\_intvl} + \text{depth\_first\_sam\_cen}$ with `quality[j][k] > 50` is accumulated into overlapping vertical bins (`vstep` spacing, `vbin` window width).
2. To suppress acoustic sidelobe contamination near the seabed, `hdf5EC150read` inspects the 4-beam `slant_range_to_bottom[j][0..3]`, finds `min_slant_range - bin_length[j]`, projects it to vertical depth via $\cos(20^\circ)$ (`guess_vdepth = min_slant_range * cos(20.0 * M_PI / 180.0)`), and zeroes out `bin_av_geo_N/E/D` below `trim_pix = guess_vdepth / vstep`.
3. Appends the ping columns to `<out>.N.r4`, `<out>.E.r4`, `<out>.D.r4`, and `<out>.Q.r4`, updating `JHChead.dy` and `JHChead.ymax` across all input files for seamless curtain visualization in [`jview`](../JV/jview.md).
