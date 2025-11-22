---
layout: default
title: showPingRate
parent: OMG Tools
nav_order: 62
---
# showPingRate

## Description
`showPingRate` is a utility designed to analyze and visualize ping rate or coverage density from OMG-HDCS multibeam data. It can generate various plots, including:
1.  **Ping Rate vs. Depth:** Visualizes how ping rate changes with water depth.
2.  **Coverage Density Map:** Creates a 2D map showing the density of valid soundings across a specified geographic area (depth vs. across-track distance). This can be useful for assessing survey coverage and identifying gaps or areas of dense data.
3.  **Backscatter Map:** Can also map average backscatter values to a coverage density map.

The output can be in a custom float array format (`.r4`) or PGM (Portable Graymap) image format.

## Usage
```bash
showPingRate <omgfiles(s)> [OPTIONS]
```

## Arguments

| Option | Description |
|---|---|
| `<omgfiles(s)>` | **Required.** One or more paths to input OMG-HDCS merged files. |
| `-maxdepth <val>` | **Required for `-show_coverage`.** Maximum water depth for the plot/map (in meters). |
| `-maxtime <val>` | Maximum time difference between pings for ping rate plot (in seconds). |
| `-angsect_range <min> <max>` | Defines an angular sector range (in degrees) for the ping rate plot. | `50` to `80` |
| `-pixdimen <val>` | Dimension of the output plot in pixels (for ping rate plot). | `200` |
| `-draft <val>` | Specifies the draft (in meters) to subtract from observed depths. | `1.0` |
| `-tide <filename>` | Specifies a binary tide file (`.nav` format) to apply tide correction (for systems that have it irreversibly subtracted). |

### Coverage / Backscatter Map Options (`-show_coverage`)
| Option | Description |
|---|---|
| `-show_coverage` | Generate a 2D coverage density map (depth vs. across-track distance). Requires `-maxdepth`, `-maxacross`, and `-pixel`. |
| `-maxacross <val>` | **Required for `-show_coverage`.** Maximum absolute across-track distance for the map (in meters). |
| `-pixel <val>` | **Required for `-show_coverage`.** Pixel size for the coverage map (in meters). |
| `-show_BS` | (Used with `-show_coverage`). Instead of counting hits, maps the average backscatter value to the coverage map. |
| `-normallize` | (Used with `-show_coverage`). Normalizes the coverage counts by the average count in each depth row. |
| `-pgm` | Output the coverage map in PGM (Portable Graymap) image format. |
| `-range <min> <max>` | (Used with `-pgm`). Stretches the output grayscale values in the PGM image between `min` and `max`. | `0` to `2.0` (for coverage counts) or `-50` to `-1` (for BS values) |

### Other Options
| Option | Description |
|---|---|
| `-v` | Enable verbose output. |

## How It Works
1.  **Initialization:** Parses command-line arguments to set up parameters for plotting (e.g., `maxdepth`, `maxtime`, `pixel` size, `draft`).
2.  **File Setup:** Opens input OMG-HDCS merged files and creates an output file (default "pingstack" or "CoverageStack.r4" if `-show_coverage`). If `-pgm` is specified, it also creates a PGM image file.
3.  **Data Structures:** Allocates memory for a float array (`fdata`) to store the plot data (ping counts or backscatter values).
4.  **Header Writing:** Writes a JHC image header to the output `.r4` file based on the chosen plot type and dimensions.
5.  **Data Processing:** Iterates through each input OMG-HDCS merged file and each profile (ping) within it:
    *   **Ping Rate Plot (Default behavior):**
        *   Calculates the time difference between consecutive pings (`deltatime`).
        *   Determines a representative depth for the ping (average of two central beams).
        *   If a tide file is provided, applies tide correction to the depth.
        *   Increments a counter in the `fdata` array at coordinates corresponding to (depth, deltatime) or (depth, elevation angle) if `-angsect_range` is used.
    *   **Coverage/Backscatter Map (`-show_coverage`):**
        *   For each valid beam in a ping, it calculates its (across-track, depth) position relative to the sonar.
        *   Maps this position to pixel coordinates (`x`, `y`) on the output grid.
        *   If `show_BS` is *not* set, it increments the count in `fdata` at `(x, y)`.
        *   If `show_BS` *is* set, it averages the beam's reflectivity (`bsval`) into `fdata` at `(x, y)`.
6.  **Post-Processing (`-show_coverage`):**
    *   If `normallize` is enabled, it normalizes the coverage counts in each depth row by their average.
    *   If `fillgap` is enabled (hardcoded `1`), it performs a simple 4-neighbor average to fill small gaps in the coverage map.
7.  **Output Writing:**
    *   Writes the processed `fdata` array to the output `.r4` file.
    *   If `pgm_flag` is set, it converts the `fdata` (or `bdata` for PGM output) to an 8-bit grayscale image, applying min/max range stretching, and writes it to the output `.pgm` file.
