---
layout: default
title: to8bit
parent: Sidescan Radiometric & Geometric Suite (sidescan)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 23
tool_name: to8bit
source_path: code/sidescan/mock/to8bit
category: Sidescan & Backscatter Modeling
input_formats:
- 32-bit floating-point array (e.g. ssmock / fullmock output)
output_formats:
- 8-bit XFB raster (.xfb)
related_tools:
- ssmock.f
- fullmock.f
- synthetic
---

# to8bit

## Description
`to8bit` is a C-shell pipeline script (written by John Hughes Clarke, October 22, 1989) in `code/sidescan/mock/` that converts a 32-bit floating-point synthetic sidescan array (such as the grazing-angle grid output by [`ssmock.f`](ssmock.f.html) or [`fullmock.f`](fullmock.f.html)) into an 8-bit `.xfb` display image.

## Usage

```csh
to8bit <filename> <reclen> <low> <high>
```
* **`<filename>` (`$1`)**: Input floating-point grid file.
* **`<reclen>` (`$2`)**: Row length in pixels (e.g., `512`).
* **`<low>` (`$3`)**: Minimum floating-point value mapped to `0`.
* **`<high>` (`$4`)**: Maximum floating-point value mapped to `255`.

## Pipeline Executed

```csh
mask < $1 | color -low $3 -high $4 | fill -v127 | makexfb -reclen $2 > $1.xfb
```
1. `mask`: Masks flagged no-data values (`-999.0`).
2. `color -low $3 -high $4`: Linearly stretches floating-point values between `<low>` and `<high>` to 8-bit greyscale.
3. `fill -v127`: Fills masked background pixels with mid-grey (`127`).
4. `makexfb -reclen $2`: Packages the byte stream into an XFB raster file (`<filename>.xfb`).
