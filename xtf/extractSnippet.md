---
layout: default
title: extractSnippet
parent: XTF Tools
nav_order: 3
tool_name: extractSnippet
source_path: code/xtf/extractSnippet.c
category: Backscatter & Image Processing
input_formats: [".xtf"]
output_formats: [".8bit", ".pgm"]
related_tools: ["extractRI", "stripSS", "xtfTool", "xtf2omg_reson"]
---

# extractSnippet

## Overview
`extractSnippet` extracts Reson SeaBat snippet packets (`XTF_HEADER_RESON_SNIPPET`, packet ID 19) from an XTF file and renders them as an 8-bit waterfall image (`.8bit` or `.pgm`) mapped across slant-range sample offsets, or dumps a single ping's snippet traces to stdout when `-ping` is specified.

## Usage
```bash
extractSnippet [-v] [-pgm] [-nocorr] [-ping <ping_num>] -in <file.xtf>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<file.xtf>` | **Required** | Path to the input `.xtf` file (unlike `extractRI`, include the `.xtf` extension). |
| `-pgm` | None | Off (`.8bit`) | Output image in Portable Graymap (`<basename>.pgm`) format instead of OMG/JHC (`<basename>.8bit`) format. |
| `-nocorr` | None | Off | Skip radiometric/TVG correction (`corrRESON_SNIPPET`) when rendering snippet samples. |
| `-ping` | `<ping_num>` | `0` (All) | Inspect/extract a specific snippet ping number. |
| `-v` | None | Off | Enable verbose diagnostic output. |

## How It Works
1. **Indexing & Offset Scanning:** Builds an XTF packet index with `buildXTFIndex()` and scans all `XTF_HEADER_RESON_SNIPPET` (ID 19) packets (skipping the 256-byte XTF wrapper header on each) to determine the minimum (`minOffset`) and maximum (`maxOffset = FragOffset + SnipSamples`) sample offsets across all beams.
2. **Image Allocation:** Creates an output raster of width `2 * maxOffset` (port and starboard slant-range samples) and height `numSnippetRecords`, writing either a PGM header (`writePGM`) or OMG 8-bit header (`writeJHC`).
3. **Snippet Mapping:** For each snippet record, optionally applies `corrRESON_SNIPPET()` (unless `-nocorr` is set) and places each beam's 8-bit snippet samples into the port or starboard half of the scanline according to its `FragOffset`.

## Practical Examples

**1. Generate a PGM waterfall image of Reson snippets from an XTF file:**
```bash
extractSnippet -pgm -in line02.xtf
```

**2. Generate an uncorrected OMG `.8bit` snippet image:**
```bash
extractSnippet -nocorr -in line02.xtf
```
