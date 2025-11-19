# differ

## Description
`differ` is a powerful command-line utility for comparing two JHC-format 32-bit floating-point grid files (`.r4` files). Its primary function is to calculate the pixel-wise difference between two surfaces (e.g., Digital Terrain Models from different epochs). The tool also provides advanced options for statistical analysis, volumetric calculations, handling spatial misalignments, and masking.

## Usage
```bash
differ -first <file1.r4> -second <file2.r4> -out <output.r4> [OPTIONS]
```

## Core Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-first <file1.r4>` | **Required.** The path to the first input float grid file (the minuend). | `-first dtm_2022.r4` |
| `-second <file2.r4>` | **Required.** The path to the second input float grid file (the subtrahend). | `-second dtm_2021.r4` |
| `-out <output.r4>` | **Required.** The path for the output float grid file that will store the difference (`first - second`). | `-out difference_map.r4` |

## Feature Options

### Analysis and Statistics
| Option | Description | Default / Example |
|---|---|---|
| `-stats <min> <max> <step>` | Enables detailed statistical analysis. It calculates the mean and standard deviation of the differences and generates a histogram of the difference values, which is saved to `<outname>.statistics`. `<min>`, `<max>`, and `<step>` define the histogram's range and bin size. | `-stats -5.0 5.0 0.1` |
| `-volume_calc_net` | Calculates the net volumetric change between the two surfaces by summing the difference at each pixel multiplied by the pixel area. | |
| `-volume_calc_gain` | Calculates the total positive (gain) volumetric change, where the first surface is higher than the second. | |
| `-volume_calc_loss` | Calculates the total negative (loss) volumetric change, where the second surface is higher than the first. | |
| `-perc_wd` | Calculates the difference as a percentage relative to the value in the first file: `((first - second) / first) * 100.0`. | |
| `-xplot` | Creates a simple two-column ASCII file named `<outname>.xplot` containing the paired values from the first and second grids, suitable for generating a scatter plot. | |

### Alignment and Filtering
| Option | Description | Default / Example |
|---|---|---|
| `-min_within_pixels <num>` | Instead of a simple 1-to-1 subtraction, this enables a search mode. For each pixel in the first grid, it searches a square neighborhood of `+/- num` pixels in the second grid and finds the minimum absolute difference. The output value is this minimum signed difference. This is extremely useful for comparing surveys with small, unknown horizontal offsets. | `-min_within_pixels 3` |
| `-mask <mask_file>` | Applies an 8-bit mask file. The differencing operation will only be performed on pixels where the mask value is non-zero. | `-mask valid_area.mask` |
| `-shift <xpix> <ypix>` | Applies a simple integer pixel shift to the *second* grid before differencing. Useful for correcting known, uniform misalignments. | `-shift 2 -1` |
| `-addvalue <value>` | Adds a constant floating-point offset to each value in the first grid before differencing. This is equivalent to applying a vertical shift to the first surface. | `-addvalue -0.35` |
| `-sane_range <min> <max>` | Filters the input data. Any pixel value in either input grid that falls outside this specified min/max range is treated as zero and ignored in the calculation. | `-sane_range -2000 50` |
| `-v` | Enable verbose output during processing. | |
