---
layout: default
title: correlate
parent: Grid Tools
nav_order: 16
---
---
layout: default
title: correlate
parent: Grid Tools
nav_order: 16
---
# correlate

## Description
`correlate` is a command-line utility designed to perform image correlation between a stereo pair of 8-bit images (master and slave). It searches for the best match of a user-defined window from the master image within a specified search range in the slave image. It outputs three 8-bit JHC-format grid files: one for the X-shift, one for the Y-shift, and one for the correlation coefficient (or residual difference) for each correlated pixel location in the master image. This tool is fundamental for stereo photogrammetry or motion tracking applications.

## Usage
```bash
correlate -name <file_prefix> [OPTIONS]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-name <file_prefix>` | **Required.** Specifies a prefix for the input and output filenames. The tool expects input files named `<file_prefix>.master` and `<file_prefix>.slave` (both 8-bit JHC format). Output files will be `<file_prefix>.xshift`, `<file_prefix>.yshift`, and `<file_prefix>.sdev`. | `-name image_pair` (expects `image_pair.master`, `image_pair.slave`, outputs `image_pair.xshift`, etc.) |
| `-xbound <min_x> <max_x>` | Defines the X-axis (column) bounds within the master image where correlation will be performed. `<min_x>` and `<max_x>` are integer pixel coordinates. | (Defaults to full image width) |
| `-ybound <min_y> <max_y>` | Defines the Y-axis (row) bounds within the master image where correlation will be performed. `<min_y>` and `<max_y>` are integer pixel coordinates. | (Defaults to full image height) |
| `-window <x_size> <y_size>` | Specifies the dimensions of the correlation window (template) in pixels. `<x_size>` is the width, and `<y_size>` is the height. | `10 10` |
| `-range <x_range> <y_range>` | Defines the maximum search range (in pixels) for the correlation window in the slave image. `<x_range>` is the X-axis search extent, and `<y_range>` is the Y-axis search extent. | `10 5` |
| `-skip <value>` | Specifies the pixel interval at which correlation is performed. A value of `1` means every pixel, `5` means every 5th pixel, etc. | `10` |
| `-grossoffset <x_offset> <y_offset>` | Specifies an initial gross offset (in pixels) for the X and Y dimensions to start the correlation search from. This can speed up processing if the images have a known large offset. | `0 0` |
| `-coeff` | Output correlation coefficient values (0-100) as the similarity metric. This is the default. | (Default) |
| `-pixfract` | If enabled, also outputs an ASCII file (`XYZ.list`) containing sub-pixel accurate correlation results. | |
| `-secondpass` | Enables a second pass mode where previous X/Y shift files (`.xshift`, `.yshift`) are used to initialize the search, allowing for more refined results. Requires a file prefix to load the previous shifts. | |
| `-v` | Enable verbose output during processing. | |

## How It Works
1.  **File Opening:** Opens the master and slave input images (`.master`, `.slave`) and creates output files for X-shift (`.xshift`), Y-shift (`.yshift`), and correlation coefficient (`.sdev`).
2.  **Header Reading:** Reads `JHC_header` from input image files to get dimensions.
3.  **Parameter Setup:** Initializes `x_size`, `y_size` (window size), `x_range`, `y_range` (search range), `skip_pixels`, `gross_offset_x`, `gross_offset_y`, and `min_coeff` from command-line arguments.
4.  **Correlation Loop:** Iterates through the master image based on `skip_pixels` and `xbound`/`ybound`:
    *   For each pixel in the master image, it extracts a `window_x_size` x `window_y_size` template.
    *   It then searches within a `search_range_x` x `search_range_y` area in the slave image around the expected corresponding location (adjusted by `gross_offset` or `secondpass` data).
    *   **Correlation Metric:** Calculates the correlation coefficient (or inverse sum of squared differences) between the master template and each candidate window in the slave image.
    *   The location of the best match gives the X and Y shifts, and the value of the match is the correlation coefficient.
    *   These values are written to the respective output `.xshift`, `.yshift`, and `.sdev` files.
5.  **Sub-pixel Refinement (`-pixfract`):** If enabled, it applies sub-pixel interpolation to refine the shift estimates.
6.  **Output Header:** Creates and writes `JHC_header` for the output shift and correlation files.

## Output Files
*   `<file_prefix>.xshift`: An 8-bit JHC grid of X-shifts.
*   `<file_prefix>.yshift`: An 8-bit JHC grid of Y-shifts.
*   `<file_prefix>.sdev`: An 8-bit JHC grid of correlation coefficients (or residual differences).
*   `XYZ.list`: An ASCII file with sub-pixel correlation results (if `-pixfract` is used).

## Dependencies
*   `array.h`: For `JHC_header` structure and image data handling.
*   `support.h`: For general utility functions and error handling.
*   `math.h`: For mathematical functions.

## Notes
The correlation coefficient is typically scaled to an 8-bit range (0-100) for storage in the `.sdev` image. This tool is often used as a preprocessing step for creating Digital Elevation Models from stereo optical imagery or for tracking displacement in time-lapse image sequences.
