---
layout: default
title: Reson SeaBat 9001/8101 Legacy (Sbat)
parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 2
has_children: true
---

# Sbat Tools

Tools in the `Sbat/` directory convert early **Reson SeaBat 9001**, **SeaBat 9002**, and **SeaBat 8101** multibeam datasets—stored in UNB-Reson binary telegrams, Lloyd Huff ASCII format, or early GSF (`gsf_mbc97`) files—into OMG HDCS `.depth` / `.merged` bathymetry files.

## Tool Summary

| Tool | Source | Description |
| :--- | :--- | :--- |
| [8101toOMG](8101toOMG) | `Sbat/8101toOMG.c` | Converts 101-beam Reson SeaBat 8101 swath bathymetry from GSF files into OMG HDCS v2 `.merged` format. |
| [GSF9002toOMG](GSF9002toOMG) | `Sbat/GSF9002toOMG.c` | Converts 60-beam Reson SeaBat 9001/9002 swath bathymetry and HMPS beam flags from GSF files into OMG HDCS v2 `.merged` format. |
| [RESON2OMG](RESON2OMG) | `Sbat/RESON2OMG.c` | Converts 60-beam UNB-Reson binary telegram files (`RESON_NAV`, `RESON_DEPTH`, `RESON_SVP`, `RESON_PARAMETER`) into OMG HDCS v1 `.depth` files. |
| [Sbat2OMG](Sbat2OMG) | `Sbat/Sbat2OMG.c` | Converts 60-beam Lloyd Huff ASCII format Reson SeaBat 9001 files (with UTM Easting/Northing coordinates) into OMG HDCS v1 `.depth` files. |
