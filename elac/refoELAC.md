# refoELAC

## Description
`refoELAC` is a command-line utility designed to convert raw Honeywell ELAC Bottom Chart FAU (Fast Acquisition Unit) format multibeam data into the OMG-HDCS (Ocean Mapping Group - Hydrographic Data Cleaning System) `.merged` format. It processes the proprietary ELAC data, extracts bathymetry, position, and attitude information, applies a Mercator projection for geographical coordinates, and writes the data into a standard OMG-HDCS merged file, complete with image extensions. It also generates auxiliary files for amplitude and quality histograms.

## Usage
```bash
refoELAC [OPTIONS] <input_FAU_file> <output_merged_file>
```

## Output Files
*   `<output_merged_file>`: The converted OMG-HDCS `.merged` file.
*   `<output_merged_file>.quality`: An ASCII file containing quality histograms by grazing angle.
*   `<output_merged_file>.amplitudes`: An ASCII file containing amplitude histograms.

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output during processing. | |
| `-constant <value>` | Apply a constant offset to the northing values during conversion (used to adjust for specific projection origins). | `0` |
| `-merid <longitude>` | Specifies the central meridian (longitude) for the Mercator projection. | `-69.0` |
| `-proj_lat <latitude>` | Specifies the projection latitude for the Mercator projection. | `45.83333333` |
| `<input_FAU_file>` | **Required.** The input Honeywell ELAC Bottom Chart FAU format data file. | `elac_raw_data.fau` |
| `<output_merged_file>` | **Required.** The base name for the output OMG-HDCS merged file and its associated amplitude and quality histogram files. | `elac_converted.merged` |