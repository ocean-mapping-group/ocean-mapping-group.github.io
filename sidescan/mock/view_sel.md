---
layout: default
title: view_sel
parent: Mock Tools
grand_parent: sidescan
nav_order: 17
---
# view_sel

## Description
`view_sel` is an interactive C program designed for advanced viewing and analysis of backscatter strength and grazing angle mosaics, primarily through an X-windows graphical user interface. It allows users to:
*   **Select Regions of Interest:** Interactively define areas on a displayed image using a "rubber band" selection.
*   **View Sub-images:** Zoom into selected areas, potentially with decimation or expansion.
*   **Compute Angular Dependence:** Calculate and display the mean and standard deviation of backscatter as a function of grazing angle for selected regions, similar to `selective_back.c`.
*   **Classification and Masking:** Analyze pixels based on an external classification image or create masks.

This tool is a powerful interactive environment for exploring the statistical relationship between backscatter and grazing angle within specific areas of interest in sidescan imagery.

## Usage
```bash
view_sel [-table <prefix>] [-bksct <bksct_file>] [-imping <imping_file>] [-class <class_file>] [-range <low> <high>] [-dB <min_dB> <max_dB>] [-min_graz <angle>] [-view] [-image <image_file>] [-color <value>] [-top_y <y0>] [-bot_y <y1>] [-left_x <x0>] [-right_x <x1>] [-topo <topo_file>]
```

## Arguments

| Option | Description |
|---|---|
| `-table <prefix>` | Specifies a prefix for output files (table image, ASCII mean file). |
| `-bksct <bksct_file>` | Path to a backscatter mosaic file (ACRES format). Can be used multiple times to add more files. |
| `-imping <imping_file>` | Path to an impinging (grazing) angle mosaic file (ACRES format). Can be used multiple times. |
| `-class <class_file>` | An external classification image file (ACRES format). Pixels from the backscatter/impinging mosaics will only be processed if their corresponding pixel in this file falls within the `-range`. |
| `-range <low> <high>` | When used with `-class`, specifies the inclusive range of pixel values in the classification image to consider. |
| `-dB <min_dB> <max_dB>` | Defines the minimum and maximum decibel range for the output table's y-axis. |
| `-min_graz <angle>` | Sets a minimum grazing angle (in degrees) threshold for data to be included in the analysis. |
| `-view` | Activates the interactive X-windows viewing mode. |
| `-image <image_file>` | An optional image file (ACRES format) to be "painted" with a specified color (`-color`) where classification criteria are met. |
| `-color <value>` | The 8-bit color value to "paint" pixels in the `image_file` if using the `-image` and `-class` options. |
| `-top_y <y0>` | Top row of the geographic region of interest for analysis (can be interactively selected in `-view` mode). |
| `-bot_y <y1>` | Bottom row of the geographic region of interest for analysis (can be interactively selected in `-view` mode). |
| `-left_x <x0>` | Left column of the geographic region of interest for analysis (can be interactively selected in `-view` mode). |
| `-right_x <x1>` | Right column of the geographic region of interest for analysis (can be interactively selected in `-view` mode). |
| `-topo <topo_file>` | Topographic image file (ACRES format), used for background display in viewing mode. |

## How It Works
`view_sel` has two primary modes: a non-interactive mode for calculating angular dependence statistics, and an interactive X-windows viewing mode.

**Non-Interactive Mode (Default, if `-view` is not used):**
1.  **Input Loading:** Loads backscatter, impinging angle, and optionally classification images (ACRES format).
2.  **Region Definition:** Determines the region of interest either from command-line arguments (`-top_y`, etc.) or by processing all available data. If `-class` is used, the region is implicitly defined by the valid pixels in the classification image within the specified range.
3.  **Data Accumulation (`calc_ang_dep` function):**
    *   Iterates through pixels within the defined region.
    *   For each pixel, if its backscatter and grazing angle values are valid and meet any classification criteria, it increments a counter in a `table_pointer[back_stbd_bin][graz_stbd_bin]` array. This array represents the density of backscatter versus grazing angle.
    *   It also accumulates raw backscatter values for mean and standard deviation calculations (without converting to dB).
4.  **Statistical Calculation:**
    *   Calculates the mean backscatter (`aver`) and standard deviation (`std_dev`) for each grazing angle bin from the `table_pointer` data.
    *   Calculates mean and standard deviation from the non-dB backscatter data (`Sbmean`, `Sbdev`) for each grazing angle.
5.  **Output Generation:**
    *   **`.table` file:** Generates a JHC image format file (`<prefix>.table`) visualizing the mean and standard deviation curves of backscatter vs. grazing angle.
    *   **`.mean` file:** Generates an ASCII file (`<prefix>.mean`) containing the statistical data, including mean and standard deviation of backscatter (in linear units and dB) for each grazing angle.
    *   **Image "Painting" (Optional):** If `-image` and `-class` are enabled, the specified image file can be modified by coloring pixels that meet the classification criteria.

**Interactive Viewing Mode (if `-view` is used):**
1.  **X-Windows Initialization:** Initializes an X-windows display, setting up main windows, sub-windows, and colormaps.
2.  **Image Display:** Loads the input image (specified by `-image` or derived from other inputs) and displays a decimated version of it in the main window.
3.  **Event Processing:** Enters an event loop to handle user interactions:
    *   **Rubber Band Selection:** Allows users to draw a "rubber band" rectangle on the main image.
    *   **Sub-image Viewing:** When a region is selected, a new sub-window is created (`view_subimage`) to display the selected area, potentially expanded.
    *   **Angular Plot (`view_plot`):** A sub-window can also be created to display the angular dependence plot (`table_pointer` content) for a selected region, showing mean and standard deviation curves.
    *   **Pixel Information:** Displays pixel coordinates and value when the mouse hovers over an image.
    *   **Masking:** Allows users to interactively define a mask.
    *   **Color Map Control:** Provides controls to adjust the color mapping.
4.  **`refresh_window`:** Handles window redrawing upon expose events or data updates.
5.  **Termination:** Exits when the user clicks an "EXIT" icon or presses 'e'.
