---
layout: default
title: glgain
parent: Gain Tools
grand_parent: sidescan
nav_order: 2
---
# glgain

## Description
`glgain` is a utility designed to apply gain adjustments to JCU GLORIA format sidescan files. It allows for independent control over the port and starboard sides, applying either multiplicative or additive gain factors. Additionally, it includes a `fixsb` flag that performs specific hardcoded manipulations on pixel values, likely for a particular sensor or data anomaly.

## Usage
```bash
glgain [-add] [-fixsb] [-start <ping>] [-end <ping>] [-port <gain_value>] [-stbd <gain_value>] <infile> <outfile>
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-add` | If specified, the gain value(s) will be *added* to the pixel intensities instead of multiplied. | Multiply |
| `-fixsb` | Activates a hardcoded set of pixel value manipulations for both port and starboard sides. This appears to filter out or remap specific digital number (DN) values. | (None) |
| `-start <ping>` | Specifies the starting ping number (record) from which to apply the gain. | `0` |
| `-end <ping>` | Specifies the ending ping number (record) up to which to apply the gain. | `100000` |
| `-port <gain_value>` | Specifies the gain factor to apply to the port side data. | `1.0` |
| `-stbd <gain_value>` | Specifies the gain factor to apply to the starboard side data. | `1.0` |
| `<infile>` | **Required.** The input JCU GLORIA file. |
| `<outfile>` | **Required.** The output JCU GLORIA file with gain adjustments applied. |

## How It Works
1.  **Input/Output File Handling:** The tool opens the input GLORIA file for reading and the output file for writing.
2.  **Record-by-Record Processing:** It iterates through each record (ping) in the input file.
3.  **Ping Range Check:** Gain is only applied to records falling within the specified `-start` and `-end` ping numbers.
4.  **Port Side Gain:**
    *   If `-port` is specified (and `port_gain` is not 1.0):
        *   For each pixel on the port side:
            *   If the pixel value is 255 (unassigned), it remains 255.
            *   Otherwise, if `-add` is specified, `port_gain` is added; otherwise, it's multiplied.
            *   The resulting value is clamped to a maximum of 254.
5.  **Starboard Side Gain:**
    *   If `-stbd` is specified (and `stbd_gain` is not 1.0):
        *   For each pixel on the starboard side, the process is identical to the port side.
6.  **`fixsb` Flag Logic:**
    *   If `-fixsb` is set, a series of `if-else if` statements are executed for both port and starboard pixels. This logic specifically checks for and remaps certain pixel values:
        *   Values `8, 9, 10, 11, 13` are remapped to `255`.
        *   Values `12, 14` are remapped to `0`.
        *   A value of `255` is remapped to `254`.
        *   Other values might trigger error messages for values less than 8 or exactly 15. This suggests a very specific data-cleaning or anomaly-fixing routine.
7.  **Write Output:** The modified `glo_rec` is written to the output file.
8.  **Loop:** This process repeats for all records in the input file.
