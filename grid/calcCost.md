---
layout: default
title: calcCost
parent: Grid Tools
nav_order: 9
---
---
layout: default
title: calcCost
parent: Grid Tools
nav_order: 9
---
# calcCost

## Description
`calcCost` is a command-line utility for performing a detailed cost-benefit analysis and logistical planning for bathymetric surveys. It takes a Digital Terrain Model (DTM) as input and evaluates the optimal sonar system (from a predefined list or user-defined specifications) for mapping different depth zones. For each pixel in the DTM, it calculates the most cost-effective sonar, the associated survey area, estimated survey days, data volume, and total cost, including transit to/from home ports. It supports various currency conversions and outputs detailed reports on survey parameters and costs.

## Usage
```bash
calcCost [OPTIONS] -dtm <dtm_file.r4> -out <params_file>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-dtm <dtm_file.r4>` | **Required.** Specifies the path to the input JHC-format 32-bit floating-point DTM (`.r4`) file. | `bathymetry.r4` |
| `-out <params_file>` | **Required.** Specifies the path for the output file containing the calculated survey parameters and costs. | `survey_report.txt` |
| `-system <index> <descriptor_file>` | Defines a sonar system. `<index>` is a zero-based integer (0-9) to identify the sonar. `<descriptor_file>` is an ASCII file specifying the sonar's characteristics (draft, min/max depth, angular sector, max width, speed, efficiency, day rate, mission endurance, transit speed/dayrate). This option can be used multiple times to define different sonar systems. | `-system 0 sonar_a.txt` |
| `-ports <portsfile>` | Specifies an ASCII file containing a list of home port locations (name, latitude, longitude) from which transit costs will be calculated. | `home_ports.txt` |
| `-mindepth <value>` | Sets a minimum depth threshold (meters). Pixels shallower than this will not be surveyed. | `0.0` |
| `-maxdepth <value>` | Sets a maximum depth threshold (meters). Pixels deeper than this will not be surveyed. | `20000.0` |
| `-IRP` | Set output currency to Irish Pound. | |
| `-NZD` | Set output currency to New Zealand Dollar. | |
| `-CAN` | Set output currency to Canadian Dollar. | |
| `-USD` | Set output currency to US Dollar. | |
| `-UKP` | Set output currency to UK Pound. | |
| `-v` | Enable verbose output during processing. | |

## How It Works
1.  **Input Loading:** Reads the input DTM (`-dtm`) and optionally a `portsfile` (`-ports`). It also reads `descriptor_file`s for each sonar system defined by `-system`.
2.  **DTM Iteration:** For each pixel in the DTM that falls within the `mindepth` and `maxdepth` thresholds:
    *   It determines the water depth at that pixel.
    *   For each defined sonar system, it checks if that system is capable of surveying at the current water depth and calculates the effective swath width and survey efficiency.
    *   It then calculates the survey area, estimated survey days, and data volume.
    *   If `portsfile` is provided, it calculates transit costs to/from the nearest port.
    *   It identifies the most cost-effective sonar system for that pixel.
3.  **Cost Aggregation:** The tool aggregates survey parameters and costs for each sonar system and for the overall survey area.
4.  **Currency Conversion:** Converts costs to the specified output currency (IRP, NZD, CAN, USD, UKP).
5.  **Output Report:** Generates a detailed ASCII report (`-out`) containing:
    *   Summary of the survey area and total cost.
    *   Breakdown of costs by sonar system.
    *   Estimated survey days and data volume.
    *   Maps (if implemented) showing optimal sonar choice per pixel.

## Output Files
*   `<params_file>`: An ASCII file detailing the calculated survey parameters and costs.

## Dependencies
*   `array.h`: For `JHC_header` structure and DTM data handling.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection, used in distance calculations.

## Notes
This tool is highly configurable and can be used for detailed pre-survey planning and resource allocation. The accuracy of the cost estimates depends heavily on the quality of the sonar `descriptor_file`s and `portsfile` data. The various currency conversion options make it suitable for international use.
