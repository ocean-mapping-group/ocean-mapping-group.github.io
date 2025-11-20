---
layout: default
title: classSS
parent: Classification Tools
nav_order: 2
---
# classSS

## Description
`classSS` is a command-line utility for extracting spectral classification parameters from sidescan sonar imagery, or from multibeam data if specified. It processes input images (typically from `ss_slantrange` files) by dividing them into patches and performing spectral analysis. It can use fixed classification sectors or dynamically adjust based on valid pixels. The tool calculates various attributes for each patch, including average amplitude, sigma, and spectral characteristics, and outputs these into a classification file.

## Usage
```bash
classSS [OPTIONS] -out <classification_file> <ss_slantrange_file(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-NoPings <count>` | Number of pings to process in each batch for spectral analysis. | `64` (default `16`) |
| `-NoPixels <count>` | Number of pixels to process in each patch for spectral analysis. | `256` (default `128`) |
| `-swath <degrees>` | Defines the maximum swath angle for multibeam classification (e.g., `65`). This also sets default `out_class_STB` and `out_class_PRT` values. | `75` |
| `-in_class <degrees>` | Inner classification angle (defines a region closer to nadir). | `15` (default `20`) |
| `-out_class <degrees>` | Outer classification angle for both starboard and port sides. This will override `-swath` for these limits if used. | `60` (default `75`) |
| `-out_class_STB <degrees>` | Outer classification angle for the starboard side only. | `60` (default `75`) |
| `-out_class_PRT <degrees>` | Outer classification angle for the port side only. | `60` (default `75`) |
| `-fixed_sectors` | Use a fixed set of 3 classification sectors per side, equally spaced, suitable for fixed slant range sidescan. | |
| `-show_boxes` | Generate `.boxes` files alongside the input files, visualizing the classification sectors. | |
| `-out <classification_file>` | **Required.** Specifies the output file where the extracted classification parameters will be written. | `output.class` |
| `<ss_slantrange_file(s)>` | **Required.** One or more input sidescan slant range image files. | `side_scan_01.sr side_scan_02.sr` |
