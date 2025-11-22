---
layout: default
title: set_values
parent: SUB2K Motif Tools
grand_parent: code
nav_order: 16
---
# set_values

## Description
`set_values.c` is a Motif GUI source file that provides a function (`set_values`) to populate the text input fields of the "Spacings" and "Thresholds" configuration dialogs. Its primary purpose is to ensure that when these dialogs are displayed, the text widgets reflect the current values of the global parameters they control, providing up-to-date feedback to the user.

## How It Works
1.  **`set_values()` function:**
    *   This function uses `XtSetValues` to update the `XmNvalue` resource of various `XmText` (or `XmTextField`) widgets.
    *   **Spacing Parameters:** It retrieves the current values of global variables such as `PORT_NOMINAL_SPACING`, `PORT_AB_AC_ratio`, `PORT_AB_AD_ratio`, `STBD_NOMINAL_SPACING`, `STBD_AB_AC_ratio`, and `STBD_AB_AD_ratio`. These `float` values are formatted into strings using `sprintf` and then set as the `XmNvalue` for `SpacingText1` through `SpacingText6` respectively.
    *   **Threshold Parameters:** Similarly, it retrieves the current integer values of global variables `athresh`, `pthresh`, `oftotal`, `nobelow`, and `firstsam`. These are formatted into strings and set as the `XmNvalue` for `ThresholdText1` through `ThresholdText5` respectively.
This function effectively synchronizes the displayed GUI values with the internal application state, making the configuration dialogs user-friendly.
