---
layout: default
title: shptree
parent: Shapelib GIS Library & Tools (shapelib-1.3.0a2)
nav_order: 12
module_name: shptree
source_path: code/shapelib-1.3.0a2/shptree.c
category: GIS & ESRI Shapefile Library / Tools
input_formats: [".shp", ".shx", ".qix (spatial quadtree index)"]
output_formats: [".qix (spatial quadtree index)"]
related_tools: ["shptreedump", "shpopen", "safileio"]
---

# shptree (`shptree.c`)

## Overview

`shptree.c` (`code/shapelib-1.3.0a2/shptree.c`, 1,035 lines, Revision 1.12) implements the **Shapelib Spatial Quadtree Indexing and Bounding-Box Query API**, authored by Frank Warmerdam.

When querying large shapefiles (containing tens of thousands of soundings, tracklines, or coastline polygons) for features intersecting a geographic viewport, scanning every shape in `.shp` is $O(N)$. `shptree.c` constructs a hierarchical spatial tree (`SHPTree` / `SHPTreeNode`) that recursively splits each node's bounding box along its longest axis (`SHPTreeSplitBounds`) using a $55\%$ overlap ratio (`SHP_SPLIT_RATIO = 0.55`). Shapes that fit completely inside a child subnode (`SHPCheckObjectContained`) are pushed down the tree (up to `MAX_DEFAULT_TREE_DEPTH = 12` levels), while shapes straddling a split boundary remain stored in the parent node. Furthermore, `shptree.c` supports serializing the quadtree to disk in MapServer/GDAL **`.qix`** binary spatial index format (`SHPWriteTree`) and searching `.qix` files directly on disk without loading the entire tree into memory (`SHPSearchDiskTree`).

---

## Core Data Structures (`shapefil.h`)

### `SHPTreeNode` & `SHPTree`

```c
#define MAX_SUBNODE 4
#define MAX_DEFAULT_TREE_DEPTH 12

typedef struct shape_tree_node
{
    double  adfBoundsMin[4];                 /* Node minimum [X, Y, Z, M] bounds */
    double  adfBoundsMax[4];                 /* Node maximum [X, Y, Z, M] bounds */
    int     nShapeCount;                     /* Number of shapes stored directly at this node */
    int     *panShapeIds;                    /* Array of 0-based shape IDs [nShapeCount] */
    SHPObject **papsShapeObj;                /* Optional cached SHPObject pointers (or NULL) */
    int     nSubNodes;                       /* Number of active child subnodes (0..MAX_SUBNODE) */
    struct shape_tree_node *apsSubNode[MAX_SUBNODE];
} SHPTreeNode;

typedef struct
{
    SHPHandle    hSHP;                       /* Associated shapefile handle */
    int          nMaxDepth;                  /* Maximum tree depth (auto-estimated <= 12 if 0) */
    int          nDimension;                 /* Spatial dimensions indexed (typically 2) */
    int          nTotalCount;                /* Total shapes indexed in tree */
    SHPTreeNode *psRoot;                     /* Root quadtree node covering full shapefile bounds */
} SHPTree;
```

---

## Public API Reference

| Function | Signature / Description |
| :--- | :--- |
| `SHPCreateTree` | `SHPTree *SHPCreateTree(SHPHandle hSHP, int nDimension, int nMaxDepth, double *padfBoundsMin, double *padfBoundsMax)`: Allocates a `SHPTree`, automatically estimates `nMaxDepth` (targeting ~8 shapes per leaf, capped at `MAX_DEFAULT_TREE_DEPTH = 12`) if `nMaxDepth == 0`, initializes `psRoot` from `hSHP`'s global bounds, and inserts all shapes in `hSHP` via `SHPTreeAddShapeId()`. |
| `SHPDestroyTree` | `void SHPDestroyTree(SHPTree *hTree)`: Recursively frees all `SHPTreeNode`s (`SHPDestroyTreeNode`) and the `SHPTree` handle. |
| `SHPTreeAddShapeId` | `int SHPTreeAddShapeId(SHPTree *hTree, SHPObject *psObject)`: Inserts `psObject->nShapeId` into `hTree->psRoot` via `SHPTreeNodeAddShapeId()`, splitting nodes along their longest dimension (`SHP_SPLIT_RATIO = 0.55`) until `nMaxDepth` is reached or `psObject` no longer fits within a single child subnode. |
| `SHPTreeTrimExtraNodes` | `void SHPTreeTrimExtraNodes(SHPTree *hTree)`: Recursively prunes empty leaf subnodes (`nShapeCount == 0 && nSubNodes == 0`) from the tree after construction. |
| `SHPTreeFindLikelyShapes` | `int *SHPTreeFindLikelyShapes(SHPTree *hTree, double *padfBoundsMin, double *padfBoundsMax, int *pnShapeCount)`: Traverses `hTree` (`SHPTreeCollectShapeIds`), collecting all `nShapeId`s from nodes whose bounding boxes overlap `[padfBoundsMin, padfBoundsMax]`, sorts the resulting IDs in ascending order via `qsort(panShapeList, ..., SHPCompareInts)`, and returns the newly allocated `int *` array. |
| `SHPCheckBoundsOverlap` | `int SHPCheckBoundsOverlap(double *padfBox1Min, double *padfBox1Max, double *padfBox2Min, double *padfBox2Max, int nDimension)`: Returns `TRUE` (`1`) if two `nDimension`-dimensional bounding boxes overlap, or `FALSE` (`0`) if disjoint. |
| `SHPWriteTree` | `int SHPWriteTree(SHPTree *hTree, const char *pszFilename)`: Serializes `hTree` to a binary `.qix` spatial index file (3-byte `"SQT"` magic header, endian tag, version `1`, total shape count, max depth, and recursive node records). |
| `SHPSearchDiskTree` | `int *SHPSearchDiskTree(FILE *fp, double *padfBoundsMin, double *padfBoundsMax, int *pnShapeCount)`: Queries an open `.qix` binary file directly on disk (`SHPSearchDiskTreeNode`), returning a sorted `int *` array of candidate shape IDs without building an in-memory `SHPTree`. |

---

## Architectural Fit

`shptree.o` provides fast 2D/3D spatial indexing for Shapelib-based tools and is exercised directly by the [`shptreedump`](shptreedump.md) CLI utility.
