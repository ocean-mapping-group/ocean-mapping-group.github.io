---
layout: default
title: omg_line
parent: Core Shared Libraries (subr)
module_name: omg_line
source_path: code/subr/omg_line.c
header_path: code/subr/omg_line.h
category: Survey Planning & Geometry
related_tools:
  - jview (JV)
  - line_export
---

# omg_line

## Overview & Purpose

`omg_line` manages survey planning lines (`OMG_Line` and `OMG_Line_List`), providing binary file persistence (`.lines` format), dual geographic/projected coordinate synchronization, and interactive 2D computational geometry operations. Designed primarily for interactive line planning in **JView (`JV`)** and exporting survey plans via **`line_export`**, the library supports adding, deleting, reversing, reordering, parallel-offsetting, splitting, extending, vertex-moving, joining, and clipping survey lines against a bounding clip segment.

## Key Data Structures, Constants & Macros

### Constants & Macros
- `OMG_LINE_VERSION_1_SIZE` (`32` bytes): On-disk size of a single Version 1 line record (`4 * sizeof(double)` for `lon1`, `lat1`, `lon2`, `lat2`).
- `OMG_LINE_LIST_VERSION_1` (`1`): File format version identifier.
- `OMG_LINE_INCREMENT` (`1`) / `OMG_LINE_DECREMENT` (`-1`): Direction step constants for `reorder_OMG_Lines`.
- `LEFT_OF_LINE` (`1`) / `RIGHT_OF_LINE` (`2`): Offset side specifiers for `add_OMG_Line_Parallel`.

### Core Structs
- `OMG_Line`: Represents a single directed two-point survey line segment:
  - Persistent geographic endpoints (stored on disk in little-endian IEEE 754 doubles): `lon1`, `lat1`, `lon2`, `lat2`.
  - In-memory projected map/pixel coordinates (computed via `Project` / `inv_proj` using a `JHC_header`): `x1`, `y1`, `x2`, `y2`.
- `OMG_Line_List`: Container for an ordered collection of `OMG_Line` segments:
  - On-disk header fields: `int version`, `int num_lines`.
  - In-memory housekeeping: allocated capacity `size_lines`, `char *line_filename`, dynamic array `OMG_Line *lines`, reference map projection `JHC_header map_header`, and `int selected_line` index.

## Public Functions & Signatures

### Initialization, I/O & Projection
- `int init_OMG_Line(OMG_Line *line)` / `int reverse_OMG_Line(OMG_Line *line)` / `int print_OMG_Line(OMG_Line *line)`
  - Zero-initializes a line, swaps its start and end vertices (`lat1`/`lon1`/`x1`/`y1` $\leftrightarrow$ `lat2`/`lon2`/`x2`/`y2`), or prints formatted degrees/decimal-minutes endpoints using `position2string`.
- `int init_OMG_Line_List(OMG_Line_List *list)` / `int free_OMG_Line_List(OMG_Line_List *list)` / `int print_OMG_Line_List(OMG_Line_List *list)`
  - Lifecycle and diagnostic output for `OMG_Line_List`.
- `int set_OMG_Line_List_Projection(OMG_Line_List *list, JHC_header map_header)`
  - Assigns the `JHC_header` map projection structure used to project geographic coordinates into pixel/grid space.
- `OMG_Line_List read_OMG_Line_List(char *line_filename, JHC_header map_header)`
  - Reads a binary `.lines` file (8-byte little-endian header of `version` and `num_lines`, followed by `num_lines` 32-byte records of `lon1, lat1, lon2, lat2`), projecting each line upon insertion via `add_OMG_Line`.
- `int write_OMG_Line_List(OMG_Line_List *list)`
  - Writes the `OMG_Line_List` to `list->line_filename` (defaulting to `"lines.lines"` if unset) in little-endian binary format.
- `char *position2string(double lat, double lon)`
  - Formats decimal-degree latitude and longitude into a newly allocated `"DD MM.MMMM' N/S, DDD MM.MMMM' E/W"` string.

### Interactive Editing & Computational Geometry
- `int add_OMG_Line(OMG_Line_List *list, OMG_Line *line, int position)`
  - Automatically forward-projects (`Project`) if `x1..y2` are zero, or inverse-projects (`inv_proj`) if `lat1..lon2` are zero. Dynamically doubles `list->lines` capacity (starting at 10) when full, shifts existing elements to insert at `position` (or appends at the end if `position == -1`), and updates `selected_line`.
- `int remove_OMG_Line(OMG_Line_List *list, int line_number)`
  - Removes `line_number` and shifts subsequent lines down.
- `int add_OMG_Line_Parallel(OMG_Line_List *list, int side, int number, float spacing)`
  - Computes the azimuth of `selected_line` in pixel coordinates (where $+x$ is right and $+y$ is down), rotates $\pm 90^\circ$ for `LEFT_OF_LINE` or `RIGHT_OF_LINE`, scales `spacing` by `list->map_header.xstep`, and inserts `number` parallel lines.
- `int get_point_cpa(OMG_Line *line, double x, double y, double *x_cpa, double *y_cpa, double *distance, int *on_segment)`
  - Computes the Closest Point of Approach (CPA) from $(x, y)$ to the infinite line through `line` by intersecting perpendicular slopes ($m_2 = -1/m_1$), calculates Euclidean `*distance`, and sets `*on_segment = 1` if `(*y_cpa - y1) * (*y_cpa - y2) < 0`.
- `int get_closest_OMG_Line(OMG_Line_List *list, double lat, double lon, double x, double y)`
  - Returns the index of the line segment with the minimum perpendicular CPA distance where `on_segment == 1`, or `-1` if none.
- `int split_OMG_Line(OMG_Line_List *list, int line_number, double lat, double lon, double x, double y)`
  - Projects $(x, y)$ onto `line_number` via `get_point_cpa` and replaces the original segment with two collinear sub-segments meeting at `(x_split, y_split)`.
- `int extend_OMG_Line(OMG_Line_List *list, int line_number, double lat, double lon, double x, double y)`
  - Finds the CPA of $(x, y)$ along the line's trajectory and replaces the nearer endpoint of `line_number` with `(x_split, y_split)`.
- `int move_OMG_Line_point(OMG_Line_List *list, int line_number, double lat, double lon, double x, double y)`
  - Identifies the endpoint of `line_number` closest to $(x, y)$ and updates every line in `list` sharing that exact vertex to the new coordinates $(x, y)$, preserving connected polyline vertices.
- `int join_OMG_Lines(OMG_Line_List *list, int line_number, double lat, double lon, double x, double y)`
  - Snaps the nearest endpoint of the closest other line in `list` to the selected endpoint of `line_number`.
- `int reorder_OMG_Lines(OMG_Line_List *list, int direction)`
  - Swaps `selected_line` with its neighbor at `selected_line + direction` (wrapping around list boundaries).
- `int get_line_intersection(OMG_Line *l1, OMG_Line *l2, double *x, double *y)` & `int clip_OMG_Lines(OMG_Line_List *list, OMG_Line *clip_line)`
  - Computes the intersection of two line segments and verifies it lies on both segments; `clip_OMG_Lines` truncates the nearer endpoint of every line in `list` that intersects `clip_line`.

## How It Fits Into the OMG Architecture

`omg_line` is included directly in **`JV_global.h`** to provide interactive survey line planning and editing inside **JView (`code/JV/`)**, and in **`line_export`** (`code/line/line_export.c`) to export binary `.lines` plans into ASCII waypoints and shipboard navigation formats.
