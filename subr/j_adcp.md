---
layout: default
title: j_adcp
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/j_adcp.c
category: Oceanographic & Acoustic Sensor I/O
related_tools:
- adcputilities
- watercolumn / current profiling tools
module_name: j_adcp
header_path: code/subr/j_adcp.h
---

# `j_adcp` — Teledyne RDI ADCP (ASCII, WinADCP & VmDas Binary) Parser Library

## Overview & Purpose in the OMG Architecture

`j_adcp` (`code/subr/j_adcp.c`, `code/subr/j_adcp.h`), originally authored by John E. Hughes Clarke in September 2000 and extended in April 2010 (aboard USNS *Heezen*) and by Ian Church (IWC) for VmDas binary files, provides unified data structures and I/O routines for reading **Teledyne RD Instruments (RDI) 4-beam Acoustic Doppler Current Profiler (ADCP)** datasets.

Marine acoustic surveys frequently log ADCP ensembles alongside multibeam bathymetry and water-column backscatter to characterize current shear, internal waves, suspended sediment backscatter, and vessel bottom-track velocity. `j_adcp` abstracts three distinct RDI data representations into a single in-memory `ADCP_header` and `ADCP_record` model:
1. **Classic OMG / RDI ASCII playback dumps** (`jADCP_read_header`, `jADCP_read_next_rec`)
2. **WinADCP tab-delimited ASCII exports** (`jwinADCP_read_header`, `jwinADCP_read_next_rec`), dynamically adapting to user-selected column labels, units, and depth bin numbers.
3. **RDI VmDas binary PD0/ENX/STA ensemble files** (`vmdasRecs`, `vmdasReadDataRec`), decoding binary headers, fixed/variable leaders, velocity profiles, echo intensity, percent-good, bottom-track, and VmDas navigation blocks.

---

## Key Data Structures, Constants & Macros

### Constants
- `MAX_BINS` (`200`): Maximum number of vertical depth cells (bins) per ADCP ensemble.

### Core Structs (`code/subr/j_adcp.h`)

#### `ADCP_header`
Stores instrument configuration and ensemble setup parameters:
- `char NOTE_1[80]`, `NOTE_2[80]`: Free-text header notes.
- `float depth_cell_length_cm`: Vertical bin size (cm).
- `float blank_after_TX_cm`: Transmit blanking distance (cm).
- `float adcp_depth_cm`: Transducer draft/depth below surface (cm).
- `int no_depth_cells`: Number of depth bins per ensemble.
- `int no_pings_per_ensemble`: Pings averaged per ensemble.
- `float time_per_ensemble_hsec`: Ensemble interval in hundredths of seconds.
- `int profiling_mode`: RDI profiling mode identifier.
- `short headingAlignment`, `headingBias`: Transducer heading alignment and bias (hundredths of degrees, added for VmDas).

#### `ADCP_bin`
Stores per-depth-cell measurements for a single vertical bin:
- `float depth`: Center depth of the bin.
- `float vel_magnitude`, `vel_direction`: Horizontal current speed and direction.
- `float east_vel_component`, `north_vel_component`, `verti_vel_component`, `error_velocity`: 3D orthogonal velocity components and 4-beam error velocity.
- `float BS_beam1`, `BS_beam2`, `BS_beam3`, `BS_beam4`: Per-beam acoustic backscatter / echo intensity (counts or dB).
- `float percent_good`, `PG1`, `PG2`, `PG3`, `PG4`: Overall and 4-beam solution percent-good quality metrics.
- `float discharge`: Calculated water discharge for river/estuary transects.

#### `ADCP_record`
Complete ensemble record combining timestamp, attitude, bottom-track, navigation, discharge, and an array of `ADCP_bin` cells:
- **Timestamp & Ensemble ID**: `year`, `month`, `day`, `hour`, `minute`, `sec`, `hsec`, `y2kyear`, `jday`, `dtime` (Unix epoch seconds), `ensemble_no`, `no_ensembles`.
- **Attitude & Environmental Sensors**: `pitch`, `roll`, `corr_heading`, `adcp_temp`, `soundSpeed` (m/s), `sal` (ppt), `temp` (°C).
- **Bottom Track & Depth**: `bottom_track_vel_EW`, `bottom_track_vel_NS`, `bottom_track_vel_UD`, `bottom_track_vel_ERR`, `depth`, `beam1_depth` .. `beam4_depth`.
- **Navigation & Track Totals**: `latitude`, `longitude`, `lat_nav`, `lon_nav`, `cmg_nav`, `azi_bias`, `GGA_alt`, `GGA_dalt`, `GGA_HDOP`, `total_elapsed_dist`, `total_elapsed_time`, `total_dist_north`, `total_dist_east`, `total_dist_made_good`.
- **Discharge Summary**: `middle_discharge`, `top_discharge`, `bottom_discharge`, `start_shore_discharge`, `start_shore_distance`, `end_shore_discharge`, `end_shore_distance`, `start_middle_depth`, `end_middle_depth`.
- **Bin Array & Scaling**: `no_bins`, `units[2]`, `vel_ref[4]`, `intensity_units[10]`, `intensity_scale_factor`, `sound_absorption_factor`, `depth_multiplier`, `vector_multiplier`, and `ADCP_bin bins[MAX_BINS]`.

#### `winADCP_cluster` (and global `winA[10000]`)
Metadata descriptor used to parse variable-column WinADCP tab-delimited exports:
- `char label[50]`, `units[10]`, `binno[10]`, `value[20]`, `int ibinno`, `nochars`.

---

## Public Functions & Signatures

### Format-Agnostic Dispatchers
- `int j_which_ADCP_read_header(FILE *file, ADCP_header *adcp_head, int vflag, int winADCP)`
  Dispatches header reading to `jwinADCP_read_header()` if `winADCP` is non-zero, or `jADCP_read_header()` otherwise.
- `int j_which_ADCP_read_next_rec(FILE *file, ADCP_record *adcp_rec, int vflag, int winADCP)`
  Dispatches ensemble record reading to `jwinADCP_read_next_rec()` or `jADCP_read_next_rec()`.

### Classic RDI ASCII Format Functions
- `int jADCP_read_header(FILE *file, ADCP_header *adcp_head, int vflag)`
  Reads the 3-line classic ASCII header (`NOTE_1`, `NOTE_2`, and the 7 numeric setup parameters).
- `int jADCP_read_next_rec(FILE *file, ADCP_record *adcp_rec, int vflag)`
  Parses multi-line classic RDI ASCII ensemble blocks, converting 2-digit years to Y2K years, computing Unix epoch `dtime` via `stdtime_from_month_day()`, and populating `adcp_rec->bins[0..no_bins-1]`.

### WinADCP Tab-Delimited ASCII Functions
- `int jwinADCP_read_header(FILE *file, ADCP_header *adcp_head, int vflag)`
  Reads the 16-line WinADCP text preamble, extracting `no_pings_per_ensemble`, `time_per_ensemble_hsec`, `blank_after_TX_cm`, `depth_cell_length_cm`, and parsing the tab-delimited column header rows (labels on line 12, units on line 13, bin indices on line 14) into the `winA[]` descriptor array.
- `int jwinADCP_read_next_rec(FILE *file, ADCP_record *adcp_rec, int vflag)`
  Tokenizes each tab-delimited ensemble row against the `winA[]` column descriptors (`Ens`, `YR`, `MO`, `DA`, `HH`, `MM`, `SS`, `Hea`, `Pit`, `Rol`, `Tem`, `BD1`–`BD4`, `Eas`, `Nor`, `Ver`, `Err`, `Mag`, `Dir`, `EAS`, `PG1`–`PG4`, `FLat`/`FLon`, `LLat`/`LLon`, etc.), automatically computing bin depths and course-made-good (`cmg_nav`).

### VmDas Binary Format & Diagnostic Functions
- `int vmdasRecs(FILE *file)`
  Determines the total number of binary ensemble records in an RDI VmDas file by reading the byte size of the first ensemble (`0x7f7f` header ID) and dividing total file length.
- `int vmdasReadDataRec(FILE *file, ADCP_header *adcp_head, ADCP_record *adcp_rec, int vflag)`
  Reads a binary VmDas ensemble (`0x7f7f`), walks the data-type offset table, and decodes Fixed Leader (`0x0000`), Variable Leader (`0x0080`), Velocity (`0x0100`), Correlation (`0x0200`), Echo Intensity (`0x0300`), Percent Good (`0x0400`), Bottom Track (`0x0600`), and VmDas Navigation (`0x2000`) data blocks.
- `void printADCPHead(ADCP_header *adcp_head)` / `void printADCPRec(ADCP_record *adcp_rec)`
  Prints formatted diagnostic summaries of header and ensemble contents to `stdout`.

---

## How It Fits Into the OMG Architecture

`j_adcp` serves all ADCP processing, plotting, and acoustic water-column comparison utilities in the OMG codebase. It depends on `stdtime.h` for calendar-to-epoch conversions and `support.h` (`getc_line`) for line-buffered file parsing.
