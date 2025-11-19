# EK_BottomBS (Module within EKlook)

## Description
`EK_BottomBS` is a module within the `EKlook` interactive application. Its primary role is to manage the "BOTTOM Detect / ARC window," a graphical user interface element that allows users to interactively adjust parameters related to bottom detection and Angular Response Curve (ARC) generation for EK series echosounder data. This module provides controls for applying various corrections, enabling depth and mount angle guides, flushing or dumping ARCs, and visualizing the processed data within `EKlook`.

## Interactive Controls

This module exposes the following interactive controls within the `EKlook` application:

| Control | Description | Related Variable |
|---|---|---|
| **Buttons (Toggle Corrections)** | | |
| `addTL` | Toggles the inclusion of Transmission Loss (TL) corrections in ARC calculations. | `BSaddTL` |
| `addBP` | Toggles the inclusion of Beam Pattern (BP) corrections in ARC calculations. | `BSaddBP` |
| `addArea` | Toggles the inclusion of Ensonified Area (Area) corrections in ARC calculations. | `BSaddArea` |
| `depthGuide` | Toggles the use of Nadir Depth as a guide for bottom detection. | `useNadirDepthGuide` |
| `mountGuide` | Toggles the use of Mount Angle as a guide for bottom detection. | `useMountAngleGuide` |
| **Buttons (ARC Operations)** | | |
| `dump BStrack` | Dumps bottom track parameters to a file. | |
| `flushARC` | Clears the accumulated Angular Response Curves (ARCs). | `ARC_cummulative`, `ARC_byPing` |
| `dump ARC` | Dumps the current accumulated ARC to a file. | `ARC_cummulative` |
| `stack all ARC` | Stacks all envelopes into a cumulative ARC and dumps it. | `ARC_cummulative` |
| `show Area/Grazing` | Toggles the display of ensonified area versus grazing angle. | `showAreaGrazing` |
| **Sliders** | | |
| `Angle Sensitivity` | Adjusts the angle sensitivity for along and across angles. | `Along_AngleSensitivity` (and `Across_AngleSensitivity`) |
| `Bulk Calibration` | Adjusts a bulk calibration value (in dB) applied to the backscatter. | `BulkCalibration` |
| `Nadir Depth` | Sets the nadir depth used as a guide. | `NadirDepth` |
| `Mount Angle` | Adjusts the roll mount angle of the EK system. | `EKMountAngle.roll` |
| `Sub-Window FFT Length` | Controls the size of the envelope window for FFT analysis (e.g., 64, 32, 16, 8, 4, 2). | `envWinSize` |

## Visualizations

The module displays various graphical representations within the `EKlook` application:
*   **Matched-Filtered Echo Envelope (dB):** Shows the envelope of the echo.
*   **Fore/Aft Phase:** Displays the raw and low-pass filtered phase.
*   **Port/Starboard Phase:** Displays the raw and low-pass filtered phase.
*   **Highlighted Envelope Subwindow Spectrum:** Shows the FFT spectrum of a selected subwindow of the envelope.
*   **Apparent Echo Envelope using Highlighted Frequency Slice:** Displays the envelope using a specific frequency slice.
*   **Highlighted Envelope Subwindow I/Q (In-phase/Quadrature) data:** Shows the raw I and Q components and magnitude.
*   **ARC (Angular Response Curve) Window:** Plots the ARC, including individual ping ARCs and cumulative ARCs.
*   **ARC Count Window:** Displays the normalized bin counts for the ARC.

## Key Bindings (within the module's graphic windows)

*   `KEY_Z`: Zeros or resets a selected slider's value (e.g., Angle Sensitivity to default, Bulk Calibration to 0, Nadir Depth to 100, Mount Angle to 35, EnvWinSize to 23).
*   `KEY_Q` / `KEY_ESC`: Closes the "BOTTOM Detect / ARC window."
*   `KEY_UP` / `KEY_DOWN`: Adjusts the `BSmax` and `BSmin` (backscatter display range) in the ARC plot.
*   `KEY_LEFT` / `KEY_RIGHT`: Adjusts selected slider values or navigates through envelope subwindows and frequency slices.
*   `KEY_SPACE`: Toggles `whichARC` (displaying either broadband trace directly or FFT bin counts).
