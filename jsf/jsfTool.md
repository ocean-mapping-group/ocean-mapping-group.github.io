---
layout: default
title: jsfTool
parent: EdgeTech JSF Sidescan & Sub-Bottom (jsf)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 5
tool_name: jsfTool
source_path: code/jsf/jsfTool.c
category: Diagnostics & Indexing
input_formats:
- .jsf
output_formats:
- stdout (ASCII summary & packet dumps)
related_tools:
- jsf2omg
- jsf2glo
- jsf2nav
- jsf2orientation
---

# jsfTool

## Overview
`jsfTool` is a diagnostic utility for inspecting EdgeTech `.jsf` files. It verifies message synchronization (`0x1601` header marker), counts the occurrences of every JSF message type across the file, and optionally dumps decoded message headers and payloads (`80` Sonar Data, `2020` Orientation, `3000` Bathymetric Data, `3001` Attitude, `3002` Pressure, `3004` Position) to stdout.

## Usage

```bash
jsfTool [-v] [-contents] [-vid <ID>] -in <inputfile.jsf>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<inputfile.jsf>` | **Required** | Path to the input EdgeTech `.jsf` file. |
| `-contents` | None | Off | Fast inventory mode: seek over message payloads without parsing them and print only the message type count summary at the end. |
| `-v` | None | Off | Print the `JSF_Message_Header` for every message in the file. |
| `-vid` | `<ID>` | Off | Print the decoded payload for a specific JSF message ID (`80`, `2020`, `3000`, `3001`, `3002`, or `3004`). May be specified multiple times. |

## How It Works
1. **Header Parsing:** Loops through the `.jsf` file calling `parse_JSF_Message_Header()`, checking that `header.start == JSF_SONAR_MESSAGE_HEADER_START` (`0x1601`), and incrementing `count[header.message_type]`.
2. **Payload Decoding:** Unless `-contents` is set, dispatches recognized message types (`80`, `2020`, `3000`, `3001`, `3002`, `3004`) to their `omg_jsf` parser functions and prints their fields when enabled via `-vid <ID>`.
3. **Summary Inventory:** Upon reaching EOF, prints `<message_id> (<message_name>): <count>` for all message types encountered.

## Practical Examples

**1. Cepatly list the message inventory of a `.jsf` file:**

```bash
jsfTool -contents -in survey01.jsf
```

**2. Dump all JSF Bathymetric (3000) and Pressure/SV (3002) messages:**

```bash
jsfTool -vid 3000 -vid 3002 -in survey01.jsf
```
