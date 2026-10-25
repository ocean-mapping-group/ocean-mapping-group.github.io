---
layout: default
title: iwc_support
parent: Ian Church (ianc) Tools
nav_order: 13
tool_name: iwc_support
source_path: code/ianc/subr/iwc_support.c
category: Ocean Modeling & Hydrographic Utilities (ianc)
input_formats: ["In-memory C arrays, ZVpair arrays, coordinate/time vectors"]
output_formats: ["2D dynamically allocated arrays, statistical metrics, nearest-neighbor indices"]
related_tools: ["modelAnalysis", "modelMerge", "HycomSSP", "oceanReader", "iwc_water", "iwc_adcp"]
---

# iwc_support

## Description

`iwc_support` (`code/ianc/subr/iwc_support.c` and `code/ianc/subr/iwc_support.h`) is the core mathematical, statistical, spatial/temporal nearest-neighbor indexing, and memory-management utility library for Ian Church's (`ianc`) tools. Created in March 2013, it provides five categories of reusable C functions:

1. **Filename Extension Utilities**: Strip or extract file extensions (`removeEXT`, `getExt`).
2. **2D Dynamic Array Management**: Allocate, populate from 1D NetCDF buffers, and free 2D arrays of `double`, `float`, `int`, and `unsigned char` (`make2D*`, `convert2D`, `free2D*`).
3. **Geophysical & Trigonometric Conversions**: International Gravity Formula 1967 (`gravity`) and degree/radian conversions (`deg2rad`, `rad2deg`).
4. **Descriptive & IHO Error Statistics**: Mean, median, scaled standard deviation, RMSE, min/max, central frequency within a threshold band, and positive/negative outlier frequencies (`mean1`, `median1`, `standarddeviation1`, `rmse1`, `centralFreq`, `posOutlierFreq`, `negOutlierFreq`).
5. **Spatiotemporal & Vertical Nearest-Neighbor Search**: Locate the 1st, 2nd, 3rd, or *N*-th closest spatial node (`closeDist`, `closeDist2`, `closeDist3`, `closeXFloat`), closest timestamp with inverse-distance linear interpolation weights (`closeTime`), and closest depth level (`closeValue`, `closeDepth`, `closeFloat`).

## Public API & Usage

### Header Include

```c
#include "j_watercolumn.h"
#include "iwc_support.h"
```

### Example C Usage

```c
double w1, w2;
/* Find closest model node and 2nd/3rd closest nodes for IDW interpolation */
int n1 = closeDist(obsX, obsY, xNode, yNode, nodelength);
int n2 = closeDist2(obsX, obsY, xNode, yNode, nodelength);
int n3 = closeDist3(obsX, obsY, xNode, yNode, nodelength);

/* Find closest model time step and temporal interpolation weights */
int tIdx = closeTime(obsTime, modelTimes, numTimeSteps, &w1, &w2);

/* Compute 95% confidence (1.96 sigma) standard deviation and RMSE of SVP diffs */
float sd95 = standarddeviation1(sspDiffs, count, 1.96f);
float rmse = rmse1(modelSSP, obsSSP, count);
```

## API Reference

### String & 2D Array Memory Functions

| Function | Signature | Description |
| :--- | :--- | :--- |
| `removeEXT` | `char *removeEXT(char *mystr)` | Returns a newly `malloc`'d copy of `mystr` with the last `.` and extension removed. |
| `getExt` | `const char *getExt(const char *fspec)` | Returns a pointer to the last `.` extension in `fspec` (or `""` if none). |
| `make2DDouble` | `double **make2DDouble(int sizeX, int sizeY)` | Allocates a `sizeX` by `sizeY` zero-initialized (`calloc`) 2D `double` array. |
| `make2DFloat` | `float **make2DFloat(int sizeX, int sizeY)` | Allocates a `sizeX` by `sizeY` zero-initialized 2D `float` array. |
| `make2DInt` | `int **make2DInt(int sizeX, int sizeY)` | Allocates a `sizeX` by `sizeY` zero-initialized 2D `int` array. |
| `make2DUchar` | `unsigned char **make2DUchar(int sizeX, int sizeY)` | Allocates a `sizeX` by `sizeY` zero-initialized 2D `unsigned char` array. |
| `convert2D` | `void convert2D(float *array, float **theArray, int sizeX, int sizeY)` | Copies a flat 1D row-major `float` array (`array[i * sizeY + j]`) into a 2D `theArray[i][j]`. |
| `free2DDouble` / `free2DFloat` / `free2Dint` / `free2Duchar` | `void free2D*(<type> **array, int sizeX)` | Frees all `sizeX` row pointers and the outer array pointer. |

### Geophysical, Math & Statistical Functions

| Function | Signature | Description |
| :--- | :--- | :--- |
| `gravity` | `double gravity(double latitude)` | Computes normal gravitational acceleration (`m/s^2`) at `latitude` (degrees) using the **1967 International Gravity Formula**: `9.780327 * (1 + 0.0053024*sin^2(lat) - 0.0000058*sin^2(2*lat))`. |
| `deg2rad` / `rad2deg` | `double deg2rad(double d)` / `double rad2deg(double r)` | Converts between degrees and radians using `M_PI`. |
| `mean1` | `float mean1(float *array, int n)` | Arithmetic mean of `n` floats. |
| `median1` | `float median1(float *array, int n)` | Sorts `array` in-place via bubble sort and returns the median value. |
| `standarddeviation1` | `float standarddeviation1(float array[], int n, float sigma)` | Sample standard deviation (`sqrt(sum((x - mean)^2) / (n - 1))`) multiplied by scaling factor `sigma` (e.g., `1.0` for 1σ, `1.96` for 95% CI). |
| `rmse1` | `float rmse1(float array[], float vals[], int n)` | Root Mean Square Error `sqrt(sum((array[j] - vals[j])^2) / n)`. |
| `min1` / `max1` | `float min1(float array[], int n)` / `max1(...)` | Minimum or maximum value in a `float` array of length `n`. |
| `minInt` / `maxInt` | `int minInt(int array[], int n)` / `maxInt(...)` | Minimum or maximum value in an `int` array of length `n`. |
| `centralFreq` | `float centralFreq(float array[], float limit, int n)` | Percentage (`0–100%`) of elements strictly within `(-limit, +limit)`. |
| `posOutlierFreq` | `float posOutlierFreq(float array[], float limit, int n)` | Percentage of elements strictly greater than `+limit`. |
| `negOutlierFreq` | `float negOutlierFreq(float array[], float limit, int n)` | Percentage of elements strictly less than `-limit`. |

### Spatial, Temporal & Vertical Indexing Functions

| Function | Signature | Description |
| :--- | :--- | :--- |
| `closeDist` | `int closeDist(double x, double y, float *xNode, float *yNode, size_t nodelength)` | Returns the index `i` of the node minimizing Euclidean distance `sqrt((x - xNode[i])^2 + (y - yNode[i])^2)`. |
| `closeDist2` | `int closeDist2(double x, double y, float *xNode, float *yNode, size_t nodelength)` | Returns the index of the **2nd closest** node to `(x, y)` (used for 3-point inverse-distance weighting in `modelAnalysis`). |
| `closeDist3` | `int closeDist3(double x, double y, float *xNode, float *yNode, size_t nodelength)` | Returns the index of the **3rd closest** node to `(x, y)`. |
| `closeTime` | `int closeTime(double time_of_obs, double *daysStd, size_t timerecs, double *weight1, double *weight2)` | Returns the index `i` of the closest timestamp in `daysStd` and populates inverse time-difference weights `*weight1 = 1 / (time_of_obs - daysStd[i])` and `*weight2 = 1 / (time_of_obs - daysStd[i +/- 1])`. Warns if `difference > 86400` s. |
| `closeValue` | `int closeValue(float level, ZVpair *array, int values_in_array)` | Returns the index in a `ZVpair` sound-velocity array (`j_watercolumn.h`) whose `.depth` is closest to `level`. |
| `closeDepth` | `int closeDepth(double depth, double *array, size_t values_in_array)` | Returns the index in a `double` array closest to `depth`. |
| `closeFloat` | `int closeFloat(float depth, float *array, size_t values_in_array)` | Returns the index in a `float` array closest to `depth`. |
| `closeXFloat` | `int closeXFloat(float depth, float *array, size_t values_in_array, int nPoint)` | Returns the index of the `nPoint`-th closest value in `array` to `depth` (used by `HycomSSP -use_nearest` to step outward from dry land nodes). |

## How It Works

* **3-Node Inverse Distance Weighting Support**: By providing `closeDist()`, `closeDist2()`, and `closeDist3()`, `iwc_support` enables `modelAnalysis` to triangulate any arbitrary transect point or observation coordinate within an unstructured FVCOM mesh without requiring a full spatial quadtree.
* **Temporal Linear Interpolation Weights**: `closeTime()` not only finds the nearest discrete model output timestamp `daysStd[index]`, but also determines whether `time_of_obs` falls before or after `daysStd[index]` and computes the reciprocal time-offset weights `weight1` and `weight2` for bracketing time-step interpolation.
