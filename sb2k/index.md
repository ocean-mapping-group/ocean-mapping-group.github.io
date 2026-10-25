---
layout: default
title: SeaBeam 2000 / 2100 (sb2k)
parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 6
has_children: true
---

# SB2K Tools

Tools in the `sb2k/` directory process multibeam bathymetry and sidescan imagery from **SeaBeam** systems—including original 19-beam "Classic" SeaBeam (URI format), Scripps Institution of Oceanography (SIO) **SeaBeam 2000** (`SB2K`), and **SeaBeam 2100** (`SB2100`) systems—converting them into OMG HDCS formats and correcting apparent depths.

## Tool Summary

| Tool | Source | Description |
| :--- | :--- | :--- |
| [deApparent](deApparent) | `sb2k/deApparent.c` | Removes the 1500 m/s "apparent depth" assumption in SeaBeam `.merged` files using the harmonic mean sound velocity from an `.svp` file. |
| [mergeSB2K](mergeSB2K) | `sb2k/mergeSB2K.c` | Links GLORIA-format sidescan records onto beam 61 of SeaBeam 2000 `.merged` bathymetry files. |
| [refoSB_Classic](refoSB_Classic) | `sb2k/refoSB_Classic.c` | Converts 19-beam URI-format "Classic" SeaBeam (as well as PMEL BSSS and SNBESS variants) into OMG HDCS `.merged` format. |
| [unravelSB2100](unravelSB2100) | `sb2k/unravelSB2100.c` | Converts SeaBeam 2100 (`DR`, `SS`, `PR`, `TR` records) into OMG HDCS v3 `.merged`, `.ss`, and `.merged.ss_data` files. |
| [unravelSB2K](unravelSB2K) | `sb2k/unravelSB2K.c` | Extracts navigation (`.nav`), sound velocity (`.svp`), bathymetry (`.depth`), and sidescan imagery (`.reflect`, `.merged.ss_data`) from SIO SeaBeam 2000 files. |
