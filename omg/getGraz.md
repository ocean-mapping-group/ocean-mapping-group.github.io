---
layout: default
title: getGraz
parent: OMG Tools
nav_order: 105
---
# getGraz

## Description
`getGraz` is a utility designed to create or update a Look-Up Table (LUT) of backscatter (Sb) values versus true grazing angle, derived from multibeam sonar data. It compares observed depths from merged files against a Digital Terrain Model (DTM) to calculate true grazing angles and stores these alongside the corresponding backscatter values.

The tool aims to correct backscatter data for the true grazing angle, accounting for seabed slopes and potentially removing the Simrad Lambertian Correction. The LUT can then be used for backscatter classification or further analysis.

## Usage
```bash
getGraz <merged_file(s)> -lut <LUThandle> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<merged_file(s)>` | **Required.** One or more paths to input OMG-HDCS merged files. |
| `-lut <LUThandle>` | **Required.** The handle (base name) for the Look-Up Table files. The tool will generate/update `<LUThandle>.lut` and `<LUThandle>.num` files. |
| `-flat` | Use a flat seafloor assumption (nadir topography only) for DTM depth. |
| `-numsam <val>` | Specifies the maximum number of backscatter samples to store per pixel in the LUT. | `5` |
| `-v` | Enable verbose output. |

## How It Works
1.  **Initialization:** Parses command-line arguments to set various flags, including `flat_flag` (for flat seafloor), `NUMSAM` (max samples per pixel), and output filenames.
2.  **DTM Loading:** Reads the input `.r4` (float grid) DTM file (specified by `outname`, which is typically derived from the DTM filename). This DTM represents the reference surface.
3.  **LUT File Setup:**
    *   Attempts to open `<LUThandle>.lut` and `<LUThandle>.num` files.
    *   If these files do not exist, it creates them and initializes them with blank data and a JHC header.
    *   If they exist, it reads the existing `num` array (which stores the count of samples per pixel).
4.  **Profile and Beam Iteration:** Loops through each input merged file and then through each profile (ping) and beam within:
    *   **Data Validation:** Checks if `beams[j].observedDepth` is valid and if the beam's `status` is not flagged.
    *   **Geographic Positioning:** Locates the beam's geographic position (lat/lon) and projects it onto the DTM grid (`x`, `y`).
    *   **DTM Depth Lookup:** Retrieves `true_depth`, `true_east`, and `true_south` from the DTM at the beam's projected location.
    *   **Grazing Angle Calculation:**
        *   Calculates `angle` based on `acrossTrack` and `depth` (relative to `CREED_DRAFT`).
        *   Calculates `beam_azi` (beam azimuth).
        *   Uses `vectangle` (an external function) to compute the `true_grazing_angle` by comparing the beam's angle and azimuth with the seafloor slope derived from the DTM.
    *   **Backscatter Processing:**
        *   If `true_grazing_angle` is valid (not negative), it extracts `Sb` (backscatter from `beams[j].reflectivity`).
        *   It then "uncorrects" the Simrad Lambertian Correction from `Sb` using `10.0 * log10(pow(cos(angle * M_PI / 180.0), 2.0))`.
    *   **LUT Accumulation:**
        *   If the pixel (`x`, `y`) in the DTM has fewer than `NUMSAM` samples already stored, it creates an `Sb_value` structure with `file`, `profile`, `beam`, `azi`, `graz` (true grazing angle), and `Sb` (uncorrected backscatter).
        *   It then writes this `Sb_value` to the `.lut` file at the appropriate offset and increments the count in the `num` array for that pixel.
    *   **Verbose Output:** If `verbose_flag` is set, it prints detailed information for selected beams.
5.  **Final `num` Array Update:** After processing all files, it writes the updated `num` array (containing sample counts per pixel) back to the `.num` file.
6.  **Cleanup:** Closes all open files and frees allocated memory.

## Output Files
*   `<LUThandle>.lut`: A custom binary file containing backscatter values (`Sb_value` structures) mapped by geographic pixel.
*   `<LUThandle>.num`: A JHC `.r4` grid file containing the count of `Sb_value` samples per geographic pixel.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `array.h`: For `JHC_header` structure and DTM data handling.
*   `support.h`: For general utility functions and error handling.
*   `j_proj.h`: For coordinate projection functions.
*   `backscatter.h`: For `vectangle` function.

## Notes
This tool allows for the construction of spatially organized Look-Up Tables of backscatter vs. grazing angle. This is fundamental for building empirical models of the seafloor's acoustic response, which can then be used for seafloor classification or correcting backscatter imagery. The removal of the Simrad Lambertian correction is critical for getting true backscatter values that reflect the seafloor rather than sonar processing.