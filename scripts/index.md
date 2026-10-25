---
layout: default
title: Automated Processing Scripts (scripts)
parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 11
has_children: true
---

# Helper Scripts (`scripts`)

The `scripts` directory contains Bash, `tcsh`, and Perl automation utilities for batch-unraveling Kongsberg multibeam data (`.kmall`, `.kmwcd`, `.all`, `.wcd`), initializing grid (`.r4`) and sidescan mosaic (`.mos`) file sets from `.blank` mapsheets, and performing batch filename manipulation.

---

## Multibeam Unraveling & Batch Pipelines

* [`unravel_KMALL_2500m_RevHplus_netatt2_parallel`](unravel_KMALL_parallel.html) — Parallel `xargs -P` dispatcher and `tcsh` worker (`unravel_KMALL_single`) for unpacking Kongsberg `.kmall` and `.kmwcd` files with `read_kmall`, merging attitude (`newMergeAtt`), ray-tracing (`repoint`), generating sidescan (`makess`), and indexing bounds (`getBounds`).
* [`bunravel`](bunravel.html) — Bash batch unraveler for legacy Kongsberg `.all` and `.wcd` files using `RTlite`.
* [`get_new_unravel`](get_new_unravel.html) — Bootstrap `tcsh` script to fetch a fresh `new_unravel` template into a survey working directory.

---

## Mapsheet Initialization & Filename Utilities

* [`tor4`](tor4.html) — Initializes `<prefix>.r4`, `<prefix>.r4_weights`, and `<prefix>.r4_weight_depth` files from `<prefix>.blank` for [`weigh_grid`](../grid/weigh_grid.html).
* [`tomos`](tomos.html) — Initializes `<prefix>.mos` and `<prefix>.ran` files from `<prefix>.blank` for [`mos2`](../newmos/mos2.html).
* [`get_prefix`](get_prefix.html) — Strips the trailing extension from filenames using `awk` (called by `tor4` and `tomos`).
* [`rename`](rename.html) — Perl regular-expression batch file renamer (`rename [-v] [-n] [-f] perlexpr files`).
* [Additional Script Utilities](_.html) — Summary of auxiliary scripts and `code/scripts/makefile` installation.
