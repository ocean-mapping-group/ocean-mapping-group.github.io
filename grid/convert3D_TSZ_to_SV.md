# convert3D_TSZ_to_SV

## Description
`convert3D_TSZ_to_SV` is a specialized command-line utility for converting 3D gridded Salinity (S), Temperature (T), and Depth (Z) data into Sound Velocity (SV) profiles. It's designed to process output from oceanographic models (specifically mentioned SalishSeaCast NetCDF files, which are converted to JHC `.r4` grids for S, T, and Z at various layers). For each grid cell and depth layer, it reads S and T values, uses the corresponding Z from a `.zvals` file, calculates pressure, and then computes sound velocity using the Chen-Millero equation. The output is a new set of JHC `.r4` grid files for sound velocity for each depth layer, along with copied `.zvals` and `.time` files.

## Usage
```bash
convert3D_TSZ_to_SV -prefix <SectionPath/SectionPrefix> [OPTIONS]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-prefix <SectionPath/SectionPrefix>` | **Required.** Specifies the base path and prefix for the input S, T, and Z data files. The tool expects files named `<prefix>.salinity.r4`, `<prefix>.temperature.r4`, and `<prefix>.salinity.zvals`. The output sound velocity file will be named `<prefix>.soundSpeed.r4`. | `-prefix SalishSea_Data/Converted/2024-10-26/salishsea.2024_jd299_12-00-00_Oct-26` |
| `-testTSZtoSv` | Enables an interactive test mode where the user can manually input Salinity, Temperature, and Depth values to see the calculated Sound Velocity. | |
| `-v` | Enable verbose output during processing. | |