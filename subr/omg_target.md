---
layout: default
title: omg_target
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/omg_target.c
category: Target Picking & Georeferencing
related_tools:
- targethunt
- swathed (SE)
- target_georeference
- target_dump
- target_test
module_name: omg_target
header_path: code/subr/omg_target.h
---

# omg_target

## Overview & Purpose

`omg_target` defines the binary file format (`.tgt`, Versions 0, 1, and 2), in-memory list management, spatial search routines, and 3D acoustic raytrace georeferencing functions for discrete seafloor and water-column targets in the Ocean Mapping Group (OMG) software suite. It bridges interactive target picking in **SwathEd (`SE`)** and **`targethunt`** with full 3D lever-arm, attitude, and sound velocity profile (SVP) reduction (`reduce_OMG_Target` and `reduce_OMG_Target2`).

## Key Data Structures, Constants & Macros

### Constants
- Binary Record Sizes by Version:
  - `OMG_TARGET_SIZE_V0` (`112` bytes): Original georeferenced target record (`id`, `time`, `latitude`, `longitude`, `depth_reduced`, `label[40]`, `attribute[40]`).
  - `OMG_TARGET_SIZE_V1` (`140` bytes): Adds 28 bytes of sonar-relative water-column pick geometry (`beam_number`, `sample_number`, `range`, `angle`, `across`, `depth`, `amplitude`).
  - `OMG_TARGET_SIZE_V2` (`152` bytes): Adds 12 bytes of vessel reference-point (RP) relative coordinates (`ping_number`, `across_reduced`, `along_reduced`).
- String Field Lengths:
  - `OMG_TARGET_MAX_LABEL_SIZE` (`40` bytes)
  - `OMG_TARGET_MAX_ATTRIBUTE_SIZE` (`40` bytes)

### Core Structs
- `OMG_Target`: Complete representation of a picked acoustic target:
  - Identification & Timing: `int id`, `double time` (Unix seconds since 1970), `unsigned int ping_number` (V2).
  - Sonar-Relative Geometry (V1+): `unsigned int beam_number`, `unsigned int sample_number`, `float range` (m, one-way from transducer), `float angle` (deg re vertical, +port / -stbd), `float across` (m re transducer), `float depth` (m re transducer, +down), `float amplitude`.
  - Georeferenced & Reduced Geometry: `double latitude` (deg), `double longitude` (deg), `float depth_reduced` (m re waterline), `float across_reduced` (m re RP, V2), `float along_reduced` (m re RP, V2).
  - Metadata: `char label[40]`, `char attribute[40]`.
- `OMG_Target_List`: Dynamic collection of `OMG_Target` records:
  - On-disk header fields: `int version`, `int num_targets`.
  - In-memory housekeeping: allocated capacity `int size_targets`, `char *target_filename`, and dynamic array `OMG_Target *targets`.

## Public Functions & Signatures

### List Management & Binary I/O
- `int init_OMG_Target(OMG_Target *target)` / `int init_OMG_Target_List(OMG_Target_List *list)` / `int free_OMG_Target_List(OMG_Target_List *list)`
  - Initializes or frees target structures and dynamically allocated arrays.
- `int add_OMG_Target(OMG_Target_List *list, OMG_Target *target)` / `int remove_OMG_Target(OMG_Target_List *list, int target_number)`
  - Appends a target (dynamically doubling array capacity starting from 10) or deletes `target_number` by shifting subsequent elements.
- `int read_OMG_Target_List(OMG_Target_List *list)` / `int write_OMG_Target_List(OMG_Target_List *list)`
  - Reads or writes `.tgt` files (defaulting to `"targets.tgt"`) in little-endian binary format, automatically handling Version 0 (112B), Version 1 (140B), and Version 2 (152B) record layouts. `read_OMG_Target_List` automatically sorts the list by timestamp via `sort_OMG_Target_List` for SwathEd plotting.
- `int sort_OMG_Target_List(OMG_Target_List *list)` / `int compare_targets(const void *val1, const void *val2)` / `int print_OMG_Target_List(OMG_Target_List *list)`
  - Sorts targets chronologically by `time` using `qsort` and prints formatted target attributes.

### Spatial Search & Target Georeferencing
- `int find_OMG_Target_in_swath(OMG_Target_List *list, OMG_Target *target, float *min_distance)`
  - Searches `list` for the closest target within $\pm 0.01\text{ s}$ of `target->time` based on Euclidean distance in sonar-relative `(across, depth)` space.
- `int find_OMG_Target_in_map(OMG_Target_List *list, OMG_Target *target, float *min_distance)`
  - Searches `list` for the geographically closest target using `compute_distance_2(lat1, lon1, lat2, lon2)`.
- `int reduce_OMG_Target(OMG_Target *target, j_EM_watercolumn *watercol, double lat_rp, double lon_rp, float heading)`
  - Performs fast straight-ray target reduction from `sample_number` and `beam_number` using `watercol->sound_speed`, `sampling_freq`, beam pointing angle, and transducer offsets (`tx_tdcr_depth`, `heave`, `across`, `along`), rotating by `heading` (`unrotate`) to compute `latitude`, `longitude`, and reduced offsets.
- `int reduce_OMG_Target2(OMG_Target *target, char *inname, watercolumn *svp)`
  - Performs rigorous 3D raytraced georeferencing by opening the HDCS `.merge`, `.watercol`, `.sectors`, `.orientation`, and `.param` files, interpolating transmit and receive attitude at exact sector transmit and sample receive times (`OMG_HDCS_get_interpolated_async`), rotating TX/RX lever arms, and invoking `reduce_sounding(&geometry)` with the full `watercolumn *svp`.

## How It Fits Into the OMG Architecture

`omg_target` is shared across **`targethunt`** (`code/omg/targethunt.c`), **`swathed` (`SE`)** (`SE_global.h`, `c_wcl_TOOLBOX.h`, `SE_event_loop.c`), **`c_wcpick.h`** (`code/subr/`), **`sonar_geometry.h`**, and the standalone target utilities (`target_georeference`, `target_dump`, `target_test`).
