---
layout: default
title: jsf2nav
parent: EdgeTech JSF Sidescan & Sub-Bottom (jsf)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 2
tool_name: jsf2nav
source_path: code/jsf/jsf2nav.c
category: Navigation Extraction
input_formats:
- .jsf
output_formats:
- .nav
related_tools:
- jsf2omg
- jsf2orientation
- jsf2glo
- jsfTool
- mergeNav
---

# jsf2nav

## Overview
`jsf2nav` extracts position fixes from EdgeTech JSF Position messages (message type `3004`, `JSF_Position_3004_Data`) and writes them into a binary OMG `jcu_nav_rec` navigation file (`<nav_file_prefix>.nav`).

## Usage

```bash
jsf2nav [-v] [-debug] -jsf <input_name.jsf> -nav <nav_file_prefix>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-jsf` | `<input_name.jsf>` | **Required** | Path to the input EdgeTech `.jsf` file. |
| `-nav` | `<nav_file_prefix>` | **Required** | Output prefix; creates `<nav_file_prefix>.nav`. |
| `-v` | None | Off | Print every parsed `JSF_Position_3004_Data` structure. |
| `-debug` | None | Off | Enable debug flag. |

## How It Works
1. **Message Filtering:** Iterates sequentially through all `JSF_Message_Header` blocks in the input `.jsf` file, skipping any message whose `message_type != 3004`.
2. **Validity Check:** Inspects `navigation_3004.data_validity_flags` and requires both bit `0x0008` and bit `0x0010` (valid latitude and longitude) to be set before accepting a record.
3. **OMG Navigation Output:** Populates `jcu_nav_rec` (`time`, `centisecs` from nanoseconds, `lat`, `lon`) and writes each fix to `<nav_file_prefix>.nav` via `nav_write()`.

## Practical Examples

**1. Extract navigation from an EdgeTech 4600/2205 JSF file:**

```bash
jsf2nav -v -jsf line01.jsf -nav line01
```
