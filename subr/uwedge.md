---
layout: default
title: uwedge
parent: Shared Core Libraries (subr)
module_name: uwedge
source_path: code/subr/uwedge.c
header_path: code/subr/uwedge.h
category: Raytracing, Sound Speed & Geolocation
related_tools: ["support", "j_watercolumn", "jb_watercolumn", "svp_tool"]
---

# uwedge

## Overview
`uwedge` (`uwedge.c` / `uwedge.h`), written by Jonathan Beaudoin (November 2008), is an XML parser, writer, and statistical compiler for **raytracing uncertainty wedges** (`<wedge>` XML files). Built on `libxml2` (`<libxml/parser.h>`, `<libxml/tree.h>`), it stores 2D across-track ($y$) by depth ($z$) grids of vertical depth uncertainty ($\sigma_d$) and horizontal radial positioning uncertainty ($\sigma_h$) resulting from sound velocity profile (SVP) variability.

Given a collection of pairwise difference wedges (`bwedges`) computed between multiple sound velocity casts, `Wedge_Compile()` aggregates them across the water column to produce both a **mean bias wedge** (`method="MEAN"`) and a **95% confidence level ($1.96\sigma$) standard deviation wedge** (`method="STDEV"`).

---

## Data Structures

### `WedgeNode`
Represents the vertical and horizontal uncertainty at a single `(z, y)` grid cell in the swath wedge:
```c
typedef struct {
    double sigma_d;   /* Vertical depth uncertainty / bias (m) */
    double sigma_h;   /* Horizontal radial uncertainty / bias (m) */
} WedgeNode;
```

### `Wedge`
In-memory representation of a `<wedge>` XML document:
```c
typedef struct {
    float version;            /* XML schema version (e.g. 1.0) */
    float dz, dy;             /* Depth (z) and across-track (y) grid spacing (m) */
    int Nz, Ny, Np;           /* Number of depth rows, across-track columns, and source SVP profiles */
    char *creation;           /* Creation timestamp string */
    char *method;             /* Uncertainty calculation method (e.g., "MEAN", "STDEV") */
    float draft;              /* Transducer draft (m) */
    char *surface_probe;      /* Surface sound speed sensor mode/status */
    char **source_profiles;   /* Array of Np source SVP filenames (<source><profile>...) */
    char *time;               /* Reference timestamp (<location><date>) */
    double longitude;         /* Reference longitude (<location><position><lon>) */
    double latitude;          /* Reference latitude (<location><position><lat>) */
    WedgeNode **data;         /* 2D array data[0..Nz-1][0..Ny-1] of (sigma_d, sigma_h) */
    char *filename;           /* Disk filename for reading/writing */
    int *num_per_row;         /* Valid across-track nodes in each depth row z */
} Wedge;
```

---

## Public Functions

| Function | Signature | Description |
|---|---|---|
| `Wedge_Init` | `int Wedge_Init(Wedge *wedge)` | Zeroes the `Wedge` struct via `memset`. |
| `Wedge_Alloc` | `int Wedge_Alloc(Wedge *wedge)` | Allocates `wedge->data` (`Nz x Ny` of `WedgeNode`), `wedge->num_per_row` (`Nz`), and `wedge->source_profiles` (`Np`). |
| `Wedge_Read` | `int Wedge_Read(Wedge *wedge)` | Parses the XML file at `wedge->filename` using `libxml2` (`xmlParseFile`), validates the `<wedge>` root element, allocates memory via `Wedge_Alloc()`, and populates `<method>`, `<source>`, `<location>`, and `<data><row z="..." n="...">` nodes. |
| `Wedge_Write` | `int Wedge_Write(Wedge *wedge)` | Serializes the `Wedge` structure to `wedge->filename` as a formatted `<wedge version="1.0" ...>` XML document. |
| `Wedge_Print` | `int Wedge_Print(Wedge *wedge)` | Prints a human-readable summary of the wedge metadata, grid dimensions, source profiles, and geographic location to `stdout`. |
| `Wedge_Free` | `int Wedge_Free(Wedge *wedge)` | Frees all dynamically allocated strings and 2D data arrays inside `wedge` and resets it via `Wedge_Init()`. |
| `Wedge_Compile` | `Wedge *Wedge_Compile(Wedge *bwedges, int num_bwedges)` | Takes an array of `num_bwedges` input wedges (verifying identical `dz` and `dy` resolution), performs a two-pass statistical reduction across all `(z, y)` nodes, trims outer-swath edge cells with incomplete sample counts, and returns a 2-element `Wedge` array: `return_wedge[0]` (`MEAN`) and `return_wedge[1]` (`STDEV`, scaled by `1.96` for 95% confidence). |

---

## Architectural Role
`uwedge` supports oceanographic refraction uncertainty analysis (`svp_tool` and SVP uncertainty wedge utilities), enabling hydrographers to visualize how spatial and temporal sound speed variability propagates into vertical and horizontal sounding error across the multibeam swath.
