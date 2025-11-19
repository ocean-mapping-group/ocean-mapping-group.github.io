# qualityFlag

## Description
`qualityFlag` is a command-line utility designed to flag (or unflag) hydrographic data beams in OMG-HDCS merged files based on their quality factor. It specifically targets ELAC multibeam data, using the ELAC-supplied beam quality (a crude signal-to-noise ratio), or can handle SeaBat 8101 data by interpreting specific bit flags for brightness, collinearity, and amplitude/phase detection. Beams whose quality falls outside a specified minimum and maximum range are marked as invalid.

## Usage
```bash
qualityFlag [OPTIONS] <merged_file(s)>
```

## Arguments

| Option | Description | Default / Example |
|---|---|---|
| `-v` | Enable verbose output. | |
| `-minquality <value>` | Specifies the minimum acceptable quality factor. Beams with a quality factor below this value will be flagged as invalid. | `0` |
| `-maxquality <value>` | Specifies the maximum acceptable quality factor. Beams with a quality factor above this value will be flagged as invalid. | `2` |
| `<merged_file(s)>` | **Required.** One or more input OMG-HDCS merged files (e.g., `.merged`) to be processed. The tool directly modifies the `status` and `Q_factor` fields of the beams within these files. | `survey_001.merged survey_002.merged` |