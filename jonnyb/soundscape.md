---
layout: default
title: soundscape
parent: Jonathan Beaudoin (jonnyb) Tools
nav_order: 4
tool_name: soundscape
source_path: code/jonnyb/svp/svp_tool/soundscape.c
category: Sound Velocity & Refraction Analysis (jonnyb)
input_formats: [".svp", ".sun_315 / .8bit (basemap)", ".nav", "wod.db3", "WOA01 grids"]
output_formats: [".svp", "Refraction error plots"]
related_tools: ["svp_woa01", "svp_raytrace", "wod2db3", "convertWOA01", "RefractEd"]
---

# soundscape (`svp_tool`)

## Description
`soundscape` (`code/jonnyb/svp/svp_tool/soundscape.c`, also referred to as `svp_tool`) is Jonathan Beaudoin's interactive X-Windows graphical environment for visualizing Sound Velocity Profiles (`*.svp`), comparing shipboard CTD/XBT/MVP casts against historical World Ocean Database (`WOD`) casts and World Ocean Atlas 2001 (`WOA01`) climatology, and monitoring multibeam raytracing depth and across-track refraction errors in real time.

---

## Usage

```bash
soundscape [OPTIONS] (-svp <files.svp ...> | -svp_list <listfile>)
```

### Examples

**1. Launch `soundscape` with all `.svp` casts over a sun-illuminated basemap and shiptrack:**
```bash
soundscape -map arctic_overview.sun_315 -nav cruise_track.nav -plot_all -svp svp/*.svp
```

**2. Jump directly into multibeam refraction error-monitoring mode for a 130° swath and 6.5 m draft:**
```bash
soundscape -error_monitor -draft 6.5 -angular_sector 130 -svp svp/*.svp
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-svp <*.svp>` | One or more OMG `.svp` files to load into the interactive viewer. | Required (or `-svp_list`) |
| `-svp_list <file>` | One or more ASCII list files containing paths to `.svp` files. | None |
| `-map <map.sun_315>` | Background 8-bit OMG mapsheet for the geographic map window. Falls back to `$OMG_DEFAULT_MAP` if omitted. | `$OMG_DEFAULT_MAP` |
| `-wc_map <map>` | Load a water-column imagery map in the viewer. | Disabled |
| `-nav <file.nav>` | Overlay binary `.nav` trackline (uses `.nav` depth field for bathymetry profile and `azi` field for tides). | None |
| `-shoreline` | Enable GSHHS shoreline vector overlay on the geographic map window (`wvsrtv.c`). | Disabled |
| `-plot_all` | Plot all loaded `.svp` casts immediately upon startup. | Plots none initially |
| `-rainbow` | Color-code `.svp` profiles sequentially by cast number. | Disabled |
| `-colour_by_extension` | Color-code `.svp` profiles by their filename extension. | Disabled |
| `-error_monitor` | Start directly in multibeam raytracing refraction error-monitoring mode. | Disabled |
| `-relative` | Perform relative refraction error comparison between casts. | Disabled |
| `-draft <m>` | Transducer draft (meters) used for raytracing error analysis. | `1.0` |
| `-angular_sector <deg>` | Total multibeam swath angular sector (degrees, e.g., `132`) for error analysis. | `132` |
| `-no_ssp` | Do not simulate a hull-mounted surface sound speed sensor (`SSP`) during error analysis. | Uses surface SSP |
| `-premark <files.svp>` | Pre-mark specific `.svp` files as active reference casts for error analysis. | None |
| `-max_depth <m>` | Force maximum depth axis limit (meters) in the profile viewer. | Auto |
| `-speed_range <min> <max>` | Force sound speed axis bounds (m/s, e.g., `1430 1480`). | Auto |
| `-temperature_range <min> <max>` | Force temperature axis bounds (°C, e.g., `-1.8 10.0`). | Auto |
| `-salinity_range <min> <max>` | Force salinity axis bounds (PSU, e.g., `0 35.0`). | Auto |
| `-woa_month <1..12>` | Select month ($1\dots 12$) for World Ocean Atlas (`WOA01`) climatology lookup. | Auto from cast date |
| `-debug_wod` | Enable debugging output for World Ocean Database (`WOD`) queries. | Disabled |
| `-rules <rules.txt>` | Load custom decision rules from `<rules.txt>`. | None |
| `-tiny` | Use compact window layout for $1024\times 768$ displays. | Standard size |
| `-no_rubber_band` | Disable X11 rubber-band XOR box drawing (workaround for macOS XQuartz crashes). | Enabled |
| `-v` | Enable verbose output. | Disabled |
