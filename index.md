---
layout: default
title: Home
nav_order: 1
---

# Ocean Mapping Group (OMG) Multibeam & Acoustic Software Documentation

Welcome to the comprehensive documentation repository for the **University of New Brunswick (UNB) Ocean Mapping Group (OMG)** multibeam sonar, sidescan, ADCP, scientific echosounder, sub-bottom profiler, and bathymetric LiDAR processing software suite.

Developed across three decades of ocean mapping research, this C/X11/Motif codebase provides specialized command-line and interactive utilities for unpacking, calibrating, ray-tracing, editing, gridding, and mosaicking acoustic data—with deep support for **Kongsberg Maritime** systems (`.kmall`, `.kmwcd`, `.all`, `.wcd`, `.raw`), as well as **Teledyne RDI ADCP**, **GeoAcoustics GeoSwath+ / Submetrix 2000**, **Reson SeaBat 7k/8k**, **R2Sonic**, **EdgeTech JSF**, **Klein SDF/XTF**, **Knudsen / SEG-Y**, and **Optech SHOALS LiDAR**.

This documentation is designed for two primary audiences:
1. **Graduate Students & Researchers** who need practical, step-by-step workflows and source-verified reference manuals for processing multibeam bathymetry, backscatter snippets, water column, ADCP currents, and sub-bottom data.
2. **LocalAI / LLM Agents** (via RAG chunking and fine-tuning) assisting researchers with command generation, parameter selection, and sonar processing diagnostics.

---

## Start Here: Processing Workflows & Guides

| Workflow Guide | Systems & Tools Covered |
| :--- | :--- |
| **[1. OMG File Formats & Directory Architecture](workflows/file-formats-and-architecture.html)** | How `.merged`, `.param`, `.nav`, `.orientation`, `.ss_data`, `.16_data`, `.ss`, `.blank`, `.r4`, and `.mos` files work together in `raw/`, `merged/`, `decnav/`, and `ss/`. |
| **[2. Kongsberg `.kmall` & `.kmwcd` Unraveling](workflows/kongsberg-kmall-unraveling.html)** | Complete SIS 5.x workflow (`read_kmall`, `moveOverWCinfo`, `stripNav`, `appendNav`, `mergeNav`, `newMergeAtt`, `makess`, and `unravel_KMALL_2500m_RevHplus_netatt2_parallel`) for EM2040, EM2042, EM2040C, EM712, EM304, and EM124. |
| **[3. Kongsberg `.all` & `.wcd` Legacy Unraveling](workflows/kongsberg-all-unraveling.html)** | Complete SIS 3.x/4.x workflow (`RTlite`, `bunravel`, `deTVG`, `makess -use_deTVG`) for EM120, EM122, EM300, EM302, EM710, EM1002, EM3000, and EM3002. |
| **[4. Bathymetric Gridding, Swath Editing & Mosaicking](workflows/gridding-and-mosaicking.html)** | Building `.r4` bathymetric grids (`getBounds`, `make_blank -float`, `tor4`, `weigh_grid`), sun-illuminated imagery (`r4to8bit`, `addSUN`), interactive swath cleaning (`swathed -locate`), and `.mos` sidescan mosaics (`glfill`, `tomos`, `mos2`). |
| **[5. Troubleshooting & Diagnostics Reference](workflows/troubleshooting-and-diagnostics.html)** | Symptom-cause-resolution lookup tables for echosounder ID errors, missing `.nav`/`.orientation` files, lever-arm sign flips, refraction smiles/frowns, and `make_blank` flag ordering bugs. |
| **[6. QGIS Plugin & GIS Integration Architecture](workflows/qgis-and-gis-integration.html)** | Zero-copy GDAL `.vrt` loading for `.r4`/`.sun`/`.8bit`/`.mos` rasters, `r4toESRI`, `dumpXYZ`, and the Qimera/HIPS-style **OMG Multibeam Monitor** QGIS plugin. |
| **[7. ADCP Current & Backscatter Workflow](workflows/adcp-processing-workflow.html)** | Teledyne RDI / WinADCP and Kongsberg EC150 ADCP processing (`readADCP`, `readWinADCP`, `readGenericADCP`, `mapGenericADCP`, `combineMultiADCP`, `calc_ellipse`, `makeVectorPlot`, `plotADCPgridcurrents`, `makeTSmap`). |
| **[8. Simrad EK60, EK80 & EA600 Echosounder Workflow](workflows/ek60-ek80-echosounder-workflow.html)** | Simrad `.raw` unpacking & broadband FM pulse compression (`readEA600`, `ek80_parse_proc`), interactive 6-window analysis (`EKlook`), batch Angular Response Curves (`BatchProcEK`), calibration (`comboCalibEK_ARCs`), and MVP/EK60 peak analysis (`ExtractMVP_EK60_Peaks`). |
| **[9. GeoSwath+ Interferometric & Towed Sidescan](workflows/geoswath-and-sidescan-workflows.html)** | GeoAcoustics GeoSwath+ / Submetrix 2000 (`.swa`, `.gsf`, `.xtf`), EdgeTech `.jsf`, Klein `.sdf`/`.xtf`, and GLORIA `.ss` sidescan processing (`bpick`, `glslant`, `destripe`, `glgain`, `glfill`). |
| **[10. Multi-Vendor Multibeam Converters](workflows/multibeam-vendor-converters-workflow.html)** | Teledyne Reson 7k/8k (`7k2omg`, `8k2omg`, `8101toOMG`), R2Sonic (`r2sonic2omg`), Furuno WASSP (`wassp2omg`), L-3/ELAC XSE (`xse2omg`, `refoELAC`), SeaBeam 2000/2100 (`unravelSB2K`, `unravelSB2100`), Kongsberg M3 (`M3imb2omg`), and Lowrance (`lowrance2omg`). |
| **[11. Sub-Bottom (Knudsen / SEG-Y) & Optech LiDAR](workflows/subbottom-and-lidar-workflows.html)** | Knudsen `.keb` and SEG-Y sub-bottom profiler curtains (`knud2glo`, `upKnudSEGY`, `readSB_SEGY`, `makeSeisPlot`, `pickSS`) and Optech SHOALS bathymetric LiDAR waveform processing (`refoOptech`, `refoLAS`, `processSHOALSdepths`). |
| **[12. LLM / RAG & Fine-Tuning Datasets](llm/index.html)** | Machine-readable JSON tool schemas ([`omg_tools_catalog.json`](llm/omg_tools_catalog.json)) and JSONL instruction/troubleshooting datasets ([`omg_workflows_and_troubleshooting.jsonl`](llm/omg_workflows_and_troubleshooting.jsonl)) for LocalAI integration. |

---

## Complete Codebase Directory Index

### Multibeam Unraveling & Vendor Converters
- **[KMALL Tools (`kmall/`)](kmall/index.html)** — Kongsberg SIS 5.x `.kmall` & `.kmwcd` unpacker ([`read_kmall`](kmall/read_kmall.html)).
- **[RTlite (`RTLite/`)](RTLite/index.html)** & **[RT (`RT/`)](RT/index.html)** — Legacy Kongsberg/Simrad `.all` & `.wcd` unpackers ([`RTlite`](RTLite/RTlite.html), [`RT`](RT/RT.html)).
- **[Automation Scripts (`scripts/`)](scripts/index.html)** — [`unravel_KMALL_2500m_RevHplus_netatt2_parallel`](scripts/unravel_KMALL_parallel.html), [`bunravel`](scripts/bunravel.html), [`tor4`](scripts/tor4.html), [`tomos`](scripts/tomos.html).
- **[Reson 7k/8k (`reson/`, `Sbat/`)](reson/index.html)** — Teledyne Reson `.s7k` and SeaBat 8101/9002 converters ([`Sbat/`](Sbat/index.html)).
- **[R2Sonic (`r2sonic/`)](r2sonic/index.html)**, **[WASSP (`wassp/`)](wassp/index.html)**, **[L-3 XSE (`xse/`)](xse/index.html)**, **[ELAC (`elac/`)](elac/index.html)**, **[SeaBeam (`sb2k/`)](sb2k/index.html)**, **[Kongsberg M3 (`M3/`)](M3/M3imb2omg.html)**.
- **[Generic Sensor Format (`gsf/`, `gsf_lib/`)](gsf/index.html)** — GeoSwath+, Klein 5410, and multi-sonar GSF converters.

### Sidescan, Interferometry, ADCP, Echosounders & Sub-Bottom
- **[Sidescan Processing Suite (`sidescan/`)](sidescan/index.html)** — Bottom tracking, slant-range correction, destriping, beam pattern removal, and format converters.
- **[Triton XTF (`xtf/`)](xtf/index.html)**, **[EdgeTech JSF (`jsf/`)](jsf/index.html)**, **[Klein SDF (`sdf/`)](sdf/index.html)**, **[Hawaii MR1 (`mr1/`)](mr1/index.html)**.
- **[Submetrix 2000 & GeoSwath (`sub2k/`, `sub2k_motif/`)](sub2k/index.html)** — Interferometric bathymetric sidescan unpacking and interactive Motif editor.
- **[ADCP Suite (`adcp/`)](adcp/index.html)** — Vessel-mounted and moored ADCP unpacking, tidal phase binning, tidal ellipses, and vector mapping.
- **[Simrad EK60 / EK80 (`EKlook/`, `singlebeam/`)](EKlook/index.html)** — Scientific split-beam/broadband echosounder viewer, FFT arc calibration, and singlebeam tools ([`singlebeam/`](singlebeam/index.html)).
- **[Knudsen (`knudsen/`)](knudsen/index.html)** & **[SEG-Y (`segy/`)](segy/index.html)** — Chirp sub-bottom profiler unpacking, bottom tracking, and heave-compensated seismic section plotting.
- **[Optech Bathymetric LiDAR (`Optech/`)](Optech/index.html)** — Airborne laser bathymetry waveform analysis and PPK GPS integration.

### Core Swath Processing, Navigation, Tides, Gridding, Mosaicking & Visualization
- **[OMG Swath & Attitude Tools (`omg/`)](omg/index.html)** — Ray-tracing (`newMergeAtt`, `mergeAtt`), empirical TVG removal (`deTVG`), beam pattern calibration (`newGetBP`, `getAngularResponse`), water column projection (`makeWC`), and sidescan generation (`makess`).
- **[Navigation Tools (`nav/`)](nav/index.html)** — Lever-arm reduction (`mergeNav`), filtering (`stripNav`, `filtnav`), concatenation (`appendNav`), and format/Shapefile converters.
- **[Tide Tools (`tide/`, `Tidecor/`)](tide/index.html)** — Tidal elevation merging (`mergeTide`), gauge converters, PPK GNSS height converters (`posProc_2_OMG`, `GrafNav_2_OMG`), and co-tidal zoning ([`Tidecor/`](Tidecor/index.html)).
- **[Grid Tools (`grid/`)](grid/index.html)** — Blank templates (`make_blank`), weighted gridding (`weigh_grid`), sun-illumination (`addSUN`, `r4to8bit`), GIS export (`r4toESRI`, `edhead`), and surface differencing.
- **[Sidescan Mosaicking (`newmos/`)](newmos/index.html)** & **[Image Processing (`image/`)](image/index.html)** — Range-buffered sidescan mosaicking (`mos2`, `comboMOS`) and 2D raster/image transformations.
- **[Swath Editor (`SE/`)](SE/index.html)** & **[3D Visualization (`JV/`)](JV/index.html)** — Interactive 6-panel swath editor (`swathed`) and 2D/3D OpenGL/X11 viewer (`jview`).
- **[Core Shared Libraries (`subr/`, `subr_graphics/`)](subr/index.html)** & **[Researcher Suites (`ianc/`, `jonnyb/`, `james/`, `steve/`)](jonnyb/index.html)**.
