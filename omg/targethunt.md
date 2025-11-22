---
layout: default
title: targethunt
parent: OMG Tools
nav_order: 70
---
# targethunt

## Description
`targethunt` is a specialized utility designed for detecting and marking targets within water column (WCL) multibeam sonar data. It analyzes WCL data, applies various thresholds and pattern matching techniques, and identifies potential targets based on user-defined criteria or a "target shape file".

The tool can output lists of detected targets and can optionally mark these targets directly within the water column data. It supports processing multiple merged files and offers extensive control over search parameters, output verbosity, and debugging information.

## Usage
```bash
targethunt -infile <inputfile(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `-infile <inputfile(s)>` | **Mandatory.** One or more paths to OMG-HDCS merged files containing water column data. |

### Help & Verbosity
| Option | Description |
|---|---|
| `-h` | Shows the help text. |
| `-v` | Activates verbose mode. |
| `-w` | Activates workflow mode (default is ON). |
| `-s` | Activates silent mode (no workflow, no verbose, no debug). |
| `-noinfo` | Does not print software information in the output. |

### Input/Output Files
| Option | Description |
|---|---|
| `-output` | Will print an output ASCII list of targets. |
| `-shapefile <file>` | Specifies an input ASCII file defining the target shape/pattern to search for. |
| `-print` | Prints the final list of targets to standard output. |
| `-printOnly` | Prints the existing target list (from a `.tgt` file) and exits, without processing WCL data. |

### Target Detection Parameters
| Option | Description |
|---|---|
| `-setThresh <val>` | Sets a static intensity threshold value. |
| `-dynThresh <multiplier>` | Sets a dynamic threshold multiplier (multiplied by the difference from the background). | `1` |
| `-dynThreshLayerX <multiplier>` | Sets a dynamic threshold depth layer multiplier (multiplied by pulse length). |
| `-amplOffset <val>` | Uses an `X_LogOffset` value during acquisition. | `0` |
| `-cubeSamples <val>` | Defines the size of the 3D cubic detection box in samples. |
| `-cubeBeams <val>` | Defines the size of the 3D cubic detection box in beams. |
| `-cubeSwaths <val>` | Defines the size of the 3D cubic detection box in swaths. |
| `-blockPlPat` | Blocks (ignores) time series pattern search. |
| `-blockAngPat` | Blocks (ignores) angular series pattern search. |
| `-blockSwPat` | Blocks (ignores) swath series pattern search. |
| `-minsamples <val>` / `-maxsamples <val>` | Restricts target search to a specific sample (range) number range. |
| `-minRange <val>` / `-maxRange <val>` | Restricts target search to a specific slant range (in meters) range. |
| `-minbeams <val>` / `-maxbeams <val>` | Restricts target search to a specific beam number range. |
| `-minswaths <val>` / `-maxswaths <val>` | Restricts target search to a specific swath number range. |
| `-sector <val>` | Restricts target search to a single specified sector. |
| `-useSectors <n> <s1> <s2> ... <sn>` | Restricts target search to `n` specified sectors (`s1` to `sn`). |
| `-slotSize <val>` | Defines the water column data slot size (number of swaths/pings to read at once). | `100` |
| `-force1Swath` | Forces single swath search technique (disables multiple swath search). |
| `-detect` | Performs only detection (LIMs - Local Intensity Maxima), skipping the full target hunt. |
| `-keepdetections` | Keeps all detections after target hunt (does not exclude them). |

### Area Filtering
| Option | Description |
|---|---|
| `-insideArea <minLat> <minLon> <maxLat> <maxLon>` | Searches only within a specified geographic area (Lat/Lon in `deg.min.sec` format). |
| `-insideAreaD <minLat> <minLon> <maxLat> <maxLon>` | Searches only within a specified geographic area (Lat/Lon in decimal degrees format). |
| `-boxArea <boxHeaderFile>` | (Currently commented out in code) Intended to search only inside an area defined by a `Box.header` file. |

### Dumping/Debugging Data
| Option | Description |
|---|---|
| `-dumpThresh` | Dumps all threshold values to a file. |
| `-dumpThreshCmp` | Dumps dynamic and static threshold values to a file. |
| `-dumpSamples` | Dumps sample values to a file. |
| `-dumpSw <val>` | Dumps water column swath `val` only. |
| `-dumpBm <val>` | Dumps beam `val` only. |
| `-dumpSmpl <val>` | Dumps sample (range) `val` only. |
| `-pause` | Pauses after processing each file. |

## Target Shape File Format
The `shapefile` option refers to a specific ASCII file format:
*   Line 1: A description of the file.
*   Line 2: Total number of targets.
*   Then, for each target:
    *   Line 0: Number of pieces (parts that make up the target).
    *   Line 1 to N: `sizex sizey sizez dist angle_across angle_forward dist_correctness angle_correctness` (details for each piece).
    *   Line N+1: `dist_to_seafloor` (optional, can be -1 for floating/unknown).

## How It Works
1.  **Initialization & Argument Parsing:** Sets up various control variables, debug flags, and parses command-line arguments to configure the target search.
2.  **File Iteration:** Loops through each input merged file:
    *   Constructs paths for associated water column (`.watercol`) and target (`.tgt`, `.tgtShape`) files.
    *   Reads the `OMG_HDCS_summary_header` from the merged file.
    *   **Area Filtering:** If `-insideArea` or `-boxArea` is used, it checks if the survey line falls within the specified geographic area. If not, the file is skipped.
    *   **SVP Loading (Implicit):** Loads `.param` files to get sonar configuration.
    *   **Target List Management:** Initializes an `OMG_Target_List` structure and attempts to read existing targets from the `.tgt` file.
    *   **Target Shape File:** If a `-shapefile` is provided, it's copied to the `.tgtShape` file associated with the current merged file.
3.  **WCL Data Processing in Slots:**
    *   Reads water column data from the `.watercol` file in "slots" (chunks of `slotsize` pings/swaths) to manage memory efficiently.
    *   For each slot:
        *   Reads `OMG_HDCS_profile_header` and `j_EM_watercolumn` data for all pings in the slot.
        *   Calculates geographic coordinates (longitude, latitude, depth) for the transducer position (geocenter) of each ping.
        *   **Target Hunting (`c_hunt_for_detections`, `c_mark_targets`, `c_hunt_for_targets`):** These (external) functions perform the core target detection logic:
            *   Analyze the WCL data for intensity anomalies exceeding thresholds.
            *   Apply pattern matching based on the target shape file or cubic box definitions.
            *   Mark detected targets.
    *   The loop rewinds the reading position to ensure overlapping slots for continuous detection.
4.  **Output & Storage:**
    *   Outputs the number of detections and targets found for each file.
    *   Writes the detected targets to the `.tgt` file.
    *   If `-output` is used, it also generates an ASCII `.tgt_ascii` file containing target details (latitude, longitude, label, timestamp, depth).
    *   If `-print` is used, it prints the target list to standard output.
5.  **Cleanup:** Frees allocated memory and closes files.

## External Functions/Structures (Assumed)
This tool relies heavily on external functions (e.g., `c_resetUserVars`, `c_findSwathType`, `c_hunt_for_detections`, `c_mark_targets`, `c_excludeDetections`, `c_hunt_for_targets`, `init_OMG_Target_List`, `read_OMG_Target_List`, `write_OMG_Target_List`, `print_OMG_Target_List`) and structures (e.g., `OMG_Target_List`, `OMG_Target_Shape`) defined in `targethunt.h`, `omg_target.h`, and `j_EM_watercol.h`, which are not fully provided in the snippet.
