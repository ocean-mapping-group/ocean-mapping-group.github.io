---
layout: default
title: plotSVP
parent: Ray Tools
nav_order: 169
---
# plotSVP

## Description
`plotSVP` is a comprehensive plotting and processing utility for Sound Velocity Profiles (SVPs). It can read SVP data from various formats (Simrad, MVP, Seabird, JWC, custom ASCII), calculate derived parameters (salinity, density, gradients, Richardson number), and then generate 2D plots (profiles, time-series, raster images) of these parameters.

The tool supports advanced features such as plotting multiple SVPs on the same graph, filtering profiles based on area or time, painting profiles into a 2D array, and outputting processed SVPs in JWC (JHC Water Column) format. It's a critical tool for analyzing, visualizing, and standardizing SVP data within oceanographic workflows.

## Usage
```bash
plotSVP <svpfilename(s)> [-outfile <filename.meta>] [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<svpfilename(s)>` | **Required.** One or more input SVP filenames. The type of SVP file is specified by the `-svp_type` options. |
| `-outfile <filename.meta>` | Specifies the output PostScript metafile name. | `plot.meta` |

### SVP Input Formats
| Option | Description |
|---|---|
| `-newsvp` | Input file is a "NEW" raw SVP format. |
| `-seabird` | Input file is a Seabird format. |
| `-seabird_911` | Input file is a Seabird 911 format.
    *   `-navo_911` / `-rvgs19plus` / `-hsl_19plus`: Sub-types for Seabird 911. |
| `-mvp` / `-mvp2` / `-mvp3` / `-mvp_m1` / `-mvp_raw` | Various MVP (Moving Vessel Profiler) formats.
    *   `-mvp_type <#>`: Specifies content (0-SV, 1-SV,T, 2-S,T, 3-S,T,OBS).
    *   `-m1_order <#>`: Specifies data order in MVP_m1.
    *   `-extra_m1_lines <#>`: Extra lines to skip in MVP_m1. |
| `-cnv` / `-svplus_cnv` | CNV (Conductivity-Temperature-Depth) formats. |
| `-asvp` | ASVP (Autonomous Sound Velocity Profiler) format. |
| `-jWC` | JWC (JHC Water Column) format. |
| `-nic_rich` | NIC_RICH format (for Richardson number). |
| `-os500` | OS500 Engineering format. |
| `-adcp_1` | ADCP format (for current data). |
| `-aml_csv` | AML CSV format. |
| `-custom1` / `-custom2` | Custom ASCII formats. |

### Output Types (`-to_plot`)
| Option | Description |
|---|---|
| `-velo` | Plot sound velocity (default). |
| `-temp` | Plot temperature. |
| `-sali` | Plot salinity. |
| `-dens` | Plot density. |
| `-tsplot` | Plot salinity vs. temperature (T-S plot). |
| `-harm_velo` | Plot harmonic mean velocity. |
| `-harm_v_twtt` | Plot harmonic mean velocity vs. TWTT. |
| `-millivolts` / `-macrovolts` | Plot millivolts/macrovolts. |
| `-density` | Plot density. |
| `-density_gradient` | Plot density gradient. |
| `-density_difference` | Plot density difference from a reference SVP (`-refval`). |
| `-velocity_gradient` | Plot velocity gradient. |
| `-richardson` / `-truncated_richardson` | Plot Richardson number. |
| `-curr` | Plot current magnitude (from ADCP). |
| `-bscat` | Plot backscatter (from ADCP). |
| `-turbidity` / `-dissolved_oxygen` / `-fluorescence` | Plot various water quality parameters. |
| `-beam_attenuation` / `-beam_transmission` | Plot beam attenuation/transmission. |

### Plotting & Filtering
| Option | Description | Default |
|---|---|
| `-together` | Plot all SVPs on the same graph. | |
| `-sparse` | (Not fully implemented) Intended for sparse plotting. | |
| `-xrange <min> <max>` / `-yrange <min> <max>` | Sets X/Y axis ranges. | Auto-determined for X, Y: `1410-1510` (SV), `0-0` (depth). |
| `-validVels <min> <max>` | Filters out sound velocities outside this range. | `1440-1540` |
| `-ts_square_range <min> <max>` / `-ts_diamond_range <min> <max>` | For T-S plots, marks points within these ranges with squares/diamonds. | |
| `-downcast` | Only uses the downcast portion of the profile. | |
| `-pen <val>` | Sets the pen color for the plot. | `7` (black) |
| `-pen_line <val>` | Sets the pen color for the line (if different from point). | `1` (red) |
| `-highlight <val>` | Highlights a specific SVP file by changing its plot color. | |
| `-rainbow` | Uses a rainbow color scheme for multiple SVP plots. | |
| `-lastNfiles <val>` | Only processes the last N files in the input list. | |
| `-profile <list_coords.llz>` | Plots SVP locations along a predefined profile. | |
| `-paint_in_profile <width> [-flip_paint] [-force_paint] -bottom_profile <file.llz>` | Paints SVP data into a 2D raster along a profile, using bottom profile info. | |
| `-array [-Xpixel <val>] [-Zpixel <val>] [-maxinterp <val>] [-rotate_array]` | Generates a 2D array file (`.r4`) of SVP data (vs. horizontal and vertical). | |
| `-table <col> <row>` | Arranges multiple plots in a table format. | |
| `-ancil <file.txt>` | Ancillary data file for background rendering in raster plots. | |

### Time & Location
| Option | Description |
|---|---|
| `-start <yr> <jday> <hr> <min>` / `-end <yr> <jday> <hr> <min>` | Sets a time window for processing SVPs. |
| `-usePCtime` / `-useBOTtime` | Uses PC time or BOT time for MVP files. |
| `-useBOTlatlon` | Uses BOT reported latitude/longitude for MVP files. |
| `-obs_lalo <lat> <lon>` | Observed latitude and longitude for the SVP. |
| `-obs_time <yr> <jday> <hr> <min>` | Observed time for the SVP. |
| `-navTimeBounds <navfile.nav>` | Uses time bounds from a navigation file. |
| `-external_navfile <navfile>` / `-external_nav_timeshift <shift>` | External navigation file for geo-referencing SVPs. |
| `-force_ZDA <yr> <jday>` | Forces ZDA year and Julian day. |
| `-addGPSrolloverwraps <val>` | Adds GPS rollover adjustment. |

### Density & Gradient
| Option | Description |
|---|---|
| `-density_difference -refval <refval.m1> -refsal <val> -reftemp <val>` | Calculates density difference from a reference SVP (MVP_m1 format) with reference salinity and temperature. |
| `-sali_scale <val>` / `-dens_scale <val>` | Scales salinity/density values. |

### Titles & Footers
| Option | Description |
|---|---|
| `-tit1 <string>` / `-tit2 <string>` | Sets plot titles. | |
| `-footer <string>` | Sets a footer for the plot. | |
| `-refazi <val>` | Reference azimuth for current plotting. | |

### Debugging
| Option | Description |
|---|---|
| `-v` | Enable verbose output. | |
| `-skip_extra <val>` | Skips extra lines. | |

## How It Works
1.  **Initialization:** Parses command-line arguments to set numerous options for SVP type, plotting parameters, filters, and output.
2.  **File Setup:**
    *   Opens a `plotlib` PostScript output (`plot.meta`).
    *   If `svp_type` is MVP-related, JWC, etc., it opens `svp.coords` to list SVP locations.
    *   If `array_flag` is set, it opens `svp.r4` for 2D array output.
    *   If `prof_flag` is set, it reads profile coordinates from `profname`.
    *   If `area_flag` or `only_in_area_flag` is set, it reads map header information from `areaname`.
    *   If `refvalname` is set (for density difference), it reads the reference MVP data into `the_refval`.
    *   If `ancilname` is set, it reads ancillary OS500 data.
    *   If `navTimeBounds` or `external_navfile` is set, it reads navigation data for time/location matching.
3.  **SVP Data Reading Loop:** Loops through each input SVP file specified by `svpfilename(s)`:
    *   Opens the input SVP file(s).
    *   Reads the SVP data based on `svp_type` (Simrad, MVP, Seabird, JWC, etc.), handling various header formats and data structures.
    *   For some types (MVP, Seabird), it attempts to extract time and geographic location (using NMEA `GPGGA` and `GPZDA` parsing, or `external_navfile`).
    *   Performs data validation (e.g., `validVels`) and derived calculations (e.g., guessing salinity from T, P, V; calculating harmonic velocity, gradients, Richardson number, density difference).
    *   **Downcast Filtering (`-downcast`):** If set, it truncates the SVP to only include the downcast portion.
    *   **JWC Output (`-outasJWC`):** If set, it writes the processed SVP data to a JWC file (`.jwc`), collapsing to 0.2m bins if `collapseJWC` is set.
    *   **Array Output (`-array`):** If `array_flag` is set, it paints the SVP data into a 2D float array (`svpXZ`), which can be rotated. This array represents SVP parameter values against depth and horizontal position/time.
    *   **Profile Painting (`-paint_in_profile`):** If set, it paints the profile's data into the `svpXZ` array, creating a visual representation of the profile along a track.
4.  **Plotting:**
    *   Sets up the plotting area (potentially in a table format if `tableX`/`tableY` are set).
    *   Adds titles and footers.
    *   Draws X/Y axes and labels (velocity/salinity/temperature/etc. vs. depth).
    *   Plots the SVP data as lines, using different pens for different files or highlighting (if `rainbow_flag`, `highlight`).
    *   For T-S plots, it can mark points with squares or diamonds based on range.
    *   For current plots (`-curr`), it can draw current vectors.
    *   If `tableX/tableY` are set, it divides the plotting area and plots each SVP in its respective cell.
5.  **Raster Output (`-raster`):** If `raster_flag` is set, it generates a raster image (`.raster`) of the SVP data (e.g., velocity vs. depth, or currents).
6.  **Cleanup:** Closes all open files and `plotlib` output.

## Output Files
*   `<outfile_name>`: A PostScript metafile (`.meta`) containing the SVP plots.
*   `<svpfilename_prefix>.coords`: ASCII file listing SVP locations.
*   `<svpfilename_prefix>.r4`: JHC `.r4` array file containing SVP data (if `-array` is used).
*   `<svpfilename_prefix>.jwc`: JWC format SVP file (if `-outasJWC` is used).
*   `<svpfilename_prefix>.raster`: Raster image file (if `-raster` is used).
*   `density_contrib.dump.txt`: Debug dump for density difference calculations.

## Dependencies
*   `plotlib.h`: For `plotlib` functions.
*   `support.h`: For general utility functions.
*   `stdtime.h`: For time conversion.
*   `array.h`: For `JHC_header` structure.
*   `j_proj.h`: For coordinate projection functions.
*   `j_watercolumn.h`: For water column structures and functions.
*   `jcu_nav.h`: For navigation data structures.

## Notes
`plotSVP` is a versatile tool for comprehensive analysis and visualization of sound velocity profiles, which are crucial for accurate multibeam sonar data processing. Its ability to handle diverse input formats and calculate derived oceanographic parameters makes it an invaluable asset in oceanographic research and hydrographic surveying. The tool offers a wide range of plotting and output options for flexible data representation.