---
layout: default
title: Processing Workflows & Guides
nav_order: 2
has_children: true
---

# Processing Workflows & Guides

This section provides step-by-step guides and architectural documentation for graduate students processing multibeam sonar, sidescan, ADCP, scientific echosounder, sub-bottom, and bathymetric LiDAR data with the Ocean Mapping Group (OMG) software suite, as well as structured reference workflows for LLM-assisted sonar data processing and troubleshooting.

---

## Core Multibeam, Gridding & Mosaicking Workflows

1. **[OMG File Formats & Directory Architecture](file-formats-and-architecture.html)**  
   Understand the `OMG_HDCS` binary file ecosystem (`.merged`, `.nav`, `.orientation`, `.param`, `.ss`, `.blank`, `.r4`, `.mos`), coordinate and depth sign conventions, and standard survey directory layouts (`raw/`, `merged/`, `decnav/`, `ss/`).
2. **[Kongsberg `.kmall` & `.kmwcd` Unraveling Workflow](kongsberg-kmall-unraveling.html)**  
   Complete pipeline for modern Kongsberg SIS 5.x systems (EM2040, EM2042, EM2040C, EM712, EM304, EM124), covering single-line, serial batch, and GNU Parallel processing (`unravel_KMALL_2500m_RevHplus_netatt2_parallel`), multi-sensor navigation/attitude selection, refraction/ray-tracing (`newMergeAtt`), tides, and backscatter (`makess`).
3. **[Kongsberg `.all` & `.wcd` Legacy Unraveling Workflow](kongsberg-all-unraveling.html)**  
   Complete pipeline for legacy Kongsberg SIS 3.x/4.x systems (EM120, EM122, EM300, EM302, EM710, EM1002, EM3000, EM3002, EM2040 `.all`) using `RTlite`, `bunravel`, and `deTVG` empirical TVG removal.
4. **[Bathymetric Gridding, Swath Editing & Sidescan Mosaicking](gridding-and-mosaicking.html)**  
   How to calculate survey bounds (`getBounds`), build blank raster headers (`make_blank`), grid bathymetry (`tor4`, `weigh_grid`), generate sun-illuminated imagery (`r4to8bit`, `addSUN`), clean outlier beams interactively (`swathed -locate`), and build sidescan/backscatter mosaics (`glfill`, `tomos`, `mos2`).
5. **[Troubleshooting & Diagnostics Reference](troubleshooting-and-diagnostics.html)**  
   Symptom-cause-fix decision tables for common errors in Kongsberg unraveling, lever-arm offsets, attitude sensor selection, GPS week rollovers, water column pointer alignment, and gridding/mosaicking.
6. **[QGIS Plugin & GIS Integration Architecture](qgis-and-gis-integration.html)**  
   Existing GIS export tools (`r4toESRI`, `dumpXYZ`), exact 1024-byte `JHC_header` binary layout for zero-copy GDAL `.vrt` loading in QGIS, and the Qimera/HIPS-style **OMG Multibeam Survey & Processing Monitor** QGIS plugin.

---

## Specialized Acoustic & Multi-Vendor Workflows

7. **[ADCP Current & Backscatter Processing Workflow](adcp-processing-workflow.html)**  
   Complete workflow for Teledyne RDI / WinADCP / VMDAS and Kongsberg EC150 / generic ADCP datasets (`readADCP`, `readWinADCP`, `readGenericADCP`, `mapGenericADCP`, `combineMultiADCP`, `calc_ellipse`, `normalize_adcp`, `makeVectorPlot`, `plotADCPgridcurrents`, `makeTSmap`).
8. **[Simrad EK60, EK80 & EA600 Scientific Echosounder Workflow](ek60-ek80-echosounder-workflow.html)**  
   Unpacking and FM pulse compression of Simrad `.raw` files (`readEA600`, `ek80_parse_proc`), interactive 6-window inspection (`EKlook`), batch spectral Angular Response Curve extraction (`BatchProcEK`), sphere/arc calibration (`comboCalibEK_ARCs`), and MVP/EK60 peak correlation (`ExtractMVP_EK60_Peaks`).
9. **[GeoSwath+ Interferometric & Towed Sidescan Workflows](geoswath-and-sidescan-workflows.html)**  
   End-to-end processing for GeoAcoustics GeoSwath+ (`.swa`, `.rdf`, `.gsf`, `.xtf`), Submetrix / SEA Systems 2000 (`readSWA`, `readSUB2K`, `convSUB16`), Simrad SM2000 (`sm2000toOMG`), EdgeTech `.jsf` (`jsf2glo`, `jsf2omg`), Klein `.sdf`/`.xtf` (`sdf2omg`, `klein2omg`), and GLORIA `.ss` sidescan radiometric/geometric conditioning (`bpick`, `glslant`, `destripe`, `glgain`, `glfill`).
10. **[Multi-Vendor Multibeam Converters Workflow](multibeam-vendor-converters-workflow.html)**  
    How to convert Teledyne Reson 7k/8k (`7k2omg`, `8k2omg`, `8101toOMG`), R2Sonic (`r2sonic2omg`), Furuno WASSP (`wassp2omg`), L-3 / ELAC XSE (`xse2omg`, `refoELAC`), SeaBeam 2000/2100 (`unravelSB2K`, `unravelSB2100`), Kongsberg Mesotech M3 (`M3imb2omg`), and Lowrance (`.sl2` via `lowrance2omg`) into OMG `.merged` files.
11. **[Sub-Bottom Profiler (Knudsen / SEG-Y) & Optech Bathymetric LiDAR Workflows](subbottom-and-lidar-workflows.html)**  
    Processing Knudsen 320/3260 `.keb` and SEG-Y chirp sub-bottom profiles (`knud2glo`, `upKnudSEGY`, `readSB_SEGY`, `makeSeisPlot`, `pickSS`, `mergeOtherSonarData`) and Optech SHOALS airborne bathymetric LiDAR waveforms and depths (`refoOptech`, `refoLAS`, `readINW`, `processSHOALSdepths`, `validateSHOALS`).
