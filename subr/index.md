---
layout: default
title: Core Shared C Library — libj.a (subr)
parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 1
has_children: true
---

# Shared Core Libraries (`subr/`)

The `code/subr/` directory is the foundational C library (`libsubr`) of the Ocean Mapping Group software suite. Linked into every command-line utility and interactive X11/Motif/OpenGL application, it contains **105 shared compilation modules** and **8 standalone header/support definitions** implementing OMG-HDCS file I/O, multi-vendor sonar datagram parsing, 3D raytracing and cone-intersection geometry, radiometric backscatter calibration, map projections, raster gridding, and physical oceanography equations.

---

## 1. OMG-HDCS Core Data Model & Binary Formats

Modules that read, write, index, and manipulate the Ocean Mapping Group's native binary swath, navigation, attitude, and sidescan formats:

* [`OMG_HDCS_jversion`](OMG_HDCS_jversion.html) — Master I/O library for OMG-HDCS Version 1–4 `.merged` bathymetry, `.nav` navigation, `.orientation` attitude, `.param` vessel lever-arm configuration, `.sectors`, `.surf_ss`, and rationalized profile/beam structures.
* [`USL_HDCS_hack`](USL_HDCS_hack.html) — Legacy compatibility bridge for early Universal Systems Ltd. (CARIS) HDCS structures.
* [`jcu_glo`](jcu_glo.html) — JCU/MGL 1160-byte GLORIA-format `.ss` sidescan record (`gloria_rec`) reader/writer.
* [`jcu_nav`](jcu_nav.html) — Legacy James Cook University (JCU) navigation record helpers.
* [`mr1_raw`](mr1_raw.html) & [`mr1_proc`](mr1_proc.html) — Readers and processors for HIG/SOEST Hawaii MR1 sidescan and phase-bathymetry files.
* [`omg_line`](omg_line.html) — Line/polyline vector segment file I/O (`.line` files).
* [`omg_target`](omg_target.html) — Acoustic target picking and georeferenced target record (`OMG_Target`) I/O.
* [`snapshot`](snapshot.html) — Snapshot state and metadata capture structures.

---

## 2. Vendor Sonar Format Parsers & Hardware Drivers

Libraries for decoding raw vendor multibeam, sidescan, sub-bottom, single-beam, and positioning datagrams:

### Kongsberg / Simrad (EM & EK Series)
* [`simrad_utils`](simrad_utils.html) — Parser and byte-order handler for Kongsberg/Simrad EM3000/EM300/EM120/EM710/EM2040 `.all` datagrams (`0x44`, `0x46`, `0x58`, `0x4e`, `0x53`, `0x59`, `0x6b`, etc.).
* [`simrad_tvg`](simrad_tvg.html) — Kongsberg EM Time-Varied Gain (TVG) and crossover (`BSo`, `BSn`, `TVG_xover`) law reconstruction.
* [`j_EM_watercol`](j_EM_watercol.html) — Kongsberg EM `0x6b` (`k`) water-column datagram reader and `.watercol` indexer.
* [`ek80_parse_proc`](ek80_parse_proc.html) & [`ek_IQ`](ek_IQ.html) — Kongsberg Simrad EK60/EK80 broadband/CW split-beam complex I/Q and power/angle parser and pulse-compression processor.
* [`ea400`](ea400.html) — Kongsberg EA400/EA600 single-beam hydrographic echosounder parser.
* [`sm2000`](sm2000.html) — Kongsberg Simrad SM2000 / Mesotech multibeam forward-looking/profiling sonar parser.

### Teledyne Reson (SeaBat 81-P & 7K Series)
* [`reson`](reson.html) — Reson SeaBat 8101/8111/8125/8150/8160 (`81-P`) raw bathymetry, attitude, and sidescan packet parser and 16-to-8-bit radiometric converter (`jb_fix_RESON_16bit`).
* [`snippet`](snippet.html) — Reson 81-P `SNP0` ping header and fragmented `SNP1` beam snippet reassembly and TVG correction.
* [`reson_7K`](reson_7K.html) & [`reson_7K_utils`](reson_7K_utils.html) — Teledyne Reson `.s7k` (7000, 7004, 7006, 7007, 7008, 7027, 7028, 7042) data record frame parser and `.sonar_settings` loader.
* [`reson_7K_TVG`](reson_7K_TVG.html) & [`reson_calibration`](reson_calibration.html) — Reson 7K Time-Varied Gain reconstruction and hydrophone/projector calibration curve lookup.

### R2Sonic, SeaBeam, Elac, WASSP, Knudsen, Edgetech, XTF, GSF & Hypack
* [`omg_r2sonic`](omg_r2sonic.html) — R2Sonic Sonic 2020/2022/2024 bathymetry (`BTH0`), snippet (`SNI0`), and TruePix (`TPX0`) packet parser.
* [`seabeam`](seabeam.html), [`j_sb`](j_sb.html), [`j_sb2100`](j_sb2100.html), & [`omg_xse`](omg_xse.html) — SeaBeam Classic, SeaBeam 2100 (`.sb2100`), and L-3 ELAC / SeaBeam `.xse` frame parsers.
* [`elac`](elac.html) — Honeywell/L-3 ELAC BottomChart multibeam parser.
* [`OMGmod_SEA_phasetoangle`](OMGmod_SEA_phasetoangle.html) — SEA SwathPlus interferometric stave phase-to-angle conversion library.
* [`omg_wassp`](omg_wassp.html) — ENL WASSP multibeam fishery/hydrographic sonar parser.
* [`omg_mb1`](omg_mb1.html) — Teledyne `.mb1` multibeam packet parser.
* [`M3_read`](M3_read.html) & [`Mesotech_SMB`](Mesotech_SMB.html) — Kongsberg Mesotech M3 (`.mmb`) multibeam and `.smb` sonar readers.
* [`j_knud`](j_knud.html) & [`unb_huffproc`](unb_huffproc.html) — Knudsen 320/3260 `.keb`/`.kea` echosounder parser and Huffman trace decompressor.
* [`j_SUB2K`](j_SUB2K.html) — Submetrix ISIS 100/2000 interferometric sonar reader.
* [`omg_xtf`](omg_xtf.html) & [`xtf_utils`](xtf_utils.html) — Triton Elics `.xtf` packet indexer, clock synchronizer (`synchro` modes `0..7`), and HDCS summary initializer.
* [`omg_jsf`](omg_jsf.html) & [`omg_sdf`](omg_sdf.html) — EdgeTech `.jsf` and Klein `.sdf` sidescan/sub-bottom parsers.
* [`omg_gsf`](omg_gsf.html) — SAIC Generic Sensor Format (`.gsf`) wrapper utilities.
* [`omg_hypack`](omg_hypack.html) — Hypack `.hsx` / `.raw` / `.81x` hydrographic survey line parser.
* [`omg_sbet`](omg_sbet.html) — Applanix POS/MV `.sbet` (Smoothed Best Estimate of Trajectory) and RMS error reader.
* [`jNMEA`](jNMEA.html) — NMEA-0183 (`$GPGGA`, `$GPRMC`, `$GPHDT`, `$PASHR`, etc.) GPS and attitude sentence parser.
* [`j_MCOM`](j_MCOM.html), [`j_SHP`](j_SHP.html), [`j_adcp`](j_adcp.html) — Marimatech MCOM, ESRI Shapefile (`.shp`), and RDI Workhorse ADCP readers.

---

## 3. Raytracing, Sound Speed, Physical Oceanography & 3D Geolocation

Modules responsible for converting raw acoustic travel times and steering angles into georeferenced 3D soundings:

* [`sonar_geometry`](sonar_geometry.html) — Master 3D sounding reduction engine (`Sounding_Geometry`, `get_sounding_geometry`, `intersect_cones`, `intersect_cones_travis`, `reduce_sounding`) supporting 25+ sonar types, lever arms, delayed heave, and Snell's law beam repointing.
* [`j_non_ortho_cones`](j_non_ortho_cones.html) — Analytical intersection of non-orthogonal transmit and receive array cones during pitching/rolling/yawing motion.
* [`j_watercolumn`](j_watercolumn.html) & [`jb_watercolumn`](jb_watercolumn.html) — Stratified Sound Velocity Profile (`watercolumn`) management, layer interpolation, harmonic sound speed integration, and constant-gradient arc / constant-velocity straight-line raytracers (`raytrace`).
* [`c_wcpick`](c_wcpick.html) — Automated seabed and target bottom-detection picking within multibeam water-column fans.
* [`soundspeed`](soundspeed.html) — Empirical seawater sound velocity formulas (`ChenMillero`, `Mackenzie`, `DelGrosso`, `Coppens`), pressure-depth conversions (`press2depth`, `depth2press`), and AML SV&T salinity inversion (`speed_temp2salinity`).
* [`water`](water.html) — UNESCO EOS-80 physical oceanography routines (`adtg`, `potential_temperature`, `insitu_temperature`, `conductivity2salinity`, `density`, `density0`, `sigma_t`, `freezing_point`).
* [`r_atten`](r_atten.html) — Francois & Garrison (1982) and Ainslie & McColm (1998) seawater acoustic absorption coefficient ($\alpha$ in dB/km) calculators.
* [`uwedge`](uwedge.html) — XML parser, writer, and statistical compiler (`MEAN` and 95% `STDEV`) for raytracing uncertainty wedges (`Wedge`).
* [`j_SalishSeaCast`](j_SalishSeaCast.html) & [`j_SSCOFS`](j_SSCOFS.html) — 3D hydrodynamic ocean model (SalishSeaCast and Salish Sea / Columbia River Operational Forecast System) netCDF/grid synthetic SVP extractors.
* [`etopo`](etopo.html) — ETOPO global bathymetric relief lookup helper.

---

## 4. Radiometric Backscatter, Grazing Angle & Calibration

Libraries for radiometric normalization, beam pattern compensation, and acoustic seabed classification:

* [`Echo_calib`](Echo_calib.html) — Comprehensive multibeam backscatter calibration and transmit/receive sector gain offset estimation.
* [`backscatter`](backscatter.html) & [`normalization`](normalization.html) — Lambertian / Lommel-Seeliger backscatter normalization and across-track radiometric leveling.
* [`grazing_angle`](grazing_angle.html) — True 3D seafloor grazing/incidence angle computation by intersecting acoustic ray vectors with local DEM surface normals (`.grz` generation for `makess` and `mos2`).
* [`angular_response`](angular_response.html) & [`j_ang_resp`](j_ang_resp.html) — Empirical Intrinsic Angular Response (IAR) curve extraction and angle-independent backscatter (`AIBS`) lookup tables.
* [`beam_foot`](beam_foot.html) & [`ensonification`](ensonification.html) — Pulse-length vs. beamwidth instantaneously ensonified seafloor area ($10\log_{10} A$) calculators.
* [`bP_stuff`](bP_stuff.html) — Linear/planar transducer array shading (Dolph-Chebyshev, Hamming, $\cos^2$, binomial), element summation, and 3D beam pattern modeling.
* [`ref_coeffs`](ref_coeffs.html) — Rayleigh fluid-fluid / fluid-elastic seabed acoustic reflection and impedance coefficient modeling.
* [`omg_fmgt`](omg_fmgt.html) — QPS Fledermaus Geocoder Toolbox (FMGT) compatibility helpers.

---

## 5. Map Projections, Ellipsoids & Geodesy

Coordinate reference system conversions between geographic $(\phi, \lambda)$ and projected $(X, Y)$ space:

* [`j_proj`](j_proj.html) — Unified OMG map projection dispatcher (`setup_proj`, `ll_to_xy`, `xy_to_ll`) supporting Mercator, UTM, Rotated UTM, Polar Stereographic, Lambert Conformal Conic, New Brunswick Double Stereographic, and Rectangular Lat/Lon grids.
* [`geographic`](geographic.html) — Geodetic arc lengths (`get_lat_lon_scales`) and forward/inverse range-bearing calculations on the ellipsoid.
* [`utm`](utm.html), [`geoutm`](geoutm.html), & [`utmgeo`](utmgeo.html) — Forward (`geoutm`) and inverse (`utmgeo`) Universal Transverse Mercator transformations using Snyder's equations.
* [`mercator`](mercator.html) — Standard Mercator projection routines.
* [`lambert`](lambert.html) — Lambert Conformal Conic projection routines.
* [`polarstereo`](polarstereo.html) — Polar Stereographic projection routines for Arctic/Antarctic mapping.
* [`nbstereo`](nbstereo.html) — New Brunswick Double Stereographic (ATS77 / NAD83 CSRS) projection routines.
* [`j_area`](j_area.html) — Spatial bounding polygon (`area`) inclusion testing and coordinate parsing.

---

## 6. Gridding, Matrix Math, Signal Processing & Contouring

* [`array`](array.html) & [`j_farray`](j_farray.html) — OMG 1024-byte `JHC_header` binary raster grid I/O for 8-bit (`.mos`, `.sun`), 16-bit (`short`), and 32-bit float (`.r4`, `.wt`, `.cnt`) mapsheets, including sub-area extraction and bilinear interpolation.
* [`j_dtm`](j_dtm.html) — Digital Terrain Model (DTM) surface query and slope/aspect helpers.
* [`cache`](cache.html) — Paged virtual-memory tile/row cache (`cache_init`, `cache_read`, `cache_write`, `cache_flush`) used by `mos2` and `mosaic` to update massive `.mos` and `.ran` files on disk.
* [`contour`](contour.html) — Marching-squares isoline contour extraction from 2D bathymetric grids.
* [`tin`](tin.html) — Prototype Delaunay Triangulated Irregular Network (`tin_point`) bounding-box loader.
* [`DCM_rthand`](DCM_rthand.html), [`orientation`](orientation.html), & [`vector_geometry`](vector_geometry.html) — Right-handed 3D Direction Cosine Matrices (`fmatx`), Euler roll-pitch-heading rotations (`rotate`, `unrotate`), and 3D vector algebra (`add_vector`, `cross_product`, `dot_product`, `normalize_vector`).
* [`matrix`](matrix.html) & [`dmatrix`](dmatrix.html) — Single- and double-precision linear algebra, Gaussian elimination, and matrix inversion.
* [`four1`](four1.html), [`dspectra`](dspectra.html), [`jwave_subr`](jwave_subr.html), [`pm_OP_waveproc`](pm_OP_waveproc.html), & [`rg_jack2`](rg_jack2.html) — Fast Fourier Transform (`four1`), power spectral density estimation, heave/wave spectral processing, and jackknife statistical estimators.
* [`j_wav_io`](j_wav_io.html) — RIFF `.wav` audio file reader/writer for sonified sonar and seismic traces.
* [`swath_geometry`](swath_geometry.html) — Automated multibeam common-range ambiguity (`checkCommonRangeAmbiguity`) and water-column multiple (`checkMultiple`) outlier rejection.

---

## 7. Core System, Endianness, Graphics Palettes & Time Utilities

* [`support`](support.html) — Universal CLI error/warning/usage reporting, cleanup hooks, heap string/path helpers (`mem_stripext`, `mem_replace`, `mem_strappend`), numeric/angle parsers (`strtoangle`), and `-xyzlist` loader (`load_inputfiles_from_list`).
* [`swapio`](swapio.html) & [`jb_endian`](jb_endian.html) — Big-endian (`MOTOROLA`) and Little-endian (`INTEL`) byte-swapping primitives (`get_swapped_float`, `jswapfloat_fread`, `fread_LE_short`, `fread_BE_long`).
* [`stdtime`](stdtime.html) — Calendar date, Julian day (Day of Year), Unix epoch timestamp, and `stdtime_nicetime()` formatting library.
* [`omg_buffer`](omg_buffer.html) & [`jb_utils`](jb_utils.html) — Dynamically resizing byte/line buffers (`OMG_Buffer`) and general file/math helpers.
* [`omg_colours`](omg_colours.html), [`afont`](afont.html), & [`plotlib`](plotlib.html) — HSV-to-RGB color table generation (`prime_palettes`), Hershey/bitmap raster font rendering (`af_loadfont`, `aprintf`), and PostScript/HPGL plotting primitives.
* [`interrupt`](interrupt.html) & [`serio`](serio.html) — POSIX signal/Ctrl-C interrupt handling and RS-232 serial port I/O.

---

## 8. Standalone Headers & Global Symbol Definitions in `subr/`

In addition to paired `.c`/`.h` modules, `code/subr/` contains several standalone header files and global symbol definitions shared across the suite:

| File | Purpose & Key Definitions |
|---|---|
| `wgs.h` | Defines geodetic reference ellipsoid constants (`WGS84=1`, `NAD27=2`, `CLK66=3`, `AGD84=4`, `SPHER=5`, `ATS77=6`), semi-major axes (`*_RADIUS`), eccentricities (`*_ECCEN`), flattening (`*_FLATT`), and declares global projection state (`extern int Ellipsoid`, `Proj_Type`, `float Map_Rotation`, `char Hemisphere`). |
| `Simrad_em12.h` | Comprehensive binary structure and datagram ID header (`1030` lines) for all generations of Kongsberg/Simrad multibeam echosounders: EM100 (`0x84`), EM12 (`0x94`–`0xc9`), EM1000 (`0x97`, `0xca`), EM121A (`0x88`), EM3000/EM300/EM120/EM1002 (`0x44` depth, `0x46`/`0x66` raw range/angle, `0x53` image, `0x41` attitude, `0x50` nav, `0x52` runtime, `0x55` SVP, `0x6b` watercolumn), and EM710/EM302/EM2040 (`0x58` XYZ88, `0x4e` raw range/angle 78, `0x59` seabed image 89, `0x6e` network attitude, `0x4f` quality factor, `0x33` extra parameters). |
| `OMG_mr1.h` | Defines unpacked and decimated Hawaii MR1 sidescan (`OMG_MR1_ss_rec`, binary-compatible in size with the 1160-byte JCU GLORIA `.ss` record) and interferometric phase bathymetry (`OMG_MR1_zx_rec`, `OMG_phase_bathy`, `OMG_head`) structures. |
| `unb_huffstruct.h` | Standalone structure and constant definitions (`NODE`, `CODE`, `MAX_HUFFMAN_SIZE = 80000`, `END_OF_STREAM = 256`) for Knudsen Huffman compression ([`unb_huffproc`](unb_huffproc.html)). |
| `gbh.h` | Submetrix Ltd. Generic Block Header (`GBH`, `GBlock`, `GB`) and interferometric stave phase structures (`RPS` Raw Phase Sample, `APES` Augmented Phase Sample, `PRANG` Plate Relative Angle and Range, `SMURF` seabed surface element) for Submetrix ISIS sonars. |
| `vfont.h` | Berkeley UNIX `vfont(5)` raster font file structures (`struct header` with `VFONT_MAGIC = 0436` and `struct dispatch[256]`) used by [`afont`](afont.html) to render text labels into raster grids and X11 pixmaps. |
| `j_phi.h` | Legacy mathematical constant header (`M_PI`, `M_E`) retained for source compatibility with older projection modules. |
| `main_args.h` / `main_args.c` | Defines and exports the global command-line argument counters `int ARGC;` and `char **ARGV;` when linking utilities that do not pull them from `support.o`. |
