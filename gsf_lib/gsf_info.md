---
layout: default
title: gsf_info
parent: GSF Library (gsf_lib)
nav_order: 5
tool_name: gsf_info
source_path: code/gsf_lib/gsf_info.c
category: GSF Library Module
input_formats: [".gsf"]
output_formats: ["status flags (int *)"]
related_tools: ["gsf", "gsf_dec", "gsf_enc", "gsf_indx"]
---

# gsf_info (`gsf_info.c`)

## Overview
`gsf_info.c` provides high-level inspection functions for `libgsf` that scan an open GSF file handle (`handle`) and report whether the file contains sufficient metadata and subrecords to support recalculating 3D sounding coordinates, Total Propagated Uncertainty (TPU), nominal depths, multibeam amplitude, or seabed snippet imagery. All functions rewind the file before scanning and restore the file pointer to the beginning of the file upon completion.

## Key Informational Functions

| Function | Capability Checked |
| :--- | :--- |
| `gsfFileSupportsRecalculateXYZ(int handle, int *status)` | Sets `*status = 1` if the file contains `GSF_RECORD_PROCESSING_PARAMETERS`, `GSF_RECORD_SOUND_VELOCITY_PROFILE`, and `GSF_RECORD_SWATH_BATHYMETRY_PING` records with valid travel-time and beam-angle arrays (plus sensor-specific transmit sector metadata where required). |
| `gsfFileSupportsRecalculateTPU(int handle, int *status)` | Sets `*status = 1` if the file contains all records needed to compute horizontal and vertical sounding uncertainty estimates. |
| `gsfFileSupportsRecalculateNominalDepth(int handle, int *status)` | Sets `*status = 1` if the file contains sufficient travel-time, angle, and draft information to calculate nominal (1500 m/s) depths. |
| `gsfFileContainsMBAmplitude(int handle, int *status)` | Sets `*status = 1` if `GSF_RECORD_SWATH_BATHYMETRY_PING` records contain beam-averaged amplitude subrecords (`mr_amplitude` or `mc_amplitude`). |
| `gsfFileContainsMBImagery(int handle, int *status)` | Sets `*status = 1` if `GSF_RECORD_SWATH_BATHYMETRY_PING` records contain Bathymetric Receive Beam (`brb_inten`) time-series snippet imagery. |
