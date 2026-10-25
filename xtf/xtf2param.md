---
layout: default
title: xtf2param
parent: XTF Tools
nav_order: 13
tool_name: xtf2param
source_path: code/xtf/xtf2param.c
category: Lever-Arm & Calibration
input_formats: [".xtf"]
output_formats: [".param"]
related_tools: ["xtf2nav", "xtf2orientation", "xtf2omg_reson", "xtf2omg_r2sonic", "xtf2omg_simrad", "r2v"]
---

# xtf2param

## Overview
`xtf2param` reads the 1024-byte `XTFFILEHEADER` at the start of an XTF file and extracts the transducer (`ChanInfo[i]`), positioning antenna (`NavOffset`), and Motion Reference Unit (`MRUOffset`) lever-arm and angular alignment offsets into an ASCII OMG `.param` file. Because XTF logging software (e.g., Isis, Hypack, QINSy) often uses different vessel coordinate axis conventions than OMG, `xtf2param` provides a 3x3 rotation matrix builder (`-switch_axes`, `-flip_axis`) and angular sign flippers (`-flip_roll`, `-flip_pitch`, `-flip_gyro`) to map XTF offsets into the standard right-handed OMG coordinate convention:
* **$X$:** Positive forward
* **$Y$:** Positive starboard
* **$Z$:** Positive down
* **Roll:** Positive starboard down
* **Pitch:** Positive nose up
* **Heading:** Positive clockwise (to starboard)

## Usage
```bash
xtf2param [-v] [-debug] [-wlz <m>] [-switch_axes <a1> <a2>] [-flip_axis <x|y|z>] [-flip_roll] [-flip_pitch] [-flip_gyro] -xtf <inputfile.xtf> -omg <outputfile.param>
```

## CLI Options

| Flag | Arguments | Default | Description |
| :--- | :--- | :--- | :--- |
| `-xtf` | `<inputfile.xtf>` | **Required** | Path to the input `.xtf` file. |
| `-omg` | `<outputfile.param>` | **Required** | Path to the output ASCII `.param` file. |
| `-wlz` | `<meters>` | `0.0` | Waterline $Z$-coordinate (`WLZ`, positive down in meters relative to the reference point). |
| `-switch_axes` | `<axis1> <axis2>` | Identity matrix | Map OMG `<axis1>` (`x`, `y`, or `z`) to XTF `<axis2>` (`x`, `y`, or `z`). Note: When swapping two axes (e.g., X and Y), pass `-switch_axes x y -switch_axes y x` so every row and column of the rotation matrix has exactly one non-zero entry. |
| `-flip_axis` | `x` \| `y` \| `z` | Off | Negate the specified OMG axis row in the rotation matrix (e.g., `-flip_axis z` converts positive-up XTF $Z$ offsets into positive-down OMG $Z$ offsets). |
| `-flip_roll` | None | `+1` | Invert the sign of `OffsetRoll` and `MRUOffsetRoll`. |
| `-flip_pitch` | None | `+1` | Invert the sign of `OffsetPitch` and `MRUOffsetPitch`. |
| `-flip_gyro` | None | `+1` | Invert the sign of `OffsetYaw` and `MRUOffsetYaw`. |
| `-v` | None | Off | Enable verbose output. |
| `-debug` | None | Off | Print the 3x3 integer rotation matrix after each `-switch_axes` or `-flip_axis` operation. |

## How It Works
1. **Rotation Matrix Validation:** Initializes a 3x3 identity matrix (`rotation[i][i] = 1`), applies user-specified axis swaps (`-switch_axes`) and sign inversions (`-flip_axis`), and verifies that every row and column has exactly one non-zero entry (preventing degenerate projections).
2. **Header Parsing & Transformation:** Reads `XTFFILEHEADER`, writes `WLZ`, transforms each bathymetry channel's `(OffsetX, OffsetY, OffsetZ)` into `S1Z, S1X, S1Y, S1H, S1R, S1P` (and `S2*` if dual-head), transforms `(NavOffsetX, NavOffsetY, NavOffsetZ)` into `P1Z, P1X, P1Y, P1D`, writes zeroed `P2*` entries, and transforms `(MRUOffsetX, MRUOffsetY, MRUOffsetZ)` into `MSZ, MSX, MSY, MSR, MSP, MSG`, terminating with `END OF PARAMS`.

## Practical Examples

**1. Convert an XTF header where X is Starboard, Y is Forward, and Z is Up into OMG (+Fwd, +Stbd, +Down):**
```bash
xtf2param -debug -switch_axes x y -switch_axes y x -flip_axis z -wlz 1.85 -xtf line01.xtf -omg line01.param
```
