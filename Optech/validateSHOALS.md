---
layout: default
title: validateSHOALS
parent: Optech Tools
nav_order: 123
---
# validateSHOALS

## Description
`validateSHOALS` is a specialized validation tool for SHOALS (Scanning Hydrographic Operational Airborne Lidar Survey) data. It processes two 8-bit image files: a "reference" image (typically representing backscatter intensity or other signal quality metrics) and a "height" image (e.g., bottom return height, roughness, or standard deviation of depths). By comparing overlapping pixels in these two images against user-defined thresholds, the program classifies seabed characteristics, primarily focusing on the presence of submerged vegetation (weed detection) and other data quality aspects. The output is a new 8-bit image where each pixel represents a validation status.

## Usage
```bash
validateSHOALS -reference <filename> -reference_threshold <value> -height <filename> -height_threshold <value> -out <filename> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `-reference <filename>` | **Required.** Specifies the input 8-bit image file that contains the reference data (e.g., backscatter intensity, often used to indicate signal strength from the seabed). |
| `-reference_threshold <value>` | **Required.** Sets a floating-point threshold for the reference data. Pixels above or below this threshold are evaluated for classification. |
| `-height <filename>` | **Required.** Specifies the input 8-bit image file that contains height-related data (e.g., bottom return height variability, roughness, or a derived metric of vertical uncertainty). |
| `-height_threshold <value>` | **Required.** Sets a floating-point threshold for the height data. Pixels are evaluated against this value for classification. |
| `-ignore <value>` | **Optional.** Specifies a single unsigned character pixel value (defaulting to `0`) that should be ignored in *both* input files. Pixels with this value are typically considered "no data" and are excluded from the classification process. | `0` |
| `-bs` | **Optional.** Activates a "backscatter mode" which specifically sets `ignore_ref` to `255` and `ignore_height` to `0`. This is a specific configuration for backscatter processing. | |
| `-out <filename>` | **Required.** Specifies the filename for the output 8-bit image file, which will contain the classification results. | |

## How It Works
1.  **File Handling:** Opens the specified `referencefile`, `heightfile`, and `outfile`. Reads the `JHC_header` from both input files to obtain image dimensions (`dx`, `dy`) and min/max intensity values for scaling.
2.  **Output Header Initialization:** A `JHC_header` (based on the `referencefile`'s header but with modified `min_value` and `max_value` to reflect the classification range) is written to the `outfile`.
3.  **Data Processing Loop (Pixel Classification):** Iterates through each row (`head1.dy`) and column (`head1.dx`) of the input images:
    *   Reads the 8-bit pixel data into `freference` and `fheight` buffers.
    *   **Ignoring No-Data Pixels:** Before classification, it checks if a pixel's value matches the `ignore_ref` or `ignore_height` values. If so, it marks the corresponding output pixel in `fout` as `1` (indicating "not overlapping data") and skips classification.
    *   **Value Scaling:** For valid pixels, the 8-bit unsigned char values are converted back to their original floating-point representations using the `min_value` and `max_value` stored in their respective `JHC_header`s. Special handling for backscatter data is noted if `bs_flag` is set.
    *   **Classification Logic:** A set of `if-else if` statements applies the core validation rules:
        *   If `freference_val >= reference_threshold` AND `fheight_val <= height_threshold`: **Result:** `WEED` (or vegetated rock), assigned `value = 9` (red).
        *   If `freference_val < reference_threshold` AND `fheight_val <= height_threshold`: **Result:** `SUSPICIOUS` (or vegetated sand), assigned `value = 13` (yellow).
        *   If `freference_val < reference_threshold` AND `fheight_val > height_threshold`: **Result:** `VALID SOUNDING` (unvegetated sand), assigned `value = 11` (blue).
        *   If `freference_val >= reference_threshold` AND `fheight_val > height_threshold`: **Result:** `NO WEED LIKELY` (unvegetated rock, potential hazard), assigned `value = 12` (cyan).
    *   The classified `value` (an `unsigned char` representing a color index) is stored in the `fout` buffer.
    *   After processing a row, the `fout` buffer is written to the `outfile`.
4.  **Output Header Finalization:** After all pixel rows are processed, the output `JHC_header` is updated to reflect the `min_value` (`1`) and `max_value` (`17`), defining the range of output classification colors.

## Output Files
*   `<filename>`: A new 8-bit JHC-format image file (`.8bit`) containing the classification results.

## Dependencies
*   `array.h`: For `JHC_header` structure and functions (`get_print_JHC_header`, `write_JHC_header`).
*   `support.h`: For utility functions (`usage`, `error`, `strtoint`, `strtodbl`).

## Notes
`validateSHOALS` is a specialized and essential tool within hydrographic data processing workflows, particularly for airborne lidar bathymetry. Its main purposes are automated quality control, vegetation detection, seabed characterization, and data interpretation. The tool is invaluable for hydrographers, marine scientists, and environmental managers working with SHOALS data to produce accurate charts, conduct habitat assessments, and ensure navigation safety.