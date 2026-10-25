---
layout: default
title: Bathymetric Gridding & Export (grid)
parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 1
has_children: true
---

# Grid Tools

The `grid` suite (`code/grid/`) contains **76 command-line utilities** for creating, filtering, interpolating, differencing, contouring, projecting, and exporting 2D bathymetric and backscatter grids (`.r4`, `.8bit`, `.sun`), 3D oceanographic/sound-velocity fields, and hydrodynamic model meshes.

---

## 1. Core Gridding, Accumulation & Surface Fitting

Tools for constructing 2D digital elevation models (`.r4`) from multibeam `.merged` files, ASCII XYZ soundings, or finite-element meshes:

| Tool | Description |
|------|-------------|
| [`weigh_grid`](weigh_grid.html) | Primary OMG inverse-distance / beam-footprint weighted gridding engine for `.merged` and ASCII XYZ data. |
| [`addWG`](addWG.html) | Combines intermediate `.r4_weights` and `.r4_weight_depth` accumulator files from multiple `weigh_grid` runs. |
| [`updateArray`](updateArray.html) | Recomputes a normalized `.r4` depth grid from `.r4_weights` and `.r4_weight_depth` accumulators. |
| [`addDTM`](addDTM.html) | Merges or splices multiple `.r4` digital terrain models together. |
| [`surface`](surface.html) | Fits a continuous minimum-curvature / adjustable-tension biharmonic spline surface (Smith & Wessel, 1990) to XYZ triples. |
| [`make_blank`](make_blank.html) | Creates an initialized blank `.r4` or `.8bit` mapsheet with specified projection and bounds. |
| [`make_bases`](make_bases.html) | Generates script commands and base mapsheets for tiling a survey area into sub-grids. |
| [`edhead`](edhead.html) | Views and interactively edits the 1024-byte `JHC_header` of `.r4` and `.8bit` grid files. |

---

## 2. Grid Filtering, Interpolation & Gap Filling

Tools for smoothing, cleaning, interpolating across holidays, and repairing `.r4` and `.8bit` arrays:

| Tool | Description |
|------|-------------|
| [`r4filter`](r4filter.html) | Applies spatial convolution, mean, median, or Gaussian smoothing filters to `.r4` grids. |
| [`r4interp`](r4interp.html) | Interpolates across unpopulated nodata gaps in an `.r4` grid using radial/directional search. |
| [`fillGap`](fillGap.html) | Fills small holiday gaps in `.r4` or `.8bit` grids by local neighborhood interpolation. |
| [`fixarray`](fixarray.html) | Cleans spikes, remaps nodata values, scales, or clips `.r4` floating-point grids. |
| [`maskarray`](maskarray.html) | Masks an `.r4` or `.8bit` grid using a polygon or companion mask raster. |
| [`patchWORLD`](patchWORLD.html) | Patches higher-resolution `.r4` grids into a background regional or global bathymetric grid. |

---

## 3. Grid Differencing, Quality Control & Shoal Detection

Tools for comparing surfaces, evaluating multibeam sounding residuals, and hydrographic shoal/cost analysis:

| Tool | Description |
|------|-------------|
| [`differ`](differ.html) | Computes the cell-by-cell vertical difference between two `.r4` bathymetric grids (including cross-projection regridding). |
| [`diff8bit`](diff8bit.html) | Computes pixel-by-pixel differences between two `.8bit` greyscale grids. |
| [`subtractSurface`](subtractSurface.html) | Subtracts a bilinearly interpolated `.r4` reference surface from every beam in `.merged` survey lines and stores residuals in-place. |
| [`DTMreject`](DTMreject.html) | Flags outlying beams in `.merged` files that deviate beyond a threshold from a reference `.r4` DTM. |
| [`showError`](showError.html) | Creates an 8-bit hit-count raster mapping the spatial density of rejected/flagged beams across a survey sheet. |
| [`correlate`](correlate.html) | Computes spatial cross-correlation between two grids to diagnose horizontal positioning offsets. |
| [`findShoals`](findShoals.html) | Extracts hydrographic shoal soundings and local depth minima from `.r4` grids. |
| [`calcCost`](calcCost.html) | Computes survey cost/efficiency or terrain ruggedness metrics over a bathymetric grid. |

---

## 4. Terrain Morphology, Profiles & Sub-Bottom Horizons

Tools for watershed delineation, downslope flow routing, cross-section extraction, and seismic/sub-bottom horizon picking:

| Tool | Description |
|------|-------------|
| [`defineDownSlope`](defineDownSlope.html) | Computes steepest-descent downslope flow vectors and gradient paths across an `.r4` bathymetric surface. |
| [`defineWatershed`](defineWatershed.html) | Delineates drainage basins and watershed catchments on a bathymetric or topographic `.r4` grid. |
| [`extractProfile`](extractProfile.html) | Extracts depth/elevation cross-sections from an `.r4` grid along user-defined waypoints. |
| [`plotProfile`](plotProfile.html) | Formats and plots extracted bathymetric or sub-bottom profiles as 8-bit raster images. |
| [`findHorizon`](findHorizon.html) | Tracks and extracts sub-bottom acoustic reflector horizons from profile rasters. |
| [`makeStrat`](makeStrat.html) | Builds synthetic or interpolated stratigraphic layer grids between acoustic horizons. |

---

## 5. Contouring & Vector Overlay Tools

Tools for generating, sorting, embedding, and exporting bathymetric contours:

| Tool | Description |
|------|-------------|
| [`contgrid`](contgrid.html) | Extracts unsorted binary (`bin_vect`) or ASCII contour line segments from an `.r4` grid. |
| [`sortCont`](sortCont.html) | Chains unsorted `bin_vect` contour segments into continuous polylines grouped by contour level. |
| [`embedCont`](embedCont.html) | Burns vector contour lines into an 8-bit sun-illuminated or colour-coded raster image. |
| [`getdxf`](getdxf.html) | Converts CAD `.dxf` vector polylines and contours into OMG vector format or反之. |

---

## 6. 8-Bit Raster, Sun-Illumination & Image Compositing

Tools for converting floating-point grids into 8-bit display rasters and compositing sun-illuminated imagery:

| Tool | Description |
|------|-------------|
| [`r4to8bit`](r4to8bit.html) | Scales a 32-bit floating-point `.r4` grid into an 8-bit unsigned raster (`.8bit`). |
| [`8bittor4`](8bittor4.html) | Rescales an 8-bit unsigned raster back into a 32-bit floating-point `.r4` grid. |
| [`add8bit`](add8bit.html) | Composites or blends two 8-bit raster images together. |
| [`addSUN`](addSUN.html) | Combines a colour-coded depth image with an 8-bit sun-illuminated shaded-relief image. |
| [`addGain`](addGain.html) | Applies brightness/contrast gain adjustments to 8-bit imagery. |
| [`addstamp`](addstamp.html) | Stamps an annotation, logo, or scale bar onto an 8-bit raster image. |
| [`mix_ci`](mix_ci.html) | Blends colour index (bathymetry) and intensity (backscatter/sun-illumination) rasters into a composite image. |

---

## 7. Format Import & Export Converters

Tools for importing external DEMs, satellite altimetry, and sonar telemetry into OMG `.r4`/`.8bit` formats and exporting to GIS packages:

| Tool | Description |
|------|-------------|
| [`ASCIItoJHC`](ASCIItoJHC.html) | Converts gridded ASCII depth/elevation tables into OMG `JHC_header` (`.r4` / `.8bit`) format. |
| [`r4toASCII`](r4toASCII.html) | Exports an `.r4` or `.8bit` grid to 3-column ASCII XYZ (`lon lat z` or `x y z`) or matrix text. |
| [`r4toESRI`](r4toESRI.html) | Exports an `.r4` or `.8bit` grid to ESRI Binary Grid (`.flt` + `.hdr` + `_prj.adf`) or ESRI ASCII Grid (`.asc`). |
| [`r4toGRASS`](r4toGRASS.html) | Exports an `.r4` grid to GRASS GIS raster format (`.grass_head` + `.grass_data`). |
| [`r4to16bit`](r4to16bit.html) | Converts a 32-bit `.r4` grid into a 16-bit integer binary array. |
| [`tifftor4`](tifftor4.html) | Reads TIFF image metadata via `libtiff` and initializes a corresponding `.r4` grid header. |
| [`SWtoJHC`](SWtoJHC.html) | Imports Sandwell & Smith predicted satellite-altimetry bathymetry grids into `.r4` format. |
| [`SatAlt_to_JHC`](SatAlt_to_JHC.html) | Converts global satellite altimetry gravity/bathymetry grids into OMG `.r4` mapsheets. |
| [`USGS_30sec_to_JHC`](USGS_30sec_to_JHC.html) | Converts USGS 30-arc-second global DEM tiles (`GTOPO30` / `SRTM30`) into `.r4` grids. |
| [`gtopo2ascii`](gtopo2ascii.html) | Extracts ASCII XYZ subsets from `GTOPO30` 16-bit big-endian elevation tiles. |
| [`read_dem`](read_dem.html) | Converts USGS ASCII 7.5-minute/1-degree DEMs or SDTS `.tar` archives to 16-bit binary `.bsq` rasters. |
| [`readUSGS_DEM`](readUSGS_DEM.html) | Converts USGS ASCII/SDTS DEMs to `.bsq` and dumps positive land elevations as `thedata` XYZ points for `weigh_grid`. |
| [`jplto8bit`](jplto8bit.html) | Converts JPL AIRSAR / SIR-C radar imagery into OMG `.8bit` format. |
| [`locateSAR`](locateSAR.html) | Georeferences and resamples synthetic aperture radar (SAR) imagery onto an OMG mapsheet. |
| [`selectcb`](selectcb.html) | Extracts, filters, and Mercator-projects soundings from URI SeaBeam binary files or ASCII lists. |
| [`sm2000toOMG`](sm2000toOMG.html) | Performs digital beamforming and bottom detection on raw Kongsberg Mesotech SM2000 I/Q stave data. |

---

## 8. Coordinate Projections, Synthetic Data & System Diagnostics

Tools for transforming coordinates, generating synthetic multibeam pings, and testing system I/O:

| Tool | Description |
|------|-------------|
| [`convertutm`](convertutm.html) | Batch-converts ASCII coordinate files between Geographic (Lat/Lon), UTM, and New Brunswick Stereographic. |
| [`project`](project.html) | Projects 3-column ASCII `lat lon z` files into Mercator `(x, y, z)` coordinates. |
| [`testutm`](testutm.html) | Interactive calculator for forward/inverse UTM, NB Stereographic, and Mercator coordinate conversions across 6 ellipsoids. |
| [`locate_fix`](locate_fix.html) | Computes pixel row/column coordinates for navigation fixes on a projected mapsheet. |
| [`pickrot`](pickrot.html) | Computes rotated local bounding-box coordinates for skewed survey sheets. |
| [`calcXYZ`](calcXYZ.html) | Computes 3D `(X, Y, Z)` coordinates from range/azimuth/elevation observations. |
| [`makeSynPing`](makeSynPing.html) | Ray-traces synthetic multibeam swaths over an `.r4` bathymetric surface using an `.svp` sound velocity profile. |
| [`synSurface`](synSurface.html) | Inspects and prepares `.r4` grids for synthetic swath generation. |
| [`testmmap`](testmmap.html) | Diagnostic test utility for creating memory-mapped (`mmap`) 8-bit `JHC_header` rasters. |

---

## 9. 3D Oceanographic Models, MVP Sections & Tidal Currents

Tools for processing Moving Vessel Profiler (MVP) casts, 3D ocean circulation models (QUODDY, POM), and ADCP current grids:

| Tool | Description |
|------|-------------|
| [`readQUODDY`](readQUODDY.html) | Reads Dartmouth QUODDY finite-element meshes (`.nod`, `.ele`, `.bat`), harmonic tides/currents, and interpolates `.r4` grids. |
| [`makemesh`](makemesh.html) | Generates finite-element or regular grid mesh wireframes for visualization. |
| [`showModelMesh`](showModelMesh.html) | Exports an ASCII `.mesh.llz` wireframe from curvilinear model `.lat.r4`, `.lon.r4`, and `.mask.r4` grids. |
| [`extractNodeProf`](extractNodeProf.html) | Extracts vertical water-column profiles at curvilinear 3D ocean model nodes. |
| [`convert3D_TSZ_to_SV`](convert3D_TSZ_to_SV.html) | Converts 3D model temperature, salinity, and depth (`T, S, Z`) fields into 3D sound velocity (`SV`) grids. |
| [`extractSVTS`](extractSVTS.html) | Extracts time series of sound velocity profiles from 4D ocean model outputs. |
| [`extractVertSection`](extractVertSection.html) | Slices vertical 2D cross-sections through 3D oceanographic model grids. |
| [`convertSectionUVtoRadTan`](convertSectionUVtoRadTan.html) | Rotates horizontal `(U, V)` current velocity components into along-section and across-section components. |
| [`plotADCPgridcurrents`](plotADCPgridcurrents.html) | Grids and plots vector current arrows from acoustic Doppler current profiler (ADCP) observations. |
| [`combineSeaCast`](combineSeaCast.html) | Combines multiple SeaCast / CTD / MVP water-column casts into a unified profile dataset. |
| [`cutMVPLocationSections`](cutMVPLocationSections.html) | Segments Moving Vessel Profiler (MVP) tow-yo cast locations into cross-channel sections. |
| [`ExtractMVP_EK60_Peaks`](ExtractMVP_EK60_Peaks.html) | Extracts acoustic scattering horizon peaks from co-located MVP and Simrad EK60 split-beam echosounder data. |
