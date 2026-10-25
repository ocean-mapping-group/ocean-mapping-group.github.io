---
layout: default
title: unravel_KMALL_parallel & unravel_KMALL_single
parent: Helper Scripts
nav_order: 1
tool_name: unravel_KMALL_2500m_RevHplus_netatt2_parallel
source_path: unravel_KMALL_2500m_RevHplus_netatt2_parallel
category: Raw Data Unraveling
input_formats: [".kmall", ".kmall.gz", ".kmwcd"]
output_formats: [".merged", ".merged.ss_data", ".merged.16_data", ".sectors", ".nav", ".nav.strip", ".decnav", ".orientation", ".ss", ".watercol", ".vert_prof", ".vert_prof.gif"]
related_tools: ["read_kmall", "moveOverWCinfo", "dumpFlags", "getBounds", "doallWEB_Tide", "stripNav", "appendNav", "mergeAtt", "mergeNav", "makess", "glfill", "jview", "makeWC", "fillGap", "stretchacres"]
---

# `unravel_KMALL_2500m_RevHplus_netatt2_parallel` & `unravel_KMALL_single`

## Description
The Kongsberg `.kmall` unraveling script suite consists of three scripts located in `/home/iwc/coding/`:
1. **`unravel_KMALL_2500m_RevHplus_netatt2`** — The original sequential `tcsh` script that iterates over a list of `raw/<subdir>/<line>.kmall` files one at a time.
2. **`unravel_KMALL_2500m_RevHplus_netatt2_parallel`** — A high-throughput `bash` parallel dispatcher that pre-creates all output subdirectories (`merged/<subdir>`, `decnav/<subdir>`, `ss/<subdir>`) to prevent `mkdir` race conditions and spawns up to `MAX_JOBS=20` concurrent workers via `xargs -P 20`.
3. **`unravel_KMALL_single`** — The `tcsh` single-file worker invoked by the parallel dispatcher. It uses process-isolated temporary files (`/tmp/unravel_$$_$LINE_NUMBER.*`) so 20 water-column vertical profile pipelines (`makeWC` $\rightarrow$ `fillGap` $\rightarrow$ `stretchacres` $\rightarrow$ `convert`) can run simultaneously without overwriting each other's `temp.vert_prof` or `temp.pgm` files.

---

## Usage

```bash
# Run in parallel (up to 20 files simultaneously) from the survey project root (containing raw/):
./unravel_KMALL_2500m_RevHplus_netatt2_parallel raw/JD100/*.kmall

# Run a single file via the worker directly:
./unravel_KMALL_single raw/JD100/0001_20240409_120000_Ship.kmall

# Run sequentially:
./unravel_KMALL_2500m_RevHplus_netatt2 raw/JD100/*.kmall
```

---

## Required Directory Structure

You must execute the script from a project working directory that contains a `raw/` directory organized into subdirectories (typically by Julian Day `JDxxx` or survey area):

```text
project_root/
├── raw/
│   └── JD100/
│       ├── 0001_20240409_120000_Ship.kmall     (or .kmall.gz)
│       └── 0001_20240409_120000_Ship.kmwcd     (optional companion water column file)
├── merged/                                     (auto-generated)
│   └── JD100/
├── decnav/                                     (auto-generated)
│   └── JD100/
├── ss/                                         (auto-generated)
│   └── JD100/
└── error.log                                   (auto-generated on failure)
```

---

## Complete 12-Stage Processing Pipeline (`unravel_KMALL_single`)

When `unravel_KMALL_single raw/$SUBDIR/$LINE_NUMBER.kmall` runs, it executes the following 12 stages in order:

### Stage 1: Path Parsing & Gzip Handling
* Splits the input argument `raw/$SUBDIR/$LINE_NAME` by `/` using `awk '{print $2}'` (`SUBDIR`) and `awk '{print $3}'` (`LINE_NAME`), and strips `.kmall` and `.gz` to form `LINE_NUMBER`.
* If `raw/$SUBDIR/$LINE_NAME` does not exist but `raw/$SUBDIR/$LINE_NAME.gz` exists, sets `FOUND_ZIPPED_RAW = 1` and decompresses it with `gunzip` (and re-compresses it with `gzip` in Stage 4 after `read_kmall` finishes).
* Checks whether a separate water column file `raw/$SUBDIR/$LINE_NUMBER.kmwcd` exists (`FOUND_SEPARATE_WCD = 1`).

### Stage 2: Preserve Previous `swathed` Cleaning Flags
If `merged/$SUBDIR/$LINE_NUMBER.merged` already exists from an earlier unraveling pass, runs [`dumpFlags`](../omg/dumpFlags.md) to save manual beam-rejection flags into `merged/$SUBDIR/$LINE_NUMBER.flag_bk`:
```tcsh
if (-e merged/$SUBDIR/$LINE_NUMBER.merged) then
    dumpFlags merged/$SUBDIR/$LINE_NUMBER
endif
```

### Stage 3: Unpack `.kmwcd` and `.kmall` via `read_kmall`
* **Case A: Companion `.kmwcd` file exists (`$FOUND_SEPARATE_WCD == 1`)**
  1. Runs [`read_kmall`](../kmall/read_kmall.md) on the `.kmwcd` file **first** with `-doWC -doPhase`:
     ```tcsh
     read_kmall -isRevH -doWC -doPhase \
         -in raw/$SUBDIR/$LINE_NUMBER.kmwcd \
         -out merged/$SUBDIR/$LINE_NUMBER
     ```
     This creates `<LINE_NUMBER>.watercol`, `<LINE_NUMBER>.WC_Phase1`, and a `.merged` file containing the water column ping timestamps and byte offsets.
  2. Moves that temporary `.merged` file aside to `justWC_$LINE_NUMBER.merged`:
     ```tcsh
     mv merged/$SUBDIR/$LINE_NUMBER.merged merged/$SUBDIR/justWC_$LINE_NUMBER.merged
     ```
  3. Runs `read_kmall` on the `.kmall` file **second** to unpack bathymetry (`#MRZ`), snippets, sectors, navigation (`#SPO`), attitude (`#SKM`), SVPs (`#SVP`), and installation parameters (`#IIP`):
     ```tcsh
     read_kmall -isRevH \
         -in raw/$SUBDIR/$LINE_NUMBER.kmall \
         -out merged/$SUBDIR/$LINE_NUMBER
     ```
  4. Combines the water column byte offsets from `justWC_$LINE_NUMBER.merged` into the main bathymetric `.merged` file using [`moveOverWCinfo`](../omg/moveOverWCinfo.md), then removes `justWC_$LINE_NUMBER.merged`:
     ```tcsh
     moveOverWCinfo merged/$SUBDIR/$LINE_NUMBER.merged merged/$SUBDIR/justWC_$LINE_NUMBER.merged
     rm merged/$SUBDIR/justWC_$LINE_NUMBER.merged
     ```
* **Case B: No `.kmwcd` file (`$FOUND_SEPARATE_WCD == 0`)**
  Runs `read_kmall` once on the `.kmall` file with `-doWC -doPhase` (in case `#MWC` datagrams are embedded directly inside the `.kmall` file):
  ```tcsh
  read_kmall -isRevH -doWC -doPhase \
      -in raw/$SUBDIR/$LINE_NUMBER.kmall \
      -out merged/$SUBDIR/$LINE_NUMBER
  ```

### Stage 4: Restore Cleaning Flags
If `<LINE_NUMBER>.flag_bk` was created in Stage 2, reloads the saved `swathed` rejection flags into the newly unpacked `.merged` file:
```tcsh
if (-e merged/$SUBDIR/$LINE_NUMBER.flag_bk) then
    dumpFlags -load merged/$SUBDIR/$LINE_NUMBER
endif
```

### Stage 5: Initial Spatial Bounds, WebTide & Nav Stripping
Computes initial bounding boxes from the raw `#MRZ` ping coordinates, applies WebTide tidal predictions, and strips ping navigation:
```tcsh
getBounds merged/$SUBDIR/$LINE_NUMBER.merged
doallWEB_Tide merged/$SUBDIR/$LINE_NUMBER.merged
stripNav -comp merged/$SUBDIR/$LINE_NUMBER.nav.strip merged/$SUBDIR/$LINE_NUMBER.merged
```

### Stage 6: Select Navigation Source & Create Decimated Nav (`decnav`)
Copies `.nav_1` (Position Sensor 1 from `#SPO`) to `.nav` and uses [`appendNav`](../nav/appendNav.md) to write a 10x decimated navigation file into `decnav/$SUBDIR/$LINE_NUMBER.decnav`:
```tcsh
rm merged/$SUBDIR/$LINE_NUMBER.nav
cp merged/$SUBDIR/$LINE_NUMBER.nav_1 merged/$SUBDIR/$LINE_NUMBER.nav
appendNav -skip 10 -comp decnav/$SUBDIR/$LINE_NUMBER.decnav merged/$SUBDIR/$LINE_NUMBER.nav
```

### Stage 7: Select Network Attitude Source & Run `mergeAtt`
Copies `.net_att_2` (KM Binary Sensor Input from `#SKM`, `sensorInputFormat == 1`) to `.orientation` and merges roll, pitch, heave, and heading into the `.merged` profile headers via [`mergeAtt`](../omg/mergeAtt.md):
```tcsh
rm merged/$SUBDIR/$LINE_NUMBER.orientation
cp merged/$SUBDIR/$LINE_NUMBER.net_att_2 merged/$SUBDIR/$LINE_NUMBER.orientation
mergeAtt merged/$SUBDIR/$LINE_NUMBER
```
*(Note: If your vessel logs POS MV GRP 102/103 network attitude instead of KM Binary, `.net_att_1` will be populated instead of `.net_att_2`—change `net_att_2` to `net_att_1` in the script!)*

### Stage 8: Merge Navigation (`mergeNav`) & Recompute Bounds (`getBounds`)
Merges the `.nav` file onto the `.merged` profile headers (with zero lever arms, since SIS already references `#SPO` to the RP) and updates `.merged.100_ping_bounds` and `.merged.global_bounds`:
```tcsh
mergeNav -ahead 0.0 -right 0.0 -below 0.0 -declin 0.0 -delay 0.00 merged/$SUBDIR/$LINE_NUMBER
getBounds merged/$SUBDIR/$LINE_NUMBER.merged
```

### Stage 9: Generate & Gap-Fill GLORIA Sidescan (`.ss`)
Runs [`makess`](../omg/makess.md) with a `+40` DN shift to create a temporary GLORIA sidescan file, fills across-track dropout stripes using [`glfill`](../sidescan/hist/glfill.md), and launches [`jview`](../JV/jview.md) in the background:
```tcsh
makess -DN_Shift 40 merged/$SUBDIR/$LINE_NUMBER.merged ss/$SUBDIR/$LINE_NUMBER.temp
glfill ss/$SUBDIR/$LINE_NUMBER.temp ss/$SUBDIR/$LINE_NUMBER.ss
/bin/rm ss/$SUBDIR/$LINE_NUMBER.temp
jview -gl -initstr 150 230 ss/$SUBDIR/$LINE_NUMBER.ss &
```

### Stage 10: Water Column Vertical Profile & Annotated GIF (`makeWC`)
If `$FOUND_SEPARATE_WCD == 1`, extracts an along-track nadir water column vertical curtain up to **2500 m depth** (`-maxdepth 2500 -pixel 2.5 -aspect 0.10`), fills gaps (`-ignore 88`), stretches contrast (`-low 120 -high 200`), and uses ImageMagick `convert` to produce a rotated, annotated GIF `merged/$SUBDIR/$LINE_NUMBER.vert_prof.gif`:
```tcsh
set TMPBASE = /tmp/unravel_$$_$LINE_NUMBER
makeWC -maxdepth 2500 -pixel 2.5 -aspect 0.10 -add_heave -other_heave \
    -vert_prof merged/$SUBDIR/$LINE_NUMBER.merged merged/$SUBDIR/$LINE_NUMBER.vert_prof
fillGap -ignore 88 merged/$SUBDIR/$LINE_NUMBER.vert_prof ${TMPBASE}.vert_prof
stretchacres -low 120 -high 200 -in ${TMPBASE}.vert_prof -pgm -out ${TMPBASE}.pgm
convert -rotate 90 -flop ${TMPBASE}.pgm ${TMPBASE}.ppm
convert -font helvetica -fill blue -pointsize 24 -draw "text 20,995 '$LINE_NUMBER'" \
    ${TMPBASE}.ppm merged/$SUBDIR/$LINE_NUMBER.vert_prof.gif
/bin/rm -f ${TMPBASE}.vert_prof ${TMPBASE}.pgm ${TMPBASE}.ppm
```

---

## How to Customize This Script for Different Surveys

1. **Changing Water Depth Range for Water Column Profiles (`2500m`):**
   The `2500m` in `unravel_KMALL_2500m_RevHplus_netatt2` refers to `-maxdepth 2500 -pixel 2.5` passed to `makeWC`. For shallow-water EM2040 surveys (e.g., 100 m max depth), change this to `-maxdepth 100 -pixel 0.25`. For full-ocean-depth EM124 surveys (e.g., 6000 m), change this to `-maxdepth 6000 -pixel 5.0`.
2. **Changing Attitude Source (`net_att_2` vs `net_att_1` vs `orientation_1`):**
   Check `ls -lh merged/$SUBDIR/$LINE_NUMBER.*att* merged/$SUBDIR/$LINE_NUMBER.orientation*` after running `read_kmall` on one test file. Copy whichever file is non-empty (`net_att_1` for POS MV GRP 102/103, `net_att_2` for KM Binary, or `orientation_1` for EM3000 serial) to `.orientation`.
3. **Disabling X11 Pop-Up Windows During Batch Runs:**
   In `unravel_KMALL_single` (line 184), `jview -gl -initstr 150 230 ss/$SUBDIR/$LINE_NUMBER.ss &` spawns a background X11 window for every unravelled file. Comment out line 184 (`# jview ...`) when running unattended batch jobs over hundreds of lines!
