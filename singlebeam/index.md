---
layout: default
title: Single-Beam Echosounder Tools (singlebeam)
parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 12
has_children: true
---

# Singlebeam Tools (`code/singlebeam/`)

The `singlebeam/` directory provides utilities for converting custom agency and hydrographic singlebeam echosounder logs into standard **`OMG_HDCS`** `.merged` files (`toolType = SingleBeam`, `numBeams = 1`). Once converted into `.merged` format, singlebeam survey lines can be tide-corrected (`mergeTide`), edited (`SwathEd`), and gridded (`weigh_grid`) alongside multibeam and LiDAR datasets.

For Simrad EA600, EK60, EK80, Knudsen 320/3260, and Furuno FCV-30 singlebeam/echosounder workflows, see:
* **[Simrad EA600 / EK60 / EK80 Broadband Echosounder & Singlebeam Workflow](../workflows/ek60-ek80-echosounder-workflow.html)** (`readEA600`)
* **[Sub-Bottom Profiler & Bathymetric LiDAR Workflows](../workflows/subbottom-and-lidar-workflows.html)** (`knud2glo`, `fcv30-2glo`, `readSB_SEGY`)

---

## Tool Inventory

* **[`refoCustom`](refoCustom.html)** (`code/singlebeam/refoCustom.c`): Converts custom **BC Hydro** ASCII (`-BCHydro`) and **SDG** 48-byte big-endian binary (`-SDG`) singlebeam survey files into `OMG_HDCS` `.merged` format.
* **[`makefile`](makefile.html)** (`code/singlebeam/makefile`): Build specification for compiling `refoCustom` against `OMG_HDCS_jversion.o` and `-llocal`.
