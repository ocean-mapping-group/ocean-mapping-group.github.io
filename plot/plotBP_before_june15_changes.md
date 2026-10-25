---
layout: default
title: plotBP_before_june15_changes
parent: PostScript & Vector Plotting (plot)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: plotBP_before_june15_changes
source_path: code/plot/plotBP_before_june15_changes.c
category: Scientific & Diagnostic Plotting
related_tools:
- plotBP
- getBeamPattern
- newGetBP
- makeFoot
- viewmeta
---

# plotBP_before_june15_changes

## Overview
`plotBP_before_june15_changes` (`code/plot/plotBP_before_june15_changes.c`) is the preserved pre-June 2015 revision of [`plotBP`](plotBP.html), the Ocean Mapping Group's vector plotting utility for acoustic beam patterns (`getBeamPattern`), seafloor angular response curves (`.graz` / `.ar`), and multibeam 3 dB beam footprints (`makeFoot`).

It writes device-independent vector graphics to `plot.meta` (or a user-specified `-outfile`) using [`plotlib`](../plotlib/plotlib.html), supporting both **polar** (`-polar`) and **Cartesian** (`-cartes`, default) coordinate layouts, multi-panel grid layouts (`-apart`), and smoothing filters (`-median`, `-average`).

---

## Usage

```bash
plotBP_before_june15_changes [OPTIONS] <input_file(s) ...>
```

---

## Command-Line Options

| Option | Description | Default |
|---|---|---|
| `-size <dx> <dy>` | Set overall plot page dimensions in centimeters (`dx` width, `dy` height). | `16.0` x `20.0` cm |
| `-outfile <filename>` | Output `plotlib` metafile path. | `plot.meta` |
| `-bp` | Input files are binary/ASCII beam-pattern dumps from `synSwath` or `beamPatt` (read via `read_bpfile` from [`bP_stuff`](../subr/bP_stuff.html)). Without `-bp`, reads 4-column ASCII grazing-angle/intensity files (`angle`, `intensity`, `refcorr`, `dummy`) from `getBeamPattern`. | Grazing-angle ASCII |
| `-foot` | Input files are multibeam footprint characterization files (read via `load_BF_characteristics` from [`beam_foot`](../subr/beam_foot.html)). Sets default signal range to `-3` to `0` dB. | Disabled |
| `-polar` | Render plots in polar coordinates ($-90^\circ$ to $+90^\circ$ lower hemisphere fan) instead of Cartesian axes. | Cartesian |
| `-cartes` | Render plots on Cartesian axes (Angle in degrees vs. Intensity in dB). | Default |
| `-apart` | Tile multiple input files into separate sub-panels on a $\sqrt{N} \times \lceil N/\sqrt{N}\rceil$ grid instead of overplotting on a single axis. | Overplot |
| `-rainbow` | Cycle pen colors (`1 + ii % 6`) across overlaid curves. | Pen 1 |
| `-port` / `-stbd` / `-both` | Plot only port (`-90` to `0` deg), only starboard (`0` to `+90` deg), or both sides of the swath. | `-both` |
| `-sigrange <min_dB> <max_dB>` | Set the dB intensity axis range. | `-60.0` to `0.0` dB |
| `-refrange <ref_angle> <dB_range>` | Normalize intensity curves relative to the response at `<ref_angle>` degrees (or pass `-999` to normalize to the peak response between $-80^\circ$ and $+80^\circ$). | Disabled |
| `-ref` | Plot the reference correction column (`refcorr[j]`) alongside the raw intensity curve. | Disabled |
| `-invert` | Negate intensity values (`intensity[j] = -intensity[j]`). | Disabled |
| `-average` | Apply a 3-point moving average filter (`javerage`) across valid angular bins. | Disabled |
| `-median` | Apply a 5-point moving median filter (`jmedian`) and write filtered output to `temp.median`. | Disabled |
| `-ps` | When `-bp` is active, plot `BP[TRANSMIT_PORT_STBD][LOG_POWER]` instead of `TRANSMIT_FORE_AFT`. | Fore-Aft |
| `-phase` | When `-bp` is active, plot phase response (`Phase[j]`) scaled across the signal range. | Amplitude (dB) |
| `-labelcurves` | Annotate each plotted curve with its filename index. | Disabled |
| `-title1 <str>` / `-title2 <str>` | Custom primary and secondary plot titles. | Input filename |
| `-notext` / `-sparse` | Suppress all text annotations (`-notext`) or reduce grid label density (`-sparse`). | Full labels |

---

## Differences from Current `plotBP`
This file preserves the `plotBP.c` implementation prior to the June 2015 updates (which refined multi-sector Kongsberg beam-pattern overlays and text formatting). For production plotting workflows, see [`plotBP`](plotBP.html).
