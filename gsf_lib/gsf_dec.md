---
layout: default
title: gsf_dec
parent: GSF Library (gsf_lib)
nav_order: 2
tool_name: gsf_dec
source_path: code/gsf_lib/gsf_dec.c
category: GSF Library Module
input_formats: [".gsf"]
output_formats: ["gsfRecords (in-memory C structs)"]
related_tools: ["gsf", "gsf_enc", "gsf_indx", "gsf_info", "gsf2omg_7101", "gsftest"]
---

# gsf_dec (`gsf_dec.c` / `gsf_dec.h`)

## Overview
`gsf_dec.c` contains all binary decoding routines for `libgsf`. When `gsfRead()` reads a raw GSF packet from disk into a byte buffer, `gsf_dec.c` unpacks big-endian (network byte order) integers, scaled arrays, timestamps, and sensor-specific subrecords into host-endian C data structures (`gsfRecords`) in engineering units.

## Key Decoding Functions

| Function | Record / Subrecord Decoded |
| :--- | :--- |
| `gsfDecodeHeader` | `GSF_RECORD_HEADER` (12-byte version string, e.g., `GSF-v03.04`). |
| `gsfDecodeSwathBathySummary` | `GSF_RECORD_SWATH_BATHY_SUMMARY` (time span, min/max lat, lon, and depth). |
| `gsfDecodeSwathBathymetryPing` | `GSF_RECORD_SWATH_BATHYMETRY_PING` — Unpacks ping header, scale factors (`DecodeScaleFactors`), scaled 1/2/4-byte beam arrays (`depth`, `across_track`, `along_track`, `travel_time`, `beam_angle`, `mr_amplitude`, `mc_amplitude`, `quality_flags`, etc.), sensor-specific subrecords (`DecodeReson7100Specific`, `DecodeR2SonicSpecific`, `DecodeEM3Specific`, `DecodeEM4Specific`, `DecodeSeaBat8101Specific`, etc.), and Bathymetric Receive Beam snippet time series (`DecodeBRBIntensity`). |
| `gsfDecodeSoundVelocityProfile` | `GSF_RECORD_SOUND_VELOCITY_PROFILE` (observation/application timestamps, coordinates, and depth/sound speed arrays). |
| `gsfDecodeProcessingParameters` | `GSF_RECORD_PROCESSING_PARAMETERS` (`KEY=VALUE` parameter strings). |
| `gsfDecodeSensorParameters` | `GSF_RECORD_SENSOR_PARAMETERS` (`KEY=VALUE` sensor parameter strings). |
| `gsfDecodeComment` | `GSF_RECORD_COMMENT` (timestamped comment text). |
| `gsfDecodeHistory` | `GSF_RECORD_HISTORY` (processing history log entry). |
| `gsfDecodeNavigationError` / `gsfDecodeHVNavigationError` | Navigation error estimate records. |
| `gsfDecodeAttitude` | `GSF_RECORD_ATTITUDE` (bundled time-series roll, pitch, heave, and heading arrays). |

## How Array Unscaling Works
For each beam array subrecord in a Swath Bathymetry Ping, `DecodeArraySubrecord()` inspects the `gsfScaleFactors` multiplier and offset for that subrecord ID, reads 1-, 2-, or 4-byte signed or unsigned integers per beam, divides by `multiplier`, and subtracts `offset` to yield double-precision engineering values:
$$\text{Value}_i = \frac{\text{Raw}_i}{\text{multiplier}} - \text{offset}$$
