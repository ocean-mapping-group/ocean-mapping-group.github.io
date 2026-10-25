---
layout: default
title: Attitude Tools
nav_order: 3
has_children: true
---

# Attitude & Motion Sensor Processing (`att`)

The `att` directory contains utilities for inspecting, editing, time-splitting, combining, and exporting high-rate vessel attitude files (`.att`, `.net_att`, and POS MV delayed heave logs) defined by the [`jcu_nav`](../subr/jcu_nav.md) `jcu_att_rec` binary format.

---

## Attitude Processing Utilities

* [`att2ascii`](att2ascii.md) — Converts binary OMG `.att` attitude records (`roll`, `pitch`, `heave`, `heading`, `timestamp`) to human-readable ASCII columns.
* [`attedit`](attedit.md) — Interactive graphical editor for inspecting and flagging spikes or dropouts in `.att` attitude time series.
* [`appendAtt`](appendAtt.md) — Concatenates multiple sequential binary `.att` files into a continuous attitude time series.
* [`attSplit`](attSplit.md) — Splits large binary `.att` files into smaller time-windowed segments.
* [`attCombo`](attCombo.md) — Compares or blends roll, pitch, heave, and heading channels from two independent motion sensors (`att_1` and `att_2`).
* [`heaveCombo`](heaveCombo.md) — Combines real-time inertial heave with long-period GPS/RTK vertical height variations.
* [`mergeHeave`](mergeHeave.md) & [`readDelHeave`](readDelHeave.md) — Reads Applanix POS MV Group 111/112 TrueHeave (delayed heave) binary logs and merges them into `.att` or `.merged` files.
* [`mergeHeading`](mergeHeading.md) — Merges gyrocompass or dual-antenna GPS heading records into binary `.att` files.
