---
layout: default
title: test_tvg_dirindex
parent: Mock Tools
grand_parent: sidescan
nav_order: 14
---
# test_tvg_dirindex

## Description
`test_tvg_dirindex` is a diagnostic utility primarily designed to test and display components related to the backscatter equation and beam directivity in sidescan sonar processing. It can:
*   **Test TVG Function:** Display the Time-Varying Gain (TVG) function and attenuation curves as a function of range.
*   **8-bit to 12-bit Conversion:** Convert an 8-bit digital number to a 12-bit equivalent (`-bell`).
*   **Beam Pattern Lookup:** Test a lookup function from a pre-computed beam pattern file (`-lookup`).
*   **Directivity Index Calculation:** Calculate the port and starboard directivity indices based on a 2D integration of beam patterns.

This tool is useful for verifying the behavior of acoustic models and lookup tables used in quantitative backscatter calculations.

## Usage
```bash
test_tvg_dirindex [-DB <constant>] [-dx <value>] [-rep <rate>] [-tvg] [-bell] [-lookup <filename>] [-depth <seafloor_depth>] [-min_beam <gain>]
```

## Arguments

| Option | Description | Default |
|---|---|---|
| `-DB <constant>` | Specifies a constant value (in dB) for TVG calculations (e.g., related to two-way spreading loss). | `137.6` |
| `-dx <value>` | Specifies the range increment (in meters) for TVG and attenuation calculations. | `500` |
| `-rep <rate>` | Specifies the repetition rate (e.g., ping rate). | `20` |
| `-tvg` | Activates the TVG function test mode. | (None) |
| `-bell` | Activates the 8-bit to 12-bit conversion test mode. Prompts for 8-bit input. | (None) |
| `-lookup <filename>` | Activates the beam pattern lookup test mode. Specifies the JHC image file containing the beam pattern. | (None) |
| `-depth <seafloor_depth>` | Specifies the simulated seafloor depth (in meters) for use in some calculations (e.g., slant range for TVG). | `3000` |
| `-min_beam <gain>` | Specifies a minimum beam gain factor, used in backscatter calculations. | `0.0` |

## How It Works
The tool's functionality depends on the activated flags:

**1. TVG Function Test (`-tvg`):**
*   **TVG and Attenuation Calculation:** It iterates through various ranges, calculating:
    *   `gain`: Inverse TVG function for a given range and `-DB` constant.
    *   `atten`: Two-way spherical spreading and absorption loss.
    *   `neil`: Value from a pre-computed `tvg` array (likely from `tvg_shading_loss`).
*   **Output:** Prints range, attenuation (in dB), calculated gain (in dB), and pre-computed TVG (in dB) to standard output.

**2. 8-bit to 12-bit Conversion Test (`-bell`):**
*   **Input:** Interactively prompts the user to enter an 8-bit number.
*   **Conversion:** Uses the `bit8_to_bit12` function to convert the 8-bit input to a 12-bit float value.
*   **Output:** Prints both the 8-bit and 12-bit values.

**3. Beam Pattern Lookup Test (`-lookup`):**
*   **Load Beam Pattern:** It loads a beam pattern (JHC image file) specified by `<filename>` into memory.
*   **Input:** Interactively prompts the user for a `depth` and `range`.
*   **Lookup:** Uses `get_JHC_lookup_value` to retrieve a value from the loaded beam pattern for the given `depth` and `range`.
*   **Output:** Prints the returned lookup value.

**4. Directivity Index Calculation (Default Mode, if no other flags):**
*   **Beam Pattern Integration:** It numerically integrates the power response of a GLORIA transducer over a 2D angular space (horizontal and vertical angles from -89 to 89 degrees).
*   **Vertical Beam Pattern:** Calculates the vertical directivity `vert_pow` using a two-point array model and a circular transducer model (similar to `beams.c`).
*   **Horizontal Beam Pattern:** Calculates the horizontal directivity `hori_pow` using a simpler array model.
*   **Total Power:** Multiplies `hori_pow` and `vert_pow` and sums over all angles.
*   **Directivity Index:** The directivity index is calculated as `1.0 / (total_power / number_of_sums)`. This is done for both port and starboard frequencies (`PORT_FREQ`, `STBD_FREQ`).
*   **Output:** Prints the calculated port and starboard directivity indices.
