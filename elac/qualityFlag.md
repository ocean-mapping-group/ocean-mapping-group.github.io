---
layout: default
title: qualityFlag
parent: ELAC Tools
nav_order: 1
---
# qualityFlag

## Description
`qualityFlag` is a command-line utility designed to flag (or unflag) hydrographic data beams in OMG-HDCS merged files based on their quality factor. It specifically targets ELAC multibeam data, using the ELAC-supplied beam quality (a crude signal-to-noise ratio), or can handle SeaBat 8101 data by interpreting specific bit flags for brightness, collinearity, and amplitude/phase detection. Beams whose quality falls outside a specified minimum and maximum range are marked as invalid.

## Usage
```bash
qualityFlag [OPTIONS] <merged_file(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-minquality <value>` | Specifies the minimum acceptable quality factor. Beams with a quality factor below this value will be flagged as invalid. | `0` |
| `-maxquality <value>` | Specifies the maximum acceptable quality factor. Beams with a quality factor above this value will be flagged as invalid. | `2` |
| `<merged_file(s)>` | **Required.** One or more input OMG-HDCS merged files (e.g., `.merged`) to be processed. The tool directly modifies the `status` and `Q_factor` fields of the beams within these files. | `survey_001.merged survey_002.merged` |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file.
2.  **Summary Header Reading:** Reads the summary header to determine the sonar type.
3.  **Beam Quality Check:** For each beam in each ping:
    *   It reads the beam's `Q_factor`.
    *   If the sonar is an ELAC system, it uses `Q_factor` directly.
    *   If the sonar is a SeaBat 8101, it interprets specific bit flags within `Q_factor` for brightness, collinearity, and detection type.
    *   It then compares this quality value against the user-defined `minquality` and `maxquality` thresholds.
4.  **Flagging:** If the beam's quality falls outside the acceptable range, its `status` field is set to `22` (typically indicating a rejected sounding).
5.  **In-Place Update:** The modified beam records (with updated `status` flags) are written back to the merged file.

## Output Files
The input merged files are modified in-place.

## Notes
This tool is effective for initial filtering of multibeam data based on quality indicators provided by the sonar system. It's crucial to understand the meaning of the `Q_factor` for specific sonar types to set appropriate thresholds.