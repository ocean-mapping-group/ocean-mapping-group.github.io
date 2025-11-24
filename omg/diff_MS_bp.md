---
layout: default
title: diff_MS_bp
parent: OMG Tools
nav_order: 89
---
# diff_MS_bp

## Description
`diff_MS_bp` is a utility designed to compare two multi-sector beam pattern (MS_bp) files and output the difference between them. This tool is useful for analyzing changes in beam patterns over time, between different calibrations, or after applying various corrections.

It expects both input files to have an identical set of sectors (defined by parameters like `sector_id`, `center_frequency`, `signal_length`, `waveform_id`). It calculates the point-by-point difference in dB values for each angle bin.

## Usage
```bash
diff_MS_bp -first <first_file> -second <second_file> -out <output_file> [-v]
```

## Arguments

| Option | Description |
|---|---|
| `-first <first_file>` | **Required.** Path to the first multi-sector beam pattern file. |
| `-second <second_file>` | **Required.** Path to the second multi-sector beam pattern file. |
| `-out <output_file>` | **Required.** Path for the output file which will contain the differences. |
| `-v` | Enable verbose output. |
| `-Ref_dB_level <val>` | (Present in `USAGE` but not implemented) This option likely suggests a reference dB level, but its functionality is not seen in the `main` function. |

## How It Works
1.  **Input Reading:** Reads the two input multi-sector beam pattern files (`-first` and `-second`) using `load_MS_bp` (an external function from `j_generic_beam_pattern.h`). This function populates `First_BP`/`Second_BP` (the actual beam pattern dB values) and `First_Params`/`Second_Params` (the TX sector parameters).
2.  **Sector Comparison:**
    *   It first checks if both files have the same number of sectors. If not, it errors out.
    *   It then iterates through each sector, comparing their parameters (`sector_id`, `center_frequency`, `signal_length`, `signal_bandwidth`). If these parameters don't match, it issues a warning ("Apples 'n Oranges DIFF BP").
3.  **Swath Flipping (Experimental/Heuristic):** There's an experimental section (`if(testflip)`) that attempts to "flip" the order of swaths within the beam pattern data if the `center_frequency` of the first sector is greater than that of the middle sector. This is a heuristic to ensure consistency if swath order might be inverted between files.
4.  **Difference Calculation:** For each sector and each angle bin, it calculates the difference: `Diff_BP[i][k] = First_BP[i][k] - Second_BP[i][k]`. If either `First_BP[i][k]` or `Second_BP[i][k]` is zero, the difference is set to `0`.
5.  **Output:** Writes the calculated differences (`Diff_BP`) along with the sector parameters (`First_Params`) to the specified output file using `dump_MS_bp` (an external function). The output file is a multi-sector beam pattern file, where the values represent the dB difference.

## Output Files
*   `<output_file>`: A new multi-sector beam pattern file containing the dB differences.

## Dependencies
*   `j_generic_beam_pattern.h`: For `MS_BP` structure and `load_MS_bp`, `dump_MS_bp` functions.
*   `support.h`: For general utility functions and error handling.

## Notes
This tool is valuable for quality control and detailed analysis of beam pattern stability and consistency. It helps to quantify the impact of environmental changes, system adjustments, or processing algorithms on the sonar's angular response characteristics. The `Ref_dB_level` option is mentioned in the usage but not implemented, suggesting a future enhancement or a legacy feature.