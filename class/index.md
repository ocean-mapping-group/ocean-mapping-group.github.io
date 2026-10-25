---
layout: default
title: Angular Response & Classification (class)
parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 5
has_children: true
---

# Acoustic Seafloor Classification (`class`)

The `class` directory contains tools for empirical seabed sediment classification using multibeam grazing-angle Angular Response (`AR`) strips and sidescan backscatter texture metrics.

---

## Classification & Angular Response Tools

* [`classAngStrip`](classAngStrip.html) — Classifies seafloor sediment acoustic facies along survey lines from angular response strip files (`.angstrip`).
* [`classSS`](classSS.html) — Sidescan backscatter image classification utility.
* [`compAngStrip`](compAngStrip.html) — Compares observed angular response strips against reference seabed class templates.
* [`findCloseAR`](findCloseAR.html) — Searches for the closest matching reference angular response curve in a sediment training catalog.
* [`readAngStrip`](readAngStrip.html) — Diagnostic reader and ASCII dumper for binary `.angstrip` files (`j_ang_resp`).
* [`plotGSvAR`](plotGSvAR.html) — Plots physical sediment grain-size (`phi`) ground-truth measurements against angular response parameters (mean intensity, slope, intercept).
* [`plotSSclass`](plotSSclass.html) — Plots classified sidescan acoustic facies maps and confusion matrices.
