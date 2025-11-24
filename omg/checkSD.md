---
layout: default
title: checkSD
parent: OMG Tools
nav_order: 80
---
# checkSD

## Description
`checkSD` is a diagnostic utility for analyzing the statistical deviation of multibeam soundings from a reference Digital Terrain Model (DTM). It quantifies the vertical difference (bias and standard deviation) of observed depths against the DTM, binned by beam angle (incidence angle). This tool is crucial for assessing data quality, identifying systematic biases (e.g., roll errors), and validating the accuracy of the DTM or the sounding data itself.

The tool works in two passes: first, to calculate the average bias per beam angle, and second, to calculate the standard deviation around that bias.

## Usage
```bash
checkSD <r4prefix> <soundingfiles(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<r4prefix>` | **Required.** The prefix of the `.r4` (float grid) DTM file against which soundings will be compared (e.g., `survey.dtm`). |
| `<soundingfiles(s)>` | **Required.** One or more paths to OMG-HDCS merged files (or ASCII sounding lists if `-ascii` is used) containing the soundings to be checked. |

### Processing Control
| Option | Description | Default |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-ascii` | Indicates that the sounding input files are ASCII lists (lat, lon, depth, across). | |
| `-first <ping_num>` | Process soundings only from this ping number (inclusive). Cannot be used with multiple input files. | All pings |
| `-last <ping_num>` | Process soundings only up to this ping number (inclusive). Cannot be used with multiple input files. | All pings |
| `-just_pulse_microsec <val>` | Only process pings with a `tx_pulse_len` matching this microsecond value. | |

### Data Filtering
| Option | Description | Default |
|---|---|---|
| `-useallZ` | Use all soundings, regardless of their status flags (overrides `status != 22` and `status != 1`). | |
| `-valid_depths <deep_m> <shal_m>` | Only consider soundings within this depth range (deep to shallow, in meters). | `-12000.0` to `12000.0` |
| `-MAX_nonflyer_percent <val>` | Sets a percentage threshold (e.g., `3.0` for 3%) for rejecting "wild flyers" during standard deviation calculation. Soundings deviating by more than `val`% from the reference ray are discarded from the sigma calculation. | `100.0` |

### Corrections & Adjustments
| Option | Description | Default |
|---|---|
| `-draft <val>` | Specifies the draft (in meters) to subtract from observed depths. **Mandatory**. | `0.0` |
| `-pixshift <X> <Y>` | Apply a pixel shift (X, Y) to the projected coordinates of the soundings. | `0.0` |
| `-gyro_bias <val>` | Apply a constant gyro bias (in degrees) to the vessel heading. | `0.0` |
| `-add_dyn_draft_shift` | Add `profile.longperiod_heaveCorrection` to the observed depth before comparison. | |
| `-remove_average_bias` | Remove the calculated average bias from the percentage difference calculation (for the second pass). | |

### Output Options
| Option | Description | Default |
|---|---|---|
| `-beams <first> <last>` | Only process beams within this beam number range (inclusive). | All beams |
| `-lessone` | (Not clearly documented in source, likely related to count thresholds). | `0` |
| `-smth` | Apply smoothing to the calculated percentage differences and standard deviations. | |
| `-nums` | Output absolute differences (`sigma`) and counts. | |
| `-other` | Output absolute differences (`sig2`). | |

## How It Works
1.  **Initialization:** Initializes arrays to store `ray` (mean percentage difference), `sigma` (standard deviation), `sig2` (absolute standard deviation), `perc_diff`, `abso_diff`, and `count` for each angle bin.
2.  **DTM Loading:** Reads the input `.r4` DTM file and its header, extracting projection information and the gridded depth data.
3.  **First Pass - Calculate Mean Bias:**
    *   Iterates through each sounding file and each profile/sounding within:
        *   Reads profile data (or ASCII data).
        *   If not ASCII, retrieves raw beams. If ASCII, creates a dummy beam.
        *   Applies `gyro_bias` to `profile.vesselHeading` if specified.
        *   Locates each beam geographically (lat/lon).
        *   Projects the beam's lat/lon onto the DTM grid (`x`, `y`) and applies `pixshift_X`, `pixshift_Y`.
        *   If the beam is within the DTM grid and `final_data[x,y]` is valid:
            *   Calculates `real_depth` from the DTM.
            *   Calculates `depth` from the beam (`observedDepth`), applying `tide` and `add_dyn_draft_shift`.
            *   Calculates the `angle` (incidence angle) from `acrossTrack` and `depth`.
            *   Calculates the percentage difference `(depth - real_depth) / real_depth`.
            *   Accumulates this percentage difference in `perc_diff[(int)angle + 90]` and increments `count[(int)angle + 90]`.
    *   After processing all soundings, it calculates the `ray[i]` (mean percentage difference for each angle bin).
    *   If `-remove_average_bias` is specified, it calculates an overall `av_bias` and removes it from `ray[i]` for the second pass.
4.  **Second Pass - Calculate Standard Deviation:**
    *   Resets `sigma`, `sig2`, `bias_diff`, `abso_diff`, and `count` arrays.
    *   Repeats the iteration through sounding files and soundings, performing similar calculations as in the first pass.
    *   This time, it calculates `test_bias_diff` (deviation from the mean `ray[i]`).
    *   If `test_bias_diff` is within `MAX_nonflyer_percent`, it accumulates `bias_diff` (for standard deviation around the mean bias) and `abso_diff` (for absolute standard deviation) and increments `count`.
    *   It calculates `sigma[i]` (standard deviation) and `sig2[i]` (absolute standard deviation) for each angle bin.
5.  **Output to `deviation.list`:**
    *   Opens a file named `deviation.list`.
    *   For each angle bin `i` where `count[i]` is sufficient, it writes:
        *   Beam angle (`i - 90`)
        *   Mean percentage difference (`100.0 * (ray[i] - av_bias)`)
        *   Standard deviation (`100.0 * sigma[i]`)
        *   Absolute standard deviation (`100.0 * sig2[i]`)
6.  **Cleanup:** Closes files and frees memory.

## Output Files
*   `deviation.list`: An ASCII file containing mean percentage difference, standard deviation, and absolute standard deviation per beam angle.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `array.h`: For `JHC_header` structure and DTM data handling.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.

## Notes
This tool provides a quantitative measure of multibeam data quality against a DTM, enabling the detection of systematic errors and biases. The two-pass approach is robust in distinguishing overall bias from random scatter. The output format is suitable for plotting beam-angle-dependent accuracy characteristics.