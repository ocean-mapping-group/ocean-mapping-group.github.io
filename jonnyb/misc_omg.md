---
layout: default
title: misc_omg
parent: Jonathan Beaudoin — SVP, Refraction & Snippets (jonnyb)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 9
tool_name: misc_omg
source_path: code/jonnyb/misc_omg.c
category: Developer Templates & Utilities (jonnyb)
input_formats:
- .merged (OMG-HDCS)
output_formats:
- stdout (ASCII depth, across-track, along-track)
related_tools:
- misc
- dumpSoundings
- jview
---

# misc_omg

## Description
`misc_omg` (`code/jonnyb/misc_omg.c`) is Jonathan Beaudoin's reference C template for reading and iterating through an OMG-HDCS `.merged` multibeam file using the rationalized profile and beam structures (`OMG_rational_profile` and `OMG_rational_beam` from `OMG_HDCS_jversion.h`).

When executed on a `.merged` file, `misc_omg` reads the `OMG_HDCS_summary_header`, allocates an array of `summary.numDepths` beam structures, loops over all `summary.numProfiles` pings, and prints each beam's integer `depth`, `across` (across-track offset), and `along` (along-track offset) to `stdout`.

---

## Usage

```bash
misc_omg -in <filename.merged>
```

### Example

```bash
misc_omg -in merged/JD120/0001_line.merged | head -n 20
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-in <filename.merged>` | Input OMG-HDCS `.merged` multibeam file (opened in `"rb+"` mode). | Required |

---

## How It Works

1. **Summary Header Read:**
   Opens `<filename.merged>` in `"rb+"` mode and calls `OMG_HDCS_read_summary(infile, &summary)` to determine `summary.numProfiles` (total pings) and `summary.numDepths` (maximum beams per ping).
2. **Dynamic Beam Buffer Allocation:**
   Allocates `beams = calloc(summary.numDepths, sizeof(OMG_rational_beam))`.
3. **Ping & Beam Iteration:**
   For every ping $i \in [0, \text{numProfiles}-1]$:
   * Calls `OMG_get_rational_profile(infile, i, &profile)` to read the ping header.
   * Calls `OMG_get_rational_beams(infile, i, &num_beams, beams)` to unpack the beam array.
   * Iterates over $j \in [0, \text{numDepths}-1]$ and prints:

     ```text
     <beams[j].depth> <beams[j].across> <beams[j].along>
     ```
4. **Cleanup:**
   Frees `beams` and closes `infile`.
