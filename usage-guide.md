---
layout: default
title: Quick Reference Cheat Sheet
nav_order: 4
---

# Quick Reference Command Cheat Sheet

This page provides copy-pasteable command recipes for the most common Ocean Mapping Group (OMG) multibeam processing tasks. For detailed explanations of file formats, sensor selection, and troubleshooting, see the **[Processing Workflows & Guides](workflows/index.html)**.

---

## 1. Kongsberg `.kmall` & `.kmwcd` Unraveling (SIS 5.x)

Supported models in [`read_kmall`](kmall/read_kmall.html): **EM2040 / EM2040P (`2040`)**, **EM2042 (`2042`)**, **EM2040C (`2045`)**, **EM712 (`712`)**, **EM304 (`304`)**, **EM124 (`124`)**.

### Batch Parallel Processing (Recommended)
Run from the parent directory containing `raw/*.kmall` (and optional `raw/*.kmwcd`):
```bash
./unravel_KMALL_2500m_RevHplus_netatt2_parallel
```

### Single-Line Manual Commands
```bash
mkdir -p merged decnav ss
LINE="0001_20240615_120000_Ship"

# 1. Unpack .kmwcd FIRST (if present) and save its water-column pointer .merged file
if [ -f "raw/${LINE}.kmwcd" ]; then
    read_kmall -d "merged/${LINE}" -kmall "raw/${LINE}.kmwcd" -maxdepth 2500.0
    mv "merged/${LINE}.merged" "merged/justWC_${LINE}.merged"
fi

# 2. Unpack .kmall SECOND and transfer water-column pointers
read_kmall -d "merged/${LINE}" -kmall "raw/${LINE}.kmall" -maxdepth 2500.0
if [ -f "merged/justWC_${LINE}.merged" ]; then
    moveOverWCinfo "merged/${LINE}.merged" "merged/justWC_${LINE}.merged"
    rm "merged/justWC_${LINE}.merged"
fi

# 3. Copy active navigation (.nav_1), filter spikes, append, and merge lever arms
cp "merged/${LINE}.nav_1" "merged/${LINE}.nav"
stripNav "merged/${LINE}.nav" "decnav/${LINE}.nav" 0.5 0.01 10.0
appendNav decnav/all_dec.nav "decnav/${LINE}.nav"
mergeNav -ahead 60.0 -param "merged/${LINE}.param" "merged/${LINE}.merged" decnav/all_dec.nav

# 4. Copy active attitude (.net_att_2, .net_att_1, or .orientation_1) and ray-trace 3D beams
cp "merged/${LINE}.net_att_2" "merged/${LINE}.orientation"
newMergeAtt -redoref -recalc_beamVec -wc "merged/${LINE}"

# 5. Generate sidescan (.ss) from snippets
makess -pixel 2.0 -SnippetExtend "merged/${LINE}"
mv "merged/${LINE}.ss" ss/
```

---

## 2. Kongsberg `.all` & `.wcd` Unraveling (SIS 3.x / 4.x)

Supported models in [`RTlite`](RTLite/RTlite.html): **EM120, EM122, EM300, EM302, EM710, EM1002, EM2040 (`.all`), EM3000, EM3002**.

### Batch Processing with `bunravel`
```bash
# Unpack all raw/*.all files, flatten empirical TVG (deTVG), and build 1.0 m sidescan (.ss):
bunravel -path raw -ext all -ss -pixel 1.0 -detvg
```

---

## 3. Bathymetric Gridding (`.blank` $\rightarrow$ `.r4` $\rightarrow$ `.8bit` / `.sun`)

```bash
# 1. Inspect geographic bounding box (West East South North)
getBounds -nav merged/*.merged

# 2. Create a 32-bit float blank grid header (5.0 m resolution)
# NOTE: Place <out_prefix> -float -Dx -Dy BEFORE -boundsof or -bounds!
make_blank area -float -Dx 5.0 -Dy 5.0 -boundsof -nav merged/*.merged

# 3. Grid soundings with distance-weighting (smoothing factor 2.0)
tor4 area 2.0 merged/*.merged

# 4. Create 8-bit greyscale and sun-illuminated relief images
r4to8bit -in area.r4 -range 50.0 500.0
addSUN area.r4 area.sun 315 35 4

# 5. View in 3D with jview
jview -sun area.8bit area.sun area.r4
```

---

## 4. Interactive Swath Cleaning (`swathed`)

```bash
# Open the .r4 grid in plan-view locator mode to click-and-drag around spikes:
swathed -locate area.r4 merged/*.merged

# After flagging outlier beams and saving in swathed, re-run tor4:
tor4 area 2.0 merged/*.merged
```

---

## 5. Sidescan & Backscatter Mosaicking (`.ss` $\rightarrow$ `.mos`)

```bash
# 1. Fill small along-track ping gaps in all .ss files
for f in ss/*.ss; do glfill "$f"; done

# 2. Create an 8-bit blank mosaic header primed to 255 (1.0 m resolution)
make_blank area_mos -8bit -prime 255 -Dx 1.0 -Dy 1.0 -bounds -66.55 -66.40 44.95 45.10

# 3. Initialize .mos and .ran and run mos2 (mapping ss/ back to merged/ for companion files)
cp area_mos.blank area_mos.mos
cp area_mos.blank area_mos.ran
mos2 -in area_mos.mos -ran area_mos.ran -smf 1.5 -weight_by_dist -swap_dirs ss/ merged/ -files ss/*.ss

# 4. Inspect the sidescan mosaic in jview
jview area_mos.mos
```
