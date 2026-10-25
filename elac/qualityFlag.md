---
layout: default
title: qualityFlag
parent: ELAC BottomChart Multibeam (elac)
grand_parent: 4. Multi-Vendor Sonar & LiDAR Converters
nav_order: 1
tool_name: qualityFlag
source_path: elac/qualityFlag.c
category: bathymetry_filtering
input_formats:
- OMG_HDCS
output_formats:
- OMG_HDCS
related_tools:
- refoELAC
- elac2omg
- SwathEd
---

# qualityFlag

## Overview

`qualityFlag` flags or unflags multibeam bathymetry soundings in-place within OMG HDCS `.merged` files based on their beam quality factor (`Q_factor`). It is designed primarily for Honeywell ELAC BottomChart data (where `Q_factor` encodes a signal-to-noise ratio) and Reson SeaBat 8101 data (where `Q_factor` encodes brightness, collinearity, and amplitude/phase detection bits). Beams with quality values outside the specified `[minquality, maxquality]` range are marked as rejected (`status = 22`).

## Usage

```
qualityFlag (-v) (-minquality 0) (-maxquality 2) merged_file(s)
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `<merged_file(s)>` | `<file1> [file2 ...]` | *required* | One or more OMG HDCS `.merged` files to filter in-place. |
| `-minquality` | `<value>` | `0` | Minimum acceptable quality factor; beams below this value are flagged with `status = 22`. |
| `-maxquality` | `<value>` | `2` | Maximum acceptable quality factor; beams above this value are flagged with `status = 22`. |
| `-v` | none | `0` | Enable verbose output. |

## How It Works

1. **Header Inspection**: Opens each `.merged` file in read/write mode and reads `OMG_HDCS_summary_header` to identify `summary.toolType`.
2. **Quality Evaluation**: Iterates through every ping and beam, evaluating `beams[i].Q_factor` directly for ELAC data (where lower numbers `1`–`2` indicate higher SNR quality) or decoding brightness/collinearity bit flags for `SeaBat_8101`.
3. **In-Place Flagging**: Sets `beams[i].status = 22` if the quality falls outside `[minquality, maxquality]` and writes the modified beam array back to the `.merged` file.

## Practical Examples

### Reject ELAC beams with quality factor worse than 3

```bash
qualityFlag -minquality 1 -maxquality 3 elac_line01.merged elac_line02.merged
```
