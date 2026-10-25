---
layout: default
title: normalize_adcp
parent: Jonathan Beaudoin — SVP, Refraction & Snippets (jonnyb)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 3
tool_name: normalize_adcp
source_path: code/jonnyb/gom_stuff/normalize_adcp.c
category: Water Column & ADCP Processing (jonnyb)
input_formats:
- .r4 (OMG floating-point ADCP curtain grid)
output_formats:
- .r4 (range-normalized ADCP curtain grid)
related_tools:
- mergeNav
- iwc_adcp
---

# normalize_adcp

## Description
`normalize_adcp` (`code/jonnyb/gom_stuff/normalize_adcp.c`) normalizes range/depth-dependent acoustic attenuation across an ADCP backscatter curtain stored as an OMG 32-bit floating-point grid (`.r4`, where `dx` is the depth/range bin axis and `dy` is the ping/time axis).

For each ping $i$, it accumulates non-zero water-column samples along depth bins $j \in [0, \text{dx}-1]$, stopping at the first zero-value sample encountered after valid water-column returns (so sub-bottom blanked samples are excluded). It then computes the mean amplitude $\bar{A}_j$ for each depth bin (optionally capped at `-max_count` pings), calculates the global mean $\bar{A}$ across all valid depth bins, and shifts every non-zero sample in bin $j$ by $(\bar{A} - \bar{A}_j)$.

---

## Usage

```bash
normalize_adcp [-max_count <N>] -in <infile.r4> -out <outfile.r4>
```

### Example

```bash
normalize_adcp -max_count 200 -in adcp_raw.r4 -out adcp_norm.r4
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-in <infile.r4>` | Input `.r4` floating-point ADCP curtain grid (`load_map`). | Required |
| `-out <outfile.r4>` | Output range-normalized `.r4` grid (`write_map`). | Required |
| `-max_count <N>` | Maximum number of valid pings accumulated per depth bin when estimating that bin's mean amplitude (`count[j] < max_count`). | `inmap.header.dy` (all pings) |
