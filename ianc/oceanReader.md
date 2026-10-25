---
layout: default
title: oceanReader
parent: Ian Church — Hydrodynamic & 3D Ray-Trace Suite (ianc)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 9
tool_name: oceanReader
source_path: code/ianc/oceanReader.c
category: Ocean Modeling & Hydrographic Utilities (ianc)
input_formats:
- MVP .m1 Casts (.m1)
- CARIS SVP (.svp)
- ISIIS Towed Vehicle CSV
- RDI ADCP / WinADCP
- OMG Attitude (.orientation)
- OMG Binary Navigation (.nav)
output_formats:
- OMG Extended SVP (.svp)
- Ocean Data View (.txt)
- OMG Binary Navigation (.nav)
related_tools:
- modelAnalysis
- HycomSSP
- iwc_water
- iwc_adcp
- iwc_support
---

# oceanReader

## Description

`oceanReader` is a comprehensive physical oceanography and water-column processing utility written by Ian Church in March 2013. It ingests Moving Vessel Profiler (MVP) `.m1` cast files (supporting vessel-specific header/sensor layouts for CSL *Heron*, *Amundsen*, *CCGS Matthew*, *TAGS*, and *Barge*), CARIS `.svp` profiles, RDI ADCP / WinADCP current files, and In-Situ Ichthyoplankton Imaging System (ISIIS) undulating vehicle profiles, and merges them into unified `iwc_watercol` structures.

Beyond converting `.m1` casts into OMG/CARIS `.svp` files, `oceanReader` computes physical water-column stability and turbulence metrics—including UNESCO 1983 seawater density (`-dens`), vertical density gradient (`-densGrad`), Brunt-Väisälä buoyancy frequency (`-buoy`), optical backscatter (`-obs`), and (when paired with ADCP velocity profiles and depth binning) gradient Richardson number (`-richard`), internal Froude number (`-froude`), and Reynolds number (`-reynolds`)—exporting the results to extended `.svp` files (using the `extra_field` column) and/or Ocean Data View (ODV) spreadsheets (`-odv`).

## Usage

```bash
oceanReader [-v] (-m1 <files...> | -svp <files...> | -isiis <file> | -adcp <file>) \
            [vessel_options] [calc_options] [adcp_options] [output_options]
```

### Example Commands

Convert CSL *Heron* MVP `.m1` casts into `.svp` files while computing density, buoyancy frequency, and optical backscatter, and export a combined Ocean Data View file and cast navigation file:

```bash
oceanReader -v -m1 *.m1 -heron -dens -densGrad -buoy -obs \
            -nav_m1 mvp_casts.nav -odv mvp_odv.txt
```

Merge MVP `.m1` casts with vessel-mounted WinADCP current profiles (corrected with an HDCS `.orientation` file) at 2-meter vertical bins to compute Richardson, Froude, and Reynolds numbers:

```bash
oceanReader -m1 *.m1 -heron -adcp survey.adcp -winADCP -filtPG \
            -draft 1.15 -heading vessel.orientation -binSize 2 \
            -all -odv turbulence_odv.txt
```

Add missing navigation coordinates to `.svp` or `.adcp` files from an OMG binary `.nav` file based on observation timestamps:

```bash
oceanReader -svp cast*.svp -nav vessel_track.nav -all -odv casts_with_nav.txt
```

## CLI Arguments and Options

### Input & Vessel Configuration Options

| Flag / Argument | Parameters | Description |
| :--- | :--- | :--- |
| `-v` | None | Enables verbose diagnostic output. |
| `-m1` | `<file1.m1> [...]` | Reads one or more Brooke Ocean / AML Moving Vessel Profiler (MVP) `.m1` ASCII files (up to 100,000 files) and extracts the downcast. |
| `-heron` | None | Parses `.m1` files using the standard CSL *Heron* header/column layout (default). |
| `-oldHeron` | None | Parses `.m1` files using the legacy CSL *Heron* format. |
| `-amundsen` | None | Parses `.m1` files using the CCGS *Amundsen* MVP format (including LOPC columns). |
| `-matthew` | None | Parses `.m1` files using the CCGS *Matthew* MVP format. |
| `-tags` | None | Parses `.m1` files using the USNS *TAGS* MVP format. |
| `-barge` | None | Parses `.m1` files using the Barge MVP format. |
| `-usePCtime` | None | Uses the PC timestamp header in `.m1` files instead of the NMEA `$GPGGA` UTC timestamp. |
| `-svp` | `<file1.svp> [...]` | Reads one or more existing `.svp` files via `load_watercolumns()` and converts them to `iwc_watercol` via `jwc2iwc()`. Cannot be combined with `-m1`. |
| `-isiis` | `<IsiisFile>` | Scans an ISIIS CSV telemetry file (`julian,utc,timestamp,temp,depth,...`) and counts downcast and upcast undulations. |
| `-nav` | `<file.nav>` | Matches water-column or ADCP timestamps against `<file.nav>` using `nav_time_search_double()` to populate or replace missing `(lat, lon)` coordinates. |
| `-oneValPerDepth` | None | Filters downcast observations so depth strictly increases (eliminating pressure reversals or duplicate depth samples). Automatically enabled by `-densGrad`, `-buoy`, `-adcp`, or `-all`. |
| `-binSize` | `<meters>` | Vertically averages water-column and ADCP observations into uniform depth bins of `<meters>` thickness via `binOceanObs()`. |

### Physical Calculation Options

| Flag / Argument | Parameters | Description |
| :--- | :--- | :--- |
| `-obs` | None | Calculates Optical Backscatter (`obs`) from analog voltage channel `mV1` and writes an `OBS_<file>.svp` profile. |
| `-dens` | None | Calculates seawater density (`kg/m^3`) from salinity, temperature, and pressure using `calcDensity()` (UNESCO 1983 EOS-80) and writes `DENS_<file>.svp`. |
| `-densGrad` | None | Calculates vertical density gradient (`d(rho)/dz`) across depth layers and writes `DENSGRAD_<file>.svp`. |
| `-buoy` | None | Calculates Brunt-Väisälä buoyancy frequency `N = sqrt(|(-g/rho) * (d(rho)/dz)|)` via `calcBuoy()` and writes `BUOY_<file>.svp`. |
| `-richard` | None | Calculates gradient Richardson number `Ri = ((-g/rho)*(d(rho)/dz)) / (du/dz)^2` via `calcRichard()` (requires `-adcp` and `-binSize`). |
| `-froude` | None | Calculates internal layer Froude number via `calcFroude()` (requires `-adcp` and `-binSize`). |
| `-reynolds` | None | Calculates Reynolds number `Re = (U * z) / nu` using seawater kinematic viscosity (`calcReynolds()`). |
| `-all` | None | Enables all physical calculations (`-obs`, `-dens`, `-densGrad`, `-buoy`, `-richard`, `-froude`, `-reynolds`, and `-oneValPerDepth`). |

### ADCP & Output Options

| Flag / Argument | Parameters | Description |
| :--- | :--- | :--- |
| `-adcp` | `<ADCP_inputFile>` | Reads a binary RDI ADCP file to extract velocity profiles or merge with MVP/SVP casts. |
| `-winADCP` | None | Uses WinADCP header/record parsing (`jwinADCP_read_header`) and `PG4` percent-good values. |
| `-filtPG` | None | Filters ADCP bins to only retain measurements with Percent Good `>= 50%` and velocity magnitude `> 0`. |
| `-draft` | `<meters>` | Transducer draft in meters added to ADCP bin depths (default: `0.0`). |
| `-heading` | `<File.orientation>` | Corrects ADCP compass heading using an OMG HDCS attitude file and recomputes E/W and N/S velocity components via `fixADCPBinVel()`. |
| `-useBTDir` | None | Uses ADCP bottom-track velocity direction (`atan2(BT_NS, BT_EW)`) to correct heading bias (`fixADCPBinVel()`). Mutually exclusive with `-heading`. |
| `-nav_adcp` | `<navfile.nav>` | Writes ADCP ensemble coordinates, timestamps, and depth-averaged velocity magnitude/direction to a binary `.nav` file. |
| `-rate` | `<seconds>` | Minimum time interval in seconds between records written to `-nav_adcp` (default: `0`, full rate). |
| `-nav_m1` | `<m1.nav>` | Writes the position and timestamp of each `.m1` or `.svp` cast to an OMG binary `.nav` file. |
| `-noSVP` | None | Suppresses writing output `.svp` files for each input `.m1` cast. |
| `-odv` | `<output.txt>` | Exports all processed casts and calculated variables to a tab-delimited Ocean Data View (ODV) spreadsheet. |
| `-noHeader` | None | Omits the column header row when writing the `-odv` output file (useful for appending). |
| `-onlyCalcsOut` | None | Restricts `-odv` output columns to only the explicitly requested calculated variables. |

## File Formats

* **MVP `.m1` Input**: ASCII header containing NMEA `$GPGGA` position/time strings, PC date/time, and vessel metadata, followed by comma- or space-delimited sensor columns (`Press`, `Depth`, `SV`, `Temp`, `Cond`, `Sal`, `Density`, `Volts`, `mV1..4`).
* **OMG Extended `.svp` Output**: Written via `iwc2jwc()` and `dump_watercolumn()` (`j_watercolumn.h`), storing standard depth, sound speed, temperature, and salinity alongside a 5th `extra_field` column containing the selected derived variable (`OBS_`, `DENS_`, `DENSGRAD_`, `BUOY_`, `RICHARD_`, `FROUDE_`, or `REYNOLDS_`).

## How It Works

1. **Cast Ingestion & Downcast Isolation**: When reading `.m1` files, `oceanReader` parses the `$GPGGA` NMEA sentence (`jNMEA.h`) or PC timestamp, reads all depth records, and isolates the downcast (from minimum surface depth down to maximum cast depth). If `-oneValPerDepth` is set, only strictly increasing depth steps (`depth > prevDepth`) are retained.
2. **ADCP Heading Correction & Temporal Matching**: When `-adcp` is supplied, ensembles are read and optionally corrected for gyro/compass bias using `-heading` or `-useBTDir` (`fixADCPBinVel()`). For each MVP/SVP cast, `closeTime()` matches the cast timestamp to the closest ADCP ensemble, and `closeDepth()` maps ADCP velocity bins onto the cast's binned depth layers.
3. **Vertical Binning & Hydrodynamic Equations**: If `-binSize` is specified, `binOceanObs()` averages all scalar and vector properties into uniform depth intervals and computes vertical gradients (`densGrad`, `velGrad`, `layerThick`). Finally, `calcDensity()`, `calcBuoy()`, `calcRichard()`, `calcFroude()`, and `calcReynolds()` populate the physical oceanography fields before exporting to `.svp` and/or `-odv`.
