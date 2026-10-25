---
layout: default
title: eXtended Triton Format — XTF (xtf)
parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 9
has_children: true
---

# XTF Tools

The **XTF (eXtended Triton Format)** toolset provides utilities for inspecting, indexing, extracting, and converting multi-vendor multibeam and sidescan sonar data logged in Triton Imaging XTF (`.xtf`) containers into the OMG-HDCS (Ocean Mapping Group - Hydrographic Data Conversion System) and GLORIA processing formats.

## Tool Summary

| Tool | Category | Description |
| :--- | :--- | :--- |
| [`xtfTool`](xtfTool.html) | Diagnostics & Indexing | Inspects XTF packet inventories, dumps packet contents to ASCII, writes `.idx` packet indices, and extracts raw traces, snippets, or R2Sonic payloads. |
| [`xtf2omg_reson`](xtf2omg_reson.html) | Multibeam Conversion | Converts Reson SeaBat (8101, 8111, 8125, 8150, 8160) bathymetry, sidescan traces, and snippets from XTF to OMG-HDCS v3 format. |
| [`xtf2omg_r2sonic`](xtf2omg_r2sonic.html) | Multibeam Conversion | Converts R2Sonic Sonic (2022, 2024) bathymetry (packet ID 65 or QINSy QMBE ID 28) and Footprint Time Series (FTS ID 66) snippets from XTF to OMG-HDCS v4 format. |
| [`xtf2omg_simrad`](xtf2omg_simrad.html) | Multibeam Conversion | Converts Simrad EM3000 / EM3002 raw range-and-angle and seabed image datagrams embedded in XTF into OMG-HDCS v4 format. |
| [`elac2omg`](elac2omg.html) | Multibeam Conversion | Converts ELAC HydroStar multibeam bathymetry, sidescan, attitude, and navigation from XTF into OMG-HDCS and optional GLORIA formats. |
| [`klein2omg`](klein2omg.html) | Sidescan Conversion | Converts Klein sidescan sonar records in XTF into two-beam OMG-HDCS v3 `.merged` and `.ss_data` files. |
| [`xtf2gloria`](xtf2gloria.html) | Sidescan Conversion | Converts XTF sidescan sonar records (including multi-beam Klein systems) into 8-bit 1024-pixel JCU GLORIA (`.slr`) records. |
| [`xtf2nav`](xtf2nav.html) | Navigation Extraction | Extracts navigation fixes from XTF bathymetry/sidescan ping headers, raw Reson navigation packets (ID 100), and POS/MV raw navigation packets (ID 107) into binary OMG `.nav_*` files. |
| [`xtf2orientation`](xtf2orientation.html) | Attitude Extraction | Extracts asynchronous attitude records (ID 3) and POS/MV orientation records (ID 107) from XTF into binary OMG `.orientation` and `.POSMV` files. |
| [`xtf2param`](xtf2param.html) | Lever-Arm Extraction | Extracts transducer, positioning sensor, and MRU lever-arm and angular offsets from the XTF file header into an ASCII OMG `.param` file. |
| [`stripSS`](stripSS.html) | Sidescan Visualization | Extracts XTF sidescan trace data into 8-bit JHC or PGM waterfall images with optional TVG removal, water column blanking, and Reson parameter strips. |
| [`extractRI`](extractRI.html) | Backscatter Visualization | Extracts 8-bit beam reflectivity (intensity) values from Reson bathymetry packets in XTF into a JHC (`.8bit`) or PGM (`.pgm`) image. |
| [`extractSnippet`](extractSnippet.html) | Snippet Visualization | Extracts Reson snippet packets (ID 19) from an XTF file into an 8-bit JHC (`.8bit`) or PGM (`.pgm`) image or single-ping ASCII dump. |
| [`getTVG`](getTVG.html) | Radiometric Analysis | Computes range-binned mean sidescan backscatter curves from XTF sonar packets to evaluate empirical Time Varying Gain (TVG) profiles. |

## Typical XTF Unraveling Workflow

1. **Inspect & Index the XTF File:**
   Run [`xtfTool`](xtfTool.html) with `-write_index` to inspect packet counts and generate a `<line>.idx` file, which accelerates subsequent extraction steps:

   ```bash
   xtfTool -write_index -in line01.xtf
   ```
2. **Extract Installation Parameters:**

   ```bash
   xtf2param -xtf line01.xtf -omg line01.param
   ```
3. **Unpack Bathymetry & Backscatter:**
   Use the converter matching your sonar system (`xtf2omg_reson`, `xtf2omg_r2sonic`, `xtf2omg_simrad`, or `elac2omg`):

   ```bash
   xtf2omg_reson -sonar 8101 -xtf line01.xtf -omg line01
   ```
4. **Extract Attitude & Navigation:**

   ```bash
   xtf2orientation -xtf line01.xtf -omg line01.orientation
   xtf2nav -nav sensor -hdg sensor -xtf line01.xtf -omg line01
   cp line01.nav_2 line01.nav
   ```
5. **Merge Attitude, Navigation, and Ray-Trace:**
   Use standard OMG tools (`mergeAtt`, `mergeNav`, `r2v`) on the resulting `.merged`, `.orientation`, `.nav`, and `.param` files.
