---
layout: default
title: swathed
parent: Swath Editor — swathed (SE)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
nav_order: 1
tool_name: swathed
source_path: code/SE/swathed.c
category: Interactive QC & Editing
input_formats:
- .merged
- .merged.100_ping_bounds
- .merged.global_bounds
- .watercol
- .WC_Phase1
- .WC_Phase2
- .r4
- .r4_weights
- .r4_weight_depth
- .8bit
- .ss
output_formats:
- .merged (beam status flags updated in-place)
- .r4 (updated live if -locate is used)
- .lookup
- .cleaned_areas
related_tools:
- getBounds
- dumpFlags
- weigh_grid
- jview
- RefractEd
- newMergeAtt
---

# swathed

## Description
`swathed` (Swath Editor) is the flagship interactive X-Windows graphical application of the Ocean Mapping Group, continuously developed by John Hughes Clarke and collaborators since October 1990. It provides a swath-by-swath and geographic framework for:
1. **Interactive Bathymetric Cleaning:** Flagging and unflagging outlier soundings (`beam.status`) in 2D across-track profiles, plan-view swath corridors, or 2D geographic sub-areas (`-show_2D`, `-show_geo`).
2. **Live DTM Updating (`-locate`):** When launched with `-locate <dtmprefix>`, `swathed` loads `<dtmprefix>.r4`, `.r4_weights`, and `.r4_weight_depth`. As you reject or restore soundings in `.merged` files, `swathed` can dynamically subtract and re-grid modified pings directly into the `.r4` surface and track cleaned sub-boxes in `<dtmprefix>.cleaned_areas`!
3. **2D & 3D Water Column Visualization (`-show_WC2D`, `-show_WC3D`):** Interactive fan ("pie") and 3D views of `.watercol` amplitude and `.WC_Phase1`/`.WC_Phase2` split-beam phase data (compressed via JasPer or uncompressed), including bottom-detection re-picking (`SE_BDI_DP`, `SE_PDI_LA`) and gas seep / target hunting.
4. **Patch Testing (`SE_PATCHwin`):** Interactive roll, pitch, heading, and latency calibration over rotatable sub-areas.
5. **Refraction & Time Series Analysis (`SE_REFTOOLwin`, `SE_W_TimeSeries`):** Interactive surface sound speed and SVP layer refraction correction (`.ref_coeffs`) and motion-residual time-series diagnostics (`-ts`).

> [!TIP]
> **Preserving Manual Edits Across Re-Unraveling (`dumpFlags`):**
> Because `swathed` writes sounding rejection flags directly into `<line>.merged`, re-running `read_kmall` or `RTlite` would overwrite your manual cleaning work. All OMG unraveling scripts (`unravel_KMALL_single`, `bunravel`) automatically run [`dumpFlags`](../omg/dumpFlags.html) before unpacking (which saves your `swathed` edits to `<line>.flag_bk`) and `dumpFlags -load` afterward to restore them!

---

## Usage

```bash
swathed [OPTIONS] <omgfile(s).merged ...>
```

### Common Workflow Examples

**1. Inspect and clean a single `.merged` line (e.g., during or after unraveling):**

```bash
swathed merged/JD100/0001_line.merged
```

**2. Geographic area-based cleaning over a `weigh_grid` DTM (`-locate`) using a file list (`-xyzlist`):**

```bash
# Ensure getBounds has been run on all .merged files first!
getBounds merged/JD100/*.merged

# Launch swathed over the bay_2m.r4 grid with all lines from JD100:
swathed -locate bay_2m merged/JD100/*.merged
```

**3. Inspect 2D water column "pie" fans on a `.kmall` / `.kmwcd` line up to 750 m depth:**

```bash
swathed -show_WC2D -WC_depth 750.0 merged/JD100/0001_line.merged
```

**4. Batch-export 2D water column fan images or 2D profile scatterplots and exit automatically (`-and_terminate`):**

```bash
swathed -show_WC2D -dump_WC2D_pies -and_terminate merged/JD100/0001_line.merged
```

---

## Arguments

### Input Files & Geographic Background Map (`-locate` / `-image`)

| Option | Description | Default |
|---|---|---|
| `<omgfile(s)>` | One or more `.merged` files (or `.ss` files if `-gl` is set). | Required (unless `-xyzlist` used) |
| `-xyzlist <listfile>` | Read paths of `.merged` files from an ASCII list file (matches `weigh_grid` and `mos2` syntax). | Disabled |
| `-locate <dtmprefix>` | Load `<dtmprefix>.r4`, `.r4_weights`, and `.r4_weight_depth` as the interactive geographic background map. Enables rubber-band sub-area selection (`SE_GEOwindows`) to load all intersecting `.merged` swaths in a box and live-update the `.r4` DTM as outliers are rejected. Also reads/writes `<dtmprefix>.lookup` and `<dtmprefix>.cleaned_areas`. | Line-by-line mode |
| `-image <mapfile>` | Load up to 20 background 8-bit imagery / sun-illuminated mapsheets (e.g., `<prefix>.sun_315` or `<prefix>.mos`) to display in the geographic locator window. | None |
| `-try_anyway` | Bypass the `.global_bounds` / `.100_ping_bounds` spatial intersection check and consider all input `.merged` files when selecting a geographic sub-area. | Uses `getBounds` files |
| `-nmap` | Use memory-mapped I/O (`mmap`) for large background grids. | Disabled |
| `-target <file>` / `-tgt <file>` | Load and plot target coordinates from `<file>` on the geographic window. | None |
| `-vectbin <file>` | Overlay binary vector contours (`bin_vect` format) on the geographic window. | None |
| `-boxes <file>` | Overlay bounding boxes from `<file>` on the geographic window. | None |

### Display Windows & Automated Batch Views

| Option | Description | Default |
|---|---|---|
| `-show_2D` | Automatically open the 2D sounding scatterplot window (`SE_2Dwindow`). | Closed at startup |
| `-dump_2D` | Export the 2D window view to disk. | Disabled |
| `-2D_show_botdet` | Color soundings in the 2D window by bottom detection method (Amplitude vs. Phase). | Color by depth/line |
| `-detrend_2D` | Remove regional seafloor slope trend in the 2D scatterplot window. | Disabled |
| `-force_detrend_EW_NS` | Force East-West / North-South detrending orientation in 2D window. | Disabled |
| `-force_2D_dirn <0..3>` | Force 2D viewing azimuth (`0` = South, `1` = West, `2` = North, `3` = East). | Auto (dominant heading) |
| `-force_2D_depths <min> <max>` | Lock vertical depth axis range in the 2D window to `[min, max]` meters. | Auto-scaled |
| `-force_2D_nodirty` | Hide already-flagged ("dirty") soundings (`show_flagged = 0`) in the 2D window. | Shows flagged soundings |
| `-show_geo <x1> <x2> <y1> <y2>` | Immediately open a geographic sub-area window spanning pixel coordinates `[x1..x2, y1..y2]` on the `-locate` map. | Interactive selection |
| `-show_geo2 <lat> <lon> <w_px> <h_px>` | Immediately open a geographic sub-area centered on `(lat, lon)` with pixel dimensions `w_px x h_px`. | Interactive selection |
| `-jump_to_recnum <ping>` | Jump directly to ping record `<ping>` when opening the line editor. | Ping `0` |
| `-Allowed <shoal_m> <deep_m>` | Set minimum and maximum allowed depth bounds (`Shoallest_Allowed`, `Deepest_Allowed`). | Auto |
| `-colrange <min_DN> <max_DN>` | Set color palette index range. | Full palette |
| `-mini` / `-maxi` | Use compact (`JX_TINY`) or large (`JX_LARGE`) X11 UI button sizes. | Standard |
| `-noboop` | Disable the terminal bell ("boop") sound when reaching the end of a survey line. | Enabled |
| `-and_terminate` | Automatically exit `swathed` after completing requested `-dump_*` batch operations. | Interactive event loop |

### Water Column Visualization (`-show_WC2D` / `-show_WC3D`)

| Option | Description | Default |
|---|---|---|
| `-show_WC2D` | Open the 2D Water Column wedge/pie display window (`SE_WaterColumn`). Requires `<line>.watercol` in the same directory as `<line>.merged`. | Disabled |
| `-show_WC3D` | Open the 3D Water Column display window. | Disabled |
| `-WC_depth <meters>` | Force the maximum depth range (meters) of the water column display (`max_good_depth_forced`). | Auto from bottom track |
| `-use_WC2D_zoom <minz> <maxz> <leftx> <rightx>` | Lock the 2D water column zoom window to vertical range `[minz, maxz]` (m) and across-track range `[leftx, rightx]` (m). | Full fan |
| `-wide_WC` / `-tall_and_wide_WC` | Enlarge the X11 dimensions of the water column display window. | Standard size |
| `-suppress_after_r0` | Mask out water column samples beyond the minimum slant range ($R_0$) sidelobe arc. | Disabled |
| `-dump_WC2D_pies` | Batch-render and save 2D water column fan images for every ping. | Disabled |
| `-dump_WC3D_rotate` | Batch-render rotating 3D water column frames. | Disabled |

### Pre-Filters, Vertical Corrections & Special Modes

| Option | Description | Default |
|---|---|---|
| `-pre_defluff` | Automatically run the water-column "fluff" / false bottom-detect pre-filter on startup. | Disabled |
| `-pre_median` | Run median outlier pre-filter on startup. | Disabled |
| `-pre_detrench` | Run Kongsberg sector-boundary "trench" artifact filter on startup. | Disabled |
| `-auto` / `-autoparam <file>` | Run automated outlier flagging using parameters from `<file>`. | Disabled |
| `-useproc` | Display `beam.processedDepth` instead of `beam.observedDepth`. | `observedDepth` |
| `-calcref` / `-refco` | Apply interactive refraction correction coefficients (`.ref_coeffs`). | Disabled |
| `-apply_LPH` | Apply `profile.longperiod_heaveCorrection` to depths. | Disabled |
| `-delayed_heave <attfile>` | Load external POS MV delayed heave attitude file (`<attfile>`) for comparison/application. | Disabled |
| `-invert_heave_sign` | Invert the sign of heave corrections. | Disabled |
| `-addGPSrolloverwraps <N>` | Compensate for 1024-week GPS epoch rollover (`N * 619315200` s). | `0` |
| `-ts` | Open the attitude / motion residual time-series analyzer window (`SE_W_TimeSeries`). | Disabled |
| `-ABS` | Open Anand's Backscatter calibration window (`SE_AnandBS`). | Disabled |
| `-pixel <m>` | Set sidescan display pixel size (meters) in the sidescan window (`SE_sswindow`). | Auto |
| `-ship_LOA <meters>` | Set ship Length Overall (meters) for the 3D vessel model in `SE_3D`. | Default |
