---
layout: default
title: omg2hips
parent: James Muggah (james) Tools
nav_order: 7
tool_name: omg2hips
source_path: code/james/omg2hips.c
category: Sonar Format Converters (james)
input_formats: [".merged (OMG-HDCS v3/v4)"]
output_formats: [".merged (CARIS HIPS-compatible HDCS summary header)"]
related_tools: ["jview", "swathed"]
---

# omg2hips

## Description
`omg2hips` (written by James Muggah, March 2013) converts a modern OMG-HDCS `.merged` multibeam file into a CARIS HIPS-compatible HDCS file by rewriting the file summary header using the legacy HDCS layout (`OMG_HDCS_dump_summary_hips`) and copying all profile headers and beam arrays while explicitly flagging any zero-depth soundings (`observedDepth == 0`) with `beam.status = 22`.

As the OMG-HDCS summary header evolved to store additional sensor metadata and scaling fields, older CARIS HIPS HDCS importers expected the original summary header structure and treated unflagged zero-depth beams as valid `0.0 m` shoals. `omg2hips` bridges this compatibility gap.

---

## Usage

```bash
omg2hips [-v] -in <infile.merged> -out <outfile.merged>
```

### Example

```bash
omg2hips -v -in merged/JD150/0001_line.merged -out hips_export/0001_line.merged
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-in <infile>` | Input OMG-HDCS `.merged` multibeam file. | Required |
| `-out <outfile>` | Output CARIS HIPS-compatible HDCS file. | Required |
| `-v` | Enable verbose status messages during file opening and conversion. | Disabled |

---

## How It Works

1. **Summary Header Conversion:**
   Reads the input `OMG_HDCS_summary_header` using `OMG_HDCS_read_summary(mergedfile, &summary)` and writes the CARIS HIPS-compatible summary header to `-out` using `OMG_HDCS_dump_summary_hips(outfile, &summary)`.
2. **Profile & Beam Copying with Zero-Depth Rejection:**
   Loops through every ping (`ping_counter = 0 .. summary.numProfiles - 1`):
   * Reads the ping's `OMG_HDCS_profile_header` (`OMG_HDCS_read_profile`) and writes it unchanged to `outfile` (`OMG_HDCS_write_profile`).
   * Reads the raw beam array (`OMG_HDCS_get_raw_beams`, up to 1,440 beams per ping).
   * Inspects every beam $j \in [0, \text{num\_beams}-1]$: if `!beams[j].observedDepth || beams[j].observedDepth == 0.0`, sets `beams[j].status = 22` so CARIS HIPS recognizes the beam as rejected.
   * Writes the updated beam array to `outfile` via `OMG_HDCS_put_raw_beams`.
