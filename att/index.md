---
layout: default
title: Attitude, Heave & Heading (att)
parent: 1. Multibeam Unpacking, Nav & Ray-Tracing
nav_order: 4
has_children: true
---

# Attitude & Motion Sensor Processing (`att`)

The `att` directory contains utilities for inspecting, editing, time-splitting, combining, and exporting high-rate vessel attitude files (`.att`, `.net_att`, and POS MV delayed heave logs) defined by the [`jcu_nav`](../subr/jcu_nav.html) `jcu_att_rec` binary format.

---

## Attitude Processing Utilities

* [`att2ascii`](att2ascii.html) — Converts binary OMG `.att` attitude records (`roll`, `pitch`, `heave`, `heading`, `timestamp`) to human-readable ASCII columns.
* [`attedit`](attedit.html) — Interactive graphical editor for inspecting and flagging spikes or dropouts in `.att` attitude time series.
* [`appendAtt`](appendAtt.html) — Concatenates multiple sequential binary `.att` files into a continuous attitude time series.
* [`attSplit`](attSplit.html) — Splits large binary `.att` files into smaller time-windowed segments.
* [`attCombo`](attCombo.html) — Compares or blends roll, pitch, heave, and heading channels from two independent motion sensors (`att_1` and `att_2`).
* [`heaveCombo`](heaveCombo.html) — Combines real-time inertial heave with long-period GPS/RTK vertical height variations.
* [`mergeHeave`](mergeHeave.html) & [`readDelHeave`](readDelHeave.html) — Reads Applanix POS MV Group 111/112 TrueHeave (delayed heave) binary logs and merges them into `.att` or `.merged` files.
* [`mergeHeading`](mergeHeading.html) — Merges gyrocompass or dual-antenna GPS heading records into binary `.att` files.
