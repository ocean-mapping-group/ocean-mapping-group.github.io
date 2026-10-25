---
layout: default
title: KMALL Tools
nav_order: 10
has_children: true
---

# Kongsberg `.kmall` & `.kmwcd` Unpacking (`kmall`)

The `kmall` directory contains the Ocean Mapping Group's parser and converter for modern Kongsberg Maritime **`.kmall`** (bathymetry, attitude, navigation, seabed image snippets, runtime parameters, and SVP casts) and **`.kmwcd`** (water-column datagrams) multibeam sonar files (EM2040, EM712, EM304, EM124, etc., Revision D through Revision H+).

---

## Tools & Headers in `kmall/`

* [`read_kmall`](read_kmall.md) — Primary converter (`code/kmall/read_kmall.c`) that unpacks `#MRZ` (multibeam raw range and depth), `#MWC` (water column), `#SPO` (sensor position), `#SKM` (high-rate KM binary attitude & delayed heave), `#SCL` (clock), `#SVP` / `#SVT` (sound velocity), `#IOP` (runtime parameters), and `#IIP` (installation parameters) datagrams into OMG-HDCS v4 files (`.merged`, `.nav_1..3`, `.net_att_1..2`, `.watercol`, `.sectors`, `.param`).
* **Kongsberg Datagram Headers (`EMdgmFormat.h`, `EMdgm.h`):** Official Kongsberg Maritime C struct definitions (including Revision D, Revision G, and Revision H+ extensions for phase/amplitude water-column and installation text parsing).

---

## Related Workflows & Batch Scripts

* [`unravel_KMALL_2500m_RevHplus_netatt2_parallel`](../scripts/unravel_KMALL_parallel.md) — Parallel batch dispatcher running `read_kmall`, `newMergeAtt`, `repoint`, `makess`, and `getBounds`.
* [Kongsberg `.kmall` Unraveling Workflow](../workflows/kongsberg-kmall-unraveling.md) — Step-by-step guide to unpacking and processing `.kmall` surveys.
