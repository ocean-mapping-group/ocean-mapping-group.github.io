---
layout: default
title: getHeading
parent: James Muggah — Global Mapper Tiles & Utils (james)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 3
tool_name: getHeading
source_path: code/james/getHeading.c
category: Hydrographic & Line Metadata Utilities (james)
input_formats:
- .merged
- xyzlist (ASCII file list)
output_formats:
- '.txt (ASCII 2-column table: <filename> <heading_deg>)'
related_tools:
- stripNav
- checkBounds
- merged2orientation
---

# getHeading

## Description
`getHeading` computes the circular vector-averaged vessel heading (in degrees clockwise from North, $[0^\circ, 360^\circ)$) across all pings (or every $N$-th ping via `-skip`) for up to 5,000 OMG-HDCS `.merged` files. It outputs a two-column ASCII file containing each `.merged` file path and its mean line heading (`%s %6.2f`).

Because arithmetic averaging of headings fails near the $0^\circ / 360^\circ$ wrap-around boundary, `getHeading` accumulates the mean sine and cosine components of `profile.vesselHeading` (stored in $10^{-7}$ radians in the `OMG_HDCS_profile_header`) and recovers the mean azimuth via `atan2`.

---

## Usage

```bash
getHeading -out <output.txt> [-skip <N>] [-xyzlist <listfile>] [filename(s).merged ...]
```

### Examples

**1. Compute average heading for a directory of `.merged` lines (sampling every 10th ping):**

```bash
getHeading -out line_headings.txt -skip 10 merged/JD180/*.merged
```

**2. Compute average headings for an `-xyzlist` of `.merged` files:**

```bash
getHeading -out line_headings.txt -xyzlist survey_lines.list
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-out <filename>` | Output ASCII file where `<merged_filename> <mean_heading_deg>` is written (one line per file). | Required |
| `-skip <N>` | Stride through profile headers by reading every `N`-th ping (`for (i = 0; i < summary.numProfiles; i += skip)`). Speeds up processing on large files. | `1` (every ping) |
| `-xyzlist <listfile>` | Read input `.merged` file paths from one or more ASCII list files (via `load_inputfiles_from_list`, up to 5,000 files). | Disabled |
| `<filename(s).merged>` | One or more `.merged` files specified directly on the command line. | Required (unless `-xyzlist` used) |

---

## How It Works

For each input `.merged` file:
1. Reads `OMG_HDCS_summary_header` to obtain `summary.numProfiles`.
2. Iterates over pings $i = 0, \text{skip}, 2\cdot\text{skip}, \dots < \text{numProfiles}$ and reads each `OMG_HDCS_profile_header`.
3. Converts `profile.vesselHeading` ($10^{-7}$ radians) to radians and accumulates unit-vector components:
   $$S = \sum \sin\left(\frac{\text{vesselHeading}}{10^7}\right), \qquad C = \sum \cos\left(\frac{\text{vesselHeading}}{10^7}\right)$$
4. Computes the circular mean heading in degrees:
   $$\bar{\psi} = \text{atan2}\left(\frac{S}{N}, \frac{C}{N}\right) \times \frac{180}{\pi}$$
   If $\bar{\psi} < 0$, adds $360^\circ$ so the output lies in $[0.00^\circ, 360.00^\circ)$.
5. Writes `<inname> <heading>` (`%s %6.2f \n`) to `-out`.
