---
layout: default
title: addstamp
parent: Grid Tools
nav_order: 5
---
---
layout: default
title: addstamp
parent: Grid Tools
nav_order: 5
---
# addstamp

## Description
`addstamp` is a command-line utility for "stamping" a smaller 8-bit image (a "logo") onto a larger 8-bit image file. It allows for placing the logo at specified coordinates or corners, with options for blending it with the background image or controlling overwriting behavior.

## Usage
```bash
addstamp [OPTIONS] -logo <logo_file.8bit> <8bit_image_file>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-logo <logo_file.8bit>` | **Required.** Specifies the path to the 8-bit JHC-format image file to be used as the "logo" or stamp. | `my_logo.8bit` |
| `<8bit_image_file>` | **Required.** The path to the larger JHC-format 8-bit image file onto which the logo will be stamped. This file is modified in place. | `base_image.8bit` |
| `-left_x <value>` | Specifies the X-coordinate (column) for the top-left corner of the logo on the base image. | `40` |
| `-top_y <value>` | Specifies the Y-coordinate (row) for the top-left corner of the logo on the base image. | `237` |
| `-tl` | Place the logo at the top-left corner of the base image. Overrides `-left_x` and `-top_y`. | (Equivalent to `-left_x 10 -top_y 10`) |
| `-bl` | Place the logo at the bottom-left corner of the base image. Overrides coordinate options. | |
| `-tr` | Place the logo at the top-right corner of the base image. Overrides coordinate options. | |
| `-br` | Place the logo at the bottom-right corner of the base image. Overrides coordinate options. | |
| `-blend` | Enables blending mode. The logo is smoothly blended with the background image, rather than simply overwriting it. | |
| `-power <value>` | Used with `-blend`. Controls the blending power, affecting how strongly the logo's pixel values influence the final blended result. | `1.0` |
| `-ignore <value>` | Specifies a pixel value in the logo image that should be treated as transparent (i.e., not stamped). | `0` |
| `-dontoverwrite <value>` | Specifies a pixel value in the *base* image that should not be overwritten by the logo, even if the logo has a non-transparent pixel at that location. | `-1` (no value is protected) |
| `-color <value>` | If specified (and not `-1`), all non-ignored pixels from the logo will be stamped with this specific 8-bit color value onto the base image. If `-1`, the logo's original pixel values are used. | `0` (black) |

## How It Works
1.  **File Opening:** Opens the input base image file and the logo image file.
2.  **Header Reading:** Reads the `JHC_header` from both files, extracting dimensions.
3.  **Positioning:** Determines the top-left corner `(left_x, top_y)` for placing the logo based on explicit coordinates (`-left_x`, `-top_y`) or corner flags (`-tl`, `-bl`, `-tr`, `-br`).
4.  **Pixel-wise Stamping:** Iterates through each pixel of the logo image:
    *   If the logo pixel is not `ignore_val` and the corresponding base image pixel is not `dontoverwrite_val`:
        *   **Blending (`-blend`):** If blending is enabled, the new pixel value is a weighted average of the base and logo pixels, with `power` controlling the logo's influence.
        *   **Direct Overwrite:** Otherwise, if `-color` is specified, the output pixel takes `color_val`. If not, it takes the logo pixel value.
    *   The resulting pixel is written to the base image file.
5.  **Output:** The input base image file is modified in place.

## Output Files
The input base 8-bit image file is modified in-place.

## Dependencies
*   `array.h`: For `JHC_header` structure and related functions.
*   `support.h`: For general utility functions and error handling.

## Notes
The tool modifies the base image file directly. It's recommended to create a backup of the base image before running `addstamp` if the original state needs to be preserved. `dontoverwrite` can be used to protect existing annotations or specific features on the base image.
