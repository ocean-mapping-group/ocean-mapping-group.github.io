---
layout: default
title: EK_funcs (Internal Functions for EKlook)
parent: Simrad EK60/EK80 Echosounder Suite (EKlook)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 10
tool_name: EK_funcs
source_path: code/EKlook/EK_funcs.c
category: EKlook
input_formats:
- JHC Float Trace Arrays (.MF_dB, .Raw_dB, .PS_phase, .FA_phase, .MF_IQ)
- OMG_HDCS (.merged)
- OMG Attitude (.orientation)
- Pulse Replica (.pulse)
output_formats:
- Bottom Track Guide (.BottomTrackGuide)
- Ping Parameters (.ping_Params)
- Angular Response Curves (.ARC_fullBW, .ARC_3D, .ARC_FFTbins, .ARC_FFT3D)
related_tools:
- EKlook
- BatchProcEK
- comboCalibEK_ARCs
- ek_fft_funcs
---

# EK_funcs (Internal Functions for EKlook)

## Description
`EK_funcs.c` (`code/EKlook/EK_funcs.c`) is the shared computational and I/O library used by [`EKlook`](EKlook.html), [`BatchProcEK`](BatchProcEK.html), and [`comboCalibEK_ARCs`](comboCalibEK_ARCs.html). It handles loading the matched-filtered trace file family produced by `readEA600` (`.Raw_dB`, `.MF_dB`, `.PS_phase`, `.FA_phase`, `.MF_IQ`, `.pulse`, `.merged`, `.orientation`), computing seawater sound absorption and transmission loss, ray-tracing 3D bottom strike footprints, modeling ensonified seafloor area and beam-pattern roll-off, and accumulating/exporting 2D and 3D Angular Response Curves (ARCs).

## Core Function Groups

### 1. File Loading & Memory Management
*   `read_relevant_tracefiles(int forEKlook)`: Orchestrates loading `.Raw_dB`, `.MF_dB`, `.PS_phase`, `.FA_phase`, `.MF_IQ`, `.merged`, and `.orientation` files.
*   `ekload_MatchedFilter()`: Reads `<prefix>.pulse` to initialize pulse duration, bandwidth, transmit power, Frobenius norm, and autocorrelation arrays.
*   `ekload_Trace_Raw_dB()`, `ekload_Trace_MF_dB()`, `ekload_Trace_PS_phase()`, `ekload_Trace_FA_phase()`, `ekload_Trace_MF_IQ()`: Load individual JHC float and complex trace rasters.
*   `ekload_MergedFile()`, `ekload_Orientation()`, `ekload_OtherOrientation()`: Load navigation and attitude records.
*   `load_Backdrop()`, `load_Areas()`, `read_sphereTS()`: Load optional geographic backdrops, `.r4` area maps, and reference sphere TS curves.

### 2. Target Detection, Ray-Tracing & Ensonified Area
*   `search_for_Targets()` & `find_Zero_Phase()`: Detect seabed/target amplitude peaks and regress split-beam electrical phase zero-crossings.
*   `get_TxRxOrientation()`, `locate_Bottom_Strike()`, `locate_Bottom_Footprint()`: Interpolate vessel attitude at transmit/receive epochs and project the 3D beam cone onto the seafloor.
*   `calc_Ensonified_Area()`, `calc_Envelope_Ensonified()`, `calc3_Incidence()`: Compute pulse-length-limited and beamwidth-limited ensonified seafloor area and local grazing angles (including seafloor slope from `-areas`).
*   `calc_BP_rolloff_model()` & `calc_highincid_BP_rolloff_model()`: Compute 2D off-axis transducer beam-pattern compensation.

### 3. Broadband & Spectral ARC Accumulation and I/O
*   `calc_EnvWinFFTs(int traceno)`: Computes sliding short-window FFTs across the seabed echo envelope for spectral ARC extraction.
*   `flush_ARC()`, `add_to_ARC()`, `reduce_ARC()`: Manage `ARC_combo` histogram accumulators.
*   `stack_all_Envelopes_into_ARC()` & `stack_all_Broadband_Envelopes_into_ARC()`: Accumulate full-bandwidth and FFT sub-banded ARCs across all pings in a file.
*   `load_ARC()`, `load_ARC_3D()`, `dump_ARC()`, `dump_ARC_3D()`: Read and write `.ARC_fullBW`, `.ARC_3D`, `.ARC_FFTbins`, and `.ARC_FFT3D` files.
*   `dump_BStrack()`, `load_BStrack()`, `dump_pingParams()`, `load_pingParams()`: Read and write `<prefix>.BottomTrackGuide` and `<prefix>.ping_Params`.
*   `dump_Calib_Values()`, `load_Calib_Values()`: Export and import frequency-dependent calibration tables (`.txt.r4`).
