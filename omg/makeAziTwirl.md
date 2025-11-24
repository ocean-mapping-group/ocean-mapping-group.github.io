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

| Option | Description | Default |
|---|---|---|
| `-outprefix <output_prefix>` | **Required.** The base name for the output files. | |

### Input Data Source (Choose one)
| Option | Description |
|---|---|
| `-inss <input_ss_file>` | Specifies the input GLORIA sidescan file (`GLORIA_RECLEN` format). | |
| `-merged <merged_file>` | Specifies an OMG-HDCS merged file. When used with this, `-beamgra` and `-beambs` are also required. | |
| `-beamgra <grazing_angle_file>` | **Required with `-merged`.** A JHC float grid (`.r4`) containing beam grazing angles. | |
| `-beambs <backscatter_file>` | **Required with `-merged`.** A JHC float grid (`.r4`) containing beam backscatter values. | |

### Output Resolution
| Option | Description | Default |
|---|---|
| `-pixel <size>` | For sidescan option (`-inss`). Sets the pixel size for the across-track dimension in the output orthogonal grids. | `1.0` |
| `-grangstep <step>` | For multibeam option (`-merged`). Sets the step size for grazing angle bins (in degrees) in the output orthogonal grids. | `0.25` |
| `-azidegstep <step>` | Sets the step size for azimuth bins (in degrees) in all output grids. | `0.5` |

### Filtering/Range Options
| Option | Description | Default |
|---|---|
| `-start <ping_num>` | Processes data only from the specified starting ping number. | All |
| `-end <ping_num>` | Processes data only up to the specified ending ping number. | All |

### Other Options
| Option | Description |
|---|---|
| `-v` | Enable verbose output. | |

## How It Works
`makeAziTwirl` operates by transforming sidescan or multibeam backscatter data from its original spatial domain into a polar "azimuth-angle" domain.
1.  **Input Reading:** Reads input backscatter data. This can be either:
    *   GLORIA sidescan files (`-inss`): Reads sidescan records, extracting imagery and navigation.
    *   Multibeam data (`-merged`, `-beamgra`, `-beambs`): Reads merged files, grazing angle grids, and backscatter grids.
2.  **Transformation to Azimuth-Angle Domain:**
    *   For each data point (sidescan pixel or multibeam beam), it extracts its associated backscatter intensity, azimuth (vessel heading), and across-track position or grazing angle.
    *   It then maps these values into a 2D polar array, where one axis represents azimuth (e.g., 0-360 degrees) and the other represents grazing angle or across-track distance.
    *   The `grangstep` and `azidegstep` parameters control the binning resolution of this polar array.
3.  **Accumulation and Averaging:** Backscatter intensities are accumulated in the appropriate bins of the polar array. If multiple samples fall into the same bin, they are averaged.
4.  **Output Grids:** The accumulated and averaged data is output as a set of four JHC float grid files (`.r4`):
    *   **Orthogonal Views:** Port and starboard sides in azimuth vs. grazing angle/across-track.
    *   **Radial Views:** Port and starboard sides in a transformed X-Y space.

## Output Files
The tool generates four output JHC float grid files (`.r4`) organized into "orthogonal" (azimuth vs. across-track/grazing angle) and "radial" (X vs. Y where X/Y are derived from azimuth/grazing angle) views:
*   **`<output_prefix>.ortho.port.r4`**: Orthogonal view for port side.
*   **`<output_prefix>.ortho.stbd.r4`**: Orthogonal view for starboard side.
*   **`<output_prefix>.radial.port.r4`**: Radial view for port side.
*   **`<output_prefix>.radial.stbd.r4`**: Radial view for starboard side.

## Dependencies
*   `OMG_HDCS_jversion.h`: For OMG-HDCS data structures (if multibeam input).
*   `array.h`: For `JHC_header` structure and grid data handling.
*   `support.h`: For general utility functions and error handling.

## Notes
This tool is particularly useful for detecting and visualizing artifacts or patterns in backscatter data that are correlated with the vessel's heading or the beam's azimuth. It can help identify residual angular dependencies that are not fully compensated by beam pattern correction, or features with a preferred orientation. The "radial" output provides an alternative visualization for these patterns.