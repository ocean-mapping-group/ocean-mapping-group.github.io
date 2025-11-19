# calcXYZ

## Description
`calcXYZ` is a command-line utility designed to generate XYZ coordinate data (suitable for gridding with `surface.c`) from stereo imagery or other parallax-derived inputs. It takes a correlation coefficient map (indicating data quality) and a parallax map as input. For valid points, it calculates the 3D position based on camera geometry parameters (focal length, camera separation) and outputs them as an ASCII XYZ file. It can also process sub-pixel parallax solutions.

## Usage
```bash
calcXYZ [OPTIONS] -coeff <coeff_map.8bit> -parallax <parallax_map.8bit> -out <output.xyz>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-coeff <coeff_map.8bit>` | **Required.** Specifies the path to the 8-bit JHC-format correlation coefficient map. Only pixels above a minimum coefficient threshold will be processed. | `corr_coeff.8bit` |
| `-parallax <parallax_map.8bit>` | **Required.** Specifies the path to the 8-bit JHC-format parallax map. This map typically contains encoded X-parallax values. | `x_parallax.8bit` |
| `-out <output.xyz>` | **Required.** Specifies the path for the output ASCII XYZ file. Each line in this file will contain X, Y, and Z coordinates. | `3d_points.xyz` |
| `-spix <subpixel_input_file.txt>` | If specified, the tool will read sub-pixel parallax solutions from this ASCII file instead of the 8-bit parallax map. The format of this file is assumed to be: `i j xpar ypar Xpar Ypar coeff`. | `subpix_data.txt` |
| `-mincoeff <value>` | Sets the minimum correlation coefficient threshold. Pixels with a coefficient below this value will be ignored. | `50` |
| `-flen <value>` | Specifies the camera's focal length in millimeters, used in the 3D reconstruction calculations. | `50.0` |
| `-csep <value>` | Specifies the camera separation (baseline) in millimeters, used in the 3D reconstruction calculations. | `220.0` |
| `-v` | Enable verbose output, printing detailed information during processing. | |