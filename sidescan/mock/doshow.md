---
layout: default
title: doshow
parent: Mock Tools
grand_parent: Sidescan Tools
nav_order: 18
tool_name: doshow
source_path: code/sidescan/mock/doshow
category: Sidescan & Backscatter Modeling
input_formats: ["Water depth parameter (meters)"]
output_formats: ["plot.out (ASCII curve)", "plot.meta (Metafile plot)"]
related_tools: ["showgains", "test_tvg_effect", "test_tvg_dirindex"]
---

# doshow

## Description
`doshow` is a shell script in `code/sidescan/mock/` that runs [`showgains`](showgains.md) for a user-specified water depth, converts the resulting ASCII gain table into a plot metafile with `asciiplot`, and displays it interactively with `viewmeta`.

## Usage
```bash
doshow <depth_m>
```
* **`$1` (`<depth_m>`)**: Water depth in meters passed to `showgains -depth $1`.

## Pipeline Executed
```sh
showgains -depth $1 > plot.out
asciiplot -infile plot.out
viewmeta plot.meta
```
This allows rapid visual inspection of how GLORIA Time-Varying Gain (TVG), two-way transmission loss, and vertical beam directivity combine across slant range at any given water depth.
