---
layout: default
title: Tidal Reduction & Constituents (tide)
parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 8
has_children: true
---

# Tide Tools (`tide`)

Tools in `code/tide/` for converting, modeling, differencing, interpolating, and merging tidal water-level records, PPK/RTK GPS elevations, and dynamic draft (squat) corrections onto OMG-HDCS `.merged` multibeam files.

---

## Typical Tide Processing Workflow

1. **Format Conversion (Agency ASCII / PPK $\rightarrow$ JHC ASCII or Binary):**
   Convert raw tide gauge tables or predictions (from CHS, MEDS, NOAA, USGS, XTide, Simrad, or `.wlv` files) into 4-column JHC ASCII (`jday hour min tide_m`), or convert PPK GNSS exports directly to binary using [`GrafNav_2_OMG`](GrafNav_2_OMG.html) or [`posProc_2_OMG`](posProc_2_OMG.html).
2. **Binary Compilation (`JHC ASCII` $\rightarrow$ `jcu_nav_rec` `.bin`):**
   Run [`binTide`](binTide.html) to convert the JHC ASCII tide listing into an OMG binary `jcu_nav_rec` file (where UTC epoch time is stored in `time`/`centisecs` and vertical tide offset in meters is stored in `azi`).
3. **Merging onto Multibeam Pings (`.bin` $\rightarrow$ `.merged`):**
   Run [`mergeTide`](mergeTide.html) to interpolate the binary tide series (or two-station cotidal zone via `-interpolate`) onto each ping of your OMG-HDCS `.merged` survey lines.

---

## Tool Index by Category

### 1. Core Binary Compilation, Merging & Differencing

| Tool | Description |
|---|---|
| [`mergeTide`](mergeTide.html) | Interpolates binary tide records (or RTK height `-RTK`, filtered RTK `-filtRTK`, long-period heave `-LPHC`, dynamic draft `-DDC`, or two-station spatial interpolation `-interpolate`) onto OMG-HDCS `.merged` multibeam files. |
| [`binTide`](binTide.html) | Converts JHC ASCII tide files (`jday hour min tide` or `-V2`/`-V3`) into OMG binary `jcu_nav_rec` tide files, with optional scaling, datum offset, time delay, and station coordinates. |
| [`diffTide`](diffTide.html) | Computes the vertical difference or sum between two binary `jcu_nav_rec` tide files (with optional phase delay, attenuation, and datum offset), or computes horizontal meter offsets (`-calc_horiz_diff`) between two navigation files. |
| [`makeTideSeries`](makeTideSeries.html) | Generates a synthetic binary `jcu_nav_rec` station template at a fixed latitude/longitude over a specified start/end time range and time step for harmonic tide predictors. |
| [`tide_intp_sub`](tide_intp_sub.html) | C subroutine (`tide_intp`) implementing baseline vector projection for two-station spatial cotidal interpolation. |

### 2. GNSS PPK & Vessel Squat Converters

| Tool | Description |
|---|---|
| [`GrafNav_2_OMG`](GrafNav_2_OMG.html) | Converts Waypoint GrafNav PPK GNSS position/height exports directly into OMG binary `jcu_nav_rec` (or ASCII) tide/navigation files. |
| [`posProc_2_OMG`](posProc_2_OMG.html) | Converts Applanix PosProc / POSPac PPK GNSS/INS exports directly into OMG binary `jcu_nav_rec` (or ASCII) tide/navigation files. |
| [`makeSquat`](makeSquat.html) | Computes speed-dependent vessel settlement/squat ($\text{scaler} \times v^{\text{power}}$) from binary `.nav` velocity records and stores the vertical offset in `azi` for merging via `mergeTide -DDC`. |

### 3. Canadian (CHS / DFO MEDS / Environment Canada) Format Converters

| Tool | Description |
|---|---|
| [`convCHSpredTide`](convCHSpredTide.html) | Converts CHS 24-hour predicted tide tables (and Cape Enrage measured centimeter tide tables via `-enrage_meas`) to JHC ASCII format. |
| [`medsTide`](medsTide.html) | Converts DFO Marine Environmental Data Section (MEDS) CSV/ASCII water levels (and 12-hour AM/PM XTide listings) to JHC ASCII format. |
| [`wlvTide`](wlvTide.html) | Converts `.wlv` water level files (and 24-hour UTC XTide outputs via `-UTC`) to JHC ASCII format. |
| [`convTide`](convTide.html) | Converts Coastal Ocean Water Level Information System (COWLIS) ASCII tide files to JHC ASCII format. |
| [`switchTide`](switchTide.html) | Converts 7-column predicted tide files into JHC ASCII or COWLIS (`-cowlis`) format. |
| [`quebecTide`](quebecTide.html) | Converts 81-byte fixed-record (15-minute centimeter) Quebec/CHS tide files to JHC ASCII format. |
| [`readBlueFile`](readBlueFile.html) | Parses CHS harmonic constituent BlueFiles, writing station coordinates to `outlist` and dumping 41 harmonic constituents (`M2`, `S2`, `K1`, `O1`, etc.). |
| [`dischargeTide`](dischargeTide.html) | Transposes Environment Canada daily hydrometric discharge/water-level CSV matrices (`Jan..Dec` columns) into chronological JHC V2 ASCII format. |

### 4. US (NOAA / USGS), International & Sonar Tide Converters

| Tool | Description |
|---|---|
| [`noaaTC_Tide`](noaaTC_Tide.html) | Converts NOAA CO-OPS Tides & Currents web portal ASCII files to JHC ASCII format. |
| [`noaaTide`](noaaTide.html) | Converts legacy 8-column NOAA DCP water level files to JHC ASCII format, with optional `-shift` timezone adjustment. |
| [`usgsTide`](usgsTide.html) | Converts 7-column USGS / Rich Signell ASCII tide files to JHC ASCII format. |
| [`cncTide`](cncTide.html) | Converts Rich Signell / CNC tide data (with `-fmt 2` and `-y2k` support) to JHC ASCII format. |
| [`refoXTIDE`](refoXTIDE.html) | Converts XTide raw UNIX epoch tide predictions (in feet) or `-v2` metric listings to JHC ASCII format. |
| [`simradTide`](simradTide.html) | Converts Kongsberg/Simrad ASCII tide files (`YYYYMMDDHHMM` + water level) to JHC ASCII format with sign inversion. |
| [`dutchTide`](dutchTide.html) | Converts Dutch Rijkswaterstaat (RWS) centimeter MLLW tide files to JHC ASCII format. |
| [`transTide`](transTide.html) | Converts Australian ("Oz") 81-byte fixed-record 15-minute centimeter tide files to JHC ASCII format. |
| [`refoCurrent`](refoCurrent.html) | Converts shipboard ASCII current/navigation logs into `asciiplot` files or OMG binary `jcu_nav_rec` (`-navfmt`) files. |
