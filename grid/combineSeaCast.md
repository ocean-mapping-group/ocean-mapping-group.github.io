# combineSeaCast

## Description
`combineSeaCast` is a command-line utility that processes gridded output from an oceanographic model (likely SeaCast, given the name) to derive current magnitude and azimuth. It takes four JHC-format 32-bit floating-point (`.r4`) grid files as input: latitude, longitude, U-velocity (eastward), and V-velocity (northward). It then calculates the vector magnitude and direction (azimuth) for the current at each grid node and outputs these as a series of JCU navigation records (latitude, longitude, magnitude, azimuth) to an ASCII file, suitable for plotting as vectors on a map.

## Usage
```bash
combineSeaCast -lat <file_lat.r4> -lon <file_lon.r4> -uvel <file_uvel.r4> -vvel <file_vvel.r4> -out <output.nav> [OPTIONS]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-lat <file_lat.r4>` | **Required.** Path to the JHC-format `.r4` grid file containing latitude values for each grid node. | `lat_grid.r4` |
| `-lon <file_lon.r4>` | **Required.** Path to the JHC-format `.r4` grid file containing longitude values for each grid node. | `lon_grid.r4` |
| `-uvel <file_uvel.r4>` | **Required.** Path to the JHC-format `.r4` grid file containing eastward (U) velocity components for each grid node. | `u_velocity.r4` |
| `-vvel <file_vvel.r4>` | **Required.** Path to the JHC-format `.r4` grid file containing northward (V) velocity components for each grid node. | `v_velocity.r4` |
| `-out <output.nav>` | **Required.** Path for the output JCU navigation format file, containing latitude, longitude, current magnitude, and azimuth for each grid node. | `current_vectors.nav` |
| `-v` | Enable verbose output during processing. | |