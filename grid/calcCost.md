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