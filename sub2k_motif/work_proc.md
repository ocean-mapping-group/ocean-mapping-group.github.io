---
layout: default
title: work_proc
parent: SUB2K Motif Tools
grand_parent: code
nav_order: 21
---
# work_proc

## Description
`work_proc.c` is a Motif GUI source file that defines the `plug_away` function, which serves as an `XtWorkProc` (Xt Intrinsics work procedure) for the "Submetrix 2000 unraveller" application. This function is designed to perform computationally intensive tasks, such as parsing and processing Submetrix 2000 data, in the background. It allows the graphical user interface to remain responsive while data processing is ongoing. After processing data blocks, it triggers updates to the various drawing areas of the application.

## Function

### `Boolean plug_away()`
The work procedure that performs background data processing.
*   **Reads Data Blocks:** It calls `search_for_ping_start()` to find the beginning of the next data block (`block_type`, `block_size`) in the `SUBX_infile`. It then reads the data for that block into memory (`data`).
*   **Handles Data Blocks:** It calls `handle_SUBX_block()` (defined in `j_SUB2K.h` and implemented elsewhere, likely `readSUB2K.c`) to process the contents of the newly read data block.
*   **GUI Updates:** If the processed block is of type `0x00` or `0x16` (representing raw sonar data), it triggers updates to the application's drawing areas:
    *   Calls `draw_view()` for `DA1`, `DA2`, `DA3`, and `DA4` to refresh their displays according to their `display_state`.
    *   If `DA10.pixmap` exists (meaning the bathymetry window is active), it calls `draw_bathy()` to refresh the bathymetry display.
*   **End of File Check:** It checks if the end of the `SUBX_infile` has been reached. If so, it calls `stop_parse()` to remove itself as a work procedure.
*   **Returns:** `True` if processing is complete (EOF reached), `False` otherwise (meaning it should be called again by the Xt event loop).

## How It Works
`plug_away` is a classic example of how to keep a GUI application interactive during long computations. Instead of running the entire processing loop directly, which would block the X event loop and make the GUI unresponsive, `plug_away` processes a small chunk of data and then returns control to the event loop. This allows the GUI to handle events (like redraws, button clicks) before `plug_away` is called again. This cycle continues until `plug_away` signals completion by returning `True`.
*   It relies heavily on global variables (`SUBX_infile`, `block_type`, `block_size`, `ateof`, `data`, `file_length`, `DA1`, `DA2`, `DA3`, `DA4`, `DA10`, `display_state`) to manage file state, processing data, and GUI contexts.
*   The actual heavy lifting of parsing and interpreting the binary Submetrix data blocks is handled by `handle_SUBX_block()`.
