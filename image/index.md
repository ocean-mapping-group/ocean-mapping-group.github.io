---
layout: default
title: Raster Image Processing (image)
parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 6
has_children: true
---

# Image & Raster Processing Tools (`image`)

The `image` subsystem (`code/image/`) provides 52 command-line utilities for manipulating, reprojecting, mosaicking, filtering, classifying, and converting 8-bit greyscale and 32-bit floating-point (`.r4`) `OMG1` (`JHC_header` / ACRES) raster arrays, multibeam water-column echograms (`.vert_prof`, `.wcim`), and satellite/airborne remote sensing imagery.

## Tool Categories

### 1. Contrast Stretching, Color Composites & Radial/Cloud Filtering
* **[`stretchacres`](stretchacres.html)** — Stretches 8-bit `OMG1` arrays (`.vert_prof`, `.8bit`, `.mos`), applies piecewise-linear or dB curves, draws borders/fixes, and exports Netpbm `.pgm` or `.ppm` images.
* **[`makecolcomp`](makecolcomp.html)** — Combines three 8-bit `OMG1` band files (`-red`, `-green`, `-blue`) into an 8-bit 3-3-2 RGB composite or exports the 256-entry RGB colormap.
* **[`removeRadial`](removeRadial.html)** — Compensates radial illumination drop-off (vignetting/hotspot) around a specified pixel center using additive or multiplicative power laws.
* **[`removecloud`](removecloud.html)** & **[`replacecloud`](replacecloud.html)** — Extracts and restores bright cloud pixels (`> thresh`) around spatial filtering operations.

### 2. Resampling, Cropping & Geometric Transformation
* **[`subimage`](subimage.html)** — Extracts rectangular sub-grids by pixel coordinates (`-left_x`, `-top_y`) or geographic center (`-geocentre`) from 8-bit or `.r4` `OMG1` rasters.
* **[`decimate`](decimate.html)** & **[`decr4`](decr4.html)** — Downsamples 8-bit (`decimate`) or 32-bit float (`decr4`) `OMG1` grids by integer factors using boxcar mean, minimum (`-lowest`), or shoal-biased (`-shoal_bias`) rules.
* **[`expand`](expand.html)** & **[`expandr4`](expandr4.html)** — Upsamples (or decimates) 8-bit (`expand`) or 32-bit float (`expandr4`) `OMG1` grids using block replication or masked bilinear interpolation (`-interp -mask`).
* **[`changeAspect`](changeAspect.html)** — Rescales horizontal and vertical dimensions of 8-bit or `.r4` grids independently (`-xfactor`, `-yfactor`, `-xdim`, `-ydim`).
* **[`rotateimage`](rotateimage.html)** — Rotates 8-bit `OMG1` images by 90° clockwise, flips horizontally (`-hflip`), or rotates by an arbitrary angle (`-rotate_angle`).
* **[`distortImage`](distortImage.html)** — Warps and registers an 8-bit `OMG1` image onto a reference image (`-ref`) or Mercator grid (`-geo`) using a 2-point control file.
* **[`shoalBias`](shoalBias.html)** & **[`removeOverplot`](removeOverplot.html)** — Downsamples `.r4` bathymetric DTMs to shoal-biased hydrographic bins while tracking exact sub-bin `(lat, lon)` sounding offsets.
* **[`getShifts`](getShifts.html)** — Computes per-column vertical valid-data bounds for compacting oblique strip mosaics.

### 3. Mosaicking, Map Patching & Tiling
* **[`patchArea`](patchArea.html)** & **[`patchArea_MercOnly`](patchArea_MercOnly.html)** — Reprojects and patches multiple georeferenced 8-bit or `.r4` (`.gz`) `OMG1` mapsheets across projections with automatic anti-alias downsampling.
* **[`pastemos`](pastemos.html)** & **[`paster4`](paster4.html)** — Pastes 8-bit (`pastemos`) or `.r4` float (`paster4`) sub-images onto a composite canvas, including 24-bit `.ppm` Magnitude/Azimuth color wheels and Temperature/Salinity encoding.

### 4. Polygon Masking & Stenciling
* **[`mask_make`](mask_make.html)**, **[`jb_mask_make`](jb_mask_make.html)** & **[`mask_ray`](mask_ray.html)** — Generates 8-bit filled polygon mask files from ASCII vertex lists using scanline parity or 4-way ray-casting.
* **[`stencil`](stencil.html)** & **[`stencilIPV`](stencilIPV.html)** — Masks 8-bit, `.r4` float, or multi-plane `.ipv` images using an 8-bit mask and optional underlay image (`-under`).

### 5. Multibeam Water Column & Acoustic Coverage Modeling
* **[`TAtoXZ`](TAtoXZ.html)** — Projects SM2000 water-column Time-Angle (`.TA_inten`, `.TA_phase`) frames into Cartesian across-track/depth (`.XZ_inten`, `.XZ_phase`) fan coordinates.
* **[`comboTAs`](comboTAs.html)**, **[`comboVPs`](comboVPs.html)** & **[`patchTA`](patchTA.html)** — Combines and resamples `.time_angle`, `.vert_prof`, and `.wcim` water-column files into unified along-track echograms.
* **[`stackPIEs`](stackPIEs.html)** — Stacks and averages sliding windows of `.wcim` water-column fan images with graticules, timestamps, tide shifts, and curtain slices.
* **[`projectForwardVideo`](projectForwardVideo.html)** — Orthorectifies shipboard forward-looking video frames onto a sea-surface Mercator grid for correlation with water-column data.
* **[`embedBeamSpacing`](embedBeamSpacing.html)** & **[`showCoverage`](showCoverage.html)** — Simulates multibeam beam footprints, dual-swath/multi-sector spacing, and 2D sonar equation SNR coverage.

### 6. Spectral, Histogram & Backscatter Classification Analysis
* **[`fft2dimage`](fft2dimage.html)** — Performs single-window or sliding-window 2D FFT spectral sandwave analysis on `.r4` bathymetric DTMs, outputting wavelength (`.wav.r4`), azimuth (`.azi.r4`), and amplitude (`.mag.r4`) maps.
* **[`MSpecBS_Xplot`](MSpecBS_Xplot.html)** — Cross-plots multi-frequency backscatter mosaics (`*.mos`) constrained by bathymetry (`-dep`) and maps 2D spectral clusters (`-class_mask`).
* **[`classify`](classify.html)** — Classifies seafloor backscatter from three angular-sector mosaics (`.nad`, `.mea`, `.tai`) into intensity (`.int`), slope (`.slp`), and 16-class (`.cls`) maps.
* **[`histimage`](histimage.html)** — Extracts normalized 256-bin histograms across up to 10 rectangular sub-regions.

### 7. Format Conversion & Satellite / SAR Processing
* **[`8bit2acres`](8bit2acres.html)**, **[`PCItoJHC`](PCItoJHC.html)** & **[`OMGtoPS`](OMGtoPS.html)** — Converts raw 8-bit/float, PGM/PPM, PCI/CASI (`.COR`), SIF, and World File (`.tfw`) rasters to `OMG1` and exports Encapsulated PostScript (`.eps`).
* **[`jplSARtojhc`](jplSARtojhc.html)** — Imports JPL AIRSAR / SIR-C VAX float and Compressed Stokes Matrix (`-CM`) polarimetric radar imagery into `.r4` `OMG1` files.
* **[`landsat2acres`](landsat2acres.html)**, **[`czcs2acres`](czcs2acres.html)**, **[`addheader`](addheader.html)**, **[`readheader`](readheader.html)** & **[`control_points`](control_points.html)** — De-interleaves and georeferences 4-band BIL Landsat MSS and Nimbus-7 CZCS imagery.
* **[`destripe`](destripe.html)**, **[`fix_zigzag`](fix_zigzag.html)**, **[`lsfilter`](lsfilter.html)**, **[`add_hilo`](add_hilo.html)** & **[`limit_change`](limit_change.html)** — Removes 6-detector striping and 12-line mirror-sweep zigzag artifacts from ACRES Landsat imagery.
