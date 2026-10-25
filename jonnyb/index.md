---
layout: default
title: Jonathan Beaudoin (jonnyb) Tools
nav_order: 25
has_children: true
---

# Jonathan Beaudoin (`jonnyb`) Tools

Comprehensive suite of hydrographic, acoustic backscatter (`deTVG`), dual-head sidescan blending (`ss_blend_dual_head`), ADCP normalization (`normalize_adcp`), Sound Velocity Profile (`svp/` & `soundscape` / `svp_tool`), World Ocean Atlas (`woa/`), World Ocean Database (`wod/`), and Kongsberg Simrad water-column (`simrad_code/`) utilities developed by Jonathan Beaudoin (with contributions by Anand Hiroji and John Hughes Clarke) in `code/jonnyb/`.

---

## Major Subsystems & Featured Tools

### 1. Backscatter, Sidescan & Hydrographic Processing (`code/jonnyb/gom_stuff/`)
* [`deTVG`](deTVG.md) — Removes Kongsberg Simrad real-time Time-Varying Gain (`simrad_TVG`), recalculates true seabed grazing angles (`grazing_angle.h` from 3D beam geometry, an external `.r4` DTM, or Anand's $N_{\text{ping}}\times N_{\text{beam}}$ plane fit `-use_ADH_GRZ`), applies pulse-length and beamwidth ensonified-area corrections (`ensonification.h`), and writes radiometrically corrected snippet backscatter.
* [`ss_blend_dual_head`](ss_blend_dual_head.md) — Merges separate port and starboard ping records in GLORIA `.ss` sidescan files from dual-head multibeam installations into a single unified ping record using center-seam (`-seam`), port/starboard overlay (`-overlay_port`, `-overlay_stbd`), or linear overlap feathering (`-feather`).
* [`normalize_adcp`](normalize_adcp.md) — Normalizes vertical/range attenuation across an OMG `.r4` floating-point ADCP backscatter curtain by subtracting each depth bin's ping-averaged bias relative to the overall curtain mean.
* Additional `gom_stuff/` utilities:
  * **Sidescan (`ss_*`):** `ss_dewash`, `ss_nadir_filt`, `ss_median`, `ss_trim`, `ss_no_blanks`, `ss_apply_shifts`, `ss_add_snippet_shadows`, `ss_info`, `ss2pgm`, `ss2xtf`, `ss2fmgt`, `gl2ascii`.
  * **Refraction & Raytracing (`dewobble`):** `dewobble`, `make_dewobble`, `derange`, `refract_line`, `get_envelope`, `get_sector_boundaries`, `uncrosstalk`.
  * **Navigation & Attitude:** `nav_clean`, `nav_sort`, `nav_by_time`, `nav2kml`, `ascii2nav`, `att_sort`, `att_shift_time`, `tweak_heading`, `merged2orientation`.
  * **Beam & Grid Analysis:** `buildBP`, `make_bp`, `calcDiffByBeam`, `clip_beams_by_depth`, `dumpNadirDepth`, `dumpSoundings`, `dumpSignalParams`, `getBeamSampling`, `getSignalStrength`, `getSlope`, `r4toSlope`, `trim_r4`, `median_filter`.

### 2. Interactive Soundscape / SVP Analysis (`code/jonnyb/svp/` & `svp_tool/`)
* [`soundscape`](soundscape.md) (`code/jonnyb/svp/svp_tool/soundscape.c`) — Interactive X11 graphical Sound Velocity Profile (`*.svp`) and raytracing error-monitoring environment (`svp_tool`). Integrates shipboard CTD/XBT casts, World Ocean Atlas (`woa01`), GDEM climatology, and World Ocean Database (`wod`) historical casts over an OMG `.sun_315` basemap to evaluate spatial/temporal refraction uncertainty across a multibeam swath (`-angular_sector`, `-draft`, `-error_monitor`).
* Command-line SVP processing suite (`code/jonnyb/svp/`):
  * `svp_woa01` — Extracts synthetic `.svp` casts along a `.nav` shiptrack, at `.svp` locations, or at a single `-lat`/`-lon`/`-jday` from World Ocean Atlas 2001 or GDEM (`-gdem`), with inverse-distance spatial interpolation (`-interp_space`), monthly temporal interpolation (`-interp_time`), deep profile extension (`-xnn`, `-xtsc`, `-xtsg`), and surface sound-speed splicing (`-replace_surface_ss`).
  * `svp_raytrace` — Performs constant-layer or constant-gradient (`-cg`) acoustic raytracing through an `.svp` file to a target depth (`-raytracing_depth`) or two-way travel time (`-twtt`), outputting ray paths to `.yz`.
  * `svp_align`, `svp_attenuation`, `svp_average`, `svp_calculate`, `svp_cbofs`, `svp_clip`, `svp_differ`, `svp_get_minimum_depth`, `svp_normalize`, `svp_resample`, `svp_rtofs`, `svp_section`, `svp_select`, `svp_thin`, `svp_variability`, `svp_wavelets`.

### 3. World Ocean Database & World Ocean Atlas Converters (`code/jonnyb/wod/` & `woa/`)
* [`wod2db3`](wod2db3.md) (`code/jonnyb/wod/wod2db3.c`) — Indexes native NOAA World Ocean Database (`WOD`) CTD/XBT cast archives (`ctdo*`, `.gz`) into a fast SQLite3 spatial/temporal index database (`wod.db3`) or `.csv` catalog storing instrument type, WMO square, `(lat, lon)`, date, `file_offset`, and `num_bytes` for instant retrieval in `soundscape`.
* [`convertWOA01`](convertWOA01.md) (`code/jonnyb/woa/convertWOA01.c` & `convertWOA01_mask.c`) — Converts NOAA World Ocean Atlas 2001 quarter-degree ($1440\times 720$) and one-degree ($360\times 180$) ASCII temperature (`-t`), salinity (`-s`), and gridpoint (`-gp`) climatology grids across 33 standard depth levels ($0\text{ m}$ to $5500\text{ m}$) into OMG `.r4` and `.8bit` binary mapsheets (as multi-layer volumes or `-split` per-depth files, plus `woa01_depth.r4` via `-depths`).

### 4. Kongsberg Simrad Unpacking & Water Column (`code/jonnyb/simrad_code/`)
* `EM_unpack`, `get_watercolumn`, `compress_watercolumn`, `get_seeps`, `get_centralbeams`, `get_stave`, `recalc_simrad`, `km2nav`, `km2orientation`, `km2report`, backed by `libsimrad` (`simrad_reader.c`, `simrad_datagrams.c`, `simrad_sonar_geometry.c`, `simrad_watercolumn.c`).

### 5. Developer Skeletons (`code/jonnyb/`)
* [`misc`](misc.md) — Minimal CLI argument-parsing and file I/O skeleton (`-in`, `-out`) for standalone C utilities.
* [`misc_omg`](misc_omg.md) — Minimal OMG-HDCS `.merged` reader template demonstrating `OMG_HDCS_read_summary`, `OMG_get_rational_profile`, and `OMG_get_rational_beams`.
