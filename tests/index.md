---
layout: default
title: Acoustic & Mathematical Test Harnesses (tests)
parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 15
has_children: true
---

# Test, Simulation & Diagnostic Suite (`tests`)

The `tests/` (`code/tests/`) directory houses 28 standalone C utilities, physics simulators, numerical algorithm testbeds, and format-inspection tools authored primarily by John Hughes Clarke and collaborators (1992–2025). Throughout the development of the Ocean Mapping Group (OMG) software suite, `code/tests/` has served as the proving ground where new acoustic models, signal-processing filters, coordinate rotations, and oceanographic formulas are prototyped and validated before being integrated into core libraries (`liblocal.a`, `Echo_calib.c`, `j_watercolumn.c`, `DCM_rthand.c`, `ek80_parse_proc.c`) and interactive applications (`EKlook`, `DelayEditor`, `swathed`).

---

## Functional Categories & Tool Index

### 1. Acoustic Backscatter, Target Strength & Beam Pattern Modeling

| Tool | Source File | Description |
| :--- | :--- | :--- |
| **[`comboASCIIParam`](comboASCIIParam.html)** | `code/tests/comboASCIIParam.c` | Combines separate MATLAB ASCII exports of frequency (`-xval`), grazing angle (`-yval`), and backscatter (`-zval`) into 3D ASCII tables and OMG `.r4` / `.pack.r4` floating-point grids binned across grazing angle and frequency. |
| **[`comboASCIIParam2`](comboASCIIParam2.html)** | `code/tests/comboASCIIParam2.c` | Extended multi-spectral backscatter grid processor with linear least-squares frequency calibration detrending (`do_least_squares`), sonar altitude / seawater attenuation SNR masking (`calc_atten`), and grazing-angle (`-grz`) / frequency (`-frq`) slice averaging. |
| **[`dobessel`](dobessel.html)** | `code/tests/dobessel.c` | Computes cylindrical Bessel functions of the first kind $J_n(x)$ over $x \in [0, 10]$ via power-series expansion to a user-specified relative accuracy $\epsilon$, writing `besselSeriesPlotn0.txt`. |
| **[`fakeAR`](fakeAR.html)** | `code/tests/fakeAR.c` | Generates synthetic Angular Response (AR) backscatter curves across grazing angle ($0^\circ\text{–}90^\circ$) and frequency ($10\text{–}400\text{ kHz}$) using either Jackson's composite roughness/volume scattering model (`-RG`, `do_RG_simple_model`) or a parametric `-BSn`/`-BSo`/`-Crossover` model. |
| **[`plotTxRxOverlap`](plotTxRxOverlap.html)** | `code/tests/plotTxRxOverlap.c` | Generates a 36-frame sequence of OMG `plotlib` metafile plots (`plot_001.meta`–`plot_036.meta`) illustrating the effective two-way gain loss when transmit (Tx) and receive (Rx) beam patterns are angularly misaligned (`shift`). |
| **[`testSphereTS`](testSphereTS.html)** | `code/tests/testSphereTS.c` | C prototype of MacLennan's (1981) & Rudgers' (1967) modal series solution for the acoustic Target Strength ($\text{TS}$) of an elastic calibration sphere (e.g., $38.1\text{ mm}$ tungsten carbide) immersed in seawater. |
| **[`testfn`](testfn.html)** | `code/tests/testfn.c` | Calls `show_footprint(depth, beam_width, pulse_length)` from `Echo_calib.h` to test ensonified beam-footprint vs. pulse-length geometry across a multibeam swath. |

### 2. Chirp Waveforms, Matched Filtering & FIR Signal Processing

| Tool | Source File | Description |
| :--- | :--- | :--- |
| **[`testChirp`](testChirp.html)** | `code/tests/testChirp.c` | Comprehensive simulator for CW and linear FM (chirp) sonar pulses; models Hanning envelope tapering, transducer heave Doppler shift, additive white noise, harmonic distortion (`-doharmonics`), autocorrelation, multi-target reflection convolution, matched-filter pulse compression, and FFT spectra. |
| **[`testFIR`](testFIR.html)** | `code/tests/testFIR.c` | Simulates a vertical vessel heave profile composed of sinusoids (`-sine`) and step changes (`-step`), double-differentiates to acceleration, injects accelerometer bias (`-bias`), double-integrates back to drifted heave, and compares Hanning-weighted FIR detrending against FFT high-pass filtering. |
| **[`testNormConv`](testNormConv.html)** | `code/tests/testNormConv.c` | Benchmarks complex $I/Q$ matched-filter norms ($L_2$ Euclidean/Frobenius via GSL `gsl_blas_dznrm2`, $L_1$ via `gsl_blas_dzasum`, and manual sum-of-squares) and compares direct time-domain complex convolution (`cmplx_convolve`) against radix-2 FFT/IFFT frequency-domain multiplication (`four1`). |
| **[`findTCs`](findTCs.html)** | `code/tests/findTCs.c` | Classifies 10-minute passive acoustic `.wav` spectral/filtered envelope time series (`44.1 kHz` base rate) by counting high-amplitude transient spikes per minute (`-threshold`, `-aboveOK`) and generating `.wav.datetime` epoch metadata files. |

### 3. Seawater Sound Speed, Salinity Inversion & Acoustic Attenuation

| Tool | Source File | Description |
| :--- | :--- | :--- |
| **[`testAtten`](testAtten.html)** | `code/tests/testAtten.c` | Evaluates seawater acoustic absorption (`calc_atten` in $\text{dB/km}$) as a function of temperature, salinity, depth, pH, and frequency across interactive prompts, $T\text{–}S$ look-up tables (`-table`), or full CTD water-column casts (`-convert`, `-custom122` for EM122, `-custom710` for EM710). |
| **[`testSV`](testSV.html)** | `code/tests/testSV.c` | Tests empirical seawater sound speed equations (Wilson 1962 `-wilson`, Chen & Millero 1977 `-chenmill`) and UNESCO seawater density (`-unesco_density`), generates 2D $T\text{–}S$ sound speed `.r4` grids, and tests `j_watercolumn` SVP ray-trace interpolation (`-dotrace`). |
| **[`speed2salinity`](speed2salinity.html)** | `code/tests/speed2salinity.c` | Estimates practical salinity ($0\text{–}40\text{ ppt}$ in $1.0\text{ ppt}$ steps) from comma-separated `(depth, velocity, temperature)` sound velocity profiler casts by inverting Wilson's (1962) sound speed equation (`vsw`). |
| **[`speedtosalinity`](speedtosalinity.html)** | `code/tests/speedtosalinity.c` | Higher-precision ($0.1\text{ ppt}$ resolution) salinity inversion utility supporting user selection between Wilson's (1962) (`-wilson`) and Chen & Millero's (1977) (`-cml`) sound speed equations. |
| **[`one`](one.html)** | `code/tests/one.c` | Standalone C source module implementing `this_vchemilli(t, p, s)` (Chen & Millero 1977 sound speed equation, containing a historical `+ pow(t,4)` typo in term `a3` later documented and fixed in `testSV.c` and `two.c`). |
| **[`two`](two.html)** | `code/tests/two.c` | Standalone C source module implementing the corrected `vchemilli(t, p, s)` Chen & Millero (1977) empirical seawater sound speed polynomial with optional term-by-term diagnostic printouts. |

### 4. Vessel Attitude, Lever-Arm Rotation & Horizon Geometry

| Tool | Source File | Description |
| :--- | :--- | :--- |
| **[`testrot`](testrot.html)** | `code/tests/testrot.c` | Interactive testbed for 3D Direction Cosine Matrix (DCM) coordinate transformations (`DCM_rotate` and `DCM_unrotate` from `DCM_rthand.h`), verifying vector length invariance between geographic (`GEO`) and vessel (`SONAR`) reference frames. |
| **[`twistVRU`](twistVRU.html)** | `code/tests/twistVRU.c` | Interactive solver for Vertical Reference Unit (VRU / MRU) yaw misalignment (`YM`); converts between observed roll/pitch (`OR`, `OP`) and true vessel roll/pitch (`TR`, `TP`) via forward (`RtoO`) and inverse (`OtoR`) coupled trigonometric equations. |
| **[`getHorizonRollPitch`](getHorizonRollPitch.html)** | `code/tests/getHorizonRollPitch.c` | Estimates camera/vessel roll, pitch, and vertical pixel shift from left and right horizon edge-detection profile files using threshold crossing (`-threshold`) and focal-plane baseline geometry (`-acrossdist`, `-alongdist`, `-pitchlevel`). |
| **[`interpMRU`](interpMRU.html)** | `code/tests/interpMRU.c` | Serial port listener (`/dev/ttyd2`) and binary packet decoder for 25-byte Motion Reference Unit (`'q'` header) frames containing 3-axis IEEE-754 floating-point angular orientations (`angP`, `angR`, `angY`) and linear accelerations (`accelX`, `accelY`, `accelZ`). |
| **[`drawCustom`](drawCustom.html)** | `code/tests/drawCustom.c` | Generates multi-curve ASCII plot files (`draw.ascii`) quantifying angular yaw error vs. slant range (`YAW` mode) or horizontal/vertical bathymetric displacement vs. pitch angle (`-pitch` mode). |
| **[`testRangeAzi`](testRangeAzi.html)** | `code/tests/testRangeAzi.c` | Interactive geodetic dead-reckoning calculator that projects a starting latitude/longitude (in decimal degrees or degrees/decimal minutes) along a given radial distance (meters) and azimuth ($0^\circ\text{–}360^\circ$). |

### 5. Binary/JSON Format Inspection & File Utilities

| Tool | Source File | Description |
| :--- | :--- | :--- |
| **[`readJSON`](readJSON.html)** | `code/tests/readJSON.c` | Recursive JSON parser built on `json-c` (`<json.h>`) for inspecting CRIMAC / Kongsberg Simrad EK80 processing metadata, filter coefficients (`FIL1`), and complex $I/Q$ quadrant arrays (`RAW3`). |
| **[`read4bit`](read4bit.html)** | `code/tests/read4bit.c` | Inspects 4-bit nibble-packed binary files, printing 32-bit and 8-bit binary representations (`print32bits`, `print8bits`) in verbose mode and masking the upper 4-bit nibble (`onebyte & 240`) to an output file. |
| **[`stripRawDoc`](stripRawDoc.html)** | `code/tests/stripRawDoc.c` | Forensic binary file carver and string searcher; either scans raw disk/stream dumps for a target ASCII string (`-string`) and extracts printable text, or carves embedded Microsoft Office OLE2 Compound Documents (`.doc`, `.ppt`) by matching 32-byte header and 80-byte EOF signatures (`-grab_microsoft`). |
| **[`getCR`](getCR.html)** | `code/tests/getCR.c` | Bidirectional line-ending converter between Mac/DOS Carriage Return (`ASCII 13`) and Unix Line Feed (`ASCII 10`), with `-reverse` mode converting Unix `LF` (`10`) to DOS/Windows `CR+LF` (`13 10`). |
| **[`test64`](test64.html)** | `code/tests/test64.c` | Architecture diagnostic utility that prints `INTEL` vs. `MOTOROLA` endianness flags from `swapio.h`, C primitive type sizes (`sizeof(long int)`, `int`, `short`, `float`, `double`), and 64-bit `fseek`/`ftell` file-length behavior. |
