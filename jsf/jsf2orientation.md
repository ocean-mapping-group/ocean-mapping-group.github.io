---
layout: default
title: jsf2orientation
parent: JSF Tools
nav_order: 4
tool_name: jsf2orientation
source_path: code/jsf/jsf2orientation.c
category: Attitude Extraction
input_formats: [".jsf"]
output_formats: [".orientation", ".heading"]
related_tools: ["jsf2omg", "jsf2nav", "jsf2glo", "jsfTool", "mergeAtt", "newMergeAtt"]
---

# jsf2orientation

## Overview
`jsf2orientation` extracts attitude and heading records from EdgeTech JSF Attitude messages (message type `3001`, `JSF_Attitude_3001_Data`) and writes two OMG-HDCS v3 attitude files:
* `<prefix>.orientation`: Roll, pitch, heave, and heading records (`status = 15`).
* `<prefix>.heading`: Heading-only records (`status = 4`).

## Usage
```bash
jsf2orientation [-v] [-debug] -jsf <input_name.jsf> -orientation <file_prefix>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-jsf` | `<input_name.jsf>` | **Required** | Path to the input EdgeTech `.jsf` file. |
| `-orientation` | `<file_prefix>` | **Required** | Output prefix for `<file_prefix>.orientation` and `<file_prefix>.heading`. |
| `-v` | None | Off | Print every parsed `JSF_Attitude_3001_Data` record. |
| `-debug` | None | Off | Enable debug flag. |

## How It Works
1. **Base Time Initialization:** Scans the `.jsf` file for the first message `3001` to establish `base_time` (`refTime = base_time / 100`), writes `OMG_HDCS_summary_attitude` headers to `<prefix>.orientation` and `<prefix>.heading`, and rewinds the file.
2. **Validity Bit Routing:** For every message `3001`, inspects `attitude_3001.data_validity_flags`:
   * If bit `0x01` (heading valid) is set, writes a heading record (`heading * 100.0`) to `<prefix>.heading`.
   * If bits `0x02` (roll), `0x04` (pitch), and `0x08` (heave) are all set (either alongside bit `0x01` or independently), writes a full roll/pitch/heave/heading `OMG_HDCS_attitude` record to `<prefix>.orientation`.

## Practical Examples

**1. Extract `.orientation` and `.heading` files from an EdgeTech JSF file:**
```bash
jsf2orientation -jsf line01.jsf -orientation line01
```
