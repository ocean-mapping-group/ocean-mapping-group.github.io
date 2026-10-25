---
layout: default
title: ss_blend_dual_head
parent: Jonathan Beaudoin (jonnyb) Tools
nav_order: 2
tool_name: ss_blend_dual_head
source_path: code/jonnyb/gom_stuff/ss_blend_dual_head.c
category: Backscatter & Sidescan Processing (jonnyb)
input_formats: [".ss (GLORIA format dual-head sidescan)"]
output_formats: [".ss (GLORIA format blended single-ping sidescan)"]
related_tools: ["makess", "mos2", "deTVG", "SE_sswindow"]
---

# ss_blend_dual_head

## Description
`ss_blend_dual_head` (`code/jonnyb/gom_stuff/ss_blend_dual_head.c`, written by Jonathan Beaudoin, October 2012) merges paired port and starboard GLORIA `.ss` sidescan records produced when [`makess`](../omg/makess.md) processes a dual-head multibeam echosounder (where each transducer head logs a separate ping record) into a single combined `gloria_rec` scanline per ping cycle.

---

## Usage

```bash
ss_blend_dual_head [-v] [-invalid <val>] [-swap_sides] \
    [-seam | -overlay_port | -overlay_stbd | -feather] \
    (-by_ping | -by_time) <infile.ss> <outfile.ss>
```

### Examples

**1. Feather-blend overlapping dual-head sidescan records matched by ping number:**
```bash
ss_blend_dual_head -feather -by_ping dual_line.ss blended_line.ss
```

**2. Blend at the center nadir seam matching paired heads by timestamp:**
```bash
ss_blend_dual_head -seam -by_time dual_line.ss blended_line.ss
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<infile.ss>` | Input GLORIA format (`.ss`) sidescan file containing separate port and starboard ping records. | Required |
| `<outfile.ss>` | Output GLORIA format (`.ss`) sidescan file with merged ping records. | Required |
| `-by_ping` | Match port and starboard records that share the same `ping_no` (`GL_MATCH_BY_PING`). | Either `-by_ping` or `-by_time` required |
| `-by_time` | Match port and starboard records that share the same timestamp (`GL_MATCH_BY_TIME`). | Either `-by_ping` or `-by_time` required |
| `-seam` | Blend at the center nadir seam (`GL_BLEND_SEAM`): uses port head for port pixels and starboard head for starboard pixels. | Default (`GL_BLEND_SEAM`) |
| `-overlay_port` | Overlay valid port-head samples on top of starboard-head samples in the overlap zone (`GL_BLEND_OVERLAY_PORT`). | Disabled |
| `-overlay_stbd` | Overlay valid starboard-head samples on top of port-head samples in the overlap zone (`GL_BLEND_OVERLAY_STBD`). | Disabled |
| `-feather` | Linearly feather between port and starboard backscatter intensities across the nadir overlap zone (`GL_BLEND_FEATHER`). | Disabled |
| `-swap_sides` | Swap port and starboard record assignment before blending. | Disabled |
| `-invalid <val>` | Pixel value treated as nodata/invalid in the 8-bit `.ss` scanline (`0..255`). | `255` |
| `-v` | Enable verbose output. | Disabled |
