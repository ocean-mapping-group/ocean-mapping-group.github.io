---
layout: default
title: offtrack
parent: Mock Tools
grand_parent: sidescan
nav_order: 9
---
# offtrack

## Description
`offtrack` is a comprehensive utility for simulating and processing sidescan sonar data, particularly GLORIA imagery, by incorporating detailed physical modeling. It can perform several key functions:
*   **Full Slant Range Correction (`-fullslr`):** Corrects sidescan imagery by taking into account detailed seafloor topography and water column refraction effects.
*   **Mock Image Generation (`-mock`):** Creates synthetic sidescan images that simulate how an area would appear based on its topography, beam pattern, and water column properties.
*   **Backscatter Strength Calculations (`-backscatter`):** Derives quantitative backscatter strength (S_b) values for each pixel, correcting for geometry, transmission loss, beam patterns, and insonified area.
*   **Depth Equivalent Image Generation (`-depth`):** Generates an image where pixel values directly represent the seafloor depth.

This tool integrates information from various environmental and system parameters, including detailed topography, water column sound velocity structure, beam patterns, aspherical spreading, magnetic declination, and sonar system characteristics. It also handles edge cases like cast shadows and data outside the Digital Terrain Model (DTM).

## Usage
```bash
offtrack -topo <topo_file | flat> -water <wc_file_prefix> -image <image_file> -pix <pixel_size> [-proj_lat <lat>] [-declin <declin_val>] [-somers_delay <delay>] [-min_beam <gain>] [-clip_beam <angle>] [-port_offset <offset>] [-starboard_offset <offset>] [-mock <mock_file> | -fullslr <slr_file> | -backscatter <bksct_file_prefix> | -depth <depth_file>] [-maxangle <angle>] [-maxdepth <depth>] [-mindepth <depth>] [-min <dB>] [-max <dB>] [-nadirbias] [-nofocus] [-squared] [-cast_shadow] [-debug <record>] [-first <rec>] [-last <rec>] [-verbose]
```

## Arguments

| Option | Description |
|---|---|
| `-topo <topo_file | flat>` | **Required.** Input topographic file (e.g., a `.r4` grid) or the string "flat" to assume nadir topography only. |
| `-water <wc_file_prefix>` | **Required.** Prefix for water column related files. Expects: `<prefix>.time_lag`, `<prefix>.grazing_angle`, `<prefix>.beam_port`, `<prefix>.beam_stbd`, `<prefix>.aspherical`, `<prefix>.beam_angle`. |
| `-image <image_file>` | **Required.** Input merged GLORIA image file (e.g., a `.des` or `.mer` file). |
| `-pix <pixel_size>` | **Required.** Output pixel size in meters. |
| `-proj_lat <lat>` | Projection latitude for Mercator projection. Default is taken from the topography file header. |
| `-declin <declin_val>` | Magnetic declination in degrees. Used to correct azimuth. |
| `-somers_delay <delay>` | Time delay (in seconds) applied for Somers correction. |
| `-min_beam <gain>` | Minimum beam gain factor to consider. |
| `-clip_beam <angle>` | Minimum beam angle (in degrees) to map. Beams below this angle are masked. |
| `-port_offset <offset>` | Sample offset to apply to port side data in the input image. |
| `-starboard_offset <offset>` | Sample offset to apply to starboard side data in the input image. |
| `-mock <mock_file>` | Output a synthetic sidescan image to `<mock_file>`. (Mutually exclusive with `-fullslr`, `-backscatter`, `-depth`). |
| `-fullslr <slr_file>` | Output a full slant-range corrected image to `<slr_file>`. (Mutually exclusive with `-mock`, `-backscatter`, `-depth`). |
| `-backscatter <bksct_file_prefix>` | Output a quantitative backscatter strength image to `<bksct_file_prefix>.bksct` and an impinging angle image to `<bksct_file_prefix>.imping`. (Mutually exclusive with `-mock`, `-fullslr`, `-depth`). |
| `-depth <depth_file>` | Output a depth equivalent image to `<depth_file>`. (Mutually exclusive with `-mock`, `-fullslr`, `-backscatter`). |
| `-maxangle <angle>` | Maximum angle (in degrees) for synthetic image generation or backscatter mapping. |
| `-maxdepth <depth>` | Maximum depth for scaling in depth equivalent images (negative values are shallower). |
| `-mindepth <depth>` | Minimum depth for scaling in depth equivalent images (negative values are deeper). |
| `-min <dB>` | Minimum dB value for scaling backscatter output to 8-bit. |
| `-max <dB>` | Maximum dB value for scaling backscatter output to 8-bit. |
| `-nadirbias` | Apply a nadir bias correction (linear weighting between DTM and PDR depth). |
| `-nofocus` | Disable beam focusing. |
| `-squared` | Square the TVG (Time Varying Gain) correction in backscatter calculations. |
| `-cast_shadow` | Enable cast shadow detection. |
| `-debug <record>` | Enable debug mode for a specific record, outputting detailed ASCII values. |
| `-first <rec>` | First record to process (ignored in debug mode). |
| `-last <rec>` | Last record to process (ignored in debug mode). |
| `-verbose` | Enable verbose output. |

## How It Works
`offtrack` operates by ray-tracing through a 3D environment defined by the seafloor topography and water column sound velocity structure. For each pixel in the input sidescan image, it determines the true seafloor coordinates, grazing angle, and acoustic path properties.

1.  **Input Loading:**
    *   Loads various look-up tables (LUTs) from JHC image files, including:
        *   **Topography (`-topo`):** A Digital Terrain Model (DTM) or assumes a flat seafloor.
        *   **Water Column (`-water`):** Time-lag vs. range, grazing angle vs. range, port/starboard beam patterns, and aspherical spreading component.
    *   Loads the input GLORIA image (`-image`).
2.  **Initialization:** Initializes parameters like pixel size, projection latitude, magnetic declination, and TVG (`tvg` array).
3.  **Process GLORIA Records:** The tool iterates through each record (ping) of the input GLORIA image.
4.  **Across-Swath Processing:** For each pixel (`j`) across the swath (from starboard to port):
    *   **Georeferencing:** Converts the pixel's apparent position (relative to nadir and vessel) to a geographic coordinate (`xpos`, `ypos`) on the DTM, accounting for ship's heading and offsets.
    *   **Depth Query:** Retrieves the seafloor depth (`value`) from the DTM at `(xpos, ypos)`. If `flat_flag` is set, uses a simplified nadir depth.
    *   **Nadir Bias Correction (`-nadirbias`):** If enabled, it blends the DTM-derived depth with a simplified nadir-only depth within a certain range around the nadir.
    *   **Acoustic Path Calculation:** Using the interpolated depth and range to the seafloor:
        *   `rgraze`: True grazing angle from the water column LUT.
        *   `beam_focus`: Beam focusing factor (from aspherical spreading LUT).
        *   `pixel_time`: Two-way travel time from the water column LUT.
    *   **Footprint Check:** Checks if the pixel is within the insonified footprint (valid `rgraze`, `beam_focus`, `pixel_time`).
    *   **Derived Output Calculation (based on chosen flag):**
        *   **Depth Equivalent (`-depth`):** Scales the `value` (depth) to an 8-bit pixel intensity and writes it to `out_rec`.
        *   **Full Slant Range Corrected (`-fullslr`):** Calculates the corresponding pixel index (`pixel`) in the original GLORIA image based on the `pixel_time`. The pixel value from the original image at this corrected position is written to `out_rec`. Accounts for `port_offset`, `starboard_offset`, and a `somers_delay` to avoid TVG rollover.
        *   **Mock Image (`-mock`):** Calculates the true grazing angle (`true_grazing_angle`) at the seafloor using vector algebra on the DTM. `angle_diff` is computed as `rgraze - true_grazing_angle`. This difference is then scaled to an 8-bit value and written to `result_rec`.
        *   **Backscatter Strength (`-backscatter`):** This is the most complex mode:
            *   Determines `rbeam` (beam gain) from the port/starboard beam pattern LUTs.
            *   Converts the input GLORIA image's 8-bit intensity (`old_8bit`) to a 12-bit value (`r12_bit`) and then to acoustic intensity `I_b`.
            *   Corrects `I_b` for TVG (`tvg[index]`) with optional squaring (`-squared`).
            *   Calculates `inson_area` (insonified area) based on slant range, beam width, sound speed, and pulse width, using the `true_grazing_angle`.
            *   Calculates `range_decay` based on absorption coefficient and slant range.
            *   Finally, calculates the quantitative backscatter strength `S_b` using the sonar equation.
            *   Scales `S_b` (in dB) to an 8-bit value (`new_8bit`) using `min_dB` and `max_dB`. This is written to `result_rec`.
            *   The `true_grazing_angle` is scaled and written to `out_rec` as the impinging angle image.
            *   **Cast Shadow Detection (`-cast_shadow`):** If enabled, it attempts to detect shadows by comparing current `beam_angle` to a previous one. If a shadow is detected, the `true_grazing_angle` is set to an error code.
            *   **Beam Clipping (`-clip_beam`):** Pixels with `beam_angle` below `clip_beam` are masked out.
        *   **Debugging (`-debug`):** If enabled, outputs detailed ASCII values for various calculated parameters to `fullslrfile` instead of a GLORIA image.
5.  **Output:** The generated or corrected records (`out_rec`, `result_rec`) are written to the appropriate output files.
6.  **Loop:** This process repeats until all records have been processed.
