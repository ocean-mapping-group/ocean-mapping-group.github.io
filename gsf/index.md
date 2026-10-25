---
layout: default
title: Generic Sensor Format — GSF (gsf)
parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 13
has_children: true
---

# GSF Tools

The **GSF (Generic Sensor Format)** toolset provides bidirectional conversion and inspection utilities between the SAIC/Leidos Generic Sensor Format (`.gsf`) and the OMG-HDCS (`.merged`, `.orientation`, `.param`, `.svp`, `.sonar_settings`) formats.

## Tool Summary

| Tool | Category | Description |
| :--- | :--- | :--- |
| [`omg2gsf`](omg2gsf.html) | Format Export | Converts OMG-HDCS `.merged`, `.merged.ss_data`, `.sonar_settings`, `.param`, and `.orientation` files into GSF (`.gsf`) with optional Reson 7k radiometric imagery calibration. |
| [`gsf2omg`](gsf2omg.html) | Format Import | Converts Reson 8100-series (`8101`, `8125`) GSF Swath Bathymetry Ping records into OMG-HDCS v3 `.merged` and `.merged.ss_data` files. |
| [`gsf2omg_7101`](gsf2omg_7101.html) | Format Import | Converts Reson SeaBat 7101 / 7125 (and Kongsberg EM122 `-sonar_EM122`) GSF files into OMG-HDCS v4 `.merged`, `.merged.ss_data`, `.sonar_settings`, and `.nav` files. |
| [`gsf2orientation`](gsf2orientation.html) | Attitude Extraction | Extracts GSF Attitude records (`GSF_ATTITUDE`) into a binary OMG-HDCS `.orientation` file. |
| [`gsf2param`](gsf2param.html) | Lever-Arm Extraction | Extracts lever-arm and angular alignment parameters from `GSF_SENSOR_PARAMETERS` records into an ASCII OMG `.param` file. |
| [`gsf2svp`](gsf2svp.html) | SVP Extraction | Extracts `GSF_SOUND_VELOCITY_PROFILE` records from a GSF file into numbered OMG `watercolumn` files (`<prefix>_001`, `_002`, ...). |
| [`gsfTool`](gsfTool.html) | Diagnostics | Scans a GSF file using the lightweight `omg_gsf` parser, reports record type counts, and dumps selected record IDs (`-vid`). |
| [`gsftest`](gsftest.html) | Diagnostics | Inspects GSF files using the full `gsf_lib` API, dumping R2Sonic, Reson 7125, Kongsberg EM4 (`EM710`/`EM302`/`EM122`), and EM3002 sensor/imagery subrecords, beam arrays, and snippets. |
| [`jgsf2omg`](jhc/jgsf2omg.html) | Format Import | Specialized GSF-to-OMG converter for CARIS HIPS GSF exports (e.g., SeaBat 7125). |
