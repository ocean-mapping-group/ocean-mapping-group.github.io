# `JV_event_loop.c` - JView X-Windows Event Loop Handler

This C file acts as the central event handler for the `jview` application, an X-windows-based visualization and analysis tool. It continuously processes incoming X-events (such as keyboard presses, mouse clicks, and window events) and dispatches them to appropriate functions or widgets based on the event type and the window where the event originated. Essentially, this file embodies the "main loop" for user interaction within the `jview` application, translating raw user input into specific actions and updates to the graphical interface.

## Key Features and Functions

*   **`process_x_events()`:**
    *   The core function that runs an infinite loop to monitor and process all incoming X-events for the `jview` application.
    *   It intelligently filters out redundant `MotionNotify` events unless specifically needed (e.g., for rubber-banding).
    *   Events are first routed through `parse_which_widget()` to check if they belong to specialized widget managers (e.g., SVP editor, FFT2D terrain toolbox, Wave audio FFT toolbox). This modular approach allows for dedicated handling of complex GUI components.
    *   If an event is not handled by a specific widget, it is then processed by a large `switch` statement based on `event.type`, handling generic window and input events.

*   **Detailed Event Handling:**

    *   **Window Management Events:**
        *   `ConfigureNotify`: Dynamically updates global `width` and `height` variables when the main application window is resized.
        *   `UnmapNotify`: Handles events related to windows being unmapped.
        *   `Expose`: Manages window exposure events, triggering redraws while preventing excessive refreshes to optimize performance.
        *   `ColormapNotify`: Processes changes to the active colormap (though its implementation may be commented out or minimal).

    *   **Mouse Events:**
        *   `EnterNotify`, `LeaveNotify`: Controls the visual highlighting of icons and buttons as the mouse cursor enters or exits their respective areas, providing immediate visual feedback to the user.
        *   `MotionNotify`: Tracks continuous mouse movement, primarily used for "rubber-banding" selections or interactive drawing operations within various graphic and sub-windows when mouse buttons (`button1_down`, `button3_down`) are held down. It also provides real-time pixel information (coordinates, color, floating-point equivalent) during `button2_down` (middle-click) events.
        *   `ButtonPress`: Responds to initial mouse button presses:
            *   **Left-click (`button1`):** Typically initiates a rubber-banding selection.
            *   **Middle-click (`button2`):** A versatile action that posts detailed pixel information (geo-coordinates, data values), performs context-specific operations such as reading Gloria records, displaying Sound Velocity Profile (SVP) field data, defining watershed boundaries, manipulating line sections (if in `float_flag` mode), digitizing sounding points, calculating displacements, and searching for the closest navigation, SVP, or sidescan data points. It also checks for interactions with "pickrot" and "specbox" areas.
            *   **Right-click (`button3`):** Can initiate rubber-banding (specifically for `sub_window[36]`), trigger cross-section viewing, enable SVP editing, center "pickrot" boxes, or adjust range and color limits.

    *   **Keyboard Events (`KeyPress`):** A comprehensive `switch (keysym)` block maps numerous keyboard shortcuts to a wide array of functionalities, offering efficient control over the application:
        *   **Display/Visualization Controls:** Toggles vector displays (`KEY_SPACE`), navigation overlays (`XK_N`), cross-section viewing (arrow keys in `graphic_window[0]`), histogram generation (`XK_h`), colormap inversion (`XK_i`), logarithmic colormap display (`XK_l`), and switches between different DTM visualization modes (Depth, Sun-illuminated, Pseudo-color via specific `button_window` clicks).
        *   **Editing/Manipulation:**
            *   **Pick-Rotation Boxes (`pickrot_flag`, `editrot_flag`):** Allows precise rotation (`KEY_1`, `KEY_9`, `KEY_PG_UP`, `KEY_PG_DOWN`, `KEY_PLUS`, `KEY_MINUS`), resizing (arrow keys), creation of new boxes (`XK_n`), setting of center points (via `button3` press in `graphic_window[0]`), and dumping box configurations to file (`KEY_ESC`).
            *   **Side-Scan View (SSVIEW):** Controls zoom levels (`KEY_PLUS`, `KEY_MINUS`), along-track zoom, and center adjustments.
            *   **Data Shifting:** Enables shifting of data (`KEY_PLUS`, `KEY_MINUS` in conjunction with `shift_dn_flag`).
            *   **Digitization:** Facilitates digitizing new sounding points (`button2`) and replacing existing ones (`XK_r`).
            *   **Filtering:** Applies various filters (`KEY_A` for average, `XK_m` for median) if `bpick_flag` is active.
        *   **Survey Planning Mode (`survey_planning_mode`):** Provides extensive tools for managing survey lines:
            *   Toggling the mode itself (`XK_P`).
            *   Reordering lines (`XK_3`, `XK_numbersign`).
            *   Adjusting line spacing (`XK_bracketleft`, `XK_bracketright`) and its increment (`XK_braceleft`, `XK_braceright`).
            *   Adding parallel lines (`XK_parenleft`, `XK_parenright`).
            *   Removing (`XK_d`), reversing (`XK_r`), extending (`XK_e`), splitting (`XK_s`), and joining (`XK_j`) selected lines.
            *   Writing the current line list to a file (`XK_w`).
            *   Setting a survey baseline (`XK_n`).
        *   **File Operations:** Supports dumping images to PPM format (`XK_d`), writing histograms (`XK_w`), saving pick-rotation box configurations (`KEY_ESC`), and storing digitized soundings (`KEY_ESC`, `button2`).
        *   **Color/Colormap Controls:** Allows direct manipulation of colormaps by toggling individual color channels (`icon_window[2-4]`), switching to grayscale (`icon_window[5]`), enabling false color displays (`icon_window[1]`), cycling through colormap palettes (`icon_window[6]`), loading custom colormaps (`icon_window[8]`), and saving the current colormap (`XK_c`).
        *   **Exit:** Provides standard keys for exiting the application (`KEY_ESC`, `KEY_X`, `KEY_Q`).

*   **`parse_which_widget(XEvent event)`:**
    *   A crucial dispatching function that checks the window associated with an `XEvent` to determine if it belongs to a specific, specialized widget (e.g., the SVP editor, the FFT2D terrain toolbox, or the Wave audio FFT toolbox). If a match is found, the event is then forwarded to the respective widget's dedicated event handler (`manage_SVP_events`, `manage_FFT2D_widget_events`, `manage_WAVFFT_widget_events`), promoting modularity and cleaner event processing.

*   **`set_survey_baseline(...)`:**
    *   A utility function specifically used within the survey planning mode to define and establish a baseline survey line.

## Dependencies

This module is heavily reliant on several internal libraries and header files, which collectively provide the necessary graphical primitives, utility functions, and domain-specific data structures for the `jview` application:

*   `JV_global.h`: Contains global variables, shared structures, and common definitions utilized across various components of the `jview` suite.
*   `JV_svpedit.h`: Provides declarations and definitions for managing events and data related to Sound Velocity Profile (SVP) editing.
*   `JV_FFT2D.h`: Offers declarations for managing events and data pertinent to the 2D FFT widget, enabling spectral analysis features.
*   `JV_play_WAV.h`: Includes declarations for handling events and controls associated with WAV audio playback functionality.
*   **Internal Utility Functions:** The file extensively uses functions prefixed with `jhc_` (J.H.C. utility functions for graphics and calculations), `jcu_` (J.C.U. utility functions), and various `d_` (drawing/display), `update_`, `plot_`, and `refresh_` functions, which are responsible for low-level graphical operations, data processing, and screen rendering within the `jview` environment.

## Usage

`JV_event_loop.c` is fundamental to the interactivity and overall user experience of the `jview` application. By robustly handling diverse user inputs and dispatching them to the correct processing logic, it enables users to seamlessly interact with complex scientific data visualizations, perform analytical tasks, and manage survey operations within a responsive graphical environment.