---
layout: default
title: 7k2image
parent: Reson Tools
nav_order: 175
---
# 7k2image

## Description
`7k2image` is a utility designed to extract and visualize various raw data types (snippets, watercolumn, or IQ data) from a Reson 7k (`.s7k`) file as 8-bit image data. It allows users to select a specific ping and beam to process, and then converts the raw time-series data into a visual representation, often for detailed inspection and quality control.

The tool supports IQ data visualization (real, imaginary, magnitude, phase components) and can output to a generic 8-bit image file and a corresponding ASCII text file.

## Usage
```bash
7k2image -in <inputfile> [-ping <ping_num>] [-beam <beam_num>] [-max_samples <val>] [-snippets | -watercolumn | -iq [-real|-imag|-mag|-phase]] [-v]
```

## Arguments

| Option | Description |
|---|---|
| `-in <inputfile>` | **Required.** Path to the input Reson 7k `.s7k` file. |
| `-ping <ping_num>` | Specifies the ping number to extract (1-indexed). | `1` |
| `-beam <beam_num>` | Specifies the beam number to extract. If omitted, all beams are processed. | All beams |
| `-max_samples <val>` | Sets a fixed width (number of samples) for the output image. | Auto-determined. |
| `-bt` | (Present in `USAGE` but not implemented) Intended to plot bottom track. |

### Data Source (Choose one)
| Option | Description |
|---|---|
| `-snippets` | Extracts and processes raw snippet (7008 or 7028) data. |
| `-watercolumn` | Extracts and processes beamformed watercolumn (7018) data. |
| `-iq` | Extracts and processes raw IQ (7038) data. |

### IQ Data Type (if `-iq` is used, choose one)
| Option | Description |
|---|---|
| `-real` | Visualizes the real component of IQ data. |
| `-imag` | Visualizes the imaginary component of IQ data. |
| `-mag` | Visualizes the magnitude of IQ data. |
| `-phase` | Visualizes the phase of IQ data. |

### Other
| Option | Description |
|---|---|
| `-v` | Enable verbose output. |

## Output Files
*   `image.8bit`: Binary file containing 8-bit image data. The rows represent beams, and columns represent samples.
*   `image.txt`: ASCII file containing detailed data for a specified beam (sample index, raw value, log10 value).

## How It Works

1.  **Initialization:** Parses command-line arguments, sets input `.s7k` filename, data source (`do_snippets`, `do_watercolumn`, `do_iq`), IQ component (`iq_real`, `iq_imag`, `iq_mag`, `iq_phase`), desired `ping` and `beam`, and `fixed_width`.
2.  **File Opening:** Opens the input `.s7k` file for reading. Creates `image.8bit` (for the 8-bit output image) and `image.txt` (for detailed text output).
3.  **Record Processing Loop:** Reads the `.s7k` file record by record until the desired `ping` is reached:
    *   **Sync Search:** Calls `seek_next_7K_sync()` to find the next Reson 7k synchronization pattern.
    *   **DRF Reading:** Reads the `Reson_7K_DRF` (Data Record Format) to determine the record type and size.
    *   **Record Type Filtering:** Skips records that are not of the desired type (snippets, watercolumn, or IQ).
    *   **Ping Filtering:** Skips records until the `ping` counter matches the `ping` number specified on the command line.
    *   **Data Reading:** Reads the relevant data record (`Reson_7K_7008_Generic_Data`, `Reson_7K_7028_Snippet`, `Reson_7K_7018_Beamformed_Data`, or `Reson_7K_7038_RawIQ`).
    *   **Range Determination:** Determines the `min_range`, `max_range`, and `width` (number of samples) for the output image based on the content of the data record or `fixed_width`.
    *   **Image Data Generation:** For each beam/element:
        *   Allocates a buffer `output` of `width` size.
        *   Iterates through the samples of the current beam/element:
            *   Extracts `value` from the data record (snippets, watercolumn amplitude, or IQ component).
            *   If not IQ phase, converts `value` to an 8-bit logarithmic scale (`20.0 * log10(value)`).
            *   If IQ phase, converts `value` to an 8-bit representation shifted by 127.
            *   Stores the 8-bit value in the `output` buffer.
        *   Writes the `output` buffer to `image.8bit`.
        *   If the current beam matches the `beam` specified on the command line, it prints the sample index, raw value, and log10 value to `image.txt`.
4.  **Cleanup:** Closes all open files.

## Output
*   `image.8bit`: A binary 8-bit file representing the selected data as an image. This can be viewed with image viewers that support raw 8-bit data.
*   `image.txt`: An ASCII text file with detailed per-sample information for the specified beam.
```
```