---
layout: default
title: EK_event_loop (Module within EKlook)
parent: Simrad EK60/EK80 Echosounder Suite (EKlook)
grand_parent: 3. Sidescan, Echosounders, ADCP & Sub-Bottom
nav_order: 4
tool_name: EK_event_loop
source_path: code/EKlook/EK_event_loop.c
category: EKlook
input_formats:
- X11 User Input Events
output_formats:
- GUI State Updates & Widget Dispatch
related_tools:
- EKlook
- EK_ZoomImage
- EK_BottomBS
- EK_Polar
- EK_FFT
- EK_PosMotion
---

# EK_event_loop (Module within EKlook)

## Description
`EK_event_loop.c` defines the core X11 event processing loop for the interactive [`EKlook`](EKlook.html) application. It continuously monitors mouse clicks, rubber-band drags, scroll-wheel actions, and keyboard shortcuts across the main thumbnail/histogram window and dispatches specialized widget events to [`EK_ZoomImage`](EK_ZoomImage.html), [`EK_BottomBS`](EK_BottomBS.html), [`EK_Polar`](EK_Polar.html), [`EK_FFT`](EK_FFT.html), and [`EK_PosMotion`](EK_PosMotion.html).

## Key Functionality and Interactions

| Interaction Type | Description | Controls / Bindings |
|---|---|---|
| **Event Dispatcher** | Monitors X11 events and routes them to active `EKlook` sub-windows (`FFT`, `POLAR`, `ZOOM`, `BOTTOM`, `POSMOTION`) or handles main-window actions. | |
| **Main Loop Control** | Terminates the application cleanly when the Exit button or quit key is pressed. | `Q` or `ESC` |
| **Zooming & Region Selection (Main Thumbnail)** | Rubber-band dragging in `graphic_window[1]` sets `zoomfirstsam`, `zoomlastsam`, `zoomfirsttrace`, and `zoomlasttrace`; a single click sets `min_target_sample`. | Left Mouse Button (Click & Drag) |
| **Trace Navigation (Main Thumbnail)** | Selects or steps `currenttrace` and refreshes all open sub-windows in real time. | Middle Mouse Click, Mouse Wheel (UP/DOWN), Arrow Keys (UP/DOWN) |
| **Display Threshold Adjustments (Histogram `graphic_window[2]`)** | Sets `mindB` (Left Click), `maxdB` (Right Click), or `trimdB` target search threshold (Middle Click) directly on the power histogram. | Left / Middle / Right Mouse Click, Arrow Keys (LEFT/RIGHT) |
| **Toggle Display & Sub-Windows** | Maps/unmaps sub-windows (`Image`, `Grey/Col.`, `FFT`, `Polar`, `BD/ARC`, `PosMotion`) and toggles bottom-track overlays (`showTrack`). | `KEY_SPACE`, Toolbar Icon Buttons |
