---
layout: default
title: mix_ci
parent: Bathymetric Gridding & Export (grid)
grand_parent: 2. Gridding, Mosaicking & Interactive Editors
tool_name: mix_ci
source_path: code/grid/mix_ci.c
category: gridding
input_formats:
- .8bit (color depth map)
- .sun (8-bit sun-illumination intensity map)
- .maskmap (8-bit stencil mask)
- .band1/.band2/.band3 (3-band RGB backdrop)
output_formats:
- .8bit (JHC 8-bit composite color-intensity raster)
- .ppm (24-bit RGB Portable Pixmap)
related_tools:
- addSUN
- r4to8bit
- maskarray
- selectcb
---

# mix_ci

## Overview

`mix_ci` combines an 8-bit depth/attribute **color map (`-c`)** and an 8-bit sun-illuminated **intensity map (`-i`)** into either:
1. An **8-bit indexed color-intensity `JHC_header` image** (default, using `base + color_bin * shades + shade_bin`, e.g., 8 colors $\times$ 30 shades + 16 = 256 levels), or
2. A **24-bit true-color RGB `.ppm` image (`-ppm`)** computed via continuous HSV-to-RGB transformation (`hue = 300 - 300*(color/255)`, `sat = 0.3 + 0.2*(color/255)`, `val = sun/255`), with optional stencil masking (`-mask`) and background underlay compositing (`-under`, `-urgb`, or `-undercolor`).

---

## Syntax & CLI Options

```bash
mix_ci [OPTIONS] [-c <colormap.8bit>] [-i <intensmap.sun>] -m <resultmap>
```

### Core Input & Output Options

| Option | Description | Default |
|---|---|---|
| `-c <colormap>` | Input 8-bit `JHC_header` color-coded depth/attribute file (typically produced by [`r4to8bit`](r4to8bit.html)). Required unless `-monofil` or `-justunder` is set. | None |
| `-i <intensmap>` | Input 8-bit `JHC_header` sun-illuminated intensity file (typically produced by [`addSUN`](addSUN.html)). Required unless `-justunder` is set. | None |
| `-m <resultmap>` | **Required.** Output filename (8-bit `JHC_header` image by default, or 24-bit binary `P6` `.ppm` if `-ppm` is set). | None |
| `-ppm` | Output a 24-bit true-color binary Portable Pixmap (`P6` `.ppm`) instead of an 8-bit indexed `JHC_header` raster. | Disabled (8-bit `JHC_header`) |
| `-mix <base> <colors> <shades>` | Configure the 8-bit indexed color-intensity quantization table (`base + (c * colors / 256) * shades + (i * shades / 256)`). Sets `header.rgb_bw` to `5` (`8` colors), `6` (`10` colors), or `7` (`12` colors). | `16 8 30` |

### Monochrome & Palette Options (with `-ppm`)

| Option | Description | Default |
|---|---|---|
| `-monofil` | Monochrome/single-file mode: use only the intensity map (`-i`, e.g. sidescan mosaic or sunshade) without a color map (`-c`). | Disabled |
| `-tint <R> <G> <B>` | Used with `-monofil -ppm`: tint the monochrome intensity image by `(R, G, B)` (`0..255`). | `255 255 255` |
| `-mcol` | Map 8-bit values through OMG's standard rainbow multi-color palette (`prime_palettes()`) for `-monofil` or `-under` images. | Disabled |
| `-grey16` | Preserve OMG reserved annotation colors (`DN 8..15` $\rightarrow$ pure black, red, green, blue, magenta, yellow, cyan, white) when rendering `-monofil` or `-under` images. | Disabled |
| `-classic` | Use legacy channel ordering (`R, B, G` swap) in `-ppm` / `-urgb` output. | Disabled |
| `-cmap <file>` / `-asciicmap <file>` | Parse custom binary or ASCII 256-entry RGB colormap file. | Disabled |

### Masking & Underlay Compositing Options

| Option | Description | Default |
|---|---|---|
| `-mask <maskfile>` | 8-bit `JHC_header` stencil mask file (e.g. from [`maskarray`](maskarray.html)) controlling where the foreground vs. underlay is drawn. | None |
| `-ignore <val>` | Mask digital number in `<maskfile>` that triggers drawing the background/underlay instead of the foreground. | `0` |
| `-inverse` | Invert the stencil logic so the underlay is drawn where `*mask != ignore`. | Disabled |
| `-under <underfile>` | 8-bit `JHC_header` background image drawn wherever the stencil mask triggers. | None |
| `-undercolor <R> <G> <B>` | Solid RGB color (`0..255`) used for the background (or used to tint the `-under` 8-bit image in `-ppm` mode). | `255 255 255` |
| `-urgb <prefix>` | 3-band 8-bit `JHC_header` RGB underlay (`<prefix>.band1`, `<prefix>.band2`, `<prefix>.band3`, e.g., satellite imagery or scanned nautical chart) drawn in background regions. | None |
| `-justunder` / `-just_under` | Output only the 3-band `-urgb <prefix>` underlay directly to `-ppm` without reading `-c` or `-i`. | Disabled |
| `-v` | Enable verbose row/pixel diagnostic output. | Disabled |

---

## How It Works

1. **8-Bit Indexed Mode (Default, without `-ppm`):**
   - Copies the `JHC_header` from `-i` (preserving `sun_elev`, `sun_azi`, `sun_exag` and setting `rgb_bw = 5, 6, or 7` for `8, 10, or 12` colors).
   - Combines each color pixel `*cp` and intensity pixel `*ip` into a single 8-bit index:
     $$\text{DN} = \text{base} + \left\lfloor \frac{\text{cp} \times \text{colors}}{256} \right\rfloor \times \text{shades} + \left\lfloor \frac{\text{ip} \times \text{shades}}{256} \right\rfloor$$
   - If `-mask` is active and `*cp == 8`, maps the pixel into the lower 16-level greyscale ramp (`*ip / 16`).
2. **24-Bit True-Color PPM Mode (`-ppm`):**
   - Converts normalized color $c = \text{cp}/255$ and sun intensity $s = \text{ip}/255$ into HSV (`hue = 300 - 300c`, `sat = 0.3 + 0.2c`, `val = s`) and converts to 24-bit `(R, G, B)`.
   - If `-mask` is provided and the mask pixel matches `-ignore` (or `!= ignore` with `-inverse`), replaces the foreground RGB with the `-under` 8-bit image (tinted by `-undercolor` or colored by `-mcol`/`-grey16`), the 3-band `-urgb` image (`.band1`, `.band2`, `.band3`), or the solid `-undercolor`.

---

## Examples

**1. Create a standard 8-bit color-shaded bathymetry grid (`JHC_header`) from depth `.8bit` and sunshade `.sun`:**

```bash
r4to8bit -low -200 -high -10 survey.r4 survey.8bit
addSUN -elev 30 -azi 315 -exag 5 survey.r4 survey.sun
mix_ci -c survey.8bit -i survey.sun -m survey_ci.8bit
```

**2. Create a 24-bit true-color `.ppm` of sun-shaded bathymetry composited over a sidescan mosaic background:**

```bash
maskarray survey.r4
mix_ci -ppm \
    -c survey.8bit -i survey.sun \
    -mask survey.r4.maskmap -ignore 0 \
    -under survey.mos -undercolor 200 200 200 \
    -m survey_over_sidescan.ppm
```

**3. Render a 3-band RGB chart backdrop (`chart.band1`, `.band2`, `.band3`) beneath sun-shaded bathymetry:**

```bash
mix_ci -ppm -c survey.8bit -i survey.sun -mask survey.r4.maskmap -ignore 0 -urgb chart -m chart_bathy.ppm
```

---

## Workflow Context

- **Upstream:** [`r4to8bit`](r4to8bit.html) (generates `-c`), [`addSUN`](addSUN.html) (generates `-i`), and [`maskarray`](maskarray.html) (generates `-mask`).
- **Downstream:** View 8-bit `JHC_header` outputs in `jview` (or select palettes with [`selectcb`](selectcb.html)), or convert `.ppm` outputs to PNG/TIFF for publication.
