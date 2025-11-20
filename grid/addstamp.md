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
