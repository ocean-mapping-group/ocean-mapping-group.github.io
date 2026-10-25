---
layout: default
title: jsf2glo
parent: JSF Tools
nav_order: 1
tool_name: jsf2glo
source_path: code/jsf/jsf2glo.c
category: Sidescan & Sub-Bottom Conversion
input_formats: [".jsf"]
output_formats: [".low_ss", ".hig_ss", ".subb", ".merged", ".merged.ss_data", ".merged.16_data"]
related_tools: ["jsf2omg", "jsf2nav", "jsf2orientation", "jsfTool", "mos2"]
---

# jsf2glo

## Overview
`jsf2glo` converts dual-frequency sidescan and sub-bottom profiler traces from an EdgeTech `.jsf` file into 8-bit 1024-pixel JCU GLORIA files (`<prefix>.low_ss`, `<prefix>.hig_ss`, and `<prefix>.subb`), with an option (`-out_as_OMG`) to simultaneously write an OMG-HDCS v3 2-beam `.merged` file along with `.merged.ss_data` (8-bit) and `.merged.16_data` (16-bit) trace files. It supports standard JSF Sonar Data messages (type `80`), legacy Sidescan messages (type `82`), and REMUS 600 Situation messages (type `2090`).

## Usage
```bash
jsf2glo [-v] [-log] [-DNramp <val>] [-min16bitval <val>] [-max16bitval <val>] [-maxlowslr <m>] [-maxhigslr <m>] [-maxsubslr <m>] [-out_as_OMG] -in <infile.jsf> -out <outfile_prefix>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-in` | `<infile.jsf>` | **Required** | Path to the input EdgeTech `.jsf` file. |
| `-out` | `<outfile_prefix>` | **Required** | Output prefix for `.low_ss`, `.hig_ss`, `.subb` (and `.merged`, `.merged.ss_data`, `.merged.16_data` when `-out_as_OMG` is set). |
| `-log` | None | Off (Linear) | Apply logarithmic 16-to-8-bit compression lookup table (`logval[65536]`) between `-min16bitval` and `-max16bitval`. |
| `-min16bitval` | `<int>` | `0` | Lower 16-bit amplitude threshold mapped to 8-bit DN `0`. |
| `-max16bitval` | `<int>` | `65535` | Upper 16-bit amplitude threshold mapped to 8-bit DN `255`. |
| `-DNramp` | `<float>` | `0.0` | Apply a linear digital-number ramp across the 512 pixels of each sidescan channel to compensate for across-track attenuation. |
| `-maxlowslr` | `<meters>` | Packet full range | Maximum slant range (m) to extract for the low-frequency sidescan subsystem (`subsystem == 20` or `71`). |
| `-maxhigslr` | `<meters>` | Packet full range | Maximum slant range (m) to extract for the high-frequency sidescan subsystem (`subsystem == 21`). |
| `-maxsubslr` | `<meters>` | Packet full range | Maximum slant range (m) to extract for the sub-bottom profiler subsystem (`subsystem == 0`). |
| `-out_as_OMG` | None | Off | In addition to GLORIA files, write OMG-HDCS v3 `<prefix>.merged`, `<prefix>.merged.ss_data`, and `<prefix>.merged.16_data` (`toolType = Knudsen_320`). |
| `-v` | None | Off | Enable verbose diagnostic output for JSF headers, subsystems, and coordinates. |

## How It Works
1. **Message Synchronization:** Scans the `.jsf` file for the `0x1601` start marker (`JSF_Message_Header`) and processes message types `80` (Sonar Data Trace), `82` (Sidescan Trace), and `2090` (AUV Situation message used on REMUS 600 to supply position, depth, and heading for type `82` traces).
2. **Subsystem Routing:** Routes traces based on `jsf_mess_head.subsystem`:
   * `0`: Sub-bottom profiler $\rightarrow$ `<prefix>.subb`
   * `20` or `71`: Low-frequency sidescan (e.g., 75/120 kHz) $\rightarrow$ `<prefix>.low_ss`
   * `21`: High-frequency sidescan (e.g., 410 kHz) $\rightarrow$ `<prefix>.hig_ss`
3. **Scaling & Downsampling:** Applies weighting factor scaling (`pow(2.0, -weighting_factor)`), maps 16-bit trace samples to 8-bit linearly or logarithmically (`-log`), applies optional `-DNramp` across-track gain ramping, resamples port and starboard channels into 512 pixels each (1024 pixels total), and writes GLORIA records via `jcu_writegloria()`.

## Practical Examples

**1. Convert dual-frequency EdgeTech sidescan to GLORIA with logarithmic scaling:**
```bash
jsf2glo -log -min16bitval 100 -max16bitval 25000 -in line01.jsf -out line01
```

**2. Convert sub-bottom and sidescan while also generating OMG `.merged` files:**
```bash
jsf2glo -log -out_as_OMG -in line01.jsf -out line01
```
