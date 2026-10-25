---
layout: default
title: readADCP
parent: ADCP Tools
nav_order: 10
tool_name: readADCP
source_path: code/adcp/readADCP.c
category: adcp
input_formats:
  - RDI ASCII ADCP
  - WinADCP ASCII
  - jcu_nav (.nav)
  - OMG Attitude (.orientation)
  - JHC Float DTM (.r4)
  - OMG Map (.map)
output_formats:
  - JHC 8-bit Profile (.prof / .stack_prof / .map_prof)
  - JHC 32-bit Float Array (.r4 / .map_r4)
  - jcu_nav Depth-Averaged Vectors (.nav)
  - ASCII Stack Summary (.stack_ASCII)
related_tools:
  - readADCP_g
  - readADCP_mod
  - readWinADCP
  - combineMultiADCP
  - calc_ellipse2
  - makeTSmap
  - makeVectorPlot
---

# readADCP

## Description
`readADCP` is the primary command-line processor for reading, filtering, bottom-trimming, georeferencing, and visualizing data from Teledyne RD Instruments (RDI) Acoustic Doppler Current Profilers (ADCPs). It reads standard RDI ASCII output files (as well as WinADCP ASCII exports via `-winADCP`), integrates external vessel navigation, attitude, tidal height predictions, and multibeam bathymetric DTMs, and generates both time-series vertical profiles and georeferenced 2D cross-sectional curtains.

In addition to rendering 8-bit (`.prof`) and 32-bit floating-point (`.r4`) vertical sections of velocity magnitude, azimuth, radial/tangential velocity, vertical velocity, error velocity, or calibrated volume backscatter ($S_v$), `readADCP` computes depth-averaged current vectors for every ensemble and writes them to a binary `jcu_nav` file (`<outfile>.nav`) for downstream M2 tidal phase binning (`combineMultiADCP`) and tidal ellipse analysis (`calc_ellipse2`).

## Usage
```bash
readADCP -in <infiles> -out <outfile> [OPTIONS]
```

## Key Options

### Input/Output & Auxiliary Integration
| Option | Description |
|---|---|
| `-in <infilename(s)>` | **Required.** One or more input RDI ASCII ADCP files. |
| `-out <outfile>` | **Required.** Prefix for the output files (`.prof`, `.r4`, `.nav`, `.stack_prof`, `.map_prof`, etc.). |
| `-nav <navfile>` | Use an external `jcu_nav` binary navigation file for positioning. |
| `-use_adcp_nav` | Use the GPS navigation data embedded within the ADCP ensembles. |
| `-att <attfile>` / `-orientation <file>` | Use an external OMG attitude/orientation file for heading, pitch, and roll. |
| `-tidefile <tide.nav>` | Use an external `jcu_nav` file to provide time-varying tidal height corrections. |
| `-ref_level <m>` | Vertical datum reference offset (in meters) applied with `-tidefile`. |
| `-dtm_ref <terrain.r4>` | Use a JHC `.r4` bathymetric DTM grid to mask and trim acoustic sidelobes near/below the seafloor. |
| `-use_avbeam_depth` | Use the 4-beam average ADCP bottom-track depth to trim near-bottom sidelobes. |
| `-map <mapfile.map>` | Georeference and project the vertical profiles onto an OMG `.map` grid (`<outfile>.map_prof` and `<outfile>.map_r4`). |
| `-pixel <m>` | Horizontal pixel size (in meters) when projecting onto `-map`. |
| `-stack_in_map` | Average all ensembles falling into the same horizontal map bin when `-map` is active. |
| `-export_r4` | Export 32-bit floating-point JHC arrays (`<outfile>.r4` and `<outfile>.map_r4`) alongside the 8-bit `.prof` images. |
| `-winADCP` | Enable parsing mode for tabular ASCII files exported by RDI's WinADCP software. |
| `-dump_RPTZ` / `-dump_CURR` / `-dump_BINS` | (With `-winADCP`) Dump per-ensemble ASCII current or bin files. |

### Data Selection and Quality Filtering
| Option | Description |
|---|---|
| `-start <Y J H M>` / `-end <Y J H M>` | Set start and end time window (Year, Julian Day, Hour, Minute). |
| `-startYMD <Y M D H M>` / `-endYMD <Y M D H M>` | Set start and end time window using Year, Month, Day, Hour, Minute. |
| `-duration_min <mins>` | Set processing duration in minutes from the start time. |
| `-bounds_from <navfile>` | Inherit the start/end time window from an existing `.nav` file. |
| `-mindepth <m>` / `-maxdepth <m>` | Minimum and maximum depth range (in meters) for the vertical profile and depth-averaged current calculation. |
| `-bottom_ref` | Interpret `-mindepth` and `-maxdepth` as height above the seafloor instead of depth below the surface. |
| `-onlyuseshipheading <min> <max>` | Only process ensembles where the vessel heading falls within `[min, max]` degrees (0–360). |
| `-allowable_sum_percent_good <%>` | Minimum threshold for the 4-beam sum of "Percent Good" (max 400; default `100`). |
| `-maximum_believable_magnitude <mm/s>` | Reject velocity bins with magnitude exceeding this threshold (default `10000` mm/s). |

### Processing and Display Modes
| Option | Description |
|---|---|
| `-showMAG` | **(Default)** Output horizontal velocity magnitude in the profile. |
| `-showBS` | Output acoustic backscatter intensity (raw DN or calibrated $S_v$ in dB). |
| `-do_Sv` | (With `-showBS`) Apply spherical spreading and sound absorption corrections to compute volume backscatter strength $S_v$ (dB). |
| `-Er_DN_shift <val>` | Noise floor DN shift applied when computing calibrated backscatter (`-do_Sv`). |
| `-doalltrace` | Retain the full backscatter trace below the bottom-track pick. |
| `-showAZI` | Output horizontal flow direction (azimuth in degrees true). |
| `-showVERT` | Output vertical velocity component ($w$). |
| `-showERR` | Output 4-beam error velocity ($v_{err}$), scaled by `-max_err_vel <m/s>`. |
| `-showTAN` / `-showRAD` | Output tangential or radial velocity components relative to the `-map` orientation. |
| `-maxcurrent <m/s>` | Maximum current speed for scaling MAG, TAN, RAD, and VERT outputs. |
| `-BSrange <min> <max>` | Minimum and maximum backscatter values (DN or dB) for scaling `-showBS` outputs. |
| `-ensem_stack <num>` | Average (stack) data over `<num>` consecutive ensembles, producing `<outfile>.stack_prof` and `<outfile>.stack_ASCII`. |
| `-headbias <deg>` | Apply a constant transducer heading alignment correction in degrees. |
| `-delay <sec>` | Apply a clock delay offset in seconds when interpolating external navigation/attitude. |
| `-layers <num>` | Number of vertical depth bins in the output profile (default `100`). |

## Output Files
* **`<outfile>.prof`**: 8-bit JHC image file of the vertical profiles (columns = ensembles, rows = `-layers` depth bins).
* **`<outfile>.r4`**: (With `-export_r4`) 32-bit floating-point JHC array containing physical values (m/s, degrees, or dB).
* **`<outfile>.nav`**: Binary `jcu_nav` file containing the depth-averaged current speed (`velocity`) and direction (`azi`) between `-mindepth` and `-maxdepth` for each ensemble.
* **`<outfile>.stack_prof` & `<outfile>.stack_ASCII`**: (With `-ensem_stack`) Stacked 8-bit profile image and companion ASCII timestamp log (used as a guide by [`makeTSmap`](makeTSmap.md)).
* **`<outfile>.map_prof` & `<outfile>.map_r4`**: (With `-map`) Georeferenced 2D curtain projected onto the target mapsheet.

## See Also
* [ADCP Processing & Tidal Current Analysis Workflow](../workflows/adcp-processing-workflow.md)
* [`combineMultiADCP`](combineMultiADCP.md), [`calc_ellipse2`](calc_ellipse2.md), [`makeTSmap`](makeTSmap.md)
