---
layout: default
title: shptest
parent: ESRI Shapefile C Library (shapelib-1.3.0a2)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 11
tool_name: shptest
source_path: code/shapelib-1.3.0a2/shptest.c
category: GIS & ESRI Shapefile Library / Tools
input_formats:
- CLI integer test ID (0..13)
output_formats:
- test0.shp .. test13.shp (.shp and .shx)
related_tools:
- shpdump
- shpcreate
- shpadd
- shpopen
---

# shptest

## Overview

`shptest` (`code/shapelib-1.3.0a2/shptest.c`) is a regression test generator authored by Frank Warmerdam that programmatically synthesizes sample ESRI Shapefiles (`test0.shp` through `test13.shp`) covering every geometry type supported by the ESRI Shapefile specification (`Null`, `Point`, `PointZ`, `PointM`, `MultiPoint`, `MultiPointZ`, `MultiPointM`, `Arc`, `ArcZ`, `ArcM`, `Polygon`, `PolygonZ`, `PolygonM`, and `MultiPatch`).

It is invoked by the `stream2.sh` test script (`make test` in `code/shapelib-1.3.0a2/Makefile`) to verify that `SHPCreate()`, `SHPCreateObject()`, `SHPWriteObject()`, `SHPReadObject()`, and [`shpdump`](shpdump.html) accurately round-trip 2D, 3D (`Z`), Measured (`M`), multi-part ring, and `MultiPatch` part-type (`SHPP_RING` / `SHPP_INNERRING`) geometries across big-endian and little-endian architectures.

---

## Usage

```bash
shptest <test_number>
```

### Supported `<test_number>` Values (`0`–`13`)

| `<test_number>` | Output File | `shapefil.h` Type | Internal Generator Function | Geometry Synthesized |
| :---: | :--- | :--- | :--- | :--- |
| `0` | `test0.shp` | `SHPT_NULL` (`0`) | `Test_WritePoints()` | 2 null shapes created via `SHPCreateObject(SHPT_NULL, ...)`. |
| `1` | `test1.shp` | `SHPT_POINT` (`1`) | `Test_WritePoints()` | 2 2D points at `(1, 2)` and `(10, 20)`. |
| `2` | `test2.shp` | `SHPT_POINTZ` (`11`) | `Test_WritePoints()` | 2 3D+M points at `(1, 2, 3, 4)` and `(10, 20, 30, 40)`. |
| `3` | `test3.shp` | `SHPT_POINTM` (`21`) | `Test_WritePoints()` | 2 2D+M points at `(1, 2, M=4)` and `(10, 20, M=40)`. |
| `4` | `test4.shp` | `SHPT_MULTIPOINT` (`8`) | `Test_WriteMultiPoints()` | 3 MultiPoint shapes, each containing 4 vertices. |
| `5` | `test5.shp` | `SHPT_MULTIPOINTZ` (`18`) | `Test_WriteMultiPoints()` | 3 3D+M MultiPointZ shapes, each containing 4 vertices. |
| `6` | `test6.shp` | `SHPT_MULTIPOINTM` (`28`) | `Test_WriteMultiPoints()` | 3 2D+M MultiPointM shapes, each containing 4 vertices. |
| `7` | `test7.shp` | `SHPT_ARC` (`3`) | `Test_WriteArcPoly()` | 3 single-part closed 5-vertex boxes + 1 3-part shape (15 vertices). |
| `8` | `test8.shp` | `SHPT_ARCZ` (`13`) | `Test_WriteArcPoly()` | 3D+M polyline version of Test 7. |
| `9` | `test9.shp` | `SHPT_ARCM` (`23`) | `Test_WriteArcPoly()` | 2D+M polyline version of Test 7. |
| `10` | `test10.shp` | `SHPT_POLYGON` (`5`) | `Test_WriteArcPoly()` | 3 single-ring squares + 1 3-ring polygon ($100\times 100$ outer ring with two interior hole rings at `anPartStart = {0, 5, 10}`). |
| `11` | `test11.shp` | `SHPT_POLYGONZ` (`15`) | `Test_WriteArcPoly()` | 3D+M polygon version of Test 10. |
| `12` | `test12.shp` | `SHPT_POLYGONM` (`25`) | `Test_WriteArcPoly()` | 2D+M polygon version of Test 10. |
| `13` | `test13.shp` | `SHPT_MULTIPATCH` (`31`) | `Test_WriteArcPoly()` | 3D surface MultiPatch version of Test 10 with explicit `anPartType = {SHPP_RING, SHPP_INNERRING, SHPP_INNERRING}`. |

---

## Internal Helper Functions

1. **`Test_WritePoints(int nSHPType, const char *pszFilename)`**:
   - Creates `pszFilename` with `SHPCreate()`, writes two 1-vertex shapes at `(1, 2, 3, 4)` and `(10, 20, 30, 40)`, and closes the handle.
2. **`Test_WriteMultiPoints(int nSHPType, const char *pszFilename)`**:
   - Creates `pszFilename` and writes 3 `MultiPoint` shapes (`iShape = 0..2`), each having 4 points with coordinates offset by `iShape * 10 + i`.
3. **`Test_WriteArcPoly(int nSHPType, const char *pszFilename)`**:
   - Writes 3 simple 5-vertex $1\times 1$ unit squares, followed by a 4th multi-part shape of 15 vertices split across 3 parts (`anPartStart = {0, 5, 10}`): an outer $100\times 100$ boundary (`(0,0)` to `(100,100)`) and two inner rectangular rings (`(10,20)-(30,40)` and `(60,20)-(90,40)`).
