---
layout: default
title: gsf_enc
parent: Embedded GSF C Library (gsf_lib)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 3
tool_name: gsf_enc
source_path: code/gsf_lib/gsf_enc.c
category: GSF Library Module
input_formats:
- gsfRecords (in-memory C structs)
output_formats:
- .gsf
related_tools:
- gsf
- gsf_dec
- gsf_indx
- gsf_info
- omg2gsf
---

# gsf_enc (`gsf_enc.c` / `gsf_enc.h`)

## Overview
`gsf_enc.c` contains all binary encoding routines for `libgsf`. When `gsfWrite()` is called, `gsf_enc.c` serializes host-endian `gsfRecords` C structures into network-byte-order (big-endian) GSF byte streams, applying scale factors and offsets to compress floating-point multibeam arrays into 1-, 2-, or 4-byte integers per beam.

## Key Encoding Functions

| Function | Record / Subrecord Encoded |
| :--- | :--- |
| `gsfEncodeHeader` | `GSF_RECORD_HEADER` (version string). |
| `gsfEncodeSwathBathySummary` | `GSF_RECORD_SWATH_BATHY_SUMMARY` (survey spatial and temporal bounds). |
| `gsfEncodeSwathBathymetryPing` | `GSF_RECORD_SWATH_BATHYMETRY_PING` — Encodes ping header, scale factors (`EncodeScaleFactors`), non-null beam arrays (`EncodeArraySubrecord`), sensor-specific subrecords (`EncodeReson7100Specific`, `EncodeR2SonicSpecific`, `EncodeEM3Specific`, `EncodeEM4Specific`, `EncodeSeaBat8101Specific`, etc.), and snippet time-series imagery (`EncodeBRBIntensity`). |
| `gsfEncodeSoundVelocityProfile` | `GSF_RECORD_SOUND_VELOCITY_PROFILE` (depth and sound velocity arrays scaled to cm and cm/s). |
| `gsfEncodeProcessingParameters` | `GSF_RECORD_PROCESSING_PARAMETERS` (`KEY=VALUE` processing strings). |
| `gsfEncodeSensorParameters` | `GSF_RECORD_SENSOR_PARAMETERS` (`KEY=VALUE` sensor strings). |
| `gsfEncodeComment` | `GSF_RECORD_COMMENT` (length-prefixed ASCII comment). |
| `gsfEncodeHistory` | `GSF_RECORD_HISTORY` (operator, host, command-line, and timestamp). |
| `gsfEncodeAttitude` | `GSF_RECORD_ATTITUDE` (bundled high-rate attitude arrays). |

## How Array Scaling Works
For each non-null beam array pointer in `gsfSwathBathyPing`, `EncodeArraySubrecord()` looks up the subrecord's `gsfScaleFactors` entry (`multiplier`, `offset`, and byte-size flag `c_flag`) and encodes each beam value $V_i$ as:
$$\text{Raw}_i = \text{round}\left((V_i + \text{offset}) \times \text{multiplier}\right)$$
converting the resulting 1-, 2-, or 4-byte integer to big-endian byte order via `htons()` / `htonl()`.
