---
layout: default
title: makeAziTwirl
parent: OMG Tools
nav_order: 37
---
# makeAziTwirl

## Description
`makeAziTwirl` is a specialized tool that resamples backscatter intensity data into a polar or "twirl" array, where the axes typically represent azimuth and across-track distance/grazing angle. This transformation allows for visualization and analysis of backscatter data as a function of the vessel's heading or beam azimuth.

The tool can process either GLORIA sidescan records (`-inss`) or multibeam (OMG-HDCS) data with pre-calculated grazing angles and backscatter values (`-merged`, `-beamgra`, `-beambs`).

## Usage
```bash
# For GLORIA Sidescan data
makeAziTwirl -inss <input_ss_file> -outprefix <output_prefix> [OPTIONS]

# For Multibeam data (using pre-computed grazing angles and backscatter)
makeAziTwirl -merged <merged_file> -beamgra <grazing_angle_file> -beambs <backscatter_file> -outprefix <output_prefix> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `-outprefix <output_prefix>` | **Required.** The base name for the output files. |

### Input Data Source (Choose one)
| Option | Description |
|---|---|
| `-inss <input_ss_file>` | Specifies the input GLORIA sidescan file (`GLORIA_RECLEN` format). |
| `-merged <merged_file>` | Specifies an OMG-HDCS merged file. When used with this, `-beamgra` and `-beambs` are also required. |
| `-beamgra <grazing_angle_file>` | **Required with `-merged`.** A JHC float grid (`.r4`) containing beam grazing angles. |
| `-beambs <backscatter_file>` | **Required with `-merged`.** A JHC float grid (`.r4`) containing beam backscatter values. |

### Output Resolution
| Option | Description | Default |
|---|---|---|
| `-pixel <size>` | For sidescan option (`-inss`). Sets the pixel size for the across-track dimension in the output orthogonal grids. | `1.0` |
| `-grangstep <step>` | For multibeam option (`-merged`). Sets the step size for grazing angle bins (in degrees) in the output orthogonal grids. | `0.25` |
| `-azidegstep <step>` | Sets the step size for azimuth bins (in degrees) in all output grids. | `0.5` |

### Filtering/Range Options
| Option | Description | Default |
|---|---|---|
| `-start <ping_num>` / `-end <ping_num>` | Processes data only within the specified range of pings. | All |

### Other Options
| Option | Description |
|---|---|
| `-v` | Enable verbose output. |

## Output Files
The tool generates four output JHC float grid files (`.r4`) organized into "orthogonal" (azimuth vs. across-track/grazing angle) and "radial" (X vs. Y where X/Y are derived from azimuth/grazing angle) views:
*   **`<output_prefix>.ortho.port.r4`**: Orthogonal view for port side.
*   **`<output_prefix>.ortho.stbd.r4`**: Orthogonal view for starboard side.
*   **`<output_prefix>.radial.port.r4`**: Radial view for port side.
*   **`<output_prefix>.radial.stbd.r4`**: Radial view for starboard side.