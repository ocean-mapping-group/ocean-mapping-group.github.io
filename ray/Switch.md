---
layout: default
title: Switch
parent: Ray Tools
nav_order: 172
---
# Switch

## Description
`Switch.c` is a utility designed to convert a Time-Angle (TA) lookup table (raster) into a Depth-Across (DA) lookup table. This conversion is crucial in ray tracing applications, where initial ray tracing results are often in TA space (time of flight vs. outgoing beam angle), but practical applications require results in DA space (across-track distance vs. depth).

The tool takes pre-computed lookup tables for beam angle (`.beam_angle`), time of flight (`.time_lag`), and an angle-time depth lookup table (e.g., from `Ray.c`), and uses them to interpolate depth values into a new grid representing across-track distance and depth.

## Usage
```bash
Switch -locate <ATFilename> -pro <svp_handle>
```

## Arguments

| Option | Description |
|---|---|
| `-locate <ATFilename>` | **Required.** Path to the Angle-Time (AT) depth lookup table file (e.g., from `Ray.c`). This file provides the depth for given angle and time. |
| `-pro <svp_handle>` | **Required.** Base name for the velocity profile. The tool expects:
    *   `<svp_handle>.beam_angle`: Beam angle lookup table.
    *   `<svp_handle>.time_lag`: Time of flight lookup table.
    *   It will create `<svp_handle>.Switched` as output. |
| `-v` | Enable verbose output. |

## How It Works

1.  **Initialization:** Parses command-line arguments to get input/output filenames.
2.  **File Opening and Header Reading:**
    *   Opens the Angle-Time depth lookup table file (`ATFilename`) and reads its `JHC_header` (`AThead`).
    *   Opens the beam angle (`.beam_angle`) and time of flight (`.time_lag`) lookup table files and reads their respective `JHC_header`s (`Ahead`, `Thead`).
    *   Creates the output file (`.Switched`) and copies `Thead` to `Ohead` (output header).
3.  **Memory Allocation:** Allocates memory for `AngTim` (Angle-Time depth data), `Ang` (beam angle data), `Tim` (time of flight data), and `Out` (output Depth-Across data).
4.  **Data Reading:** Reads the contents of `ATFilename`, `.beam_angle`, and `.time_lag` into `AngTim`, `Ang`, and `Tim` arrays, respectively.
5.  **Conversion Loop:** Iterates through each cell (`i`, `j`) of the output grid (Depth-Across space, dimensions from `Ohead.dx`, `Ohead.dy`):
    *   Retrieves `beam_angle` from `Ang[j * Ahead.dx + i]` and `time_of_flight` from `Tim[j * Thead.dx + i]`.
    *   If both are valid, it uses `interp_JHCarray_value()` (an external function for 2D array interpolation) to find the corresponding `depth` value from the `AngTim` lookup table, given the `beam_angle` and `time_of_flight`.
    *   Stores this `depth` value in the `Out` array at `Out[j * Ohead.dx + i]`.
    *   If either `beam_angle` or `time_of_flight` is invalid, the output `depth` is set to 0.0.
6.  **Output:** Writes the `Out` array to the `.Switched` file.
7.  **Cleanup:** Frees allocated memory and closes all files.

## Output File Format (JHC `.r4` Array Format)
*   `<svp_handle>.Switched`: A 2D floating-point array (raster) representing depth values in Depth-Across space. Each cell contains the depth corresponding to an across-track distance and depth (derived from time of flight and beam angle).
The output file contains a `JHC_header` followed by the raw float data.

## Dependencies

*   `interp_JHCarray_value()`: An external function (presumably from `array.h`) used for 2D interpolation of JHC array data.
```
```
---
layout: default
title: Switch
parent: Ray Tools
nav_order: 172
---
# Switch

## Description
`Switch.c` is a utility designed to convert a Time-Angle (TA) lookup table (raster) into a Depth-Across (DA) lookup table. This conversion is crucial in ray tracing applications, where initial ray tracing results are often in TA space (time of flight vs. outgoing beam angle), but practical applications require results in DA space (across-track distance vs. depth).

The tool takes pre-computed lookup tables for beam angle (`.beam_angle`), time of flight (`.time_lag`), and an angle-time depth lookup table (e.g., from `Ray.c`), and uses them to interpolate depth values into a new grid representing across-track distance and depth.

## Usage
```bash
Switch -locate <ATFilename> -pro <svp_handle>
```

## Arguments

| Option | Description |
|---|---|
| `-locate <ATFilename>` | **Required.** Path to the Angle-Time (AT) depth lookup table file (e.g., from `Ray.c`). This file provides the depth for given angle and time. |
| `-pro <svp_handle>` | **Required.** Base name for the velocity profile. The tool expects:
    *   `<svp_handle>.beam_angle`: Beam angle lookup table.
    *   `<svp_handle>.time_lag`: Time of flight lookup table.
    *   It will create `<svp_handle>.Switched` as output. |
| `-v` | Enable verbose output. |

## How It Works

1.  **Initialization:** Parses command-line arguments to get input/output filenames.
2.  **File Opening and Header Reading:**
    *   Opens the Angle-Time depth lookup table file (`ATFilename`) and reads its `JHC_header` (`AThead`).
    *   Opens the beam angle (`.beam_angle`) and time of flight (`.time_lag`) lookup table files and reads their respective `JHC_header`s (`Ahead`, `Thead`).
    *   Creates the output file (`.Switched`) and copies `Thead` to `Ohead` (output header).
3.  **Memory Allocation:** Allocates memory for `AngTim` (Angle-Time depth data), `Ang` (beam angle data), `Tim` (time of flight data), and `Out` (output Depth-Across data).
4.  **Data Reading:** Reads the contents of `ATFilename`, `.beam_angle`, and `.time_lag` into `AngTim`, `Ang`, and `Tim` arrays, respectively.
5.  **Conversion Loop:** Iterates through each cell (`i`, `j`) of the output grid (Depth-Across space, dimensions from `Ohead.dx`, `Ohead.dy`):
    *   Retrieves `beam_angle` from `Ang[j * Ahead.dx + i]` and `time_of_flight` from `Tim[j * Thead.dx + i]`.
    *   If both are valid, it uses `interp_JHCarray_value()` (an external function for 2D array interpolation) to find the corresponding `depth` value from the `AngTim` lookup table, given the `beam_angle` and `time_of_flight`.
    *   Stores this `depth` value in the `Out` array at `Out[j * Ohead.dx + i]`.
    *   If either `beam_angle` or `time_of_flight` is invalid, the output `depth` is set to 0.0.
6.  **Output:** Writes the `Out` array to the `.Switched` file.
7.  **Cleanup:** Frees allocated memory and closes all files.

## Output File Format (JHC `.r4` Array Format)
*   `<svp_handle>.Switched`: A 2D floating-point array (raster) representing depth values in Depth-Across space. Each cell contains the depth corresponding to an across-track distance and depth (derived from time of flight and beam angle).
The output file contains a `JHC_header` followed by the raw float data.

## Dependencies

*   `interp_JHCarray_value()`: An external function (presumably from `array.h`) used for 2D interpolation of JHC array data.
```
---
layout: default
title: Switch
parent: Ray Tools
nav_order: 172
---
# Switch

## Description
`Switch.c` is a utility designed to convert a Time-Angle (TA) lookup table (raster) into a Depth-Across (DA) lookup table. This conversion is crucial in ray tracing applications, where initial ray tracing results are often in TA space (time of flight vs. outgoing beam angle), but practical applications require results in DA space (across-track distance vs. depth).

The tool takes pre-computed lookup tables for beam angle (`.beam_angle`), time of flight (`.time_lag`), and an angle-time depth lookup table (e.g., from `Ray.c`), and uses them to interpolate depth values into a new grid representing across-track distance and depth.

## Usage
```bash
Switch -locate <ATFilename> -pro <svp_handle>
```

## Arguments

| Option | Description |
|---|---|
| `-locate <ATFilename>` | **Required.** Path to the Angle-Time (AT) depth lookup table file (e.g., from `Ray.c`). This file provides the depth for given angle and time. |
| `-pro <svp_handle>` | **Required.** Base name for the velocity profile. The tool expects:
    *   `<svp_handle>.beam_angle`: Beam angle lookup table.
    *   `<svp_handle>.time_lag`: Time of flight lookup table.
    *   It will create `<svp_handle>.Switched` as output. |
| `-v` | Enable verbose output. |

## How It Works

1.  **Initialization:** Parses command-line arguments to get input/output filenames.
2.  **File Opening and Header Reading:**
    *   Opens the Angle-Time depth lookup table file (`ATFilename`) and reads its `JHC_header` (`AThead`).
    *   Opens the beam angle (`.beam_angle`) and time of flight (`.time_lag`) lookup table files and reads their respective `JHC_header`s (`Ahead`, `Thead`).
    *   Creates the output file (`.Switched`) and copies `Thead` to `Ohead` (output header).
3.  **Memory Allocation:** Allocates memory for `AngTim` (Angle-Time depth data), `Ang` (beam angle data), `Tim` (time of flight data), and `Out` (output Depth-Across data).
4.  **Data Reading:** Reads the contents of `ATFilename`, `.beam_angle`, and `.time_lag` into `AngTim`, `Ang`, and `Tim` arrays, respectively.
5.  **Conversion Loop:** Iterates through each cell (`i`, `j`) of the output grid (Depth-Across space, dimensions from `Ohead.dx`, `Ohead.dy`):
    *   Retrieves `beam_angle` from `Ang[j * Ahead.dx + i]` and `time_of_flight` from `Tim[j * Thead.dx + i]`.
    *   If both are valid, it uses `interp_JHCarray_value()` (an external function for 2D array interpolation) to find the corresponding `depth` value from the `AngTim` lookup table, given the `beam_angle` and `time_of_flight`.
    *   Stores this `depth` value in the `Out` array at `Out[j * Ohead.dx + i]`.
    *   If either `beam_angle` or `time_of_flight` is invalid, the output `depth` is set to 0.0.
6.  **Output:** Writes the `Out` array to the `.Switched` file.
7.  **Cleanup:** Frees allocated memory and closes all files.

## Output File Format (JHC `.r4` Array Format)
*   `<svp_handle>.Switched`: A 2D floating-point array (raster) representing depth values in Depth-Across space. Each cell contains the depth corresponding to an across-track distance and depth (derived from time of flight and beam angle).
The output file contains a `JHC_header` followed by the raw float data.

## Dependencies

*   `interp_JHCarray_value()`: An external function (presumably from `array.h`) used for 2D interpolation of JHC array data.
```
```