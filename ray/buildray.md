---
layout: default
title: buildray
parent: Ray Tools
nav_order: 163
---
# buildray

## Description
`buildray` is a ray tracing utility designed to generate lookup arrays (rasters) of various parameters (grazing angle, beam angle, and one-way travel time) based on a given sound velocity profile (SVP). It uses Snell's Law to trace acoustic rays through a layered water column, which is assumed to have constant velocity within each layer.

The generated lookup arrays are useful for correcting sonar measurements, image rectification (e.g., for side-scan sonar), and other applications requiring knowledge of sound propagation through water.

## Usage
```bash
buildray -pro <svp_handle> [-range <val>] [-depth <val>] [-spacing <step> <start> <finish>] [-layerthick <val>] [-rangeres <val>] [-fishdep <val>] [-graze] [-beam] [-time] [-simradsvp] [-NEWsvp] [-verbose]
```

## Arguments

| Option | Description |
|---|---|
| `-pro <svp_handle>` | **Required.** Base name for the sound velocity profile file and output lookup arrays.
    *   Input: `<svp_handle>.profile` (default), `<svp_handle>.svp` (`-simradsvp`), or `<svp_handle>.RAWPROF` (`-NEWsvp`).
    *   Output: `<svp_handle>.grazing_angle` (`-graze`), `<svp_handle>.beam_angle` (`-beam`), `<svp_handle>.time_lag` (`-time`). |
| `-range <val>` | Maximum horizontal range for the lookup array (meters). | `22500.0` |
| `-depth <val>` | Maximum vertical depth for the lookup array (meters). | `5000.0` |
| `-spacing <step> <start> <finish>` | Defines the angular spacing for ray tracing:
    *   `step`: Angular step (degrees).
    *   `start`: Starting beam angle (degrees).
    *   `finish`: Finishing beam angle (degrees). | `0.01 0 89` |
| `-layerthick <val>` | Thickness of the constant velocity layers in the water column model (meters). | `20.0` |
| `-rangeres <val>` | Horizontal range resolution for the lookup array (meters). | `20.0` |
| `-fishdep <val>` | Depth of the transducer/fish (meters). | `50.0` |
| `-graze` | Generate a grazing angle lookup array. |
| `-beam` | Generate a beam angle lookup array. |
| `-time` | Generate a one-way travel time lookup array. |
| `-simradsvp` | Input SVP file is in Simrad SVP format (`.svp`). |
| `-NEWsvp` | Input SVP file is in a "NEW" raw format (`.RAWPROF`). |
| `-verbose` | Enable verbose output. |

## How It Works

1.  **Initialization:** Parses command-line arguments, setting various ray tracing and output parameters.
2.  **SVP Reading:**
    *   Opens the input SVP file specified by `-pro` and the format flags (`-simradsvp`, `-NEWsvp`).
    *   Calls one of the `read_in_*()` functions (`read_in_raw`, `read_in_NEW_raw`, `read_in_svp`) to load the raw sound velocity profile data (`rawvel`, `rawdep`).
    *   If `std16_flag` or `NEW_flag` is set, `make_equisvp()` is called to interpolate the raw SVP into an equi-spaced layered model (`veldep`).
3.  **Lookup Array Allocation:**
    *   Calculates `xlen` (number of range bins) and `ylen` (number of depth bins) for the output lookup arrays based on `maxrange`, `maxdepth`, `rangeres`, and `layerthick`.
    *   Allocates memory for `glookupbuf`, `blookupbuf`, and `tlookupbuf` (output arrays for grazing angle, beam angle, and travel time, respectively) if their corresponding flags (`-graze`, `-beam`, `-time`) are set.
4.  **Ray Tracing Loop:**
    *   Iterates through each `outangle` from `startangle` to `finishangle` with `anglestep`.
    *   For each `outangle`:
        *   Initializes `posx`, `posz` (current horizontal/vertical position), `ttime` (current travel time), and `rangle` (current ray angle).
        *   **Layer-by-Layer Propagation:** Iterates through the water column layers (from `depzone` to `ylen - 1`):
            *   Updates `posx`, `posz`, and `ttime` based on the ray's path through the current layer's velocity.
            *   Calculates `xoffset` and `yoffset` (indices into the lookup arrays).
            *   If `xoffset` and `yoffset` are within bounds, it populates the corresponding lookup array cells with `rangle`, `outangle`, and `ttime`.
            *   Applies Snell's Law to calculate the new `rangle` for the next layer.
            *   Handles conditions where the ray goes beyond `maxrange`, `maxdepth`, or goes horizontal (total internal reflection).
5.  **Output to JHC Header Files:**
    *   Initializes a `JHC_header` structure with plot dimensions, ranges, and metadata.
    *   Opens output files (`.grazing_angle`, `.beam_angle`, `.time_lag`) if their corresponding flags are set.
    *   Writes the `JHC_header` to each output file.
    *   Writes the populated lookup arrays (`glookupbuf`, `blookupbuf`, `tlookupbuf`) to their respective files.
6.  **Cleanup:** Frees allocated memory and closes all open files.

## Output Files (JHC `.r4` Array Format)
*   `<svp_handle>.grazing_angle`: A 2D floating-point array (raster) where each cell contains the grazing angle.
*   `<svp_handle>.beam_angle`: A 2D floating-point array (raster) where each cell contains the outgoing beam angle.
*   `<svp_handle>.time_lag`: A 2D floating-point array (raster) where each cell contains the one-way travel time.
Each output file contains a `JHC_header` followed by the raw float data.

## Helper Functions

*   `read_in_raw()`: Reads SVP data in a raw format (depth, velocity pairs).
*   `read_in_NEW_raw()`: Reads SVP data in another "NEW" raw format.
*   `make_equisvp()`: Interpolates raw SVP data to create an equi-spaced layered velocity profile (`veldep`).
*   `read_in_svp()`: Reads SVP data from a custom `.profile` format.
```
```
---
layout: default
title: buildray
parent: Ray Tools
nav_order: 163
---
# buildray

## Description
`buildray` is a ray tracing utility designed to generate lookup arrays (rasters) of various parameters (grazing angle, beam angle, and one-way travel time) based on a given sound velocity profile (SVP). It uses Snell's Law to trace acoustic rays through a layered water column, which is assumed to have constant velocity within each layer.

The generated lookup arrays are useful for correcting sonar measurements, image rectification (e.g., for side-scan sonar), and other applications requiring knowledge of sound propagation through water.

## Usage
```bash
buildray -pro <svp_handle> [-range <val>] [-depth <val>] [-spacing <step> <start> <finish>] [-layerthick <val>] [-rangeres <val>] [-fishdep <val>] [-graze] [-beam] [-time] [-simradsvp] [-NEWsvp] [-verbose]
```

## Arguments

| Option | Description |
|---|---|
| `-pro <svp_handle>` | **Required.** Base name for the sound velocity profile file and output lookup arrays.
    *   Input: `<svp_handle>.profile` (default), `<svp_handle>.svp` (`-simradsvp`), or `<svp_handle>.RAWPROF` (`-NEWsvp`).
    *   Output: `<svp_handle>.grazing_angle` (`-graze`), `<svp_handle>.beam_angle` (`-beam`), `<svp_handle>.time_lag` (`-time`). |
| `-range <val>` | Maximum horizontal range for the lookup array (meters). | `22500.0` |
| `-depth <val>` | Maximum vertical depth for the lookup array (meters). | `5000.0` |
| `-spacing <step> <start> <finish>` | Defines the angular spacing for ray tracing:
    *   `step`: Angular step (degrees).
    *   `start`: Starting beam angle (degrees).
    *   `finish`: Finishing beam angle (degrees). | `0.01 0 89` |
| `-layerthick <val>` | Thickness of the constant velocity layers in the water column model (meters). | `20.0` |
| `-rangeres <val>` | Horizontal range resolution for the lookup array (meters). | `20.0` |
| `-fishdep <val>` | Depth of the transducer/fish (meters). | `50.0` |
| `-graze` | Generate a grazing angle lookup array. |
| `-beam` | Generate a beam angle lookup array. |
| `-time` | Generate a one-way travel time lookup array. |
| `-simradsvp` | Input SVP file is in Simrad SVP format (`.svp`). |
| `-NEWsvp` | Input SVP file is in a "NEW" raw format (`.RAWPROF`). |
| `-verbose` | Enable verbose output. |

## How It Works

1.  **Initialization:** Parses command-line arguments, setting various ray tracing and output parameters.
2.  **SVP Reading:**
    *   Opens the input SVP file specified by `-pro` and the format flags (`-simradsvp`, `-NEWsvp`).
    *   Calls one of the `read_in_*()` functions (`read_in_raw`, `read_in_NEW_raw`, `read_in_svp`) to load the raw sound velocity profile data (`rawvel`, `rawdep`).
    *   If `std16_flag` or `NEW_flag` is set, `make_equisvp()` is called to interpolate the raw SVP into an equi-spaced layered model (`veldep`).
3.  **Lookup Array Allocation:**
    *   Calculates `xlen` (number of range bins) and `ylen` (number of depth bins) for the output lookup arrays based on `maxrange`, `maxdepth`, `rangeres`, and `layerthick`.
    *   Allocates memory for `glookupbuf`, `blookupbuf`, and `tlookupbuf` (output arrays for grazing angle, beam angle, and travel time, respectively) if their corresponding flags (`-graze`, `-beam`, `-time`) are set.
4.  **Ray Tracing Loop:**
    *   Iterates through each `outangle` from `startangle` to `finishangle` with `anglestep`.
    *   For each `outangle`:
        *   Initializes `posx`, `posz` (current horizontal/vertical position), `ttime` (current travel time), and `rangle` (current ray angle).
        *   **Layer-by-Layer Propagation:** Iterates through the water column layers (from `depzone` to `ylen - 1`):
            *   Updates `posx`, `posz`, and `ttime` based on the ray's path through the current layer's velocity.
            *   Calculates `xoffset` and `yoffset` (indices into the lookup arrays).
            *   If `xoffset` and `yoffset` are within bounds, it populates the corresponding lookup array cells with `rangle`, `outangle`, and `ttime`.
            *   Applies Snell's Law to calculate the new `rangle` for the next layer.
            *   Handles conditions where the ray goes beyond `maxrange`, `maxdepth`, or goes horizontal (total internal reflection).
5.  **Output to JHC Header Files:**
    *   Initializes a `JHC_header` structure with plot dimensions, ranges, and metadata.
    *   Opens output files (`.grazing_angle`, `.beam_angle`, `.time_lag`) if their corresponding flags are set.
    *   Writes the `JHC_header` to each output file.
    *   Writes the populated lookup arrays (`glookupbuf`, `blookupbuf`, `tlookupbuf`) to their respective files.
6.  **Cleanup:** Frees allocated memory and closes all open files.

## Output Files (JHC `.r4` Array Format)
*   `<svp_handle>.grazing_angle`: A 2D floating-point array (raster) where each cell contains the grazing angle.
*   `<svp_handle>.beam_angle`: A 2D floating-point array (raster) where each cell contains the outgoing beam angle.
*   `<svp_handle>.time_lag`: A 2D floating-point array (raster) where each cell contains the one-way travel time.
Each output file contains a `JHC_header` followed by the raw float data.

## Helper Functions

*   `read_in_raw()`: Reads SVP data in a raw format (depth, velocity pairs).
*   `read_in_NEW_raw()`: Reads SVP data in another "NEW" raw format.
*   `make_equisvp()`: Interpolates raw SVP data to create an equi-spaced layered velocity profile (`veldep`).
*   `read_in_svp()`: Reads SVP data from a custom `.profile` format.
```
```