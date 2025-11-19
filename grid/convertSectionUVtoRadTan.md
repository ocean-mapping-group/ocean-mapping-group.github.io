# convertSectionUVtoRadTan

## Description
`convertSectionUVtoRadTan` is a command-line utility designed to transform gridded U (eastward) and V (northward) velocity components, typically from an ocean model or ADCP data, into along-section and across-section velocity components. It specifically works with data representing a 2D cross-section extracted from a 3D model (e.g., using `extractVertSection`). It requires the U and V velocity grids and a separate ASCII file containing the azimuth of the profile at each point along the section. The output is three new JHC-format 32-bit floating-point (`.r4`) grids: one for along-section velocity, one for across-section velocity, and one for the current magnitude.

## Usage
```bash
convertSectionUVtoRadTan -prefix <SectionPath/SectionPrefix> [OPTIONS]
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-prefix <SectionPath/SectionPrefix>` | **Required.** Specifies the base path and prefix for the input velocity and azimuth files. The tool expects: <br> - `<prefix>.uVelocity.r4` (U-velocity) <br> - `<prefix>.vVelocity.r4` (V-velocity) <br> - `<prefix>.uVelocity.llazi` (profile azimuths). <br> Output files will be named: <br> - `<prefix>.AlongVel.r4` <br> - `<prefix>.AcrossVel.r4` <br> - `<prefix>.cMagnitude.r4` | `-prefix SalishSea_Data/Converted/Section_A/section_profile` |
| `-testrot` | Enables an interactive test mode where the user can manually input U, V, and azimuth values to see the calculated along-section and across-section components. | |
| `-v` | Enable verbose output during processing. | |