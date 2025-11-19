# EK_event_loop (Module within EKlook)

## Description
`EK_event_loop.c` defines the core event processing loop for the interactive `EKlook` X-window application. It is not a standalone command-line tool but rather a fundamental component that continuously monitors and responds to user interactions (mouse clicks, keyboard presses, window events) within the `EKlook` GUI. It dispatches events to various widgets (like FFT, POLAR, ZOOM, BOTTOM, POSMOTION widgets) for specialized handling, and manages interactions within the main `EKlook` window, such as zooming, scrolling through traces, and adjusting display parameters.

## Key Functionality and Interactions

This module facilitates the following interactions within the `EKlook` GUI:

*   **Event Dispatcher:** Continuously monitors for X events (e.g., mouse clicks, key presses, window exposures, motion notifications) and dispatches them to the relevant `EKlook` widgets (FFT, POLAR, ZOOM, BOTTOM, POSMOTION) for specific handling. Events not handled by a specific widget are processed by the main event loop.
*   **Main Loop Control:** Manages the overall execution of the `EKlook` application's event loop. The application terminates upon detecting an 'Exit' command from a button or a specific key press (e.g., `Q` or `ESC`).
*   **Zooming and Region Selection (Main Image Window):**
    *   **Rubber-banding (Left Mouse Button):** Allows users to click and drag a rectangle in the main image window (`graphic_window[1]`). Upon button release, if sufficient movement occurred, this defines the `zoomfirstsam`, `zoomlastsam`, `zoomfirsttrace`, and `zoomlasttrace` variables, updating the zoomed view.
    *   **Single Click (Left Mouse Button):** If a rubber-band selection has minimal movement, a single click sets `min_target_sample`, influencing target detection parameters.
*   **Trace Navigation and Selection (Main Image Window):**
    *   **Middle Mouse Button Click:** Sets the `currenttrace` to the trace number corresponding to the click location, updating displayed information and widget views.
    *   **Mouse Wheel Scroll (UP/DOWN):** Increments/decrements the `currenttrace` variable, effectively scrolling through the available traces.
    *   **Arrow Keys (UP/DOWN):** Provides an alternative method for incrementing/decrementing the `currenttrace`.
*   **Display Adjustments (Histogram Window `graphic_window[2]`):**
    *   **Left Mouse Button Click:** Sets the `mindB` (minimum display dB value) based on the click's X-coordinate.
    *   **Right Mouse Button Click:** Sets the `maxdB` (maximum display dB value) based on the click's X-coordinate.
    *   **Middle Mouse Button Click:** Sets the `trimdB` (trim dB value for target searching) based on the click's X-coordinate.
    *   **Arrow Keys (LEFT/RIGHT):** Adjusts `mindB` or `maxdB` values by increments.
*   **Toggle Display Options:**
    *   **`KEY_SPACE` (Main Image Window):** Toggles `showTrack` which can display the zoom window outline or bottom detection attempts.
    *   **Icon Buttons:** Handles clicks on various icon buttons (e.g., "Image", "Grey/Col.", "FFT", "Polar", "BD/ARC", "PosMotion") to map/unmap corresponding widget windows, toggle color schemes, or switch between detection modes (e.g., `WhichTraceforAmplitudeDetect` for `POLAR` vs `BOTTOM` widgets).

## Note
This module functions as the central nervous system for the `EKlook` graphical user interface. It does not accept direct command-line arguments for its operation, as its sole purpose is to manage and respond to interactive input within the running `EKlook` application. Its behavior is entirely dependent on the user's actions within the GUI.