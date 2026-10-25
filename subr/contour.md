---
layout: default
title: contour
parent: Core Shared Libraries (subr)
module_name: contour
source_path: code/subr/contour.c
header_path: code/subr/contour.h
category: Gridding, Contouring & Spatial Geometry
related_tools:
  - contgrid
  - embedCont
  - swathed
  - RT
  - QCdemo
  - project
---

# contour: Distorted Swath & Grid Iso-Depth Contouring Engine

## Overview & Purpose
`contour` (`contour.c` / `contour.h`, 670 lines) is a 2D iso-surface contouring library originally written by John E. Hughes Clarke in Fortran in December 1988 and ported to C in November 1990. Unlike standard rectilinear grid contourers, `contour()` operates directly on a distorted $16 \times 19$ quadrilateral mesh of 3D coordinates (`double xyz[16][19][3]`, representing `[along_track][across_track][lon, lat, depth]`), making it capable of contouring both regular Digital Terrain Models (DTMs) and raw ungridded multibeam swath meshes in real time.

The library resolves saddle-point (four-edge crossover) ambiguities using shortest-diagonal distance tests, computes downhill tick marks indicating slope direction, generates contour level labels along the center beam, and outputs binary vector segments (`bin_vect`) to `plotfile`.

---

## Key Global Variables & Data Structures

### Binary Vector Structure (`bin_vect`, defined in `array.h`)
```c
typedef struct {
    double x1, y1;   /* Start coordinates of contour segment (or -999999.0 flag for text label) */
    double x2, y2;   /* End coordinates of contour segment (or label position lx, ly) */
    int    color;    /* Color index of contour line */
    int    ticktype; /* Downhill tick style (+ve or -ve indicating downhill sense) */
    float  value;    /* Iso-depth value of the contour */
} bin_vect;
```

### Global State Variables
```c
bin_vect current_vect;          /* Active binary vector record written to plotfile */
float    rminlevel, rmaxlevel;  /* Minimum and maximum contour depth levels */
float    rinterval;             /* Contour interval spacing */
int      edgelabel;             /* Flag to label contours at swath edges */
int      nolevels;              /* Total number of active contour levels (up to 999) */
float    contours[1000][4];     /* Level table: [k][0]=depth, [k][1]=color, [k][2]=ticktype, [k][3]=labelflag */
FILE    *plotfile;              /* Output binary stream for bin_vect contour segments */
```

---

## Public Functions & Signatures

### `void contour(double xyz[16][19][3], int start, int end, int sub_win)`
Contours a $16 \times 19$ mesh patch `xyz` across contour table indices `start` through `end`.
* **Parameters:**
  * `xyz[16][19][3]`: 3D mesh where index `0` is $X$ (longitude/easting), `1` is $Y$ (latitude/northing), and `2` is $Z$ (depth).
  * `start`, `end`: First and last indices in `contours[][]` to evaluate.
  * `sub_win`: Window/mode flag (when `!= -99`, estimates nominal across-track spacing `xtrack` from center beams `9` and `10` to filter out stretched data gaps).
* **Algorithmic Workflow:**
  1. **Gap Rejection:** Skips any along-track step where the center-beam spacing `centrestep` exceeds $3 \times \text{xtrack}$, or where any of the four cell corners (`tlz`, `trz`, `blz`, `brz`) equals `0.0`.
  2. **Edge Linear Interpolation:** Adds a small perturbation `noise = 0.01` to the contour level `rlevel` to avoid exact vertex degeneracies, then computes linear interpolation weights (`wtl`, `wtr`, `wlt`, `wlb`, `wrt`, `wrb`, `wbl`, `wbr`) along the top, left, right, and bottom edges of each quadrilateral cell.
  3. **17-Case Marching Quad Classification:** Classifies the edge crossings (`top`, `bottom`, `left`, `right` $\in \{-1, 0, +1\}$) into 17 topological cases:
     * **Cases 1–13:** Single segment crossing two adjacent or opposite cell edges; calls `plotcon()` with the appropriate downhill `sense` ($\pm 1$).
     * **Cases 14–17 (Saddle Point / Four-Edge Crossover):** Computes latitude-scaled (`llrat = cos(lat)`) diagonal lengths `tldiag`, `trdiag`, `bldiag`, and `brdiag`, and connects the pair of crossings with the shorter total diagonal length `(tldiag + brdiag) < (trdiag + bldiag)`.
  4. **Center-Beam Labeling:** When a contour crosses the center beam (`iy == 9`) and `labelflag == 1` (with `labeldelay == 0`), emits a special `bin_vect` marker (`x1 = y1 = -999999.0`, `x2 = lx`, `y2 = ly`) and sets a 100-cell cooldown (`labeldelay = 100`).

### `void contrange(double rmin, double rmax, FILE *file)`
Reads contour specification parameters (`rminlevel`, `rmaxlevel`, `rinterval`, and labeling frequency `labcon`) from `file` (or interactively from `stdin`) and populates `contours[0..nolevels][0..3]` with depth values, cycling colors (`1..5`), tick types (`1..3`), and label flags.

### `void plotcon(double x1, double y1, double x2, double y2, long sense, double xtrack, long col, long ticktype, int sub_win)`
Constructs and writes a contour segment `bin_vect` between `(x1, y1)` and `(x2, y2)` to `plotfile`. Rejects zero-length segments or segments longer than $4 \times \text{xtrack}$, computes downhill perpendicular tick vectors (`tickx`, `ticky`) of length `xtrack / 5` at the segment midpoint `(xmid, ymid)`, encodes downhill `sense` into the sign of `current_vect.ticktype`, and writes `current_vect` to `plotfile`.

---

## How It Fits Into the OMG Architecture
`contour` is used for both batch DTM contouring and real-time swath waterfall contouring across the OMG codebase:
* **Grid Contouring Utilities (`code/grid/contgrid.c`, `code/grid/embedCont.c`):** Slices DTMs into $16 \times 19$ patches and calls `contrange()` and `contour()` to generate binary vector contour files (`.vec`) and embedded raster contours.
* **Real-Time & Interactive Swath Viewers (`RT`, `swathed`, `QCdemo`):** Contours incoming multibeam pings on the fly to display real-time bathymetric contours over sidescan and sun-illuminated surfaces.
