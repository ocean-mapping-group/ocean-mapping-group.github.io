---
layout: default
title: SE_generic
parent: SwathEd (SE) Tools
nav_order: 23
tool_name: SE_generic
source_path: code/SE/SE_generic.c
category: Interactive QC & Editing (SwathEd)
input_formats: []
output_formats: []
related_tools: ["swathed", "SE_global", "SE_mainwin", "SE_event_loop"]
---

# `SE_generic.c` — Template Stub for SwathEd Extension Modules

## Overview & Purpose
`SE_generic.c` and its companion header `SE_generic.h` were created by John E. Hughes Clarke in April 1999 during the modularization of the original monolithic `swathed.c` X-Windows codebase into separate functional compilation units (`SE_mainwin.c`, `SE_omgIOwin.c`, `SE_GEOwindows.c`, `SE_sswindow.c`, `SE_listwin.c`, `SE_2Dwindow.c`, `SE_AUTOFLAGwin.c`, etc.).

`SE_generic.c` serves as a clean, minimal boilerplate skeleton and compilation unit placeholder for adding new interactive tools or sub-windows to the `SwathEd` (`SE`) suite while maintaining consistent header inclusion and build structure in `code/SE/Makefile`.

---

## Source Structure & Contents

### Header (`code/SE/SE_generic.h`)
Defines the standard include guard `_SE_generic`:
```c
#ifndef _SE_generic
#define _SE_generic

#endif
```

### Implementation (`code/SE/SE_generic.c`)
Includes the shared SwathEd global state header [`SE_global.h`](SE_global.md) and its own module header `SE_generic.h`, followed by a commented template function stub:
```c
#include "SE_global.h"
#include "SE_generic.h"

/*
void function()
{

}
*/
```

---

## Role in the `SwathEd` Modular Architecture

When `swathed` was refactored in April–July 1999 from a single large source file into a modular multi-window X11 application, every functional subsystem was split into a paired `.c`/`.h` module following the pattern established in `SE_generic.c` and `SE_generic.h`:

| Architectural Element | Implementation Pattern across `SE_*.c` Modules |
|---|---|
| **Global State Access** | Every module includes [`SE_global.h`](SE_global.md) first to access shared `OMG_HDCS_summary_header`, `OMG_HDCS_profile_header`, the 100-ping `box[SE_NO_MAX][SE_NO_SWATHS]` depth matrix, and X11 display/colormap handles via `X_extra.h`. |
| **Header Guard Convention** | All SwathEd headers use `#ifndef _SE_<modulename>` / `#define _SE_<modulename>` matching `_SE_generic`. |
| **Widget & Window Lifecycle** | Subsequent tools built from this template—such as [`SE_WaterColumn.c`](SE_WaterColumn.md), [`SE_PhaseBathy.c`](SE_PhaseBathy.md), [`SE_W_TimeSeries.c`](SE_W_TimeSeries.md), [`SE_BDI_DP.c`](SE_BDI_DP.md), [`SE_PDI_LA.c`](SE_PDI_LA.md), and [`SE_AnandBS.c`](SE_AnandBS.md)—extend this skeleton with `jX_widget_params` structures, `make_*_widget()`, `manage_*_widget_events()`, and `refresh_*_widget_window()` callbacks dispatched by [`SE_event_loop.c`](SE_event_loop.md). |

---

## Dependencies & Build Integration
- **Included Headers:** [`SE_global.h`](SE_global.md), `SE_generic.h` (which transitively pulls in `support.h`, `OMG_HDCS_jversion.h`, `j_watercolumn.h`, `sonar_geometry.h`, and `X_extra.h`).
- **Build Target:** Compiled as part of the `code/SE/` object library and linked into the `swathed` executable alongside [`SE_global.c`](SE_global.md), [`SE_mainwin.c`](SE_mainwin.md), and [`SE_omgIOwin.c`](SE_omgIOwin.md).
