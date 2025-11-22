---
layout: default
title: Str2XmString
parent: SUB2K Motif Tools
grand_parent: code
nav_order: 18
---
# Str2XmString

## Description
`Str2XmString` is a small C utility function designed to convert a standard NULL-terminated C string (`char *`) into an `XmString` (Motif string). `XmString` is a compound string data type used by Motif widgets for displaying text, which supports features like internationalization, multiple fonts, and text direction. This function provides a convenient way to integrate standard C strings into Motif GUI elements.

## Function

### `XmString Str2XmString(char *string)`
Converts a standard C string to an `XmString`.
*   `string`: A pointer to the NULL-terminated C string to be converted.
*   **Returns:** An `XmString` representation of the input string. This `XmString` should typically be freed by the caller using `XmStringFree` when it is no longer needed to prevent memory leaks.

## How It Works
The function uses the Motif library call `XmStringCreateLtoR()`:
*   `XmStringCreateLtoR(string, XmSTRING_DEFAULT_CHARSET)` creates an `XmString` from the input `char *string`.
*   `XmSTRING_DEFAULT_CHARSET` specifies the character set to be used for the conversion, typically the default character set of the locale.
This function provides a simple yet essential bridge between standard C string handling and Motif's `XmString` text management.
