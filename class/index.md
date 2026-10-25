---
layout: default
title: class Tools
has_children: true
nav_order: 4
---

# Acoustic Seafloor Classification (`class`)

The `class` directory contains tools for empirical seabed sediment classification using multibeam grazing-angle Angular Response (`AR`) strips and sidescan backscatter texture metrics.

---

## Classification & Angular Response Tools

* [`classAngStrip`](classAngStrip.md) — Classifies seafloor sediment acoustic facies along survey lines from angular response strip files (`.angstrip`).
* [`classSS`](classSS.md) — Sidescan backscatter image classification utility.
* [`compAngStrip`](compAngStrip.md) — Compares observed angular response strips against reference seabed class templates.
* [`findCloseAR`](findCloseAR.md) — Searches for the closest matching reference angular response curve in a sediment training catalog.
* [`readAngStrip`](readAngStrip.md) — Diagnostic reader and ASCII dumper for binary `.angstrip` files (`j_ang_resp`).
* [`plotGSvAR`](plotGSvAR.md) — Plots physical sediment grain-size (`phi`) ground-truth measurements against angular response parameters (mean intensity, slope, intercept).
* [`plotSSclass`](plotSSclass.md) — Plots classified sidescan acoustic facies maps and confusion matrices.
