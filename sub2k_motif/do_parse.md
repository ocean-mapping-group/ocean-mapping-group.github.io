---
layout: default
title: do_parse
parent: SUB2K Motif Tools
grand_parent: code
nav_order: 7
---
# do_parse

## Description
`do_parse.c` is a Motif GUI source file that provides functions for controlling the parsing of Submetrix 2000 data within the "Submetrix 2000 unraveller" application. It allows the application to initiate data parsing as a background process (`go_parse`) and to halt this process (`stop_parse`). The parsing itself is executed by a work procedure (`plug_away`) integrated into the Xt Intrinsics event loop, ensuring the GUI remains responsive during potentially long parsing operations.

## Functions

### `void go_parse()`
Initiates the data parsing process.
*   Checks if a file is `opened`. If not, it prints a message and returns.
*   If a file is open, it adds `plug_away` as an `XtWorkProc` to the Xt application context, which causes `plug_away` to be called repeatedly by Xt whenever there are no pending X events.

### `void stop_parse()`
Stops the currently running data parsing process.
*   Removes the `plug_away` work procedure from the Xt application context, effectively halting the background parsing.

## How It Works
This module utilizes the Xt Intrinsics work procedure mechanism to perform CPU-intensive tasks (like data parsing) in the background without freezing the graphical user interface.
1.  **Work Procedure (`plug_away`):** The `plug_away` function (defined elsewhere, likely in `RTsubx.c`) contains the actual logic for reading and processing the Submetrix 2000 data.
2.  **`XtAppAddWorkProc`:** When `go_parse` is called, `XtAppAddWorkProc` schedules `plug_away` to be executed by Xt. The Xt event loop will call `plug_away` whenever there are no events to process, allowing incremental parsing.
3.  **`XtRemoveWorkProc`:** When `stop_parse` is called, `XtRemoveWorkProc` removes `plug_away` from the schedule, stopping its execution.
This separation ensures that the GUI remains interactive while data processing occurs in the background, providing a better user experience for large data files.
