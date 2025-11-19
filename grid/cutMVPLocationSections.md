# cutMVPLocationSections

## Description
`cutMVPLocationSections` is a specialized command-line utility designed to extract and combine vertical profile data along a specified X-location (column) from a series of images with corresponding MVP (Moving Vessel Profiler) data. It takes an MVP file, one or more image files (either 8-bit or float JHC grids), and an X-coordinate. It resamples the MVP data and extracts vertical slices from the image(s) at that X-location. The output is a single ASCII file containing combined depth, sound velocity, and image intensity values along the vertical section, suitable for further analysis or plotting.

## Usage
```bash
cutMVPLocationSections -mvpfile <mvp_file.m1> -outfile <output.ascii> -xloc <x_pixel_location> -allimages <image1> [image2 ...] [OPTIONS]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-mvpfile <mvp_file.m1>` | **Required.** Specifies the path to the input MVP (Moving Vessel Profiler) data file, typically in an `.m1` format. | `mvp_data.m1` |
| `-outfile <output.ascii>` | **Required.** Specifies the path for the output ASCII file. This file will contain the combined vertical profile data. | `vertical_section.txt` |
| `-xloc <x_pixel_location>` | **Required.** Specifies the X-coordinate (column index) in the image(s) from which to extract the vertical section. | `-xloc 7` (extracts from column 7) |
| `-allimages <image1> [image2 ...]` | **Required.** Specifies one or more input image files. These can be either 8-bit or float JHC-format grid files (`.8bit` or `.r4`). Multiple image files can be provided. | `-allimages Reg_Sect.L034.018kHz.r4 Reg_Sect.L034.038kHz.r4` |
| `-zpix <value>` | Specifies the vertical pixel step value (e.g., in meters per pixel) used for resampling the MVP depth data. | `1.0` |
| `-xwidth <value>` | Specifies the width in pixels around the `-xloc` to average image intensities, providing a smoothed profile. | `1` (no averaging, single column) |
| `-upcast` | Process only the upcast portion of the MVP profile. | |
| `-downcast` | Process only the downcast portion of the MVP profile. | |
| `-bothcast` | Process both upcast and downcast portions of the MVP profile. This is the default. | |
| `-v` | Enable verbose output during processing. | |
