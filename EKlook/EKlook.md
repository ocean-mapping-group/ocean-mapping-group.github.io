# EKlook

## Description
`EKlook` is an interactive X-window application designed for visualizing and analyzing EK series echosounder data, particularly focusing on matched-filtered traces. It allows users to examine various aspects of the echosounder data, including trace power, phase, bottom detection, and angular response, through a graphical interface with several specialized widgets. The tool supports loading background maps, area files, and sphere target strength models for comprehensive analysis.

## Usage
```bash
EKlook [OPTIONS] -prefix <EK_file_prefix>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-mountangle <degrees>` | Forces a specific mount roll angle (in degrees) for calculations. If used with `-guidedepth`, it attempts to guess better min/max depths. | `45.0` |
| `-guidedepth <meters>` | Forces a specific nadir depth (in meters) for calculations. If used with `-mountangle`, it attempts to guess better min/max depths. | `400.0` |
| `-sensitivity <value>` | Sets the Angle Sensitivity for along and across angles. | `10.0` |
| `-twowaybeamwidth <degrees>` | Sets the two-way beam width in degrees. | `12.0` |
| `-backdrop <orthomap.mos>` | Specifies an 8-bit image file to use as a geographic backdrop in the position/motion view. | `orthomap.mos` |
| `-areas <AreaMapFileName(s)>` | Specifies one or more area map files (e.g., `.r4` files) for defining spatial regions of interest. | `custom_rot_mapsheet.r4` |
| `-sphereTS <sphereTS_filename>` | Specifies a file containing sphere target strength data versus frequency for comparison. | `TSvFreq.dat` |
| `-prefix <EK_file_prefix>` | **Required.** Specifies the file prefix for the EK data files (e.g., `matchedfilted`). The tool will look for files like `EK_file_prefix.MF_dB`. | `matchedfilted` |
| `-forgot` | Adjusts `mindB`, `maxdB`, and `trimdB` by subtracting 120.0 dB, typically for older data or specific sensor types. Also disables `BulkCalibration`. | |

## Interactive Widgets / Views

`EKlook` provides several interactive sub-windows (widgets) for detailed analysis:
*   **ZOOM EK-Trace window:** For zoomed-in viewing and analysis of individual traces (managed by `EK_ZoomImage.c`).
*   **FFT EK-Trace window:** For Fast Fourier Transform analysis of trace segments (managed by `EK_FFT.c`).
*   **POLAR EK-Trace window:** For polar plots of target strength and phase information (managed by `EK_Polar.c`).
*   **BOTTOM Detect / ARC window:** For adjusting bottom detection parameters and generating Angular Response Curves (ARCs) (managed by `EK_BottomBS.c`).
*   **Position-Motion EK-Trace window:** For visualizing geographic position, vessel motion, and bottom strike points in 2D and 3D (managed by `EK_PosMotion.c`).

## General Interactions
*   **Main Thumbnail Image:** An overview of the entire file's trace power, allowing selection of zoomed regions.
*   **Power Histogram:** A histogram of trace power, used for adjusting display greyscale/color ranges.
*   **Mouse Wheel:** Scrolls through traces in the main thumbnail view.
*   **Middle Mouse Button Click (Main Thumbnail):** Selects a `currenttrace` for detailed analysis in other widgets.
*   **Left Mouse Drag (Rubber Banding, Main Thumbnail):** Defines a new zoom area for detailed inspection.

## Note
`EKlook` is an interactive graphical application. While it takes initial command-line arguments, much of its functionality and analysis is performed through the GUI. The descriptions of its sub-modules (`EK_ZoomImage`, `EK_FFT`, `EK_Polar`, `EK_BottomBS`, `EK_PosMotion`) provide more detail on the interactive controls and visualizations available within each specific window.