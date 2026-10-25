---
layout: default
title: modelAnalysis
parent: Ian Church — Hydrodynamic & 3D Ray-Trace Suite (ianc)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 7
tool_name: modelAnalysis
source_path: code/ianc/modelAnalysis.c
category: Ocean Modeling & Hydrographic Utilities (ianc)
input_formats:
- FVCOM NetCDF (.nc)
- CARIS SVP (.svp)
- RDI ADCP / WinADCP
- OMG Attitude (.orientation)
- OMG Binary Navigation (.nav)
- OMG R4 Area Mask (.r4)
- MVP .m1
output_formats:
- FVCOM NetCDF (in-place variables)
- CARIS SVP (.svp)
- OMG Binary Navigation (.nav)
- Ocean Data View (.txt)
- ArcGIS Vector (.txt)
- CSV Error & Flux Reports (.csv)
- OMG JHC Map Sheet Headers
related_tools:
- modelMerge
- HycomSSP
- oceanReader
- iwc_support
- iwc_water
- iwc_adcp
---

# modelAnalysis

## Description

`modelAnalysis` is the primary hydrodynamic model analysis, validation, ray-tracing, and volume-flux computation engine in the `ianc` suite. Developed by Ian Church between 2011 and 2014 (spanning over 4,800 lines of C), `modelAnalysis` ingests unstructured-grid Finite Volume Community Ocean Model (FVCOM) NetCDF outputs (local `.nc` files or online `-NEGOFS` forecasts) and integrates them with hydrographic field observations including CARIS `.svp` sound velocity profiles, vessel-mounted RDI ADCP / WinADCP current profiles, OMG `.orientation` attitude files, and `.nav` navigation tracks.

The tool supports seven major workflows:
1. **3D Sound Speed & Synthetic SVP Generation**: Computes Chen-Millero sound speed across all FVCOM sigma layers and nodes (`-calc_ssp`), extracts synthetic `.svp` casts at observed SVP locations (`-svp_model`) or along a decimated navigation track (`-calc_svp_nav`).
2. **SVP Model-Observation Error Statistics**: Computes time-interpolated differences (`model - observation`) for sound speed, temperature, and salinity stratified by freshwater (`<10` PSU), brackish (`10–20` PSU), and saltwater (`>20` PSU) regimes (`-svp_error`, `-output_error`, `-output_sal_diffs`).
3. **ADCP Assimilation, Heading Correction & Validation**: Reads binary ADCP ensembles (`-adcp`, `-winADCP`), corrects compass bias using OMG `.orientation` attitude data (`-heading`), maps ADCP bins onto FVCOM triangular elements and sigma layers, writes ADCP velocities and model-observation residuals directly into the NetCDF file (`-add2model`, `-fsADCP`), and computes regional maximum currents within an `.r4` polygon mask (`-areaCalc`, `-levels`).
4. **Multibeam Ray-Tracing Uncertainty Analysis**: Traces acoustic rays at a specified swath angle (`-swath`, default `65°`) and transducer draft (`-draft`) through the time-varying 3D FVCOM sound speed field (`modelTT()`) and compares the resulting depth against depths reconstructed using reference SVP casts (`-svp_ref`, `depthWRefSVP()`) against IHO standards (`-iho_ratio`), writing `ray_error`, `percent_error`, and `iho_error` variables into the NetCDF file.
5. **Cross-Sectional Volume Flux Calculation**: Integrates total, freshwater, brackish, and saltwater volume flux across a user-defined transect (`-calcVFlux`, `-start`, `-end`, `-outFlux`, `-outODVFlux`), optionally incorporating optical backscatter (`extra_field`) from nearby `.svp` casts.
6. **Automated Transect Profile Segmentation**: Fits piecewise linear transect segments to a set of SVP cast locations using recursive RMS splitting (`-Profile`, `-use_Profile`, `-create_Headers`).
7. **Residual Currents & GIS / ODV Exports**: Computes tidal residual velocity vectors (`-resid`, `-output_arcmap`) and exports node, element, model-at-SVP, or flux-transect data to Ocean Data View (`-outODVNode`, `-outODVEle`, `-outODVModel`, `-outODVFlux`).

## Usage

```bash
modelAnalysis [-v] -nc <netcdf_file> [model_options] [svp_options] [adcp_options] [raytrace_options] [flux_options]
```

### Example Commands

Calculate 3D sound speed in an FVCOM NetCDF file and evaluate model vs. observed SVP cast errors:

```bash
modelAnalysis -v -nc sjh_fvcom.nc -Year 2011 -JDay 172 -Hour 0 -Min 0 -Sec 0 \
              -svp_error -svp casts/*.svp -output_error svp_stats.csv
```

Compare vessel-mounted ADCP data (with HDCS orientation heading correction) against FVCOM element velocities and embed the results in the NetCDF file:

```bash
modelAnalysis -v -nc sjh_fvcom.nc -Year 2011 -JDay 172 -Hour 0 -Min 0 -Sec 0 \
              -adcp line01.adcp -winADCP -draft 1.15 -heading vessel.orientation \
              -add2model -dumpDiffs adcp_diffs.txt -output_error adcp_stats.csv
```

Perform multibeam ray-tracing depth error analysis across the FVCOM grid using reference SVP casts at a 65° swath angle:

```bash
modelAnalysis -nc sjh_fvcom.nc -Year 2011 -JDay 172 -Hour 0 -Min 0 -Sec 0 \
              -svp_ref ref_cast01.svp ref_cast02.svp -draft 1.2 -swath 65 -iho_ratio 0.75
```

Compute cross-channel volume flux across a transect between two lat/lon endpoints:

```bash
modelAnalysis -nc sjh_fvcom.nc -Year 2011 -JDay 172 -Hour 0 -Min 0 -Sec 0 \
              -calcVFlux -start 45.261 -66.050 -end 45.257 -66.045 \
              -outFlux transect_flux.csv -outODVFlux transect_odv
```

## CLI Arguments and Options

### Model & General Options

| Flag / Argument | Parameters | Description |
| :--- | :--- | :--- |
| `-v` | None | Enables verbose diagnostic output. |
| `-nc` | `<netcdf_File>` | **Required.** Input (and in-place output) FVCOM NetCDF file. |
| `-lat` | `<degrees>` | Approximate latitude of the model domain for pressure/gravity calculations (default: `45.0`). |
| `-Year`, `-JDay`, `-Hour`, `-Min`, `-Sec` | `<int>` | Start timestamp of the FVCOM model run (required for `-svp_error`, `-svp_model`, `-calc_svp_nav`, and `-svp_ref`). |
| `-NEGOFS` | None | Uses Lambert Conformal Conic projection parameters configured for the Northeast Coastal Ocean Forecast System (NEGOFS) grid. |
| `-calc_ssp` | None | Computes 3D sound speed (`sound_speed`) from model `temp` and `salinity` using `ChenMillero()` and writes it into the NetCDF file. |
| `-output_ssp` | `<soundSpeed.xyz>` | Exports calculated sound speed values to an ASCII file. |
| `-output_elev` | `<output.txt>` | Outputs the tidal elevation (`zeta`) time series of a model node to a text file. |
| `-calc_svp_nav` | `<input.nav>` | Generates synthetic CARIS `.svp` profiles along the decimated track of an input `.nav` file. |
| `-navIn` / `-navOut` | `<in.nav>` / `<out.nav>` | Reads `<in.nav>` and writes `<out.nav>` populated with model velocity direction and magnitude at each navigation point. |
| `-resid` | None | Computes time-averaged residual northward and eastward current velocities across the model run and stores `resid_north` / `resid_east` in the NetCDF file. |
| `-output_arcmap` | `<arcMapVect.txt>` | Exports residual surface/depth-averaged velocities as an ArcGIS vector text file (`Node,Lat,Lon,Mag,Angle`). |
| `-output_error` | `<output.csv>` | Writes summary error statistics (mean, standard deviation, RMSE, central frequency, outliers) for SVP and/or ADCP comparisons to CSV. |
| `-velLoc` / `-outVel` | `<lat> <lon>` / `<vel.csv>` | Extracts velocity time series at the element closest to `<lat> <lon>` and writes to `<vel.csv>`. |

### SVP, Profile & ODV Options

| Flag / Argument | Parameters | Description |
| :--- | :--- | :--- |
| `-svp` | `<svp_file1> [...]` | Loads up to 10,000 CARIS `.svp` observation files. |
| `-nav_svp` | `<navfile.nav>` | Writes the spatial positions and timestamps of loaded `-svp` casts as an OMG binary `.nav` file. |
| `-svp_error` | None | Computes model-minus-observation sound speed, temperature, and salinity errors at each cast location and depth (requires model start time and `-svp`). |
| `-svp_model` | None | Extracts synthetic `.svp` profiles from the FVCOM model at the exact times and locations of the input `-svp` casts. |
| `-output_sal_diffs` | `<SalDiffOutput.txt>` | Writes detailed salinity differences between model and observations to a text file. |
| `-Profile` | `<profile.txt>` | Computes a piecewise linear transect through the `-svp` cast coordinates (splitting segments whenever RMS distance exceeds `RMSLimit = 50` m) and writes `<profile.txt>`. |
| `-use_Profile` | `<profile.txt>` | Reads a previously generated profile segment file for transect analysis. |
| `-create_Headers` | None | Generates OMG `JHC_header` map sheet header files for each profile segment for visualization in `plotSVP`. |
| `-outODVNode` | `<odvNodeFile.txt>` | Exports model node variables (such as salinity) to an Ocean Data View spreadsheet. |
| `-outODVEle` | `<odvEleFile.txt>` | Exports model element variables (velocity magnitude) to an Ocean Data View spreadsheet. |
| `-outODVModel` | `<odvProfiles.txt>` | Exports model profiles extracted at `-svp` cast locations to an Ocean Data View file. |

### ADCP, Ray-Tracing & Volume Flux Options

| Flag / Argument | Parameters | Description |
| :--- | :--- | :--- |
| `-adcp` | `<ADCP_inputFile>` | Reads a binary RDI ADCP file (`jADCP_read_header`) for comparison or assimilation into the model grid. |
| `-winADCP` | None | Parses the input ADCP file using WinADCP header/record conventions (`jwinADCP_read_header`). |
| `-heading` | `<file.orientation>` | Corrects ADCP compass heading using an OMG HDCS attitude file (`OMG_HDCS_read_attitude`) and recalculates bin E/W and N/S velocity components via `fixADCPBinVel()`. |
| `-add2model` | None | Writes gridded ADCP northward/eastward velocities (`adcp_north`, `adcp_east`) and model differences (`adcp_north_diff`, `adcp_east_diff`) into the FVCOM NetCDF file. |
| `-fsADCP` | None | Clears/resets existing ADCP variables in the NetCDF file before adding new ADCP observations. |
| `-dumpDiffs` | `<ADCPDiffFile.txt>` | Writes individual ADCP vs. model velocity comparisons to a text file. |
| `-nav_adcp` | `<navfile.nav>` | Exports ADCP ensemble positions and timestamps to an OMG binary `.nav` file. |
| `-areaCalc` | `<area.r4>` | Restricts SVP error or ADCP/model maximum current analysis to nodes/elements falling within valid pixels of `<area.r4>`. |
| `-levels` | `<l1> [l2 ...]` | Specifies model sigma layer indices (e.g., `-levels 2 11 19`) for level-specific maximum current extraction. |
| `-svp_ref` | `<svp_file1> [...]` | Enables multibeam ray-tracing uncertainty analysis using the specified reference `.svp` casts. |
| `-draft` | `<meters>` | Transducer draft in meters for ADCP bin depth offset or ray-tracing start depth. |
| `-swath` | `<degrees>` | Maximum multibeam swath angle from nadir in degrees for ray-tracing error analysis (default: `65`). |
| `-iho_ratio` | `<float>` | Fraction of the IHO Special Order total vertical uncertainty budget allocated to sound speed error (default: `1.0`). |
| `-calcVFlux` / `-flipVFlux` | None | Computes volume flux (total, salt `>20` PSU, brackish `10–20` PSU, fresh `<10` PSU) across the transect from `-start <lat> <lon>` to `-end <lat> <lon>`. `-flipVFlux` reverses the across-transect sign convention. |
| `-maxdist` | `<meters>` | Maximum distance in meters (default: `100`) to associate an `-svp` optical backscatter cast with the flux transect. |
| `-navOBSsvp` | `<navfile.nav>` | Outputs `.svp` casts used in optical backscatter flux calculations as a `.nav` file. |
| `-outFlux` / `-outODVFlux` | `<csv>` / `<prefix>` | Writes time-series volume flux results to `<csv>` and/or per-timestep transect grids to ODV files. |

## File Formats

* **FVCOM NetCDF (`.nc`)**: Unstructured finite-volume mesh with dimensions `node`, `nele`, `siglay`, `siglev`, and `time`, and variables `x`, `y`, `xc`, `yc`, `nv`, `h` (depth), `zeta`, `temp`, `salinity`, `u`, `v`, `wet_nodes`, and `Itime`/`time`. `modelAnalysis` can also define and populate new NetCDF variables in-place: `sound_speed`, `ray_error`, `percent_error`, `iho_error`, `resid_north`, `resid_east`, `adcp_north`, `adcp_east`, `adcp_north_diff`, and `adcp_east_diff`.

## How It Works

1. **Mesh & Coordinate Projection Setup**: `modelAnalysis` opens the FVCOM NetCDF file in `NC_WRITE` mode, reads the unstructured node (`x`, `y`) and element centroid (`xc`, `yc`) coordinates, and converts geographic observation coordinates (`lat`, `lon`) into the model's projected coordinate system (UTM or Lambert Conformal Conic via `PROJ` / `geo_to_utm()`).
2. **Spatiotemporal Interpolation**: Using `closeDist()` and `closeTime()` (from `iwc_support.c`), field observations (SVP casts, ADCP ensembles, or navigation points) are matched to the closest wet model node or element centroid and linearly interpolated between bracketing model time steps using inverse time-difference weights (`weight1`, `weight2`).
3. **Harmonic Ray Tracing (`modelTT` and `depthWRefSVP`)**: For each wet node and time step when `-svp_ref` is active, `modelTT()` traces a ray launched at `swathWidth` degrees from `draft` through each model sigma layer (`layDepth * (h + zeta)`) using Snell's Law (`sin(theta_i) / c_i = p`) and harmonic layer sound speeds to compute true one-way travel time `TT`. `depthWRefSVP()` then reconstructs the apparent depth along that ray using the nearest reference `.svp` cast and `TT`, storing the vertical depth error (`ray_error`), percentage depth error (`percent_error`), and ratio to the IHO Special Order limit (`0.25^2 + (0.0075 * depth)^2`) in the NetCDF file.
4. **Transect Flux Integration (`-calcVFlux`)**: The line between `-start` and `-end` is discretized into `nInterp = 100` segments. At each segment and sigma layer, velocities (`u`, `v`) and salinity are inverse-distance-weighted from the 3 closest elements/nodes (`closeDist`, `closeDist2`, `closeDist3`), rotated into across-transect and along-transect components, multiplied by the vertical cell cross-sectional area `fluxArea`, and integrated over time into total, saltwater, brackish, and freshwater volume fluxes.
