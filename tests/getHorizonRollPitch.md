---
layout: default
title: getHorizonRollPitch
parent: Acoustic & Mathematical Test Harnesses (tests)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 8
tool_name: getHorizonRollPitch
source_path: code/tests/getHorizonRollPitch.c
category: Attitude Error & Geometry Plotting (tests)
input_formats:
- Left-side 2-column ASCII intensity/gradient profile (xval, yval)
- Right-side 2-column ASCII intensity/gradient profile (xval, yval)
output_formats:
- temp.rollpitch (ASCII report of left/right horizon positions, roll, pitch, and vertical pixel shift)
related_tools:
- twistVRU
- testrot
- DelayEditor
---

# getHorizonRollPitch

## Overview
`getHorizonRollPitch` (`code/tests/getHorizonRollPitch.c`, authored by John Hughes Clarke in September 2020) computes vessel/camera roll angle, pitch angle, and vertical pixel shift from a pair of vertical image intensity/gradient profiles extracted along the left (`leffile`) and right (`rigfile`) sides of a shipboard horizon-tracking camera frame.

By detecting the vertical pixel coordinate (`xval`) where the intensity/edge metric (`yval`) first exceeds a user-defined `-threshold` on both the left and right sides of the image, the tool calculates the horizon tilt (roll) across the horizontal pixel separation (`-acrossdist`) and the horizon elevation offset (pitch) relative to the nominal zero-pitch pixel row (`-pitchlevel`) and focal length in pixels (`-alongdist`).

---

## Syntax & CLI Options

```bash
getHorizonRollPitch [-v] [-threshold <val>] [-acrossdist <px>] \
                    [-pitchlevel <px>] [-alongdist <px>] \
                    <left_profile.txt> <right_profile.txt>
```

| Option | Description | Default |
| :--- | :--- | :--- |
| `<left_profile.txt>` | **Required.** Positional argument 1: 2-column ASCII file (`pixel_row intensity`) for the left column of the horizon image. | None |
| `<right_profile.txt>` | **Required.** Positional argument 2: 2-column ASCII file (`pixel_row intensity`) for the right column of the horizon image. | None |
| `-threshold <val>` | Intensity or edge-gradient threshold (`yval > threshold`) used to trigger horizon detection on both profiles (parsed via `strtoint`). | `5.0` |
| `-acrossdist <px>` | Horizontal pixel distance separating the left and right vertical scan lines (`acrossdist`). | `1600` |
| `-pitchlevel <px>` | Reference vertical pixel coordinate corresponding to $0^\circ$ pitch (`pitchlevel`). | `500` |
| `-alongdist <px>` | Effective along-axis focal distance in pixels (`alongdist`) used to convert vertical pixel offset into pitch angle. | `500` (`USAGE` shows `800`) |
| `-v` | Increment verbose flag (`verbose_flag++`). | `0` |

---

## Horizon Detection & Trigonometric Equations

1. **Threshold Horizon Picking:**
   * Scans `leffile` line-by-line (`fscanf(leffile, "%f%f", &xval, &yval)`) and records `leftrange = xval` at the first sample where `yval > threshold`.
   * Scans `rigfile` line-by-line and records `rightrange = xval` at the first sample where `yval > threshold`.
   * Computes the midpoint horizon row:
     $$\bar{y}_{\text{horiz}} = \text{averagerange} = \frac{y_{\text{left}} + y_{\text{right}}}{2}$$

2. **Roll and Pitch Calculation:**
   Using the horizontal pixel baseline $D_{\text{across}}$ (`acrossdist`), effective focal distance $D_{\text{along}}$ (`alongdist`), and zero-pitch horizon row $y_0$ (`pitchlevel`), roll and pitch (in degrees) are computed as:

   $$\text{Roll} = \frac{180}{\pi} \arctan\!\left(\frac{y_{\text{left}} - y_{\text{right}}}{D_{\text{across}}}\right)$$

   $$\text{Pitch} = \frac{180}{\pi} \arctan\!\left(\frac{\bar{y}_{\text{horiz}} - y_0}{D_{\text{along}}}\right)$$

   $$\Delta y_{\text{pix}} = \text{vertpixshift} = \bar{y}_{\text{horiz}} - y_0$$

---

## Output File (`temp.rollpitch`)

`getHorizonRollPitch` always writes its results to `temp.rollpitch` in the current working directory (as well as printing summary lines to `stdout`):

```text
 left  482.000000
 right  514.000000
 average  498.000000
roll -1.145763
pitch -0.143239
vertpixshift -2.000000
```

---

## Example Usage

```bash
# Compute horizon roll and pitch from left/right vertical edge profiles
getHorizonRollPitch -threshold 15 -acrossdist 1600 -pitchlevel 500 -alongdist 800 \
                    frame001_left.prof frame001_right.prof
cat temp.rollpitch
```
