---
layout: default
title: j_SSCOFS
parent: Core Shared C Library — libj.a (subr)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
source_path: code/subr/j_SSCOFS.c
category: Oceanographic Models, Tides & Sound Velocity
related_tools:
- extractNodeProf
- extractSVTS
- extractVertSection
module_name: j_SSCOFS
header_path: code/subr/j_SSCOFS.h
---

# `j_SSCOFS` — Unstructured Finite-Element Hydrodynamic Ocean Model Loader (`QUODDY` / `SSCOFS` / `STOFS-3D`)

## Overview & Purpose
The `j_SSCOFS` module (`code/subr/j_SSCOFS.c` and `code/subr/j_SSCOFS.h`) provides data structures and mesh-loading routines for unstructured Triangular Irregular Network (TIN) finite-element coastal ocean circulation models—specifically NOAA's **Salish Sea and Columbia River Operational Forecast System (`SSCOFS`)** and **STOFS-3D Atlantic**. Written by John Hughes Clarke in July 2025, it adopts the `QUODDY` finite-element mesh convention (`.nod` vertex coordinates, `.bat` node depths, and `.ele` 3-node triangle connectivity) paired with a pre-rasterized OMG `.r4` element-index lookup grid (`mapelem`) to enable fast spatial querying of 3D temperature, salinity, and sound-speed fields.

---

## Constants, Data Structures & Global State (`j_SSCOFS.h`)

### 1. Constants
- `#define QUODDYMAXLAYERS 500`: Maximum vertical sigma/z-level layers supported at each unstructured mesh node.

### 2. Mesh & Raster Index Structures

```c
typedef struct {
    int nolayers;
    float layerdepth[QUODDYMAXLAYERS];
    float depth;        /* Bathymetric depth at node from .bat file (m) */
    double lat;         /* Node latitude (decimal degrees) */
    double lon;         /* Node longitude (decimal degrees) */
} QUODDY_node;

typedef struct {
    int nodenum[3];         /* 1-based (or 0-based) node indices of triangle vertices */
    QUODDY_node *node[3];   /* Direct pointers to the 3 vertex nodes */
} QUODDY_element;

typedef struct {
    int nonodes;
    QUODDY_node *node;
    int noelems;
    QUODDY_element *element;
    JHC_header mapelem_head; /* OMG raster header for spatial element lookup grid */
    float *mapelem;          /* 2D float raster mapping (x,y) cell to element ID */
} SSCOFS_bits;
```
- **Global Instance:** `SSCOFS_bits theSSCOFS;` (defined in `j_SSCOFS.c` and exported via `j_SSCOFS.h`).

---

## Public Functions & Signatures

### 1. Finite-Element Mesh & Element-Map Loader

```c
int SSCOFS_load_quoddy_mapelem(char *quoddyprefix, char *mapelemname);
```
- **Purpose:** Allocates `theSSCOFS` in memory and loads the complete unstructured triangular mesh (`<quoddyprefix>.nod`, `<quoddyprefix>.bat`, `<quoddyprefix>.ele`) together with the pre-gridded OMG element-index raster (`mapelemname`).
- **Implementation Details:**
  1. **Large-Mesh Memory Allocation:** Allocates `theSSCOFS.node` for up to `3,000,000` `QUODDY_node` entries and `theSSCOFS.element` for up to `6,000,000` `QUODDY_element` triangles—sized specifically to accommodate massive operational meshes such as NOAA STOFS-3D Atlantic (~2.2M nodes / ~4.4M elements).
  2. **Node Coordinate & Bathymetry Ingestion (`.nod` & `.bat`):** Opens `<quoddyprefix>.nod` and `<quoddyprefix>.bat` in lockstep, reading `(node_id, lon, lat)` and `(node_id, depth)` pairs into `theSSCOFS.node[nonodes]`.
  3. **Triangular Element Connectivity (`.ele`):** Opens `<quoddyprefix>.ele` and reads 4-integer lines `(elem_id, nodenum[0], nodenum[1], nodenum[2])` into `theSSCOFS.element[noelems]`.
  4. **Spatial Index Grid (`mapelem`):** Opens `mapelemname`, reads its `JHC_header` via `jread_header()`, allocates `xdim * ydim` floats, and loads the rasterized triangle index map via `jread_data()`.

### 2. Spatial Node/Element Lookup Hook

```c
int SSCOFS_find_nodelem(double lon, double lat, int *elem, int *nod);
```
- **Purpose:** Interface hook to resolve a geographic `(lon, lat)` query coordinate into its containing finite-element triangle `*elem` and nearest vertex `*nod` using `theSSCOFS`.

---

## How It Fits Into the OMG Architecture
`j_SSCOFS` supports the extraction of synthetic sound velocity profiles (SVPs) and 3D oceanographic transects from unstructured hydrodynamic forecast models:
- **Vertical Profile & Time-Series Extraction (`extractNodeProf`, `extractSVTS`):** `code/grid/extractNodeProf.c` and `code/grid/extractSVTS.c` load the `QUODDY` mesh and `mapelem` grid to extract time-varying temperature, salinity, and sound-speed casts at specific survey coordinates for multibeam raytracing.
- **2D Vertical Curtain Sections (`extractVertSection`):** `code/grid/extractVertSection.c` interpolates unstructured finite-element nodes across arbitrary vessel tracklines to visualize coastal fronts, estuarine plumes, and internal waves alongside acoustic water-column imagery.
