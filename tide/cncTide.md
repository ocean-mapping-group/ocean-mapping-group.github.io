---
layout: default
title: cncTide
parent: Tide Tools
---

# cncTide

## Description
`cncTide` is a utility that translates Rich Signell's tide data format into the standard OMG tide format. It reads CNC (likely Canadian Hydrographic Service) tide data files and converts them for use in ocean mapping processing workflows.

## Usage
```bash
cncTide (-v) (-fmt 2) -y2k -tide tidefilename mergefile(s)
```

## Arguments

| Option | Description |
|---|---|
| `-v` | Enable verbose output |
| `-fmt 2` | Specify format version |
| `-y2k` | Enable Y2K date handling |
| `-tide tidefilename` | Input tide data file |
| `mergefile(s)` | Output merge file(s) |

## How It Works
1. **Data Reading:** Reads tide data from Rich Signell's format
2. **Format Conversion:** Translates to OMG standard format
3. **Date Handling:** Supports Y2K compliant date processing
4. **Output:** Generates merge-compatible tide files
