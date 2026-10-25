---
layout: default
title: Steve Brucker — Backscatter & Calibration (steve)
parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 9
has_children: true
---

# Steve Brucker (`steve`) Tools

Utilities developed by Steve Brucker (`code/steve/`) for validating spatial and temporal bounding boxes across large multibeam survey archives (`.merged`, `.100ping_bounds`, and `.file_bounds`).

---

## Tool Index

| Tool | Source File | Description |
|---|---|---|
| [`checkBounds`](checkBounds.html) | `code/steve/checkBounds.c` | Reads `OMG_HDCS_summary_header`, `.100ping_bounds`, and `.file_bounds` across single `.merged` files or `-xyzlist` batch lists; exports global `[mintime, maxtime, minlat, maxlat, minlon, maxlon]` bounds to binary or ASCII files and flags files with corners $>50$ nautical miles from the summary header reference position (`refLat`/`refLong`). |

---

## Workflow Context

In large regional compilations (such as the Arctic Seabed Mapping Project on CCGS *Amundsen*), thousands of `.merged` survey lines are indexed by [`getBounds`](../omg/getBounds.html) into `.100ping_bounds` and `.file_bounds` sidecar files before gridding with [`weigh_grid`](../grid/weigh_grid.html) or interactive area editing with [`swathed`](../SE/swathed.html). Corrupted navigation fixes or unflagged zero-coordinate jumps can inflate a file's bounding box by hundreds of kilometers, causing `weigh_grid` or `swathed -locate` to unnecessarily scan the file on every mapsheet.

`checkBounds` provides a fast batch diagnostic pass over an `-xyzlist` of `.merged` files to:
1. Verify that `.100ping_bounds` and `.file_bounds` exist and are readable.
2. Flag any survey line whose top-left or bottom-right bounding box corner deviates by more than **50 nautical miles** from `summary.refLat` / `summary.refLong` (`LOOKS LIKE THERES A PROBLEM IN: <file>`).
3. Export a consolidated ASCII or binary table of global time and geographic extents (`mintime`, `maxtime`, `minlat`, `maxlat`, `minlon`, `maxlon`) for GIS cataloging or automated mapsheet selection.
