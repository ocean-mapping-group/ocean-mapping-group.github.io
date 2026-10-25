---
layout: default
title: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 9
has_children: true
---

# 4. Multi-Vendor Sonar & LiDAR Converters

Format converters and unpacking pipelines for Reson SeaBat (.s7k), R2Sonic, GeoSwath+ / Submetrix (.rdf), Furuno WASSP, ELAC, SeaBeam, GSF, XSE, HYPACK, CARIS HIPS, Optech SHOALS LiDAR, and NetCDF/HDF5.

---

## Directory Modules in This Category

| Module | Directory | Purpose & Key Tools |
| :--- | :--- | :--- |
| **[Reson SeaBat 7k/8k (reson)](../reson/)** | `reson/` | Teledyne Reson `.s7k` multibeam, snippet, and water-column converters (`7k2omg`, `7k2ss`, `7k2nav`, `7k2orientation`, `8k2omg`). |
| **[Reson SeaBat 9001/8101 Legacy (Sbat)](../Sbat/)** | `Sbat/` | Legacy Reson SeaBat 9001/8101 serial/tape telegram unpackers and calibration tools. |
| **[R2Sonic 2020/2022/2024 (r2sonic)](../r2sonic/)** | `r2sonic/` | R2Sonic `.r2s` / `.bth` truePix, bathymetry, and water-column converters (`r2s2omg`). |
| **[Furuno WASSP Multibeam (wassp)](../wassp/)** | `wassp/` | Furuno WASSP `.wsp` / network stream converters to `OMG_HDCS` (`.merged`). |
| **[ELAC BottomChart Multibeam (elac)](../elac/)** | `elac/` | Honeywell/Wärtsilä ELAC BottomChart `.ela` reformatters (`refoELAC`, `qualityFlag`). |
| **[SeaBeam 2000 / 2100 (sb2k)](../sb2k/)** | `sb2k/` | SeaBeam 2000 and 2100 deep-water multibeam format converters. |
| **[GeoSwath+ / Submetrix 2000 CLI (sub2k)](../sub2k/)** | `sub2k/` | Command-line interferometric phase-differencing sonar processors for Submetrix ISIS / GeoAcoustics GeoSwath+ (`.rdf`). |
| **[GeoSwath+ / Submetrix Motif GUI (sub2k_motif)](../sub2k_motif/)** | `sub2k_motif/` | Interactive X11/Motif interferometric phase-binning and calibration suite for Submetrix / GeoSwath+. |
| **[Kongsberg Mesotech M3 Sonar (M3)](../M3/)** | `M3/` | Kongsberg Mesotech M3 imaging and profiling sonar `.imb` / `.smb` converters (`M3imb2omg`, `DDSsmb_read`). |
| **[MB-System .mb1 Format (mb1)](../mb1/)** | `mb1/` | Bidirectional converters between MB-System `.mb1` soundings and `OMG_HDCS` `.merged` files. |
| **[Humminbird Side-Imaging Sonar (humm)](../humm/)** | `humm/` | Humminbird `.dat` / `.son` recreational sidescan and down-imaging converter (`humm2omg`). |
| **[L-3 / SeaBeam XSE Format (xse)](../xse/)** | `xse/` | eXtended Shipboard Data (`.xse`) frame parser for SeaBeam and ELAC systems (`xse2omg`). |
| **[Generic Sensor Format — GSF (gsf)](../gsf/)** | `gsf/` | SAIC/Leidos Generic Sensor Format (`.gsf`) import/export utilities (`gsf2omg`, `omg2gsf`). |
| **[HYPACK HSX / RAW Converters (hypack)](../hypack/)** | `hypack/` | HYPACK `.hsx` and `.raw` multibeam/singlebeam survey line converters. |
| **[CARIS HIPS Integration Utilities (hips_goodies)](../hips_goodies/)** | `hips_goodies/` | HDCS v3/v4 converters and vessel configuration bridges between CARIS HIPS/SIPS and OMG. |
| **[Optech SHOALS Bathymetric LiDAR (Optech)](../Optech/)** | `Optech/` | Optech SHOALS airborne bathymetric LiDAR waveform and sounding unpackers. |
| **[ROSS Multi-Transducer Channel Sweep (ROSS)](../ROSS/)** | `ROSS/` | ROSS acoustic sweep system multi-channel harbour/river survey converters. |
| **[NetCDF & HDF5 Ocean/Sonar Readers (netcdf)](../netcdf/)** | `netcdf/` | Copernicus oceanographic NetCDF (`ncCopernicusRead`) and Simrad EC150/EK80 HDF5/NetCDF readers. |
