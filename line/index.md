---
layout: default
title: Survey Line Export Utilities (line)
parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 13
has_children: true
---

# Survey Line Planning & Export (`line`)

The `line` directory contains utilities for exporting planned hydrographic survey lines drawn interactively in [`jview`](../JV/jview.html) (`.lines` format, managed by [`omg_line`](../subr/omg_line.html)) to helm acquisition systems.

---

## Tools in `line/`

* [`line_export`](line_export.html) — Converts OMG `.lines` survey line lists (with reference `JHC_header` mapsheet `-map`) into HYPACK `.lnw` UTM planned line/route files (`-hypack -merid <deg>`) or Kongsberg SIS `.asciiplan` geographic line plans (`-sis`).
