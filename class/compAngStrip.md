---
layout: default
title: compAngStrip
parent: Classification Tools
nav_order: 3
---
# compAngStrip

## Description
`compAngStrip` processes OMG-HDCS multibeam sonar data (e.g., EM1000 files) to estimate the angular response (AR) as it changes along a survey strip. It averages data over a user-specified number of swaths (a "stack"). The tool can extract angular response based on various intensity interpretations (linear or logarithmic), apply corrections (such as removing TVG or SRA effects), and handle different grazing angle definitions. Its primary output is a series of `JEM_Angular_Response` binary structures (written to an attribute file) containing the summed angular response, flags, and geographical coordinates, which can be further processed by tools like `classAngStrip`.

## Usage
```bash
compAngStrip [OPTIONS] -prefix <prefix> -suffix <suffix> <filebodyname(s)>
```
The tool constructs input merged file names as `<prefix>/<filebodyname>/<suffix>` (e.g., `/drives/wherever/survey_0123.merged`). It then expects associated sidescan data files (e.g., `survey_0123.ss_data`).

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-out_prefix <prefix>` | Specifies a prefix for the output Angular Response (AR) attribute files. | `../AR/` |
| `-attrib` | Enables the output of binary `JEM_Angular_Response` structures to an attribute file. If not specified, a simple rolling average ASCII file is generated. | |
| `-log` | Averages logarithmic intensities for backscatter; default is linear intensities. | |
| `-DN_Shift <value>` | Apply a Digital Number (DN) shift to backscatter values. | `40` |
| `-sonar_rel` | Use raw sonar-relative steering angles (not real grazing angles). | |
| `-draft <meters>` | Specifies the draft of the sonar. If not provided, it's derived from the `.param` file. | `1.0` |
| `-across_shift <meters>` | Specifies an across-track shift. If not provided, it's derived from the `.param` file. | `2.3` |
| `-ss` | Process sidescan data (`.ss_data` files) in addition to merged bathymetry data. | |
| `-stack <count>` | Number of pings (swaths) to average together for each angular response estimate. | `500` |
| `-use_deTVG` | Use de-TVG (Time Varied Gain) corrected sidescan data (`.ss_data_deTVG`). | |
| `-use_deSRA` | Use de-SRA (Slant Range Attenuation) corrected sidescan data (`.ss_data_deSRA`). | |
| `-use_deSRA_deTVG` | Use sidescan data corrected for both de-SRA and de-TVG effects (`.ss_data_deSRA_deTVG`). | |
| `-use_deVRA` | Use de-VRA (Vertical Range Attenuation) corrected sidescan data (`.ss_data_deVRA`). | |
| `-use_real_grazing` | Use dynamically calculated (real) grazing angles instead of nominal ones. | |
| `-read_GRA <ext>` | Reads grazing angle data from a file with the specified extension (`.Grazing` file) located in the merged directory. This implies `-use_real_grazing`. | `.grz` |
| `-attenremove` | Removes absorption correction. | |
| `-attengain <value>` | Applies an iterative attenuation gain correction. | |
| `-prefix <path>` | **Required.** Specifies the prefix path for input files. | `/drives/wherever/` |
| `-suffix <extension>` | **Required.** Specifies the file extension (suffix) for input merged files (e.g., `.merged`). | `.merged` |
| `<filebodyname(s)>` | **Required.** One or more base names of the survey lines (e.g., `survey_0123`). | `survey_0123 survey_0124` |
