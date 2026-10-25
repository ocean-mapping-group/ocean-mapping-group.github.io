---
layout: default
title: Reson 7k (s7k) Multibeam & Water Column Tools
parent: Formats & Converters
has_children: true
nav_order: 11
---

# Reson 7k (`s7k`) Multibeam & Water Column Tools (`reson/`)

The `reson/` directory contains the Ocean Mapping Group's ingestion, inspection, water-column processing, and conversion utilities for **Teledyne Reson SeaBat 7000-series (`.s7k`)** multibeam echosounders (including SeaBat 7125, 7101, 7111, 7150, 7160, and T20/T50 systems).

Reson `.s7k` Data Record Frames wrap each sensor datagram in a 64-byte Data Record Frame header followed by a Record Type Header, an optional Record Data section, and a 4-byte checksum. The tools in this directory parse raw `.s7k` logs directly to generate OMG `.merged` swath bathymetry, `.bck` / `.ss_data` sidescan imagery, `.wci` water-column structures, and repacked `.s7k` subsets.

---

## Tool Inventory

| Tool | Source File | Primary Purpose | Input Formats | Output Formats |
| :--- | :--- | :--- | :--- | :--- |
| [`7k2omg`](7k2omg.html) | `reson/7k2omg.c` | Convert Reson `.s7k` bathymetry (7006/7027), sonar settings (7000), navigation (1003), attitude (1012/1013), heading (1015), and snippets (7008/7028) into OMG `.merged`, `.param`, `.orientation`, and `.bck` files | `.s7k`, `.data` | `.merged`, `.param`, `.orientation`, `.nav`, `.bck` |
| [`7k2ss`](7k2ss.html) | `reson/7k2ss.c` | Extract Reson `.s7k` snippet/sidescan imagery (Record 7007/7008/7028) into OMG `.ss_data` sidescan traces | `.s7k` | `.ss_data` |
| [`7kTool`](7kTool.html) | `reson/7kTool.c` | Interactive Motif/X11 and CLI diagnostic inspector for scanning, dumping, and graphing Reson `.s7k` Data Record Frames | `.s7k` | Diagnostic text, X11 plots |
| [`WC2medusa`](WC2medusa.html) | `reson/WC2medusa.c` | Extract and process Reson `.s7k` water-column amplitudes and phases (Record 7018) for Medusa/water-column acoustic analysis | `.s7k` | Water-column amplitude/phase dumps |
| [`WCIviewer_7k`](WCIviewer_7k.html) | `reson/WCIviewer_7k.c` | Convert and visualize Reson `.s7k` Beamformed Water Column (Record 7018) and snippet (7008/7028) records into OMG `.wci` water-column files | `.s7k` | `.wci` |
| [`repack7k`](repack7k.html) | `reson/repack7k.c` | Filter, strip, or time-window large Reson `.s7k` files (e.g., removing bulky Record 7018 water-column packets while preserving bathymetry and navigation) | `.s7k` | Filtered `.s7k` |

---

## Supported Reson `s7k` Record Types

| Record ID | Record Name | Used By |
| :--- | :--- | :--- |
| **1003** | Position | `7k2omg`, `7k2ss`, `7kTool`, `WCIviewer_7k` |
| **1012** | Roll, Pitch, Heave | `7k2omg`, `7kTool`, `WCIviewer_7k` |
| **1013** | Heading | `7k2omg`, `7kTool`, `WCIviewer_7k` |
| **1015** | Navigation | `7k2omg`, `7kTool` |
| **1016** | Attitude | `7k2omg`, `7kTool` |
| **7000** | Sonar Settings (frequency, power, gain, pulse width, absorption, spreading, sound velocity) | `7k2omg`, `7k2ss`, `7kTool`, `WCIviewer_7k` |
| **7004** | Beam Geometry (beam pointing angles and widths) | `7k2omg`, `7kTool`, `WCIviewer_7k` |
| **7006** | Bathymetric Data (legacy two-way travel time, quality flags, intensity) | `7k2omg`, `7k2ss`, `7kTool` |
| **7007** | Side Scan Data | `7k2ss`, `7kTool` |
| **7008** | Generic Water Column / Snippet Data | `7k2omg`, `7k2ss`, `7kTool`, `WCIviewer_7k` |
| **7018** | Beamformed Magnitude and Phase Water Column Data | `WC2medusa`, `WCIviewer_7k`, `repack7k`, `7kTool` |
| **7027** | Raw Detection Data (SeaBat 7125/T20/T50 high-density detections) | `7k2omg`, `7k2ss`, `7kTool`, `WCIviewer_7k` |
| **7028** | Snippet Data (dedicated snippet amplitude series per beam) | `7k2omg`, `7k2ss`, `7kTool`, `WCIviewer_7k` |

---

## Typical Processing Workflows

### 1. Standard Reson `.s7k` Swath Bathymetry & Backscatter Ingestion
```bash
# Inspect record inventory in a raw .s7k file
7kTool -in 20120815_142000.s7k -summary

# Convert bathymetry (7006 or 7027), orientation (1012/1013), parameters (7000), and snippets (7028)
7k2omg -in 20120815_142000.s7k -out line01 -7027 -snippets
```

### 2. Stripping Water Column Records (`7018`) to Reduce File Size
```bash
# Create a compact .s7k file without Record 7018 water-column packets
repack7k -in raw_with_wci.s7k -out compact_bathy.s7k -no7018
```
