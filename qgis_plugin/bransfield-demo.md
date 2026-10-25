---
layout: default
title: Antarctica (02_Bransfield) Live Demo
parent: QGIS Survey & Processing Monitor
nav_order: 1
---

# Antarctica (`02_Bransfield`) 349-Line Survey Verification & Live Map

This page demonstrates the **OMG Multibeam Survey & Processing Monitor** tested in strict read-only mode against the **2026 Antarctica Bransfield Strait (`OMG_Care2026 / 02_Bransfield`)** dataset acquired aboard **RV *Almirante Viel***.

---

## Interactive 349-Line Survey Monitor (Embedded Live Viewer)

Click any multibeam survey line on the map or in the right-hand table to inspect its **Julian Day (`74`–`81`)**, **Pipeline Stage**, **Ping Count**, **Vessel Speed**, **Heading**, **Waterline Offset (`WLZ`)**, and companion file status. Use the top-right buttons to switch trackline coloring between **Julian Day**, **Pipeline Stage**, and **Water Column (`.vert_prof`) Availability**:

<div style="margin: 1rem 0 1.5rem 0; border: 1px solid #334155; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.4);">
  <div style="background: #1e293b; padding: 0.5rem 1rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155;">
    <span style="font-size: 0.85rem; font-weight: 600; color: #38bdf8;">🌐 RV Almirante Viel — 02_Bransfield (349 Kongsberg EM124 Survey Lines)</span>
    <a href="assets/bransfield_interactive_map.html" target="_blank" style="font-size: 0.8rem; color: #4ade80; text-decoration: none; font-weight: 600;">↗ Open Full-Screen Viewer</a>
  </div>
  <iframe src="assets/bransfield_interactive_map.html" style="width: 100%; height: 640px; border: none;" loading="lazy"></iframe>
</div>

---

## 2-Panel Static Overview Map (Julian Day vs. Pipeline QC Status)

![Bransfield Strait 349-Line Overview Map](assets/bransfield_survey_overview.svg)

---

## Key Diagnostic Findings from `02_Bransfield`

| Metric / Property | Verified Value |
| :--- | :--- |
| **Vessel & Multibeam Sonar** | RV *Almirante Viel* — **Kongsberg EM124** ($1.0^\circ \times 1.0^\circ$, `KMALL Rev J`, `SN=10039`, `toolType=40`) |
| **Survey Dates & Julian Days** | March 15–22, 2026 — **Julian Days `74`, `75`, `76`, `77`, `78`, `79`, `80`, `81`** |
| **Geographic Bounding Box** | `West: -62.07751°`, `East: -57.91577°`, `South: -63.34375°`, `North: -59.84505°` |
| **Total Survey Lines Scanned** | **349 lines** (`decnav/{74..81}/*.decnav`, `merged/{74..81}/*.merged`, `ss/{74..81}/*.ss`) |
| **Complete Lines (with `.kmwcd` Water Column)** | **340 lines** (`COMPLETE (Bathy + WC + Nav + Att + SS)`) |
| **Complete Lines (Bathy + SS, no `.kmwcd`)** | **8 lines** (`74/0034`, `76/0156`, `78/0255`, `79/0269`, `80/0319`, `80/0336`, `80/0337`, `81/0369`) |
| **Flagged Incomplete Line (`mergeAtt` Halt)** | **1 line (`76/0116_20260317_000158_Almirante_Viel`)** — 2-ping file where `.net_att_2` was `0 bytes` while `.orientation_1` was `1,268 bytes`, causing `mergeAtt` to halt before `makess` and `makeWC`. |
