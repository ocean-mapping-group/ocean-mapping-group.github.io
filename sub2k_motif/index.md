---
layout: default
title: GeoSwath+ / Submetrix Motif GUI (sub2k_motif)
parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 8
has_children: true
---

# Submetrix Motif GUI (`sub2k_motif/`)

The `sub2k_motif/` directory contains the source code for **`RTsubx`**, an interactive X11/Motif (and LessTif) graphical user interface and shared library (`libsubx.so`) for viewing, threshold-filtering, across-track binning, and converting **Submetrix 2000 / ISIS (`.sub`, `.rrc`)** interferometric bathymetric sidescan sonar data.

Whereas the command-line [`readSUB2K`](../sub2k/readSUB2K.html) utility in [`sub2k/`](../sub2k/index.html) processes an entire `.sub` / `.rrc` file in batch mode, `RTsubx` provides an interactive ping-by-ping and swath-by-swath visual environment where an operator can inspect raw interferometric point clouds, adjust coherence/amplitude thresholds and across-track bin spacing on the fly, and view real-time bathymetric profile cross-sections before writing OMG output files.

---

## Application & Module Inventory

| Module / File | Source File | Role in `RTsubx` / `libsubx.so` |
| :--- | :--- | :--- |
| [`RTsubx`](RTsubx.html) | `sub2k_motif/RTsubx.c` | Top-level X11/Motif application entry point (`main`), initializing Xt toolkit, parsing CLI options, creating windows, and entering `XtAppMainLoop` |
| [`init_windows`](init_windows.html) | `sub2k_motif/init_windows.c` | Constructs the main Motif widget hierarchy (menu bar, control sliders/buttons, drawing areas, and status labels) |
| [`bathy_window`](bathy_window.html) | `sub2k_motif/bathy_window.c` | Creates and manages the dedicated bathymetric cross-section / swath profile display window |
| [`bathy_events`](bathy_events.html) | `sub2k_motif/bathy_events.c` | Handles X11 expose, resize, and mouse/pointer interaction events inside the bathymetry profile window |
| [`draw_bathy`](draw_bathy.html) | `sub2k_motif/draw_bathy.c` | Renders raw interferometric soundings and binned swath depth profiles onto the bathymetry drawing area |
| [`draw_view`](draw_view.html) | `sub2k_motif/draw_view.c` | Renders plan-view /waterfall swath coverage and colour-coded depth/intensity imagery |
| [`da_all_events`](da_all_events.html) | `sub2k_motif/da_all_events.c` | Handles X11 expose, button press, and motion events for the primary drawing area canvas |
| [`work_proc`](work_proc.html) | `sub2k_motif/work_proc.c` | Xt background work procedure (`XtAppAddWorkProc`) that continuously reads and processes incoming `.sub` / `.rrc` pings without blocking the GUI event loop |
| [`callbacks`](callbacks.html) | `sub2k_motif/callbacks.c` | Motif widget callback functions for menu actions, play/pause/step controls, and display toggles |
| [`file`](file.html) | `sub2k_motif/file.c` | File I/O management for opening Submetrix `.sub` / `.rrc` input files and writing processed output |
| [`file_selection`](file_selection.html) | `sub2k_motif/file_selection.c` | Motif `XmCreateFileSelectionDialog` wrapper for interactive input/output file browsing |
| [`spacing_select`](spacing_select.html) | `sub2k_motif/spacing_select.c` | Dialog and scale callbacks for configuring across-track bathymetric bin spacing |
| [`threshold_select`](threshold_select.html) | `sub2k_motif/threshold_select.c` | Dialog and scale callbacks for tuning interferometric amplitude/quality rejection thresholds |
| [`set_values`](set_values.html) | `sub2k_motif/set_values.c` | Synchronizes internal processing state variables with Motif widget labels and slider positions |
| [`do_parse`](do_parse.html) | `sub2k_motif/do_parse.c` | Parses command-line arguments and configuration parameters for `RTsubx` |
| [`Str2XmString`](Str2XmString.html) | `sub2k_motif/Str2XmString.c` | Helper converting standard C `char *` strings (including newline-delimited multi-line strings) into Motif `XmString` compound strings |
| [`about`](about.html) | `sub2k_motif/about.c` | Displays the Motif "About RTsubx" information dialog |
| [`error`](error.html) | `sub2k_motif/error.c` | Displays modal Motif error message dialogs |
| [`warning`](warning.html) | `sub2k_motif/warning.c` | Displays Motif warning dialogs for non-fatal processing alerts |
| [`cantsave`](cantsave.html) | `sub2k_motif/cantsave.c` | Displays an alert dialog when an output file cannot be written or saved |
| [`makefile`](makefile.html) | `sub2k_motif/makefile` | Primary build file compiling `libsubx.so` and linking `RTsubx` against Motif (`-lXm -lXt -lX11`) and OMG libraries (`-llocal_graphics -llocal`) |
| [`makefile.test_shared`](makefile.test_shared.html) | `sub2k_motif/makefile.test_shared` | Alternate shared-library test Makefile linking `RTsubx` against `libsubx.so` |
