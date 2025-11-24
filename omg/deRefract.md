---
layout: default
title: deRefract
parent: OMG Tools
nav_order: 88
---
# deRefract

## Description
`deRefract` is a utility designed to apply corrections for refraction and other empirical adjustments to multibeam sonar data. It can apply either a set of subjective empirical correction coefficients (defined in `swathed` and interpolated along the line) or an "empirical hack angular correction" for poorly refraction-corrected data. The tool can process both standard OMG-HDCS merged files and USL-HDCS observed depth files.

It allows for fine-tuning of depth and across-track values to compensate for sound speed variations in the water column and instrument-specific biases.

## Usage
```bash
deRefract <mergefile(s)> [-v] (-coeffs | -hackfn <filename>) [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<mergefile(s)>` | **Required.** One or more paths to OMG-HDCS merged files or USL-HDCS line directories. These files are modified in place. |
| `-v` | Enable verbose output. |

### Correction Methods (Choose one)
| Option | Description |
|---|---|
| `-coeffs` | Apply empirical correction coefficients loaded from a `.ref_coeffs` file. |
| `-hackfn <filename>` | Apply a hack function based on an external file (`tidefilename`). This uses the older, pre-coefficient method. |

### Coefficient-Based Options (`-coeffs`)
| Option | Description |
|---|---|
| `-depthshift` | Apply a depth shift based on the coefficient data. |
| `-perc_depth` | Apply a percentage depth correction based on the coefficient data. |

### Older Hackfn Options (`-hackfn`)
| Option | Description |
|---|---|
| `-beams <val>` | Specifies the number of beams for the hack function (if not 60). | `60` |
| `-symm` | Applies corrections symmetrically to port and starboard sides. |
| `-roll_offset <val>` | Applies a constant roll offset (in degrees). |

### File Type
| Option | Description |
|---|---|
| `-hdcs` | Process USL-HDCS observed depth files instead of OMG-HDCS merged files. |

### Other Options
| Option | Description |
|---|---|
| `-mode <value>` | Only apply corrections to profiles (pings) with this specific mode value. | `999` (all modes) |

## How It Works
1.  **File Processing:** The tool iterates through each provided merged file (or USL-HDCS directory).
2.  **Summary Header Reading & File Type Handling:** Reads the summary header and handles both OMG-HDCS and USL-HDCS file formats, mapping USL-HDCS data to OMG structures.
3.  **Coefficient Loading (`-coeffs`):** If `-coeffs` is used, it attempts to read `ref_coeff` data from a `.ref_coeffs` file and sets them up. If not found, it uses null coefficients. It also calls `jREF_decide_array_type` to set the array type based on `summary.toolType`.
4.  **Hackfn Method Setup (`-hackfn`):** If `-hackfn` is used (and not `-coeffs`), it loads original depth and range data from `tidename`. It then calculates `dangle` (angular shift) or `dep_shift` (depth shift/multiplier) values per beam based on the `depthshift` or `perc_depth` flags, using a least-squares fit if `depthshift` is active.
5.  **Profile and Beam Iteration:** For each profile (ping) in the file:
    *   **Mode Filtering:** If `-mode` is specified, it only processes pings whose `profile.mode` matches the `mode_choice`.
    *   Reads the raw beams for the current profile (converting USL-HDCS beams to OMG format if `hdcs_flag` is set).
    *   For each beam `i` that has an `observedDepth` and `reflectivity`:
        *   **Coefficient-Based Correction (`-coeffs`):**
            *   Gets coefficients for the current ping using `get_coeffs`.
            *   Sets up refraction coefficients using `set_up_ref_coefficients`.
            *   Calls `get_refracted_location` to calculate `depth_out` and `across_out` from `depth_in` and `across_in` based on the refraction coefficients.
            *   Updates `beams[i].observedDepth` and `beams[i].acrossTrack`.
        *   **Hackfn-Based Correction (pre-coefficient method):**
            *   If `depthshift` is active, it modifies `beams[i].observedDepth` using `depthmove[i]` or `depth_multiplier[i]`.
            *   Otherwise (for angle shift), it calculates `orig_angle` from `orig_depth` and `orig_range`. It applies `angshift` (from `dangle[i]` or `symangle[i]`) and `roll_offset` to get `real_angle`. It then recalculates `real_depth` and `real_range` from this `real_angle` and `slant_range`, updating `beams[i].observedDepth` and `beams[i].acrossTrack`.
6.  **In-Place Update:** The modified `beams` (with corrected depths and across-track values) are written back to the merged file (or USL-HDCS file) for the current profile.

## Output Files
The input merged files are modified in-place.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures.
*   `support.h`: For general utility functions and error handling.
*   `ref_coeffs.h`: For refraction coefficient structures and functions.

## Notes
This tool offers both a modern (coefficient-based) and a legacy (hack function) approach to correcting bathymetric data for refraction and other systematic biases. Due to its empirical nature, careful validation of the applied corrections is essential. The tool modifies merged files in place, so backups are recommended.