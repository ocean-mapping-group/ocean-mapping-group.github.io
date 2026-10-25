---
layout: default
title: shptreedump
parent: ESRI Shapefile C Library (shapelib-1.3.0a2)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 13
tool_name: shptreedump
source_path: code/shapelib-1.3.0a2/shptreedump.c
category: GIS & ESRI Shapefile Library / Tools
input_formats:
- .shp
- .shx
- .qix (spatial quadtree index)
output_formats:
- .qix (spatial quadtree index)
- STDOUT quadtree hierarchy or search results
related_tools:
- shptree
- shpdump
- shpopen
---

# shptreedump

## Overview

`shptreedump` (`code/shapelib-1.3.0a2/shptreedump.c`) is a command-line spatial indexing, inspection, and query utility authored by Frank Warmerdam that exercises the [`shptree`](shptree.html) quadtree API (`SHPCreateTree`, `SHPTreeTrimExtraNodes`, `SHPWriteTree`, `SHPTreeFindLikelyShapes`, and `SHPSearchDiskTree`).

It serves three primary functions:
1. **ASCII Tree Visualization**: Builds an in-memory quadtree for a `.shp` file and prints a hierarchical, indented S-expression dump of every `SHPTreeNode`, its bounding box, and the shape IDs (or full vertex geometries with `-v`) stored at that node.
2. **Binary `.qix` Index Generation (`-o`)**: Builds and trims a quadtree for a `.shp` file and writes it out to a binary `.qix` spatial index file via `SHPWriteTree()`.
3. **Bounding-Box Spatial Search (`-search`)**: Queries either an in-memory quadtree (built on-the-fly from `<shp_file>`) or an existing on-disk `.qix` index file (`-i <index.qix>`) for all shapes intersecting `<xmin> <ymin> <xmax> <ymax>`.

---

## Usage

```bash
shptreedump [-maxdepth <n>] [-search <xmin> <ymin> <xmax> <ymax>] \
            [-v] [-o <indexfilename.qix>] [-i <indexfilename.qix>] \
            <shp_file>
```

### Command-Line Options

| Flag | Arguments | Description |
| :--- | :--- | :--- |
| `-maxdepth` | `<n>` | Maximum depth of the constructed quadtree (default `0`, which instructs `SHPCreateTree()` to auto-select a depth up to `MAX_DEFAULT_TREE_DEPTH = 12` targeting ~8 shapes per leaf node). |
| `-v` | *(none)* | **Verbose / Expand Shapes**: When dumping the tree hierarchy, reads and prints the full `ShapeId`, `Min`/`Max` bounds, and `Vertex[i]` coordinates of every shape (`EmitShape()`) instead of only printing integer shape IDs. |
| `-o` | `<indexfilename.qix>` | Writes the constructed and trimmed quadtree to a binary `.qix` spatial index file via `SHPWriteTree()` instead of dumping ASCII text to `stdout`. |
| `-search` | `<xmin> <ymin> <xmax> <ymax>` | Executes a 2D spatial bounding-box search. Validates `xmin <= xmax` and `ymin <= ymax`. |
| `-i` | `<indexfilename.qix>` | Used together with `-search`: searches the pre-built binary `.qix` file directly on disk via `SHPSearchDiskTree()` and prints `Result: <id1> <id2> ...` without needing to open `<shp_file>`. |
| `<shp_file>` | *(positional)* | Path/basename of the input ESRI Shapefile (required unless `-search` is combined with `-i <indexfilename.qix>`). |

---

## Internal Two-Phase Spatial Search (`SHPTreeNodeSearchAndDump`)

When `-search <xmin> <ymin> <xmax> <ymax>` is run against `<shp_file>` (without `-i`):
1. **Phase 1 — Quadtree Node Filtering (`SHPTreeFindLikelyShapes`)**:
   - Collects a sorted list (`panHits`) of `nShapeCount` candidate shape IDs stored in any `SHPTreeNode` whose node bounding box overlaps the search rectangle.
2. **Phase 2 — Exact Shape Bounding-Box Verification (`SHPCheckBoundsOverlap`)**:
   - Because a quadtree node's bounding box is larger than the individual shapes stored within it, `SHPTreeNodeSearchAndDump()` reads each candidate `psObject = SHPReadObject(hTree->hSHP, panHits[i])` and tests `SHPCheckBoundsOverlap(padfBoundsMin, padfBoundsMax, &(psObject->dfXMin), &(psObject->dfXMax), hTree->nDimension)`:
     - If disjoint: prints `Shape <id>: not in area of interest, but fetched.` (illustrating a Phase 1 false positive).
     - If overlapping: prints `Shape <id>: appears to be in area of interest.`.

---

## Example Workflows

```bash
# 1. Dump an ASCII representation of a shapefile's quadtree (limited to 4 levels)
shptreedump -maxdepth 4 nav_tracks.shp

# 2. Generate a binary .qix spatial index file and query it on disk
shptreedump -o nav_tracks.qix nav_tracks.shp
shptreedump -i nav_tracks.qix -search -63.60 44.60 -63.50 44.70
```
